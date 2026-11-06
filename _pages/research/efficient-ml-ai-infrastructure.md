---
layout: default
title: "Efficient ML & AI Infrastructure"
description: "Research on compression, vocabulary, distillation and training and inference systems, with open questions about infrastructure for multi-agent exploration, AI for AI and self-improvement."
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
  - Long-horizon agents
  - Multi-agent systems
  - AI for AI
  - Recursive self-improvement
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
  <p class="research-dek">What can we do with the resources saved by a smaller model or faster inference? Try another line of inquiry, replicate a result, or run an experiment that was previously out of reach. Work on compression, vocabulary, caches and training systems leads naturally to questions about autonomous exploration and AI for AI.</p>
  <p class="research-meta">By <a href="{{ '/' | relative_url }}">Chaofan Tao (陶超凡)</a> · Last updated <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%B %-d, %Y" }}</time></p>

  <p>My early work focused on quantization and pruning, followed by research on vocabulary, long contexts, distillation, and training and inference systems. These projects span different stages and collaborations. They also share a set of questions: which computation contributes to capability, which information must survive, and which work can be avoided or reused?</p>
  <p>As agents conduct longer investigations and begin to help improve AI systems, these choices accumulate. Saving memory on one inference could let more candidates run concurrently. An approximation that loses an important detail could also affect the next dozen actions. Following those consequences helps place a local efficiency result in the larger research process.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/efficiency-lifecycle.svg' | relative_url }}" alt="Five areas of efficiency research and related work: vocabulary design, model compression, context caches, computation and serving, and knowledge transfer." width="960" height="300" loading="eager"></div>
    <figcaption>From representations to runtime systems, each choice affects how much useful learning and exploration a fixed budget can support.</figcaption>
  </figure>

  <p class="research-toc">On this page: <a href="#design">Vocabulary</a> · <a href="#compress">Compression</a> · <a href="#remember">Memory and caches</a> · <a href="#serve">Training and serving</a> · <a href="#transfer">Transfer</a> · <a href="#long-horizon">Autonomous research</a> · <a href="#insights">Measuring progress</a> · <a href="#open-questions">Open questions</a></p>

  <h2 id="design">Why should the same text cost different amounts of compute?</h2>
  <p>The number of tokens representing a passage determines how much sequence processing it needs. Larger vocabularies usually shorten the sequence, but enlarge the embedding and output layers and require enough data to learn rare entries. Vocabulary belongs in the same design problem as model size and data.</p>
  <p>In <a href="https://arxiv.org/abs/2407.13623">Scaling Laws with Vocabulary</a>, we separated vocabulary parameters from the rest of the network and compared data in characters across tokenizers. In one experiment at a fixed compute budget, moving from a 32K to a 43K vocabulary raised ARC-Challenge performance from 29.1 to 32.0. Reallocating an existing budget changed the capability learned from it.</p>
  <p>Multilingual text, code and tool calls change token frequencies and sequence lengths. A choice suited to training also needs its output-layer cost assessed at deployment. Could vocabulary design account for the whole period of use? The <a href="https://huggingface.co/spaces/sail/scaling-with-vocab-demo">interactive calculator</a> gives estimates under the paper's setup, and the <a href="https://github.com/sail-sg/scaling-with-vocab">code</a> supports further investigation of the trade-offs.</p>

  <h2 id="compress">Which distinctions must survive compression?</h2>
  <p>In our <a href="https://arxiv.org/abs/2203.10705">work on quantizing generative language models</a>, reduced precision made different token embeddings too similar, weakening distinctions needed to choose the next token. Weight distributions also differed across modules, making a uniform setting unsuitable. We used token-level contrastive distillation to preserve distinctions and dynamic scaling to adapt the quantization range by module. This work received an ACL 2022 Outstanding Paper Award.</p>
  <p>Subsequent <a href="https://aclanthology.org/2023.findings-acl.692/">structured pruning</a> learned which network structures could be removed. For vision-language models, <a href="https://arxiv.org/abs/2301.13741">UPop</a> jointly allocated compression across modalities, while <a href="https://arxiv.org/abs/2305.17455">CrossGET</a> used information across image and text to merge similar tokens. Each method has to identify which differences the task needs.</p>
  <p>For a model that acts, the consequences extend into later steps. A change in tool choice changes what evidence becomes available next. Could compression be assessed through these complete interactions, alongside single-response scores? That would help establish whether additional retries consume the compute originally saved.</p>

  <h2 id="remember">The detail worth keeping might be one line</h2>
  <p>A long record can contain one sentence explaining why an experiment failed. Keeping it might prevent repeated trips down the same path. Once a problem is understood, a much longer log may be useful only for a few results. The difficulty is that an apparently minor detail may matter many steps later.</p>
  <p>The KV cache stores intermediate representations of earlier tokens to avoid repeated computation, but consumes more memory as context grows. <a href="https://arxiv.org/abs/2406.13035">D2O</a> allocates budgets using attention patterns across layers and compensates for eviction through recall or merging. <a href="https://arxiv.org/abs/2410.03090">UNComp</a> uses matrix entropy to guide compression through the distribution of information. <a href="https://arxiv.org/abs/2606.10537">Prefilling-dLLM</a> addresses repeated prefix computation in diffusion models by reusing chunked caches across denoising steps.</p>
  <p>Recent <a href="https://arxiv.org/abs/2609.31395">ActKV</a> work manages caches according to their contribution to subsequent actions. <a href="https://arxiv.org/abs/2610.28577">Cache Engineering for Agents</a> lets agents operate directly on active caches and shows that identical text can correspond to different internal states after different cache operations. This raises a concrete training question: if execution used those operations, would replaying the text reconstruct the original decision conditions?</p>
  <p>Shared memory among agents adds another layer. A record saying that method A works better may depend on a particular dataset and experiment setup. Could conclusions be stored with their evidence and conditions, then checked again when those conditions change? Internal caches and external experiment records both matter here, but require separate investigation.</p>

  <h2 id="serve">A system has to keep running after the first successful run</h2>
  <p>In <a href="https://www.legox.net/blog/lego-rl/">Lego-RL's timing analysis</a>, an OpenHands SDK trial takes about 920 seconds on average, with 91.3% spent in execution, including inference and tool interaction. Trial lengths differ, so a synchronous batch waits for its slowest member. Asynchronous scheduling can fill the gaps, while introducing another problem: the model may have been updated by the time a record reaches training.</p>
  <p>The reported step-time speedup was 2.5×, with an estimated scheduling gain of about 1.9× after correcting for GPU compute-throughput differences. <a href="https://www.legox.net/blog/lego-rl-sao/">SAO</a> saves on repeated sampling of the same task by using a learned value model for the training baseline. It reached its own best checkpoint with 73.7% fewer trajectories than GSPO, at Verified scores of 68.6% and 70.4% respectively. These are different sources of efficiency, with concrete cost and capability trade-offs.</p>
  <p>For inference, <a href="https://arxiv.org/abs/2509.15148">ATTS</a> reduces synchronization between draft and target models using online calibration and conformal prediction. <a href="https://arxiv.org/abs/2511.11617">AnchorTP</a> accelerates failure recovery by preserving available GPU state, repartitioning computation and reducing data movement. Autonomous research adds questions about the experiment's own progress and which results remain valid. Restoring an inference service leaves the resumption of a long experiment to be established separately.</p>

  <h2 id="transfer">How can a useful discovery be retained?</h2>
  <p>Distillation studies how a student inherits a teacher's capabilities. Our <a href="https://arxiv.org/abs/2404.02657">comparison of forward and reverse KL divergence</a> found that, in the studied setting, they approach the same objective with sufficient training but differ under limited budgets. Forward KL initially emphasizes high-probability regions, reverse KL the tail. Adaptive KL adjusts their relative weights.</p>
  <p><a href="https://arxiv.org/abs/2510.10925">PerSyn</a> selects a teacher for each prompt and student's learnability before generating data, avoiding the cost of asking every teacher and filtering afterward. This connects to <a href="{{ '/research/agentic-intelligence/#experience' | relative_url }}">Terminal-Lego's demonstration study</a>: useful experience still has to be retained in a form that supports learning.</p>
  <p>If several agents discover a better search or experimental method, how should the next system inherit it? Keeping code, storing a skill and distilling behavior into weights could have different costs and ranges of transfer. How would we establish that the system inherited a method, rather than answers to one collection of tasks? This is a further connection between efficiency and self-improvement.</p>

  <h2 id="long-horizon">Where should autonomous research spend its compute?</h2>
  <p>A research round can run several candidates while also budgeting selection, replication and subsequent training. Parallelism can shorten waits and add duplicate work or expensive aggregation. In the exploratory experiments in <a href="https://arxiv.org/abs/2610.00980">Can AI Scientists Coordinate at Runtime?</a>, dynamic member selection helped, while adding more elaborate coordination and verification did not consistently improve outcomes under the tested budgets. Allocating resources between exploration and checking is itself a problem to learn and evaluate.</p>
  <p><a href="https://arxiv.org/abs/2608.20318">AI4AI-Bench</a> makes the training algorithm the object of improvement: agents modify learning methods, which are then rerun from scratch and checked by hidden evaluators. This helps separate faster program execution from better learning. The former could permit more experiments in the same time; the latter could change the capability obtained from a fixed amount of computation.</p>
  <p><a href="https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/">AlphaEvolve's</a> work on algorithms and computing infrastructure also shows how improvements produced by AI can feed back into AI execution. An open question follows: can these savings sustain more useful exploration and independent replication, making the next round of discovery more efficient? This is where model efficiency meets recursive self-improvement (RSI).</p>
  <p>A module's speedup alone cannot answer that question. The accounting needs candidate generation, failed attempts, evaluation, replication and deployment, together with evidence that gains survive new tasks or models. If each round spends more to find a better candidate, a comparison with a fixed research method at the same cumulative budget would help establish whether the process of discovery improved.</p>

  <h2 id="insights">Comparing different kinds of progress</h2>
  <div class="research-table-wrap">
    <table>
      <thead><tr><th>Object of study</th><th>What to measure together</th></tr></thead>
      <tbody>
        <tr><td>A model computation</td><td>Compute, memory and latency at matched task quality</td></tr>
        <tr><td>A complete investigation</td><td>The cost of all attempts and checks, alongside task completion</td></tr>
        <tr><td>Successive self-improvement rounds</td><td>Cumulative research cost, held-out gains and the efficiency of subsequent discovery</td></tr>
      </tbody>
    </table>
  </div>
  <p>These levels help distinguish local acceleration, task completion and improved research capability. The last needs particularly careful experiments. A better final score could come from more trials, adaptation to an evaluator, or a method that transfers. Separating those explanations poses a more demanding research question than throughput alone can answer.</p>

  <h2 id="open-questions">Questions worth pursuing further</h2>
  <ul>
    <li>Can multiple agents share reusable computation and experimental results while preserving different lines of exploration?</li>
    <li>As model weights, tools and cache policies change, what records support faithful training, replication and recovery?</li>
    <li>At a fixed cumulative budget, can a system become more effective at discovering improvements from one round to the next? Do those gains transfer across models and tasks?</li>
  </ul>

  <p class="research-readmore">Code and experiments: <a href="https://github.com/sail-sg/scaling-with-vocab">Vocabulary study</a> · <a href="https://huggingface.co/spaces/sail/scaling-with-vocab-demo">Vocabulary calculator</a> · <a href="https://github.com/LegoX/Lego-RL">Lego-RL</a> · <a href="https://www.legox.net/blog/lego-rl-sao/">SAO experiments</a></p>

{% include research/paper-list.liquid group="efficient" lang="en" %}

  <p>Related: <a href="{{ '/research/agentic-intelligence/' | relative_url }}">Agentic intelligence</a></p>
</div>
