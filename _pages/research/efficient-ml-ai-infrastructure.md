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
  <p class="research-dek">Most efficiency problems begin with an assumption that quietly stopped being true. This essay follows one model's lifecycle, from design to serving, and the assumption each piece of our work removes.</p>
  <p class="research-meta">By <a href="{{ '/' | relative_url }}">Chaofan Tao (陶超凡)</a> and collaborators · Last updated <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%B %-d, %Y" }}</time></p>

  <p>Efficiency is usually framed as a trade: give up some quality to save compute or memory. In our experience the bigger wins come from somewhere else. A method fails, or wastes resources, because it relies on an assumption that was reasonable when it was designed and no longer holds: that the tokenizer can be fixed before scaling, that every part of a network tolerates compression the same way, that every cached token is equally important, that synchronization is free, that hardware does not fail, or that the strongest teacher teaches best.</p>
  <p>Finding the broken assumption tends to be harder than fixing it, and the fix is often simple once the diagnosis is right. The projects on this page are organized by the stage of the model lifecycle where the assumption lives. The quantization work in the second stage received an ACL 2022 Outstanding Paper Award.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/efficiency-lifecycle.svg' | relative_url }}" alt="Diagram of five lifecycle stages, design, compress, remember, compute and serve, and transfer, each paired with the assumption our work shows to be false and the projects that address it." width="960" height="300" loading="eager"></div>
    <figcaption>Efficiency across the model lifecycle. Each stage pairs a common assumption with the work that shows where it breaks.</figcaption>
  </figure>

  <p class="research-toc">On this page: <a href="#design">Design</a> · <a href="#compress">Compress</a> · <a href="#remember">Remember</a> · <a href="#serve">Compute and serve</a> · <a href="#transfer">Transfer</a> · <a href="#insights">What ties it together</a> · <a href="#open-questions">Open questions</a></p>

  <h2 id="design">1. Design: the tokenizer is not a free choice</h2>
  <p class="research-claim">Vocabulary size is a scaling dimension, and most models under-invest in it.</p>
  <p>Classic scaling laws describe how loss changes with parameters and data, and leave the vocabulary out. As a result, models of similar size ship with very different vocabularies. <a href="https://arxiv.org/abs/2407.13623">Scaling Laws with Vocabulary</a> (NeurIPS) puts it back in. It separates vocabulary parameters from the rest of the network, measures data in characters rather than tokens so that tokenizers can be compared fairly, and uses a loss that does not depend on vocabulary size. Three independent estimates, from IsoFLOPs analysis, a derivative-based method and a parametric loss fit, agree.</p>
  <p>The mechanism behind the optimum is a trade-off. A larger vocabulary splits text into fewer tokens and covers more concepts, but embeddings for rare tokens are hard to learn when compute is limited. As compute grows, the balance shifts: vocabulary should grow with the model, though more slowly than the rest of it, and many popular models remain under-provisioned. The data regime matters too. With scarce data a smaller vocabulary avoids overfitting rare tokens; with far more data than is compute-optimal, a larger one pays off, while a bigger vocabulary also adds inference cost. A useful way to picture the optimum: under a fixed compute budget, it is the vocabulary that lets the model read the most training text. Smaller vocabularies spend compute on more tokens for the same text; larger ones spend it on the embedding and output layers. An <a href="https://huggingface.co/spaces/sail/scaling-with-vocab-demo">interactive calculator</a> turns this into a practical choice.</p>

  <h2 id="compress">2. Compress: not every part of a model is alike</h2>
  <p class="research-claim">Compression fails where a model is least uniform, so the fix is to treat its parts differently.</p>
  <p>Quantization methods that worked for BERT-style encoders broke on GPT-style generators, and it was not clear why. The diagnosis in <a href="https://arxiv.org/abs/2203.10705">Compression of Generative Pre-trained Language Models via Quantization</a> (ACL 2022 Outstanding Paper) has two parts. At low precision, word embeddings become nearly identical, so a generative model can no longer tell tokens apart when it chooses the next one. And weight distributions differ widely across modules, so one quantizer setting fits none of them well. Token-level contrastive distillation keeps each token's representation close to the full-precision teacher's and distinct from other tokens; module-wise dynamic scaling learns a separate range per module. <a href="https://doi.org/10.18653/v1/2023.findings-acl.692">Structured pruning</a> applies the same idea to removal, learning which components of a generative model can go.</p>
  <p>Vision-language models make non-uniformity even more visible, because the two modalities carry information differently. <a href="https://arxiv.org/abs/2301.13741">UPop</a> searches for a smaller sub-network across vision and language jointly, so each modality's pruning ratio is learned rather than set by hand, and alternates search with retraining. <a href="https://arxiv.org/abs/2305.17455">CrossGET</a> merges redundant tokens at inference time, using one modality to guide matching in the other.</p>

  <h2 id="remember">3. Remember: not every cached token matters, but keep a way back</h2>
  <p class="research-claim">Long-context memory can shrink a lot, provided eviction is adaptive and reversible.</p>
  <p>The KV cache stores keys and values for every previous token and soon dominates memory in long-context inference. Dropping uniformly is wasteful because layers differ: <a href="https://arxiv.org/abs/2406.13035">D2O</a> gives each layer its own budget according to how concentrated its attention is, and keeps a way to recall or merge discarded tokens that resemble kept ones, all without fine-tuning. <a href="https://arxiv.org/abs/2410.03090">UNComp</a> asks the question in information terms, using matrix entropy as an uncertainty signal to find what can be compressed; the same analysis exposes the heads and layers responsible for retrieval.</p>
  <p>Diffusion language models raise a different version of the problem, because they re-encode the whole prefix at every denoising step. <a href="https://arxiv.org/abs/2606.10537">Prefilling-dLLM</a> caches the prefix once, in chunks, and decodes over only the chunks and tokens relevant to the query, without retraining. A small detail turned out to matter: a beginning-of-sequence token at the start of each chunk acts as a periodic attention anchor, and with it sparse prefilling can even outperform dense attention.</p>

  <h2 id="serve">4. Compute and serve: coordination costs more than arithmetic</h2>
  <p class="research-claim">At scale, the bottleneck is usually waiting, and the risk is usually lost state.</p>
  <p>Test-time scaling improves answers by spending more compute during generation, often with a small model drafting and a large model checking. <a href="https://arxiv.org/abs/2509.15148">ATTS</a> analyzes where the time goes and finds that synchronization, not arithmetic, is the main bottleneck. It replaces synchronous checks with asynchronous inference calibrated online by conformal prediction, scaling along both sequential and parallel dimensions while keeping statistical control over how often drafts are rejected.</p>
  <p>Serving has its own hidden assumption: that GPUs do not fail. In multi-GPU tensor parallelism, a single failure can take down the whole service. <a href="https://arxiv.org/abs/2511.11617">AnchorTP</a> keeps weights and KV caches alive in a daemon outside the inference process, repartitions the model across the remaining GPUs with unequal widths, and plans the minimum data movement needed to recover.</p>
  <p><strong>Infrastructure for training agents.</strong> The same two lessons reappear, in sharper form, when training agents with <a href="{{ '/research/agentic-intelligence/#signal' | relative_url }}">harness-native reinforcement learning</a>. In Lego-RL, almost all of a training trial is the agent acting: reading files, editing code and running tests in a sandbox. Trials are long and uneven, so synchronous batches wait for their slowest member; asynchronous scheduling lets new trials start as soon as a slot frees up. When the trainer updates the weights mid-trial, partial rollout pauses generation, loads the new weights and resumes on the same replica from its cached prefix, so a long attempt is not thrown away. Starting a sandbox is dominated by building its image, so prebuilt task images, a mounted agent runtime and lazy image pulls remove most of that wait. One deliberate exception: the grading toolchain is baked into each image even though it costs a little time, because a reproducible reward is worth more than a faster one. Agentic RL is, to a large degree, an efficiency and reliability problem.</p>

  <h2 id="transfer">5. Transfer: the strongest teacher is not the best teacher</h2>
  <p class="research-claim">Distillation works best when the signal matches what the student can learn, not when the teacher is strongest.</p>
  <p>For LLMs, <a href="https://arxiv.org/abs/2404.02657">forward and reverse KL divergence</a> turn out to share the same optimum, and neither shows the mode-seeking or mean-seeking behavior usually attributed to it. The practical difference appears early in training, when forward KL focuses on the head of the teacher's distribution and reverse KL on the tail; Adaptive KL weights the two accordingly. <a href="https://arxiv.org/abs/2510.10925">PerSyn</a> starts from the observation that stronger models are not always better teachers, and routes each prompt to the teacher a given student learns from best before generating any data, instead of generating with every teacher and selecting afterwards.</p>
  <p>The same conclusion shows up independently in agent training, where grounded trajectories from weaker agents teach better than answers from stronger ones, and where <a href="{{ '/research/agentic-intelligence/#signal' | relative_url }}">verbal feedback from black-box teachers</a> can guide a student without exposing token probabilities.</p>

  <h2 id="insights">What ties it together</h2>
  <ol class="research-insights">
    <li><strong>Diagnose the broken assumption before optimizing.</strong> Each result here started from asking why an existing method failed, not from trying a faster variant. The fix was usually small once the cause was clear.</li>
    <li><strong>Non-uniformity is the rule.</strong> Layers, modules, modalities, tokens and teachers all differ. Allocating budgets adaptively, per layer, module, modality or prompt, recurs across compression, caching and distillation.</li>
    <li><strong>Keep a way back.</strong> Recallable evictions, state preserved outside the process that can crash, and rollouts that survive weight updates make aggressive optimization safe.</li>
    <li><strong>Coordination dominates at scale.</strong> In test-time scaling, serving and agent training alike, the biggest gains come from removing waiting rather than speeding up arithmetic.</li>
    <li><strong>Efficiency shapes what can be learned.</strong> Rare-token embeddings that compute cannot train, and teachers whose outputs a student cannot absorb, show that efficiency is not only about cost but about what a model is able to learn.</li>
  </ol>

  <h2 id="open-questions">Open questions</h2>
  <ul>
    <li>How should vocabulary be chosen once inference cost, multilingual data and code are part of the objective?</li>
    <li>What should long-context memory keep for agents, whose context is dominated by tool outputs rather than prose?</li>
    <li>How far can rollout efficiency go in agentic RL, where acting, not computing gradients, takes most of the time?</li>
    <li>Can the fault-tolerance ideas used in serving make long training runs equally resilient?</li>
  </ul>

  {% include research/paper-list.liquid group="efficient" lang="en" %}

  <p>Related: <a href="{{ '/research/agentic-intelligence/' | relative_url }}">Agentic coding, reasoning and evaluation</a></p>
</div>
