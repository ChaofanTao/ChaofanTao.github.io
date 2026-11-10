---
layout: default
title: "Efficient ML & AI Infrastructure"
description: "Chaofan Tao's research on efficient machine learning and AI infrastructure: quantization and pruning, vocabulary scaling, KV cache compression, fast test-time scaling, distillation and resilient training and serving, and his thoughts on infrastructure for large-scale agentic data, trajectory-level efficiency, very long-horizon runs and AI for Science."
permalink: /research/efficient-ml-ai-infrastructure/
research_lang: en
last_modified_at: 2026-11-09
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
  - Agentic data infrastructure
  - AI for AI
  - AI for Science
---

{% include research/styles.liquid %}
{% include research/jsonld.liquid group="efficient" %}

<div class="research-page">
  <nav class="research-breadcrumb" aria-label="Breadcrumb">
    <a href="{{ '/' | relative_url }}">Chaofan Tao</a><span aria-hidden="true">/</span>
    <a href="{{ '/research/' | relative_url }}">Research</a><span aria-hidden="true">/</span>
    <span>Efficient ML and AI infrastructure</span>
  </nav>

  <h1>Efficient ML &amp; AI Infrastructure</h1>
  <p class="research-dek">My work in this area began with compressing language models and has moved toward the systems that train agents. In the current era, I think the unit of efficiency is no longer a single forward pass but a whole trajectory, and the infrastructure that produces agentic data becomes as important as the model itself.</p>
  <p class="research-meta">By <a href="{{ '/' | relative_url }}">Chaofan Tao (陶超凡)</a> · Last updated <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%B %-d, %Y" }}</time></p>

  <p>Most of my work on efficiency began the same way: an existing method failed, or wasted resources, and the useful question was why. Usually the answer was an assumption that had quietly stopped being true. That the tokenizer can be fixed before scaling. That every part of a network tolerates compression equally. That every cached token matters. That waiting for synchronization is free. That GPUs don't fail. That the strongest teacher teaches best. Once the broken assumption is clear, the fix is often simple.</p>
  <p>This page follows those questions through a model's life, from design to compression, memory, serving and transfer, and then to the infrastructure for training agents. The last part is where I think the most important efficiency problems now are.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/efficiency-lifecycle.svg' | relative_url }}" alt="Diagram of five lifecycle stages, design, compress, remember, compute and serve, and transfer, each paired with its central question and the projects that address it. All projects are work by Chaofan Tao and collaborators." width="960" height="325" loading="eager"></div>
    <figcaption>Efficiency across a model's life. Each stage pairs its central question with the work that addresses it.</figcaption>
    <div class="research-works" id="works">
      <p class="research-works-note">All work in this figure is by Chaofan Tao and collaborators:</p>
      <p><strong>Design</strong>: <a href="https://arxiv.org/abs/2407.13623">Scaling Laws with Vocabulary</a> <span class="research-venue">(NeurIPS 2024)</span></p>
      <p><strong>Compress</strong>: <a href="https://arxiv.org/abs/2203.10705">Quantization of generative LMs</a> <span class="research-venue">(ACL 2022 Outstanding Paper)</span> · <a href="https://doi.org/10.18653/v1/2023.findings-acl.692">Structured pruning</a> <span class="research-venue">(Findings of ACL 2023)</span> · <a href="https://arxiv.org/abs/2301.13741">UPop</a> <span class="research-venue">(ICML 2023)</span> · <a href="https://arxiv.org/abs/2305.17455">CrossGET</a> <span class="research-venue">(ICML 2024)</span></p>
      <p><strong>Remember</strong>: <a href="https://arxiv.org/abs/2406.13035">D2O</a> <span class="research-venue">(ICLR 2025)</span> · <a href="https://arxiv.org/abs/2410.03090">UNComp</a> <span class="research-venue">(EMNLP 2025)</span> · <a href="https://arxiv.org/abs/2606.10537">Prefilling-dLLM</a> <span class="research-venue">(EMNLP 2026)</span></p>
      <p><strong>Compute and serve</strong>: <a href="https://arxiv.org/abs/2509.15148">ATTS</a> <span class="research-venue">(ICLR 2026)</span> · <a href="https://arxiv.org/abs/2511.11617">AnchorTP</a> <span class="research-venue">(DATE 2026)</span> · <a href="https://arxiv.org/abs/2608.17393">Lego-RL</a> <span class="research-venue">(arXiv 2026)</span></p>
      <p><strong>Transfer</strong>: <a href="https://arxiv.org/abs/2404.02657">Adaptive KL</a> <span class="research-venue">(COLING 2025)</span> · <a href="https://arxiv.org/abs/2510.10925">PerSyn</a> <span class="research-venue">(ACL 2026)</span></p>
    </div>
  </figure>

  <p class="research-toc">On this page: <a href="#compress">Representations and compression</a> · <a href="#remember">Memory and inference</a> · <a href="#transfer">Transfer</a> · <a href="#serve">Systems and reliability</a> · <a href="#at-a-glance">At a glance</a> · <a href="#lessons">What we learned</a> · <a href="#outlook">Some thoughts on the future</a> · <a href="#open-questions">Open questions</a></p>

  <h2 id="compress">1. Representations and compression</h2>
  <p><strong>Generative models turned out to be harder to compress, and the reason was in the representations.</strong> My work in this direction began with <a href="https://arxiv.org/abs/2203.10705">quantizing generative language models</a>, which received an ACL 2022 Outstanding Paper Award. Methods that worked for BERT-style encoders fell apart on GPT-style generators, and it wasn't clear why. We traced it to two problems. At low precision, word embeddings collapse until they look almost the same, so a model choosing its next token can no longer tell the options apart. And weights in different modules are spread very differently, so no single quantizer setting suits them all. Token-level contrastive distillation keeps each token's representation distinct, and module-wise dynamic scaling gives each module its own range.</p>
  <p><a href="https://doi.org/10.18653/v1/2023.findings-acl.692">Structured pruning for generative models</a> applied the same idea to removal, learning which components can go. For vision-language models, where images and text carry information very differently, <a href="https://arxiv.org/abs/2301.13741">UPop</a> searches for a smaller network across both modalities at once, so the model learns how much to prune from each, and <a href="https://arxiv.org/abs/2305.17455">CrossGET</a> merges redundant tokens at run time, using one modality to guide matching in the other.</p>
  <p><strong>The vocabulary is a less obvious place to look.</strong> Scaling laws usually leave it out, which is why models of similar size ship with very different vocabularies. In <a href="https://arxiv.org/abs/2407.13623">Scaling Laws with Vocabulary</a>, we treated vocabulary size as a scaling dimension in its own right. Three independent ways of estimating the best size agreed: it grows with compute, though more slowly than the rest of the model, and most models under-invest in it. The reason is a trade-off. A bigger vocabulary represents the same text with fewer tokens, but under a limited budget, rare tokens never get trained well. It gives a principled basis for the move toward larger vocabularies in recent models, and an <a href="https://huggingface.co/spaces/sail/scaling-with-vocab-demo">interactive calculator</a> turns it into a practical choice.</p>

  <h2 id="remember">2. Memory and inference</h2>
  <p><strong>In long-context inference, trimming the KV cache evenly wastes memory, because layers behave differently.</strong> <a href="https://arxiv.org/abs/2406.13035">D2O</a> gives each layer its own budget based on how focused its attention is, and keeps a way to recall or merge dropped tokens that resemble kept ones, without any fine-tuning. <a href="https://arxiv.org/abs/2410.03090">UNComp</a> looks at the same question through information content, using matrix entropy to find what can be compressed; the same analysis points to the heads and layers responsible for retrieval.</p>
  <p><a href="https://arxiv.org/abs/2606.10537">Prefilling-dLLM</a> handles diffusion language models, which re-read the whole prompt at every denoising step, by caching the prompt once in chunks and decoding over only the relevant ones. A small detail mattered there: a beginning-of-sequence token at the start of each chunk gives attention a stable anchor, and with it the sparse version can even beat full attention.</p>
  <p><strong>Test-time scaling improves performance at the cost of substantial memory-bound execution and synchronization overhead.</strong> In <a href="https://arxiv.org/abs/2509.15148">ATTS</a>, when we measured where the time actually went, the main cost was waiting for synchronization, not arithmetic. ATTS replaces those synchronous checks with asynchronous inference and uses conformal prediction, calibrated on the fly, to keep statistical control over how often drafts are rejected.</p>

  <h2 id="transfer">3. Transfer: matching the teacher to the student</h2>
  <p>Distillation passes a teacher's ability to a smaller student. A common story says forward KL divergence spreads out to cover the teacher's distribution while reverse KL locks onto its main mode. For LLMs, <a href="https://arxiv.org/abs/2404.02657">we found</a> that neither really happens: the two share the same optimum, and the practical difference appears early in training, when forward KL focuses on the most likely tokens and reverse KL on the tail. Adaptive KL weights them accordingly. <a href="https://arxiv.org/abs/2510.10925">PerSyn</a> starts from the observation that stronger models are not always better teachers, and sends each prompt to the teacher a particular student learns from best, before any data is generated. The same lesson, that what transfers depends on what the student can absorb, appears again in our <a href="{{ '/research/agentic-intelligence/#data' | relative_url }}">agent trajectory work</a>.</p>

  <h2 id="serve">4. Systems and reliability</h2>
  <p><strong>Serving rests on another hidden assumption: that GPUs don't fail.</strong> With tensor parallelism across several GPUs, losing one can take the whole service down. <a href="https://arxiv.org/abs/2511.11617">AnchorTP</a> keeps the weights and KV caches alive in a separate process that survives the crash, re-splits the model across the remaining GPUs, and plans the least data movement needed to recover.</p>
  <p><strong>Training agents brings these lessons (e.g., waiting and lost state) into sharper focus.</strong> In <a href="https://arxiv.org/abs/2608.17393">Lego-RL</a>, almost all of a training attempt is the agent working in a sandbox, and attempts vary widely in length, so synchronous batches keep waiting for the slowest member; asynchronous scheduling fills those gaps, and partial rollout lets a long attempt survive a weight update by continuing from its cached prefix. Prebuilt task images and lazy image pulls remove most of the sandbox start-up wait, while the grading tools are deliberately baked into every image, because a reward you can reproduce is worth more than one you get slightly faster. How Lego-RL keeps training faithful to what the agent actually did, and how it tells infrastructure failures from policy problems, is covered on the <a href="{{ '/research/agentic-intelligence/#learning' | relative_url }}">agentic intelligence page</a>.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/legox/lego-rl-workflow.png' | relative_url }}" alt="Lego-RL closed-loop workflow: data preparation with sandbox management, image cache, lazy pulls and anti-hacking; run validation; the training run with sandbox execution, in-process proxy, rollout and trainer; a live UI with failure breakdowns and trajectory viewer; and human review." width="1600" height="878" loading="lazy"></div>
    <figcaption>The Lego-RL workflow, from data preparation and sandbox management to live failure diagnosis and human review. Figure from the <a href="https://www.legox.net/blog/lego-rl/">Lego-RL blog</a>.</figcaption>
  </figure>

  <h2 id="at-a-glance">At a glance</h2>
  <p class="research-works-note">All work in this table is by Chaofan Tao and collaborators. Paper links and venues are in the <a href="#works">list under the opening figure</a>.</p>
  <div class="research-table-wrap">
    <table>
      <thead><tr><th>Assumption that broke</th><th>Work</th><th>Diagnosis</th><th>Fix</th></tr></thead>
      <tbody>
        <tr><td>The tokenizer can be fixed before scaling</td><td>Scaling Laws with Vocabulary</td><td>The best vocabulary grows with compute, more slowly than the rest of the model</td><td>Predict vocabulary size from the compute budget</td></tr>
        <tr><td>Every part tolerates low precision equally</td><td>Quantization</td><td>Embeddings collapse; weight ranges differ across modules</td><td>Token-level contrastive distillation; module-wise scaling</td></tr>
        <tr><td>Structure can be pruned uniformly</td><td>Structured pruning · UPop</td><td>Components and modalities differ in how much they can lose</td><td>Learnable masks; pruning ratios learned per modality</td></tr>
        <tr><td>Every visual token is needed</td><td>CrossGET</td><td>Many tokens are redundant across modalities</td><td>Cross-modal guided token merging</td></tr>
        <tr><td>Every cached token matters equally</td><td>D2O · UNComp</td><td>Layers and heads need different things</td><td>Per-layer budgets with recall; entropy-guided compression</td></tr>
        <tr><td>The prompt must be re-read every step</td><td>Prefilling-dLLM</td><td>Diffusion models repeat work on the prefix</td><td>Chunked cache with start-of-sequence anchors</td></tr>
        <tr><td>Synchronization is free</td><td>ATTS</td><td>Waiting dominates test-time scaling</td><td>Asynchronous inference with conformal prediction</td></tr>
        <tr><td>GPUs don't fail</td><td>AnchorTP</td><td>One failure takes the whole service down</td><td>State kept outside the process; minimal migration</td></tr>
        <tr><td>Forward and reverse KL behave differently</td><td>Adaptive KL</td><td>Same optimum; they differ early, on head versus tail</td><td>Weight the two adaptively</td></tr>
        <tr><td>The strongest teacher teaches best</td><td>PerSyn</td><td>What matters is what the student can learn</td><td>Route each prompt to the best-suited teacher</td></tr>
        <tr><td>Agent RL is bounded by the optimizer</td><td>Lego-RL infrastructure</td><td>Most time goes to agents acting and waiting</td><td>Asynchronous scheduling, partial rollout, prebuilt images</td></tr>
      </tbody>
    </table>
  </div>

  <h2 id="lessons">What we learned</h2>
  <ol class="research-insights">
    <li><strong>Find the broken assumption before optimizing.</strong> Every result here started with asking why an existing method failed. Once the cause was clear, the fix was usually small.</li>
    <li><strong>Unevenness is a common fact.</strong> Layers, modules, modalities, tokens and teachers all differ, and giving each its own budget keeps paying off.</li>
    <li><strong>Keep a way back.</strong> Dropped tokens that can be recalled, state that survives a crash, attempts that survive a weight update: these make aggressive optimization safe.</li>
    <li><strong>At scale, waiting is the real cost.</strong> In test-time scaling, serving and agent training alike, the largest gains came from removing waiting rather than from faster arithmetic.</li>
    <li><strong>Efficiency decides what a model can learn.</strong> Rare tokens that never get enough compute and teacher outputs a student can't absorb show that efficiency is about capability, not only cost.</li>
  </ol>

  <h2 id="outlook">Some thoughts on the future</h2>
  <p>These are personal views, each an extension of something the work above taught us.</p>

  <h3 id="agentic-data">Infrastructure for large-scale agentic data is the bottleneck</h3>
  <p><strong>For agents, data means executable environments with a way to check the outcome.</strong> Building LegoFlow and Terminal-Lego showed us where the cost goes: finding candidates is cheap, while building environments, proving tasks with tests, and rolling out and screening trajectories take almost all the effort, and few candidates survive. I think the scaling unit for agentic data is the verified, reproducible environment, and infrastructure should be judged by how many it can build and keep honest per unit of compute.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/agentic-data-pipeline.svg' | relative_url }}" alt="Pipeline from candidate tasks through building environments, verifying tasks, rolling out trajectories and screening them to training data; each stage keeps fewer items, and most of the cost sits in the middle stages handled by LegoFlow's Curator and Tracer." width="960" height="340" loading="lazy"></div>
    <figcaption>Where the cost of agentic data goes. Finding candidates is cheap; building, verifying, rolling out and screening is where the effort lies.</figcaption>
  </figure>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/legox/terminal-lego-pipeline.png' | relative_url }}" alt="Terminal-Lego construction pipeline: collecting high-quality Stack Overflow questions, generating instructions, environments, solutions, Dockerfiles and tests in cascade, reviewing tests, and a Docker round trip that keeps only tasks that pass verification." width="1600" height="892" loading="lazy"></div>
    <figcaption>A concrete example: <a href="https://arxiv.org/abs/2606.03461">Terminal-Lego</a> keeps a task only after a full Docker round trip confirms it. Figure from the <a href="https://www.legox.net/blog/terminal-lego/">Terminal-Lego blog</a>.</figcaption>
  </figure>
  <p>Software is the easy case, because tests give a clean signal. The next wave is cowork data, documents, spreadsheets, email and multi-app workflows with people in the loop, where checking outcomes is much harder. I expect the teams that build this infrastructure, not those with the most raw logs, to have the best agentic data.</p>

  <div class="research-table-wrap">
    <table>
      <thead><tr><th></th><th>Coding data</th><th>Cowork data</th></tr></thead>
      <tbody>
        <tr><td>Environment</td><td>A repository snapshot in a container</td><td>Documents, spreadsheets, email, several apps, often a person</td></tr>
        <tr><td>Outcome check</td><td>Original fails the tests, the fix passes</td><td>App state plus a quality judgment; rarely unit tests</td></tr>
        <tr><td>Main difficulty</td><td>Answer leakage, scale, shallow trajectories</td><td>Simulating apps and people; judging "done well"</td></tr>
        <tr><td>Infrastructure</td><td>Fast builds, isolated sandboxes, anti-leakage, provenance</td><td>Simulated apps and users, quality checkers, replayable sessions</td></tr>
      </tbody>
    </table>
  </div>

  <h3 id="trajectory-efficiency">Efficiency should be measured at a granular level</h3>
  <p>Most efficiency methods, including ours, are judged one response at a time, but for an agent, dropping one detail can cost several extra steps later. Efficiency should be measured per task, as total compute, memory and time to a verified result, and the D2O and UNComp idea of keeping a way back should apply to observations and actions, not only tokens.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/trajectory-efficiency.svg' | relative_url }}" alt="Two trajectories: with full context, the agent reaches a verified result in a few steps; with a detail dropped from the context, each call is cheaper but extra steps to re-read, retry and re-test make the whole task slower and costlier." width="900" height="300" loading="lazy"></div>
    <figcaption>Saved per call, lost per task. Efficiency for agents should be measured over the whole trajectory to a verified result.</figcaption>
  </figure>

  <h3 id="long-runs">Very long-horizon runs need layered memory and resumable state</h3>
  <p>No context window holds weeks of tool output, so memory will need layers: a short working context, compressed summaries, and a searchable store for exact details, a project-level version of D2O's recall. Since machines and sandboxes will fail over weeks, AnchorTP's separation of state from crashing processes and partial rollout's resuming should become standard.</p>

  <h3 id="verification-compute">AI for AI and AI for Science: compute should flow to verification</h3>
  <p>In AI-for-AI loops, checking is where reliability is won or lost, so cheaper reviewers and verifiers, of the kind <a href="https://arxiv.org/abs/2607.06065">SWE-Review</a> points to, are likely the biggest lever. Science sharpens this, because the expensive step is the experiment. The draft-and-check pattern may fit: a cheap surrogate screens many candidates, the expensive experiment checks the most promising, and calibrated rules set how much to filter, at the risk of removing exactly the surprising ones. Failed experiments should be kept, with their settings.</p>

  <h2 id="open-questions">Open questions</h2>
  <p>Questions I find most important for this direction, some raised by our own work and some by where the field is now.</p>
  <ul class="research-questions">
    <li><strong>Is there a scaling law for agentic data?</strong> For text we know how loss scales with tokens. For agents the unit is a verified environment, and we do not know how capability scales with their number, variety and difficulty, what each should cost, or how to check environments that have no unit tests, such as cowork tasks.</li>
    <li><strong>What is compute-optimal for an agent?</strong> We know how to split training compute between <a href="https://arxiv.org/abs/2203.15556">parameters and data</a>, and that <a href="https://arxiv.org/abs/2408.03314">test-time compute</a> can beat a larger model. An agent's budget can also go to more turns, more attempts or more checking, so deciding when to answer, think longer, act or verify is itself a policy it has to learn. How ATTS splits compute between drafting and checking (<a href="https://arxiv.org/abs/2509.15148">paper</a> · <a href="https://github.com/menik1126/Asynchronous-Test-Time-Scaling">code</a>), and where LegoFlow found teachers should think hard, are small pieces of that policy.</li>
    <li><strong>How far can training and inference drift apart before RL breaks?</strong> Asynchronous and partial rollouts make data slightly off-policy, and even the same weights can produce <a href="https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/">different numbers</a> in an inference engine and a trainer. Throughput rewards more drift and stability punishes it; the safe boundary is still found by trial and error.</li>
    <li><strong>Can small models learn long-horizon agent skills?</strong> The best teacher is the one a student can learn from, but it is unclear whether a small model can absorb planning and self-checking from traces, or whether some of that only appears at scale.</li>
    <li><strong>Which efficiency techniques survive new architectures?</strong> Diffusion language models, hybrid attention, etc.</li>
  </ul>

  <!-- <p class="research-readmore">Code and experiments: <a href="https://github.com/sail-sg/scaling-with-vocab">Vocabulary study</a> · <a href="https://huggingface.co/spaces/sail/scaling-with-vocab-demo">Vocabulary calculator</a> · <a href="https://github.com/LegoX/Lego-RL">Lego-RL</a> · <a href="https://github.com/LegoX/LegoFlow">LegoFlow</a></p> -->

  {% include research/paper-list.liquid group="efficient" lang="en" %}

  <p>Related: <a href="{{ '/research/agentic-intelligence/' | relative_url }}">Agentic intelligence</a></p>
</div>
