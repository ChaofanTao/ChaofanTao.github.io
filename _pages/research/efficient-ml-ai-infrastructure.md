---
layout: default
title: "Efficient ML & AI Infrastructure"
description: "Research notes by Chaofan Tao on vocabulary, compression, caches and training systems, and their implications for the compute, user time and rework needed to complete long projects."
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
  - Human-agent collaboration
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
  <p class="research-dek">For an agent working with a user on a long project, efficiency has to be measured through to delivery: compute spent, user time required, and work repeated when requirements change. These questions connect my earlier work on model efficiency to the agent systems I want to study next.</p>
  <p class="research-meta">By <a href="{{ '/' | relative_url }}">Chaofan Tao (陶超凡)</a> · Last updated <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%B %-d, %Y" }}</time></p>

  <p>My early work focused on quantization and pruning: making generative models smaller while preserving their performance. Work on vocabulary, long contexts and agent training gradually connected these questions. Vocabulary changes how many tokens represent the same text. Cache management determines which earlier information remains available. Scheduling and recovery determine whether already completed computation survives.</p>
  <p>There is no universal answer in which larger, smaller or faster always wins. I find it more useful to specify the capability we want to retain, then identify where compute, memory and time are going. Building a complete project from requirements adds communication, verification and later modifications to that accounting. This essay follows our existing work toward that broader question.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/efficiency-lifecycle.svg' | relative_url }}" alt="Five connected efficiency problems: vocabulary design, model compression, context caching, computation and serving, and knowledge transfer. Each involves a choice about resource allocation." width="960" height="300" loading="eager"></div>
    <figcaption>Efficiency decisions propagate through the workflow. Savings at one stage matter only if they do not create a larger cost later.</figcaption>
  </figure>

  <p class="research-toc">On this page: <a href="#design">Vocabulary</a> · <a href="#compress">Compression</a> · <a href="#remember">Context and caches</a> · <a href="#serve">Training and serving</a> · <a href="#transfer">Distillation</a> · <a href="#long-horizon">Costs of collaboration</a> · <a href="#insights">Measuring efficiency</a> · <a href="#open-questions">Open questions</a></p>

  <h2 id="design">1. Vocabulary allocates compute too</h2>
  <p>Comparing the number of tokens two models process requires care about how they tokenize text. A larger vocabulary usually represents the same text in fewer tokens, but enlarges the embedding and output layers and needs enough data to learn rare entries. Vocabulary size belongs in the same design problem as model size, data and compute.</p>
  <p>In <a href="https://arxiv.org/abs/2407.13623">Scaling Laws with Vocabulary</a>, we separated vocabulary parameters from the rest of the network, measured data in characters and compared training across vocabulary sizes. One concrete result: at the same 2.3 × 10<sup>21</sup> FLOPs budget, increasing the vocabulary from 32K to 43K raised ARC-Challenge performance from 29.1 to 32.0. Changing the allocation of a fixed budget changed the capability obtained from it.</p>
  <p>The paper's estimates depend on its models, data and training setup. They are not a prescription to keep enlarging every current model's vocabulary. Multilingual text, code and tool calls change the distribution; a larger output layer also has an inference cost. The <a href="https://huggingface.co/spaces/sail/scaling-with-vocab-demo">interactive calculator</a> provides a starting point, with validation still needed for a new workload.</p>

  <h2 id="compress">2. Before compressing, understand what could be lost</h2>
  <p>In <a href="https://arxiv.org/abs/2203.10705">Compression of Generative Pre-trained Language Models via Quantization</a>, we investigated why methods effective for encoders degraded when applied to generative models. Two issues mattered: reduced precision made different token embeddings too similar, while weight distributions differed enough across modules to make a uniform quantization setting unsuitable.</p>
  <p>Token-level contrastive distillation preserved distinctions between representations, and module-wise dynamic scaling adapted quantization ranges. This work received an ACL 2022 Outstanding Paper Award. Our subsequent <a href="https://aclanthology.org/2023.findings-acl.692/">structured pruning study</a> examined which network structures could be removed, using learnable masks to inform the choice.</p>
  <p>Vision-language models also benefit from allocating resources unevenly. <a href="https://arxiv.org/abs/2301.13741">UPop</a> jointly searches compression ratios across vision and language, progressively searching and retraining. <a href="https://arxiv.org/abs/2305.17455">CrossGET</a> uses information across image and text to merge similar tokens during inference. Their objects of compression differ, but both ask how to identify redundancy while retaining distinctions the task needs.</p>
  <p>For agents, I would add a further check: could a small approximation error change the next tool call? Single-response scores can screen methods, but complete interaction tasks are needed to measure errors, retries and final success. That is an evaluation requirement suggested by the earlier compression work, rather than an agent result those papers already demonstrate.</p>

  <h2 id="remember">3. A long context does not guarantee the evidence survives</h2>
  <p>The KV cache stores intermediate representations of earlier tokens, avoiding repeated computation during generation. Its memory footprint grows with context. <a href="https://arxiv.org/abs/2406.13035">D2O</a> allocates cache budgets according to attention patterns across layers and compensates for eviction through similarity-based recall or merging. <a href="https://arxiv.org/abs/2410.03090">UNComp</a> uses matrix entropy to analyze information distribution and guide adaptive compression. Compensation reduces information loss; it does not make every discarded detail exactly recoverable.</p>
  <p><a href="https://arxiv.org/abs/2606.10537">Prefilling-dLLM</a> addresses repeated computation in diffusion language models, where denoising repeatedly processes a long prompt. It caches chunks in advance and selects relevant chunks and tokens for decoding. The paper also analyzes how beginning-of-sequence tokens influence attention within chunks. Avoiding repeated prefix processing is related to, but distinct from, evicting an autoregressive model's cache.</p>
  <p>Agents introduce a harder question: information that looks unimportant now may matter dozens of steps later. A short test result that ruled out a hypothesis may be worth retaining after a long search result is no longer useful. Recent work makes this connection explicit. <a href="https://arxiv.org/abs/2609.31395">ActKV</a> prioritizes cache entries for their contribution to subsequent actions. <a href="https://arxiv.org/abs/2610.28577">Cache Engineering for Agents, from October 2026</a>, lets agents control active cache state and shows why identical token sequences can correspond to different internal states after different cache operations.</p>
  <p>This creates a direct connection to training consistency. If execution includes cache eviction or position adjustment, does replaying only the text reconstruct the same policy? Earlier results on token alignment do not settle that question. The runtime state needs to be part of the investigation.</p>

  <h2 id="serve">4. How much of a training run is actually spent updating the model?</h2>
  <p>In <a href="https://www.legox.net/blog/lego-rl/">Lego-RL's timing analysis</a>, an OpenHands SDK trial takes about 920 seconds on average, with 91.3% in agent execution. That stage includes both inference and tool interaction; it should not be read as nine-tenths of the run waiting for tools. The scheduling issue is that trial lengths vary greatly. A synchronous batch waits for its slowest member, whereas asynchronous scheduling can start new work as capacity becomes available.</p>
  <p>Asynchrony brings a trade-off: the policy may have changed by the time a trajectory finishes. Scheduling must control that gap, while pausing and resuming partial generation requires the right state. Lego-RL reports a measured 2.5× step-time speedup; correcting for different GPU compute throughput gives an estimated scheduling gain of about 1.9×. Keeping those comparisons separate helps identify where the improvement comes from.</p>
  <p><a href="https://www.legox.net/blog/lego-rl-sao/">Single-Rollout Asynchronous Optimization (SAO)</a> targets another expense: sampling a group of attempts at the same task to compare rewards. A learned critic supplies the baseline for learning from one attempt. In the reported experiment, SAO used 73.7% fewer trajectories to reach its own best checkpoint than GSPO, with Verified scores of 68.6% versus 70.4%. That is a useful cost-quality trade-off, rather than a saving measured at matched accuracy. Critic inference and training also belong in the cost.</p>
  <p>Serving presents related choices. <a href="https://arxiv.org/abs/2509.15148">ATTS</a> addresses synchronization between draft and target models using online calibration and conformal prediction for asynchronous inference. Its statistical control concerns the rejection process, rather than universal output correctness. <a href="https://arxiv.org/abs/2511.11617">AnchorTP</a> studies recovery after failure: preserve available GPU state through a separate daemon, adjust tensor-parallel partitions and reduce data movement. Its recovery results apply to the failure scenarios studied.</p>
  <p>These findings make me want to consider scheduling, caches and reliability together. Removing waits and preserving completed work are useful only while rewards, state and updates remain trustworthy. Producing unusable training records more quickly does not make learning more efficient.</p>

  <h2 id="transfer">5. Distillation should be assessed through the student</h2>
  <p>A teacher's output has to fit what the student can learn. Our <a href="https://arxiv.org/abs/2404.02657">study of forward and reverse KL divergence</a> found that, in the distillation setting studied, they converge toward the same objective with sufficient training. Their practical difference appears under finite training budgets: forward KL initially emphasizes the high-probability region, reverse KL the tail. Adaptive KL adjusts their relative weights accordingly.</p>
  <p><a href="https://arxiv.org/abs/2510.10925">PerSyn</a> moves selection before synthesis. It assigns a teacher based on the prompt and student learnability, avoiding having every teacher generate an answer before filtering. Alongside <a href="{{ '/research/agentic-intelligence/#experience' | relative_url }}">Terminal-Lego's demonstration study</a>, it suggests a direction worth testing further: measure data's value through the student's improvement, rather than the teacher's ranking or the apparent completeness of its answer.</p>

  <h2 id="long-horizon">6. Long projects also consume the user's time</h2>
  <p>A cheap model request need not produce a cheap workflow. An <a href="https://arxiv.org/abs/2610.09633">October 2026 study of real user task flows</a> documents sessions moving between questions, planning, execution, refactoring and review. In its SWE-TaskFlow pilot, converting tasks to multi-step interaction roughly doubled agent cost without a stable improvement in resolution. This belongs to a particular experiment, but usefully challenges the assumption that more interaction automatically improves collaboration.</p>
  <p>I would measure three costs separately: model and tool computation, time the user waits or actively participates, and rework after requirements change. A single score could hide their differences. Skipping a crucial question might save one exchange and waste the subsequent implementation; asking prematurely might transfer an investigation the agent could do to the user. Comparisons should hold delivery quality and user time budgets fixed, then examine compute and rework.</p>
  <p>Memory and recovery need a broader scope here. A long project needs records of agreed requirements, consequential design choices and their evidence, with test results tied to the code version they checked. Resuming after interruption involves the repository, dependencies and unfinished work as well as generation. AnchorTP studies inference-service recovery; persistent project records are an additional problem.</p>
  <p>I would also treat intermediate verification as a resource-allocation decision. Checking installation, module interfaces and core functionality early could reveal a wrong direction before the entire implementation is complete. Checks have a cost too. Which milestones deserve verification, which decisions need the user, and what the cache should preserve need to be measured together on long projects.</p>

  <h2 id="insights">How I would measure the next efficiency improvement</h2>
  <p>For a fixed workload, add the model, tool, verification and recovery costs of all attempts, then divide by the number of completions that pass independent checks. Failed attempts belong in that total. Report completion latency, active user time and subsequent modification cost separately. This is a synthesis of the work above, rather than a metric those papers already use in common.</p>
  <ol class="research-insights">
    <li><strong>Compare costs at the same delivery requirement.</strong> A faster method that misses a key requirement needs its trade-off reported. Sampling and cache savings should be assessed alongside acceptance, preservation of earlier features and the cost of the next change.</li>
    <li><strong>Check local savings across the complete workflow.</strong> Cache compression may save memory but increase rereading and retries. More review adds immediate cost but may prevent later failures. Measure the balance on the same tasks with the same budgets and grading rules.</li>
    <li><strong>Include runtime state in training-consistency checks.</strong> Text, model weights, cache state and the tool environment jointly affect the next action. New cache interfaces create a need for joint training and serving validation, beyond a speed measurement on either side.</li>
  </ol>

  <h2 id="open-questions">Questions still open</h2>
  <ul>
    <li>How should vocabulary be chosen when multilingual text, code, tool output and inference costs all enter the objective?</li>
    <li>Can memory for long tasks be organized around verified facts, unresolved hypotheses and failed attempts, beyond recent token use?</li>
    <li>With limited compute and user time, how should an agent allocate clarification, implementation and checking to bring more projects to an acceptable delivery?</li>
  </ul>

  <p class="research-readmore">Reproduction and further reading: <a href="https://github.com/sail-sg/scaling-with-vocab">Vocabulary study code</a> · <a href="https://huggingface.co/spaces/sail/scaling-with-vocab-demo">Vocabulary calculator</a> · <a href="https://github.com/LegoX/Lego-RL">Lego-RL code</a> · <a href="https://www.legox.net/blog/lego-rl-sao/">SAO experiments and trade-offs</a></p>

{% include research/paper-list.liquid group="efficient" lang="en" %}

  <p>Related: <a href="{{ '/research/agentic-intelligence/' | relative_url }}">Agentic coding, reasoning and evaluation</a></p>
</div>
