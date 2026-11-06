---
layout: default
title: "Efficient ML & AI Infrastructure"
description: "Chaofan Tao's research on efficient machine learning: how vocabulary design, compression, long-context memory, test-time compute, resilient serving and distillation each fail when a hidden assumption stops holding, and how to fix them."
permalink: /research/efficient-ml-ai-infrastructure/
research_lang: en
last_modified_at: 2026-11-06
og_image: /assets/img/og-image.png
figure: /assets/img/research/efficiency-lifecycle.svg
about:
  - Efficient machine learning
  - AI infrastructure
  - Scaling laws
  - Model quantization
  - KV cache compression
  - Test-time scaling
  - Knowledge distillation
---

{% include research/styles.liquid %}
{% include research/jsonld.liquid group="efficient" %}

<div class="research-page">
  <nav class="research-breadcrumb" aria-label="Breadcrumb">
    <a href="{{ '/' | relative_url }}">Chaofan Tao</a><span aria-hidden="true">/</span>
    <a href="{{ '/research/' | relative_url }}">Research</a><span aria-hidden="true">/</span>
    <span>Efficient ML and AI infrastructure</span>
    <span aria-hidden="true">·</span><a href="{{ '/zh/research/efficient-ml-ai-infrastructure/' | relative_url }}" lang="zh-Hans">中文版</a>
  </nav>

  <h1>Efficient ML &amp; AI Infrastructure</h1>
  <p class="research-dek">In my experience, most efficiency problems start with an assumption that quietly stopped being true. This page follows a model from design to serving and looks at the assumption each piece of our work takes apart.</p>
  <p class="research-meta">By <a href="{{ '/' | relative_url }}">Chaofan Tao (陶超凡)</a>, with collaborators · Last updated <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%B %-d, %Y" }}</time></p>

  <p>Efficiency is usually framed as a trade: give up a little quality to save compute or memory. The bigger wins I've seen come from somewhere else. A method fails, or wastes resources, because it rests on an assumption that made sense when it was designed and no longer holds. The tokenizer can be fixed before you scale. Every part of a network handles compression the same way. Every cached token is equally important. Waiting for synchronization is free. GPUs don't fail. The strongest teacher teaches best.</p>
  <p>Spotting the broken assumption is usually the hard part. Once the diagnosis is right, the fix often turns out to be simple. I've organized this page by where in a model's life each assumption lives. The quantization work in the second section received an ACL 2022 Outstanding Paper Award.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/efficiency-lifecycle.svg' | relative_url }}" alt="Diagram of five lifecycle stages, design, compress, remember, compute and serve, and transfer, each paired with the assumption our work shows to be false and the projects that address it." width="960" height="300" loading="eager"></div>
    <figcaption>Efficiency across a model's life. Each stage pairs a common assumption with the work that shows where it breaks.</figcaption>
  </figure>

  <p class="research-toc">On this page: <a href="#design">Design</a> · <a href="#compress">Compress</a> · <a href="#remember">Remember</a> · <a href="#serve">Compute and serve</a> · <a href="#transfer">Transfer</a> · <a href="#insights">What ties it together</a> · <a href="#open-questions">Open questions</a></p>

  <h2 id="design">1. Design: the tokenizer is not a free choice</h2>
  <p>Scaling laws tell you how loss changes as you add parameters and data. They usually say nothing about the vocabulary, and you can see the result in practice: models of similar size ship with wildly different vocabulary sizes. In <a href="https://arxiv.org/abs/2407.13623">Scaling Laws with Vocabulary</a> (NeurIPS), we treated vocabulary size as a scaling dimension in its own right. We separated vocabulary parameters from the rest of the network, measured data in characters instead of tokens so that different tokenizers could be compared fairly, and used a loss that doesn't depend on vocabulary size. Three independent ways of estimating the best size, from IsoFLOPs analysis, from derivatives, and from fitting the loss directly, all pointed the same way: most models under-invest in their vocabulary.</p>
  <p>Why is there a best size at all? It comes down to a trade-off. A bigger vocabulary splits text into fewer tokens and can represent more concepts directly, but when compute is limited, the embeddings for rare tokens never get trained well. As compute grows, the balance tips toward larger vocabularies, though they should grow more slowly than the rest of the model. How much data you have matters as well: with little data, a smaller vocabulary avoids overfitting rare tokens; with far more data than is compute-optimal, a larger one pays off, keeping in mind that a bigger vocabulary also makes inference more expensive. One picture I like: under a fixed compute budget, the best vocabulary is the one that lets the model read the most text. Go smaller and the same text costs more tokens; go bigger and the compute goes into the embedding and output layers instead. The <a href="https://huggingface.co/spaces/sail/scaling-with-vocab-demo">interactive calculator</a> turns all of this into a number you can use.</p>

  <h2 id="compress">2. Compress: not every part of a model is alike</h2>
  <p>Quantization methods that worked well for BERT-style encoders fell apart on GPT-style generators, and for a while it wasn't clear why. In <a href="https://arxiv.org/abs/2203.10705">Compression of Generative Pre-trained Language Models via Quantization</a> (ACL 2022 Outstanding Paper), we traced it to two problems. At low precision, the word embeddings collapse until they look almost the same, so a model that has to pick the next token can no longer tell its options apart. And the weights in different modules are spread out very differently, so no single quantizer setting suits all of them. The fixes follow from the diagnosis: token-level contrastive distillation keeps each token's representation close to the full-precision model's and distinct from other tokens, and module-wise dynamic scaling gives each module its own range. <a href="https://doi.org/10.18653/v1/2023.findings-acl.692">Structured pruning</a> applies the same idea to removing parts of a generative model, learning which pieces can go.</p>
  <p>Vision-language models make this unevenness even easier to see, because images and text carry information so differently. <a href="https://arxiv.org/abs/2301.13741">UPop</a> searches for a smaller network across the vision and language parts together, so the model learns how much to prune from each instead of us guessing, and it alternates between searching and retraining. <a href="https://arxiv.org/abs/2305.17455">CrossGET</a> merges redundant tokens while the model runs, letting one modality guide which tokens get matched in the other.</p>

  <h2 id="remember">3. Remember: not every cached token matters, but keep a way back</h2>
  <p>In long-context inference, the KV cache, which holds keys and values for every earlier token, soon takes up most of the memory. Trimming it evenly is wasteful because layers behave differently. <a href="https://arxiv.org/abs/2406.13035">D2O</a> gives each layer its own budget depending on how focused its attention is, and keeps a way to bring back or merge tokens it dropped if they resemble ones it kept, all without any fine-tuning. <a href="https://arxiv.org/abs/2410.03090">UNComp</a> looks at the same question in terms of information: it uses matrix entropy as a measure of uncertainty to find the parts that can be compressed, and the same analysis points to the heads and layers that do the retrieving.</p>
  <p>Diffusion language models have their own version of the problem, since they re-read the entire prompt at every denoising step. <a href="https://arxiv.org/abs/2606.10537">Prefilling-dLLM</a> caches the prompt once, in chunks, and then only uses the chunks and tokens relevant to the question, with no retraining. One small detail turned out to matter a lot: putting a beginning-of-sequence token at the start of every chunk gives attention something stable to hold on to, and with that in place, the sparse version can even beat full attention.</p>

  <h2 id="serve">4. Compute and serve: coordination costs more than arithmetic</h2>
  <p>At scale, the bottleneck is usually waiting, and the biggest risk is usually losing state. Test-time scaling is a good example of the first. It improves answers by spending more compute while generating, often with a small model drafting and a large one checking. When we looked at where the time actually went, in <a href="https://arxiv.org/abs/2509.15148">ATTS</a>, the main cost was synchronization, not arithmetic. ATTS replaces those synchronous checks with asynchronous inference, using conformal prediction, calibrated on the fly, to keep statistical control over how often drafts get rejected. It scales in both directions at once: longer reasoning and more parallel attempts.</p>
  <p>Serving has its own hidden assumption: that GPUs don't fail. With tensor parallelism across several GPUs, losing one can take the whole service down. <a href="https://arxiv.org/abs/2511.11617">AnchorTP</a> keeps the weights and KV caches alive in a separate process that outlives the crash, re-splits the model across the GPUs that are left, and plans the smallest amount of data movement needed to get back up.</p>
  <p><strong>Infrastructure for training agents.</strong> Both lessons come back, more sharply, when you train agents with <a href="{{ '/research/agentic-intelligence/#signal' | relative_url }}">RL inside their real harness</a>. In Lego-RL, almost all of a training attempt is the agent at work: reading files, editing code, running tests in a sandbox. Attempts are long and very uneven, so a synchronous batch always waits for its slowest member. Asynchronous scheduling lets a new attempt start as soon as a slot opens. When the weights update mid-attempt, a partial rollout pauses generation, loads the new weights and carries on from the cached prefix on the same machine, so a long attempt isn't thrown away. Starting a sandbox is mostly spent building its image, so prebuilt task images, a mounted agent runtime and lazy image pulls remove most of that wait. There's one place where we deliberately chose the slower option: the grading tools are baked into every image, because a reward you can reproduce is worth more than one you get a little faster. A lot of agent RL, it turns out, is an efficiency and reliability problem.</p>

  <h2 id="transfer">5. Transfer: the strongest teacher is not the best teacher</h2>
  <p>Distillation works best when the signal fits what the student can learn, not when the teacher is as strong as possible. Take the choice between forward and reverse KL divergence. The common story is that one chases the main mode of the teacher and the other spreads out to cover everything. For LLMs, <a href="https://arxiv.org/abs/2404.02657">we found</a> that neither really happens: the two share the same optimum. The real difference shows up early in training, when forward KL pays attention to the teacher's most likely tokens and reverse KL to the long tail. Adaptive KL simply weights the two accordingly. <a href="https://arxiv.org/abs/2510.10925">PerSyn</a> starts from the observation that stronger models are not always better teachers, and sends each prompt to the teacher a particular student learns from best before any data is generated, instead of having every teacher answer everything and filtering afterwards.</p>
  <p>Agent training arrives at the same conclusion from a different direction. Grounded trajectories from weaker agents teach better than answers from stronger ones, and <a href="{{ '/research/agentic-intelligence/#signal' | relative_url }}">text feedback from a black-box teacher</a> can guide a student without ever exposing the teacher's probabilities.</p>

  <h2 id="insights">What ties it together</h2>
  <ol class="research-insights">
    <li><strong>Find the broken assumption before you optimize.</strong> Every result here started with asking why an existing method failed, not with trying a faster variant. Once the cause was clear, the fix was usually small.</li>
    <li><strong>Unevenness is the rule.</strong> Layers, modules, modalities, tokens and teachers all differ. Giving each its own budget, per layer, module, modality or prompt, keeps paying off in compression, caching and distillation alike.</li>
    <li><strong>Keep a way back.</strong> Dropped tokens that can be recalled, state that survives a crash, attempts that survive a weight update: these are what make aggressive optimization safe.</li>
    <li><strong>At scale, waiting is the real cost.</strong> In test-time scaling, serving and agent training, the biggest gains came from removing waiting, not from faster arithmetic.</li>
    <li><strong>Efficiency shapes what a model can learn.</strong> Rare-token embeddings that never get enough compute, teacher outputs a student can't absorb: efficiency isn't only about cost. It decides what a model is able to learn at all.</li>
  </ol>

  <h2 id="open-questions">Open questions</h2>
  <ul>
    <li>How should vocabulary be chosen once inference cost, multilingual data and code are all part of the goal?</li>
    <li>What should long-context memory keep for agents, whose context is mostly tool output rather than prose?</li>
    <li>How much faster can agent RL get, when most of the time goes into acting rather than computing gradients?</li>
    <li>Can the fault-tolerance ideas from serving make long training runs just as resilient?</li>
  </ul>

  {% include research/paper-list.liquid group="efficient" lang="en" %}

  <p>Related: <a href="{{ '/research/agentic-intelligence/' | relative_url }}">Agentic coding, reasoning and evaluation</a></p>
</div>
