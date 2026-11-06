---
layout: default
title: "Agentic Coding, Reasoning and Evaluation"
description: "Research notes by Chaofan Tao on coding agents, reasoning and evaluation, and the next challenge: working with users over long tasks to build and maintain complete projects."
permalink: /research/agentic-intelligence/
research_lang: en
last_modified_at: 2026-11-06
og_image: /assets/img/og-image.png
figure: /assets/img/research/agentic-loop.svg
about:
  - Agentic intelligence
  - Coding agents
  - Agentic reinforcement learning
  - Agentic data
  - Multimodal reasoning
  - Agent evaluation
  - Reward hacking
  - Long-horizon agents
  - Human-agent collaboration
  - Repository generation
---

{% include research/styles.liquid %}
{% include research/jsonld.liquid group="agentic" %}

<div class="research-page">
  <nav class="research-breadcrumb" aria-label="Breadcrumb">
    <a href="{{ '/' | relative_url }}">Chaofan Tao</a><span aria-hidden="true">/</span>
    <a href="{{ '/research/' | relative_url }}">Research</a><span aria-hidden="true">/</span>
    <span>Agentic coding, reasoning and evaluation</span>
    <span aria-hidden="true">·</span><a href="{{ '/zh/research/agentic-intelligence/' | relative_url }}" lang="zh-Hans">中文版</a>
  </nav>

  <h1>Agentic Coding, Reasoning and Evaluation</h1>
  <p class="research-dek">After fixing one issue, can an agent keep working with the user until the project is complete? I see our work on agent training, data and evaluation as a starting point for that harder problem: understanding requirements, keeping track of evidence, and making progress as the task changes.</p>
  <p class="research-meta">By <a href="{{ '/' | relative_url }}">Chaofan Tao (陶超凡)</a> · Last updated <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%B %-d, %Y" }}</time></p>

  <p>Fixing a well-specified issue and building a project from a few sentences of requirements ask different things of an agent. The second involves deciding what to build first, how the pieces should fit, and which questions need the user's input. Requirements may change halfway through. Getting the latest code to run is one step; keeping earlier work useful is another.</p>
  <p>I organize our related work around four questions: what <strong>environment</strong> the agent works in, what <strong>experience</strong> it collects, what <strong>training signal</strong> it receives, and how we <strong>evaluate</strong> the result. <a href="https://www.legox.net/blog/legoflow/">LegoFlow</a>, <a href="https://www.legox.net/blog/swe-lego/">SWE-Lego</a>, <a href="https://www.legox.net/blog/lego-rl/">Lego-RL</a> and <a href="https://www.legox.net/blog/swe-review/">SWE-Review</a> approach different parts of this process. Below, I explain what the experiments establish, then consider what is still missing for longer projects and sustained collaboration.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/agentic-loop.svg' | relative_url }}" alt="The agent learning process: a model and its harness sit between four connected stages, environment, experience, training signal and evaluation." width="760" height="480" loading="eager"></div>
    <figcaption>The environment shapes the experience available to the agent. Training determines what it learns from that experience, and evaluation checks whether the change is useful.</figcaption>
  </figure>

  <p class="research-toc">On this page: <a href="#environment">Environment</a> · <a href="#experience">Experience</a> · <a href="#signal">Training</a> · <a href="#evaluation">Evaluation and review</a> · <a href="#physical">Vision and robotics</a> · <a href="#long-horizon">Long tasks and collaboration</a> · <a href="#insights">What to test next</a> · <a href="#open-questions">Open questions</a></p>

  <h2 id="environment">1. Changing the harness changes the problem</h2>
  <p>A harness connects the model to tools and an environment. It decides how files are read, how tool results are presented, when history is compacted, and what happens after a failed command. Each choice changes the evidence available for the model's next action.</p>
  <p><a href="https://www.legox.net/blog/lego-rl/">Lego-RL's experiments</a> give a concrete example. The same starting Qwen3.5-35B-A3B checkpoint scores 64.0%, 62.4% and 57.2% on SWE-bench Verified through OpenHands SDK, Claude Code and OpenCode. The surrounding execution loop matters to performance. That motivated training inside the existing harness, although the comparison alone does not establish that native training beats training in a rewritten harness.</p>
  <p>Maintaining a separate model for each harness is cumbersome. We therefore tried <a href="https://www.legox.net/blog/lego-rl-cross-harness/">mixed-harness training</a>: one model learning through all three. Its average performance on the evaluated benchmarks approaches that of three separately trained and deployed models. All three harnesses participated in training, however. To distinguish a transferable way of working from adaptation to familiar interfaces, we need to hold out a harness and separately test changes in tools, context management and repositories.</p>

  <h2 id="experience">2. Solving a task and leaving a useful example are different achievements</h2>
  <p>First, a training task has to work. <a href="https://www.legox.net/blog/legoflow/">LegoFlow</a> builds tasks from merged pull requests, reconstructs an execution environment, and checks that the original code fails relevant tests while the reference patch passes. <a href="https://www.legox.net/blog/swe-lego/">SWE-Lego</a> combines real issues with tasks created by injecting bugs, balancing complexity and scale. These checks remove unusable tasks; they still leave the question of whether the tests capture the full requirement.</p>
  <p>Next comes the trajectory: what the teacher inspected, what it did, and how it checked the result. In <a href="https://arxiv.org/abs/2606.03461">Terminal-Lego</a>, the teachers' own task performance did not predict how well students learned from them. Across the teacher and student combinations studied, traces that exposed an inspect-act-verify routine transferred better. A student needs access to the evidence behind an action. A sequence of correct commands can be a poor explanation of how to solve the next problem.</p>
  <p><a href="https://www.legox.net/blog/legoflow-experiments/">LegoFlow's data experiments</a> also caution against treating reasoning length as quality. Removing the group with the shallowest reasoning improved student performance, while selecting progressively longer traces brought diminishing returns. This supports filtering examples that omit necessary analysis. It does not establish that extending an explanation will improve it. I would look for whether a trace explains consequential decisions and responds to new evidence.</p>
  <p>Some successful traces need to be excluded for a simpler reason: the teacher found the reference patch in Git history or online. Such a trace can pass the tests without demonstrating the investigation we want to teach. Prompt instructions help, but the environment matters too: remove histories that reveal the answer, restrict external access during execution, and check the submitted changes independently. Trust in the data depends on those concrete conditions.</p>
  <p class="research-readmore">Experiments and resources: <a href="https://www.legox.net/blog/legoflow-experiments/">Lessons learned from LegoFlow-SWE</a> · <a href="https://huggingface.co/datasets/Lego-X/LegoFlow-SWE">Tasks and trajectories</a> · <a href="https://www.legox.net/blog/terminal-lego/">Terminal-Lego</a></p>

  <h2 id="signal">3. Decide what to teach, and record what actually happened</h2>
  <p>Supervised fine-tuning (SFT) learns from demonstrations, but every step in a demonstration need not be an imitation target. <a href="https://arxiv.org/abs/2601.01426">SWE-Lego's</a> error masking keeps failed steps in context while excluding them from the imitation loss. The student can still see what failed and how the attempt recovered. A failure can be useful context without being an action we want the model to repeat.</p>
  <p>Reinforcement learning (RL) uses task outcomes to update behavior. One complication is that a harness can compact or rewrite history, so a saved transcript may not reconstruct the input used at generation time. <a href="https://arxiv.org/abs/2608.17393">Lego-RL</a> captures tokens, probabilities and mixture-of-experts routing as generation happens, then checks their correspondence on the training side. History rewrites still limit reconstruction, and high probability correlation does not imply numerical agreement everywhere. A healthy training curve cannot substitute for these checks.</p>
  <p>Many useful tasks lack a single executable correctness check. <a href="https://arxiv.org/abs/2601.18533">RLVRR</a> derives finer content and style rewards from reference answers. <a href="https://arxiv.org/abs/2601.21968">OVD</a> uses text feedback from a black-box teacher to rank the student's own partial trajectories, retain better portions and replace weaker continuations. These methods widen the sources of supervision. They also make it worth checking whether improvement reflects the underlying task or closer agreement with the reference and evaluator's preferences.</p>
  <p>Multimodal reasoning offers another reason to be specific about training objectives. Our <a href="https://arxiv.org/abs/2507.07562">study of long-CoT SFT and RL</a> found that SFT helped difficult questions but encouraged verbosity, while RL gave more balanced gains and shorter answers. The combinations tested retained trade-offs. <a href="https://arxiv.org/abs/2506.01713">SRPO</a> instead targets self-reflection, rewarding concise, useful corrections. These findings favor feedback aimed at a particular behavior; adding another training stage does not automatically add its benefits.</p>

  <h2 id="evaluation">4. Check the result, and how it earned its score</h2>
  <p>A passing test is valuable evidence. Its meaning depends on the coverage of the tests, the clarity of the requirements and the integrity of grading. <a href="https://arxiv.org/abs/2604.06861">REAgent</a> begins with requirements, organizing and refining the issue description before patch generation. <a href="https://arxiv.org/abs/2505.23932">SwingArena</a> places patch submission and reviewer-written tests in continuous integration, studying issue resolution across long contexts and multiple languages.</p>
  <p><a href="https://arxiv.org/abs/2607.06065">SWE-Review</a> asks what happens after submission. A reviewer explores the repository, diagnoses the issue and gives feedback on the candidate patch so the generator can revise it. We evaluate both the decision and whether the feedback helps resolve the issue. Independent investigation can still leave shared blind spots: generator and reviewer may miss the same edge case. Review and independent tests should therefore complement each other.</p>
  <p>Recent benchmark maintenance makes this concern tangible. The <a href="https://arxiv.org/abs/2610.24206">October 2026 SWE-Bench Pro V2 paper</a> documents repaired tasks and a hardened protocol: restrict network access, then reapply and grade the patch in a clean container. This echoes the answer leakage encountered in LegoFlow. More capable agents expose task defects and grading loopholes that earlier systems did not reach, so evaluation needs maintenance as capabilities change.</p>
  <p>Scores also depend on resources. In <a href="https://www.anthropic.com/research/infrastructure-noise">Anthropic's February 2026 experiments</a>, changing infrastructure allocations on Terminal-Bench 2.0 produced a six-percentage-point spread. That number belongs to the reported setup, but the implication for comparisons is broader: document CPU, memory, timeouts, network rules and retries. Otherwise, a small score difference is difficult to attribute to the model.</p>

  <h2 id="physical">5. Images, the web and physical actions</h2>
  <p>Multimodal tasks make the evidence question particularly clear: did the agent perceive the clue it needed? <a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a> requires fine visual cues to be carried through iterative image-text search and cross-checking, with tools for marking, cropping and targeted retrieval. <a href="https://arxiv.org/abs/2505.15929">PhyX</a> tests the combination of visual information, physics knowledge and real constraints. <a href="https://arxiv.org/abs/2408.09511">NAVERO</a> uses descriptions with altered actions or relations to test fine distinctions in video understanding. Together they motivate separating perception, retrieval and reasoning failures when diagnosing an incorrect answer.</p>
  <p><a href="https://arxiv.org/abs/2402.16117">RoboCodeX</a> decomposes high-level instructions into object-specific operations and generates control code. This makes the connection between plans, constraints and execution more explicit. Software habits cannot simply be carried over: physical actions may be irreversible, and when the system checks matters. Our <a href="https://arxiv.org/abs/2411.05902">survey of autoregressive models in vision</a> maps the representation and generation methods; connecting these capabilities to reliable sustained action remains a further research problem.</p>

  <h2 id="long-horizon">6. The next step: building a project with its user</h2>
  <p>Extending a single repair run is only part of the challenge. <a href="https://arxiv.org/abs/2512.12730">NL2Repo-Bench</a> starts with a requirements document and an empty workspace, asking agents to design the architecture, manage dependencies and implement an installable project. <a href="https://arxiv.org/abs/2605.15846">RoadmapBench</a> studies multi-goal version upgrades in existing repositories. These settings expose premature stopping, inconsistent changes across files and plans that fail over time.</p>
  <p><a href="https://arxiv.org/abs/2509.16198">RPG / ZeroRepo</a> explores structured planning that connects features, files, data flows and functions. It suggests a direction I would like to test: persistent project state that records accepted requirements, reasons for design decisions, verified functionality and unresolved assumptions. More conversation history alone does not ensure those distinctions survive. The records also need revision when a requirement or implementation changes; a stale plan can be as misleading as a forgotten one.</p>
  <p>With the user involved, finishing autonomously is only one possible objective. <a href="https://arxiv.org/abs/2610.29822">UserSWE, released in October 2026</a>, adds dynamic simulated users and execution checks at each turn, finding that agent rankings change with the interaction budget. Simulation cannot replace experiments with real users, but the result challenges the use of single-turn scores to describe collaboration. The timing of a question seems especially worth studying. Resolving an architectural ambiguity early could avoid substantial rework; asking something the agent could establish by reading the code may simply interrupt the user.</p>
  <p>Long projects also inherit earlier design choices. <a href="https://arxiv.org/abs/2603.24755">SlopCodeBench</a> has agents repeatedly extend their own code and tracks redundancy and concentrated complexity. It observes that passing checks can coexist with deteriorating structure. Delivery should leave a project that can accommodate the next change. That gives review a longer horizon too: did this patch break an earlier feature, lose an agreed requirement, or make the next feature harder to implement?</p>

  <h2 id="insights">What I would test next</h2>
  <p>These are research directions suggested by the work above, rather than conclusions it has already established.</p>
  <ol class="research-insights">
    <li><strong>Test project memory under changing requirements.</strong> Compare full conversation history, summaries, and explicit requirement and verification records on tasks with several requirement changes. Measure regressions, forgotten commitments and recovery after interruption alongside final success.</li>
    <li><strong>Measure the value of a question together with its burden.</strong> With a fixed budget of user time, compare clarification, direct attempts and intermediate demonstrations. Question count alone is a poor measure of collaboration. The useful outcomes are fewer misunderstandings, less rework and less repeated explanation.</li>
    <li><strong>Use the next change to assess the current delivery.</strong> After independent acceptance, add a related requirement and measure modification cost, regressions and structural changes. This tests whether the agent left a project that can keep developing, and connects directly to <a href="{{ '/research/efficient-ml-ai-infrastructure/#long-horizon' | relative_url }}">the cost of sustained work</a>.</li>
  </ol>

  <h2 id="open-questions">Questions still open</h2>
  <ul>
    <li>After implementation, testing and user discussion all contribute to an outcome, how can training identify the actions that made a difference?</li>
    <li>When requirements change, how should an agent decide which earlier decisions to revisit and which work to preserve?</li>
    <li>How can independent tests, code review and user acceptance complement each other without reducing project quality to a test pass rate?</li>
  </ul>

  <h2 id="resources">Code, data and models</h2>
  <p>The papers describe the methods and experiments; the releases make it possible to examine them further. My publication record is also available on <a href="https://scholar.google.com/citations?user=gjmfLroAAAAJ">Google Scholar</a>.</p>
  <ul>
    <li>LegoFlow: <a href="https://github.com/LegoX/LegoFlow">code</a> · <a href="https://huggingface.co/collections/Lego-X/legoflow">data</a></li>
    <li>SWE-Lego: <a href="https://github.com/LegoX/SWE-Lego">code</a> · <a href="https://huggingface.co/collections/Lego-X/swe-lego">data and models</a></li>
    <li>Terminal-Lego: <a href="https://github.com/LegoX/Terminal-Lego">code</a> · <a href="https://huggingface.co/datasets/Lego-X/Terminal-Lego-15k">data</a></li>
    <li>Lego-RL: <a href="https://github.com/LegoX/Lego-RL">code</a> · <a href="https://huggingface.co/collections/Lego-X/lego-rl">models and data</a></li>
    <li>SWE-Review: <a href="https://github.com/LegoX/SWE-Review">code</a> · <a href="https://huggingface.co/collections/Lego-X/swe-review">models and data</a></li>
  </ul>

{% include research/paper-list.liquid group="agentic" lang="en" %}

  <p>Related: <a href="{{ '/research/efficient-ml-ai-infrastructure/' | relative_url }}">Efficient ML and AI infrastructure</a></p>
</div>
