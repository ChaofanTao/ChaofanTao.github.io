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
    <span aria-hidden="true">·</span><a href="{{ '/zh/research/efficient-ml-ai-infrastructure/' | relative_url }}" lang="zh-Hans">中文版</a>
  </nav>

  <h1>Efficient ML &amp; AI Infrastructure</h1>
  <p class="research-dek">To me, efficiency means keeping the information that matters and dropping the work that doesn't. My work in this area began with compressing language models and has moved toward the systems that train agents. In the agent era, I think the unit of efficiency is no longer a single forward pass but a whole trajectory, and the infrastructure that produces agentic data becomes as important as the model itself.</p>
  <p class="research-meta">By <a href="{{ '/' | relative_url }}">Chaofan Tao (陶超凡)</a> · Last updated <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%B %-d, %Y" }}</time></p>

  <p>Most of my efficiency work began the same way: an existing method failed, or wasted resources, and the useful question was why. Usually the answer was an assumption that had quietly stopped being true. That the tokenizer can be fixed before scaling. That every part of a network tolerates compression equally. That every cached token matters. That waiting for synchronization is free. That GPUs don't fail. That the strongest teacher teaches best. Once the broken assumption is clear, the fix is often simple.</p>
  <p>This page follows those questions through a model's life, from design to compression, memory, serving and transfer, and then to the infrastructure for training agents. The last part is where I think the most important efficiency problems now are.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/efficiency-lifecycle.svg' | relative_url }}" alt="Diagram of five lifecycle stages, design, compress, remember, compute and serve, and transfer, each paired with its central question and the projects that address it. All projects are work by Chaofan Tao and collaborators." width="960" height="325" loading="eager"></div>
    <figcaption>Efficiency across a model's life. Each stage pairs its central question with the work that addresses it.</figcaption>
    <div class="research-works">
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
  <p>My work in this direction began with <a href="https://arxiv.org/abs/2203.10705">quantizing generative language models</a> <span class="research-venue">(ACL 2022 Outstanding Paper)</span>. Methods that worked for BERT-style encoders fell apart on GPT-style generators, and it wasn't clear why. We traced it to two problems. At low precision, word embeddings collapse until they look almost the same, so a model choosing its next token can no longer tell the options apart. And weights in different modules are spread very differently, so no single quantizer setting suits them all. Token-level contrastive distillation keeps each token's representation distinct, and module-wise dynamic scaling gives each module its own range. The diagnosis mattered more than the method: it explained why generation is harder to compress than classification.</p>
  <p><a href="https://doi.org/10.18653/v1/2023.findings-acl.692">Structured pruning for generative models</a> <span class="research-venue">(Findings of ACL 2023)</span> applied the same idea to removal, learning which components can go. For vision-language models, where images and text carry information very differently, <a href="https://arxiv.org/abs/2301.13741">UPop</a> <span class="research-venue">(ICML 2023)</span> searches for a smaller network across both modalities at once, so the model learns how much to prune from each, and <a href="https://arxiv.org/abs/2305.17455">CrossGET</a> <span class="research-venue">(ICML 2024)</span> merges redundant tokens at run time, using one modality to guide matching in the other.</p>
  <p>The vocabulary is a less obvious place to look. Scaling laws usually leave it out, which is why models of similar size ship with very different vocabularies. In <a href="https://arxiv.org/abs/2407.13623">Scaling Laws with Vocabulary</a> <span class="research-venue">(NeurIPS 2024)</span>, we treated vocabulary size as a scaling dimension in its own right. Three independent ways of estimating the best size agreed: it grows with compute, though more slowly than the rest of the model, and most models under-invest in it. The reason is a trade-off. A bigger vocabulary represents the same text with fewer tokens, but under a limited budget, rare tokens never get trained well. It gives a principled basis for the move toward larger vocabularies in recent models, and an <a href="https://huggingface.co/spaces/sail/scaling-with-vocab-demo">interactive calculator</a> turns it into a practical choice.</p>

  <h2 id="remember">2. Memory and inference</h2>
  <p>In long-context inference, the KV cache soon takes most of the memory, and trimming it evenly wastes it, because layers behave differently. <a href="https://arxiv.org/abs/2406.13035">D2O</a> <span class="research-venue">(ICLR 2025)</span> gives each layer its own budget based on how focused its attention is, and keeps a way to recall or merge dropped tokens that resemble kept ones, without any fine-tuning. <a href="https://arxiv.org/abs/2410.03090">UNComp</a> <span class="research-venue">(EMNLP 2025)</span> looks at the same question through information content, using matrix entropy to find what can be compressed; the same analysis points to the heads and layers responsible for retrieval. <a href="https://arxiv.org/abs/2606.10537">Prefilling-dLLM</a> <span class="research-venue">(EMNLP 2026)</span> handles diffusion language models, which re-read the whole prompt at every denoising step, by caching the prompt once in chunks and decoding over only the relevant ones. A small detail mattered there: a beginning-of-sequence token at the start of each chunk gives attention a stable anchor, and with it the sparse version can even beat full attention.</p>
  <p>Test-time scaling improves answers by spending more compute while generating, often with a small model drafting and a large one checking. In <a href="https://arxiv.org/abs/2509.15148">ATTS</a> <span class="research-venue">(ICLR 2026)</span>, when we measured where the time actually went, the main cost was waiting for synchronization, not arithmetic. ATTS replaces those synchronous checks with asynchronous inference and uses conformal prediction, calibrated on the fly, to keep statistical control over how often drafts are rejected.</p>

  <h2 id="transfer">3. Transfer: matching the teacher to the student</h2>
  <p>Distillation passes a teacher's ability to a smaller student. A common story says forward KL divergence spreads out to cover the teacher's distribution while reverse KL locks onto its main mode. For LLMs, <a href="https://arxiv.org/abs/2404.02657">we found</a> <span class="research-venue">(COLING 2025)</span> that neither really happens: the two share the same optimum, and the practical difference appears early in training, when forward KL focuses on the most likely tokens and reverse KL on the tail. Adaptive KL weights them accordingly. <a href="https://arxiv.org/abs/2510.10925">PerSyn</a> <span class="research-venue">(ACL 2026)</span> starts from the observation that stronger models are not always better teachers, and sends each prompt to the teacher a particular student learns from best, before any data is generated. The same lesson, that what transfers depends on what the student can absorb, appears again in our <a href="{{ '/research/agentic-intelligence/#data' | relative_url }}">agent trajectory work</a>.</p>

  <h2 id="serve">4. Systems and reliability</h2>
  <p>Serving rests on another hidden assumption: that GPUs don't fail. With tensor parallelism across several GPUs, losing one can take the whole service down. <a href="https://arxiv.org/abs/2511.11617">AnchorTP</a> <span class="research-venue">(DATE 2026)</span> keeps the weights and KV caches alive in a separate process that survives the crash, re-splits the model across the remaining GPUs, and plans the least data movement needed to recover.</p>
  <p>Training agents brings both lessons, waiting and lost state, into sharper focus. In <a href="https://arxiv.org/abs/2608.17393">Lego-RL</a> <span class="research-venue">(arXiv 2026)</span>, almost all of a training attempt is the agent working in a sandbox, and attempts vary widely in length, so synchronous batches keep waiting for the slowest member. Asynchronous scheduling fills those gaps. When weights update mid-attempt, partial rollout pauses generation, loads the new weights and continues from the cached prefix, so long attempts aren't thrown away. Sandbox start-up is dominated by building images, so prebuilt task images and lazy image pulls remove most of that wait, while the grading tools are deliberately baked into every image, because a reward you can reproduce is worth more than one you get slightly faster. Dashboards that break down why each attempt ended let us tell infrastructure failures from genuine policy problems before misreading a reward curve. <a href="https://www.legox.net/blog/lego-rl-sao/">Single-rollout optimization</a> <span class="research-venue">(LegoX blog, 2026)</span> attacks a different cost: it replaces repeated sampling of the same task with a learned critic, so far fewer trajectories are needed to train.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/legox/lego-rl-workflow.png' | relative_url }}" alt="Lego-RL closed-loop workflow: data preparation with sandbox management, image cache, lazy pulls and anti-hacking; run validation; the training run with sandbox execution, in-process proxy, rollout and trainer; a live UI with failure breakdowns and trajectory viewer; and human review." width="1600" height="878" loading="lazy"></div>
    <figcaption>The Lego-RL workflow, from data preparation and sandbox management to live failure diagnosis and human review. Figure from the <a href="https://www.legox.net/blog/lego-rl/">Lego-RL blog</a>.</figcaption>
  </figure>

  <h2 id="at-a-glance">At a glance</h2>
  <p class="research-works-note">All work in this table is by Chaofan Tao and collaborators.</p>
  <div class="research-table-wrap">
    <table>
      <thead><tr><th>Assumption that broke</th><th>Work</th><th>Diagnosis</th><th>Fix</th></tr></thead>
      <tbody>
        <tr><td>The tokenizer can be fixed before scaling</td><td><a href="https://arxiv.org/abs/2407.13623">Scaling Laws with Vocabulary</a> <span class="research-venue">(NeurIPS 2024)</span></td><td>The best vocabulary grows with compute, more slowly than the rest of the model</td><td>Predict vocabulary size from the compute budget</td></tr>
        <tr><td>Every part tolerates low precision equally</td><td><a href="https://arxiv.org/abs/2203.10705">Quantization</a> <span class="research-venue">(ACL 2022 Outstanding Paper)</span></td><td>Embeddings collapse; weight ranges differ across modules</td><td>Token-level contrastive distillation; module-wise scaling</td></tr>
        <tr><td>Structure can be pruned uniformly</td><td><a href="https://doi.org/10.18653/v1/2023.findings-acl.692">Structured pruning</a> <span class="research-venue">(Findings of ACL 2023)</span> · <a href="https://arxiv.org/abs/2301.13741">UPop</a> <span class="research-venue">(ICML 2023)</span></td><td>Components and modalities differ in how much they can lose</td><td>Learnable masks; pruning ratios learned per modality</td></tr>
        <tr><td>Every visual token is needed</td><td><a href="https://arxiv.org/abs/2305.17455">CrossGET</a> <span class="research-venue">(ICML 2024)</span></td><td>Many tokens are redundant across modalities</td><td>Cross-modal guided token merging</td></tr>
        <tr><td>Every cached token matters equally</td><td><a href="https://arxiv.org/abs/2406.13035">D2O</a> <span class="research-venue">(ICLR 2025)</span> · <a href="https://arxiv.org/abs/2410.03090">UNComp</a> <span class="research-venue">(EMNLP 2025)</span></td><td>Layers and heads need different things</td><td>Per-layer budgets with recall; entropy-guided compression</td></tr>
        <tr><td>The prompt must be re-read every step</td><td><a href="https://arxiv.org/abs/2606.10537">Prefilling-dLLM</a> <span class="research-venue">(EMNLP 2026)</span></td><td>Diffusion models repeat work on the prefix</td><td>Chunked cache with start-of-sequence anchors</td></tr>
        <tr><td>Synchronization is free</td><td><a href="https://arxiv.org/abs/2509.15148">ATTS</a> <span class="research-venue">(ICLR 2026)</span></td><td>Waiting dominates test-time scaling</td><td>Asynchronous inference with conformal prediction</td></tr>
        <tr><td>GPUs don't fail</td><td><a href="https://arxiv.org/abs/2511.11617">AnchorTP</a> <span class="research-venue">(DATE 2026)</span></td><td>One failure takes the whole service down</td><td>State kept outside the process; minimal migration</td></tr>
        <tr><td>Forward and reverse KL behave differently</td><td><a href="https://arxiv.org/abs/2404.02657">Adaptive KL</a> <span class="research-venue">(COLING 2025)</span></td><td>Same optimum; they differ early, on head versus tail</td><td>Weight the two adaptively</td></tr>
        <tr><td>The strongest teacher teaches best</td><td><a href="https://arxiv.org/abs/2510.10925">PerSyn</a> <span class="research-venue">(ACL 2026)</span></td><td>What matters is what the student can learn</td><td>Route each prompt to the best-suited teacher</td></tr>
        <tr><td>Agent RL is bounded by the optimizer</td><td><a href="https://arxiv.org/abs/2608.17393">Lego-RL</a> infrastructure <span class="research-venue">(arXiv 2026)</span></td><td>Most time goes to agents acting and waiting</td><td>Asynchronous scheduling, partial rollout, prebuilt images</td></tr>
      </tbody>
    </table>
  </div>

  <h2 id="lessons">What we learned</h2>
  <ol class="research-insights">
    <li><strong>Find the broken assumption before you optimize.</strong> Every result here started with asking why an existing method failed. Once the cause was clear, the fix was usually small.</li>
    <li><strong>Unevenness is the rule.</strong> Layers, modules, modalities, tokens and teachers all differ, and giving each its own budget keeps paying off.</li>
    <li><strong>Keep a way back.</strong> Dropped tokens that can be recalled, state that survives a crash, attempts that survive a weight update: these make aggressive optimization safe.</li>
    <li><strong>At scale, waiting is the real cost.</strong> In test-time scaling, serving and agent training alike, the largest gains came from removing waiting rather than from faster arithmetic.</li>
    <li><strong>Efficiency decides what a model can learn.</strong> Rare tokens that never get enough compute and teacher outputs a student can't absorb show that efficiency is about capability, not only cost.</li>
  </ol>

  <h2 id="outlook">Some thoughts on the future</h2>
  <p>These are personal views, each an extension of something the work above taught us.</p>

  <h3 id="agentic-data">Infrastructure for large-scale agentic data is the new bottleneck</h3>
  <p>For language models, data meant text. For agents, data means executable environments with a way to check the outcome, and producing them at scale is mostly an infrastructure problem. Building LegoFlow and Terminal-Lego taught us where the cost goes: finding candidate tasks is cheap, but building their environments, proving each one with tests, rolling out trajectories and screening them for leakage and shallow reasoning is where almost all the effort lies, and only a small fraction of candidates survive. I think the scaling unit for agentic data is the verified, reproducible environment, and infrastructure should be judged by how many of those it can build, verify and keep honest per unit of compute. That means fast environment construction and caching, isolated and network-controlled sandboxes, provenance for every task and trajectory, and pipelines designed so that agents themselves can operate them, as LegoFlow's blocks already allow.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/agentic-data-pipeline.svg' | relative_url }}" alt="Pipeline from candidate tasks through building environments, verifying tasks, rolling out trajectories and screening them to training data; each stage keeps fewer items, and most of the cost sits in the middle stages handled by LegoFlow's Curator and Tracer." width="960" height="340" loading="lazy"></div>
    <figcaption>Where the cost of agentic data goes. Finding candidates is cheap; building, verifying, rolling out and screening is where the effort lies.</figcaption>
  </figure>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/legox/terminal-lego-pipeline.png' | relative_url }}" alt="Terminal-Lego construction pipeline: collecting high-quality Stack Overflow questions, generating instructions, environments, solutions, Dockerfiles and tests in cascade, reviewing tests, and a Docker round trip that keeps only tasks that pass verification." width="1600" height="892" loading="lazy"></div>
    <figcaption>A concrete example: <a href="https://arxiv.org/abs/2606.03461">Terminal-Lego</a> <span class="research-venue">(arXiv 2026)</span> keeps a task only after a full Docker round trip confirms it. Figure from the <a href="https://www.legox.net/blog/terminal-lego/">Terminal-Lego blog</a>.</figcaption>
  </figure>
  <p>Software engineering is the easiest case, because tests give a clean signal. The next wave of agentic data will come from collaborative office work, what I think of as cowork data: documents, spreadsheets, email and multi-application workflows, often with a human in the loop. There, checking the outcome is much harder. It needs simulated applications whose state can be inspected, simulated users who respond realistically, and checkers that judge whether a task was done well rather than merely done. I expect the teams that build this infrastructure, rather than the ones with the most raw logs, to have the best agentic data.</p>

  <div class="research-table-wrap">
    <table>
      <thead><tr><th></th><th>Coding data</th><th>Cowork data</th></tr></thead>
      <tbody>
        <tr><td>Environment</td><td>A repository snapshot in a container</td><td>Documents, spreadsheets, email and several applications, often with a person involved</td></tr>
        <tr><td>How the outcome is checked</td><td>Tests: the original fails, the fix passes</td><td>Inspectable application state plus a judgment of quality; usually no unit tests</td></tr>
        <tr><td>Main difficulty</td><td>Answer leakage, building environments at scale, shallow trajectories</td><td>Simulating applications and people; judging "done well", not just "done"</td></tr>
        <tr><td>Infrastructure needed</td><td>Fast builds and caching, isolated sandboxes, anti-leakage, provenance</td><td>Simulated apps with checkable state, simulated users, quality checkers, replayable sessions</td></tr>
      </tbody>
    </table>
  </div>

  <h3 id="trajectory-efficiency">Efficiency should be measured per trajectory, not per call</h3>
  <p>Most efficiency methods, including many of ours, are evaluated one response at a time. For an agent, a compression or caching choice that loses one detail can cost several extra steps later, and the savings vanish. I think efficiency for agents has to be measured at the level of the whole task: total compute, memory and time to a verified result.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/trajectory-efficiency.svg' | relative_url }}" alt="Two trajectories: with full context, the agent reaches a verified result in a few steps; with a detail dropped from the context, each call is cheaper but extra steps to re-read, retry and re-test make the whole task slower and costlier." width="900" height="300" loading="lazy"></div>
    <figcaption>Saved per call, lost per task. Efficiency for agents should be measured over the whole trajectory to a verified result.</figcaption>
  </figure>

  <p>This also changes what memory should keep. An agent's context is dominated by tool output rather than prose, so the idea behind D2O and UNComp, keeping what later steps will need and keeping a way back for what was dropped, should be applied to observations and actions, not just tokens.</p>

  <h3 id="long-runs">Very long-horizon runs: weeks of work need the memory and reliability we expect from serving</h3>
  <p>As agents take on tasks that last days or weeks, and agent training runs touch thousands of sandboxes, two old problems come back at a larger scale. The first is memory. No context window holds weeks of tool output, so an agent will need memory in layers: a short working context, compressed summaries of earlier work, and a store it can search when it needs exact details again. D2O's "recall what was dropped" and UNComp's view of which parts carry information are early versions of this at the token level; Prefilling-dLLM's idea of caching a long prefix once and reading only the relevant chunks is another. The same principles, budgeting unevenly and always keeping a way back, should carry over to the level of a whole project.</p>
  <p>The second is reliability. Over weeks, machines fail, sandboxes break and models get updated mid-task. The ideas that made serving resilient in AnchorTP, keeping state separate from the processes that can crash and recovering with the least movement, and the idea behind partial rollout, continuing from where you were instead of starting over, need to become standard for long runs. That includes records precise enough to resume an experiment and still trust its result after a failure, and cost accounting at the level of the whole task, so that we know what a week of agent work actually costs.</p>

  <h3 id="ai-for-ai-compute">In AI-for-AI loops, compute should flow to verification</h3>
  <p>When AI helps improve AI, each round spends compute on proposing candidates, running them, checking them and confirming the winners. Our agent work suggests that checking is where reliability is won or lost. So I think the efficiency question for these loops is less "how fast can we generate candidates?" and more "how cheaply can we trust a result?" Cheaper reviewers and verifiers, of the kind <a href="https://arxiv.org/abs/2607.06065">SWE-Review</a> and SWE-Lego's verifier point to, are likely to be the biggest lever. Progress should also be counted at the same total budget across rounds, including failed attempts and replication, so that an improvement in the loop is not confused with simply spending more.</p>

  <h3 id="ai-for-science">AI for Science: spend cheap compute to decide where expensive experiments go</h3>
  <p>In science, the expensive step is usually not the model but the experiment: a long simulation, a wet-lab run, time on an instrument. That makes the draft-and-check pattern from ATTS a natural fit. A cheap model or a fast surrogate simulation proposes and screens many candidates, and the expensive simulation or experiment checks only the most promising ones, with calibrated rules, like the conformal prediction in ATTS, controlling how much is filtered out at each stage. I suspect the same reasoning that made vocabulary a scaling dimension will apply to scientific data too: how molecules, sequences or measurements are broken into tokens is a design choice that should scale with the budget, not a fixed preprocessing step. And because experiments are costly to repeat, the infrastructure lessons from agentic data apply directly: every result should carry its provenance and settings, failed experiments should be kept rather than discarded, and a finding should be counted only after it is reproduced under conditions that were not used to find it.</p>

  <h2 id="open-questions">Open questions</h2>
  <ul class="research-questions">
    <li><strong>What does a verified, reproducible environment for collaborative office work look like?</strong> Without unit tests, outcomes have to be checked through application state and quality judgments, and we do not yet know how to make those checks cheap and hard to game.</li>
    <li><strong>How should vocabulary and caches be designed for agents whose context is mostly tool output?</strong> Logs, file listings and test results look nothing like the prose our tokenizers and cache policies were tuned on.</li>
    <li><strong>How much of agent RL's cost can be removed before capability starts to suffer?</strong> Asynchronous scheduling, partial rollout and single-rollout training all save compute, but each changes how fresh the training data is relative to the policy.</li>
    <li><strong>How should a week-long agent decide what to forget?</strong> At the token level we can measure what attention uses. At the project level, the value of a detail may only become clear days later.</li>
    <li><strong>How should an AI-for-AI loop split its budget between exploring and verifying?</strong> Too little checking lets false gains through; too much slows the search. We lack a principled way to set that balance.</li>
    <li><strong>When can a cheap surrogate be trusted to screen scientific experiments?</strong> A surrogate that filters out the very candidates that would have been surprising defeats the purpose. Calibration helps, but science often cares most about the cases a surrogate has never seen.</li>
  </ul>

  <p class="research-readmore">Code and experiments: <a href="https://github.com/sail-sg/scaling-with-vocab">Vocabulary study</a> · <a href="https://huggingface.co/spaces/sail/scaling-with-vocab-demo">Vocabulary calculator</a> · <a href="https://github.com/LegoX/Lego-RL">Lego-RL</a> · <a href="https://github.com/LegoX/LegoFlow">LegoFlow</a></p>

  {% include research/paper-list.liquid group="efficient" lang="en" %}

  <p>Related: <a href="{{ '/research/agentic-intelligence/' | relative_url }}">Agentic intelligence</a></p>
</div>
