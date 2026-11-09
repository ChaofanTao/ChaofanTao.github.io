---
layout: default
title: "Agentic Intelligence"
description: "Chaofan Tao's research on agentic intelligence: coding agents built in the open at LegoX (verified data, SFT and RL inside real harnesses, agentic review), multimodal reasoning, and his thoughts on very long-horizon agents, multi-agent collaboration, trustworthy evaluation, AI for AI and AI for Science."
permalink: /research/agentic-intelligence/
research_lang: en
last_modified_at: 2026-11-09
og_image: /assets/img/og-image.png
figure: /assets/img/research/agentic-loop.svg
about:
  - Agentic intelligence
  - Coding agents
  - Agentic reinforcement learning
  - Agentic data
  - Multimodal reasoning
  - Agent evaluation
  - Long-horizon agents
  - Multi-agent systems
  - AI for AI
  - AI for Science
---

{% include research/styles.liquid %}
{% include research/jsonld.liquid group="agentic" %}

<div class="research-page">
  <nav class="research-breadcrumb" aria-label="Breadcrumb">
    <a href="{{ '/' | relative_url }}">Chaofan Tao</a><span aria-hidden="true">/</span>
    <a href="{{ '/research/' | relative_url }}">Research</a><span aria-hidden="true">/</span>
    <span>Agentic intelligence</span>
    <span aria-hidden="true">·</span><a href="{{ '/zh/research/agentic-intelligence/' | relative_url }}" lang="zh-Hans">中文版</a>
  </nav>

  <h1>Agentic Intelligence</h1>
  <p class="research-dek">An agent's ability doesn't live in the model alone. It lives in the loop around it: seeing the situation, acting, learning from what happened, and being checked. At LegoX we have been building that loop in the open for coding agents, and our multimodal work tests what it needs beyond code. This page walks through what we found, and shares some thoughts on where the loop goes next.</p>
  <p class="research-meta">By <a href="{{ '/' | relative_url }}">Chaofan Tao (陶超凡)</a> · Last updated <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%B %-d, %Y" }}</time></p>

  <p>For a long time, progress in AI meant a better answer to a fixed question. Agents change the question. An agent has to notice the detail that matters, decide what to try, act, read what came back and adjust. Each of those steps can fail on its own, and each needs its own kind of evidence: whether the model saw the right thing, whether its actions were grounded in what the environment showed it, whether it learned the right lesson from an attempt, and whether we can trust the check that says it improved.</p>
  <p>Coding agents are where we study all of these at once. Code leaves a record of every action and every result, and tests give an outcome you can verify. At <a href="https://www.legox.net/">LegoX</a>, we build each part of this loop as open, reusable pieces: how verified experience is collected, how it becomes training signal, and how the result is checked. Our multimodal work asks the same questions where the environment is an image, a video, the web or a robot.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/agentic-loop.svg' | relative_url }}" alt="Diagram of the agent learning loop: the agent, a model plus its harness, sits at the center of four stages connected clockwise: environment, experience, signal and evaluation, each labeled with the projects that study it. All projects are work by Chaofan Tao and collaborators." width="760" height="505" loading="eager"></div>
    <figcaption>The agent learning loop. An attempt leaves experience, training turns it into capability, and evaluation checks whether that capability carries over to new tasks.</figcaption>
    <div class="research-works">
      <p class="research-works-note">All work in this figure is by Chaofan Tao and collaborators:</p>
      <p><strong>Environment</strong>: <a href="https://arxiv.org/abs/2608.17393">Lego-RL</a> <span class="research-venue">(arXiv 2026)</span> · <a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a> <span class="research-venue">(ICLR 2026)</span> · <a href="https://arxiv.org/abs/2402.16117">RoboCodeX</a> <span class="research-venue">(ICML 2024)</span></p>
      <p><strong>Experience</strong>: <a href="https://www.legox.net/blog/legoflow/">LegoFlow</a> <span class="research-venue">(LegoX blog, 2026)</span> · <a href="https://arxiv.org/abs/2601.01426">SWE-Lego</a> <span class="research-venue">(arXiv 2026)</span> · <a href="https://arxiv.org/abs/2606.03461">Terminal-Lego</a> <span class="research-venue">(arXiv 2026)</span></p>
      <p><strong>Signal</strong>: SWE-Lego · Lego-RL · <a href="https://arxiv.org/abs/2601.18533">RLVRR</a> <span class="research-venue">(ICLR 2026)</span> · <a href="https://arxiv.org/abs/2601.21968">OVD</a> <span class="research-venue">(arXiv 2026)</span> · <a href="https://arxiv.org/abs/2506.01713">SRPO</a> <span class="research-venue">(NeurIPS 2025)</span></p>
      <p><strong>Evaluation</strong>: <a href="https://arxiv.org/abs/2505.23932">SwingArena</a> <span class="research-venue">(ICLR 2026 Oral)</span> · <a href="https://arxiv.org/abs/2607.06065">SWE-Review</a> <span class="research-venue">(arXiv 2026)</span> · <a href="https://arxiv.org/abs/2505.15929">PhyX</a> <span class="research-venue">(TMLR 2026)</span></p>
    </div>
  </figure>

  <p class="research-toc">On this page: <a href="#coding">Coding agents as a laboratory</a> · <a href="#multimodal">Beyond code</a> · <a href="#at-a-glance">At a glance</a> · <a href="#lessons">What we learned</a> · <a href="#outlook">Some thoughts on the future</a> · <a href="#open-questions">Open questions</a></p>

  <h2 id="coding">1. Coding agents as a laboratory</h2>
  <p>A coding agent never sees a repository directly. It sees whatever its harness shows it: which files and tool outputs reach the context, when history is compacted, how errors are reported, what happens after a command fails. When we trained the same starting model inside three widely used harnesses (OpenHands, Claude Code and OpenCode) with <a href="https://arxiv.org/abs/2608.17393">Lego-RL</a>, it already behaved differently in each before any training. The harness is part of the environment, not plumbing around the model. That observation shaped how we collect data, how we train, and how we check results.</p>

  <h3 id="data">Data: experience worth learning from</h3>
  <p><strong>LegoFlow turns merged pull requests into verified tasks.</strong> <a href="https://www.legox.net/blog/legoflow/">LegoFlow</a> treats code-data engineering as a chain of blocks. Curator finds merged pull requests, gathers the issue, commits and tests, rewrites them into a task that does not leak the answer, builds an isolated environment and keeps the task only if the original code fails the tests and the reference fix passes. Because passing that check only makes a task usable, Curator also scores difficulty with a static rubric over the size of the patch, the logic it adds, how much of the codebase it touches, the tests and the detail of the instructions, with no LLM judge involved.</p>
  <p><strong>The whole pipeline can be run by an agent.</strong> Tracer rolls out trajectories in sandboxes and screens them, and Trainer and Evaluator close the loop. Every block is packaged as a plugin skill, so a coding agent such as Claude Code or Codex can run the pipeline itself, and each block has its own dashboard. In one experiment, an agent ran the whole pipeline end to end, read the evaluation, noticed that many teacher traces contained only shallow reasoning, changed the filter and trained a clearly better model in the next round.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/legox/legoflow-architecture.png' | relative_url }}" alt="LegoFlow architecture: a Root block orchestrates Curator, Tracer, Trainer and Evaluator blocks, each exposed as plugin skills with its own dashboard, producing tasks, trajectories, models and scores." width="1600" height="766" loading="lazy"></div>
    <figcaption>LegoFlow's blocks, from task curation to evaluation, each operable by a coding agent. Figure from the <a href="https://www.legox.net/blog/legoflow/">LegoFlow blog</a>.</figcaption>
  </figure>

  <p><a href="https://arxiv.org/abs/2601.01426">SWE-Lego</a> combines real tasks from resolved pull requests with synthetic ones created by injecting bugs, through LLM rewriting and syntax-tree transformations. Real tasks bring depth and realism; synthetic tasks bring scale, and for the same repositories, adding them keeps helping. <a href="https://arxiv.org/abs/2606.03461">Terminal-Lego</a> brings the same discipline to command-line work, turning Stack Overflow problems into Docker-verified tasks.</p>
  <p><strong>The lessons that mattered most were about which trajectories to keep.</strong> Terminal-Lego found that the strongest solver is not necessarily the best teacher: traces that visibly inspect, act on what they found and then verify the result teach students better than traces from stronger agents that jump straight to the answer. LegoFlow found that reasoning depth matters more than coverage. Teachers that think a little on every turn teach less than teachers that think hard when the problem calls for it, and most of the benefit comes from removing the shallowest traces rather than keeping only the longest. SWE-Lego added practical cleaning rules: repair malformed tool calls, keep the tool set small, and recycle attempts that found the right file but failed to fix it.</p>
  <p><strong>Experience also has an honesty problem.</strong> Stronger teachers are better at finding shortcuts: locating the upstream pull request, copying the patch, or reading the fix from Git history. A successful trajectory is not necessarily an honest one. What worked was two layers: tell the agent plainly not to look up solutions, and make it impossible anyway, by rewriting Git history, hiding test files and restricting the network while the agent works, then restoring them only for grading.</p>

  <h3 id="learning">Learning: turning experience into capability</h3>
  <p><strong>Plain supervised fine-tuning goes a long way when the loss gets as much care as the data.</strong> In SWE-Lego, error masking keeps the whole trajectory, mistakes included, in context but takes no gradient on the wrong steps, so the model learns from its errors without learning to repeat them. A curriculum uses trajectory length as a stand-in for difficulty and trains from easy to hard, carrying earlier data forward. At inference time, extra compute is best spent first on more interaction turns and, once that saturates, on parallel attempts, with a verifier that answers "yes" or "no" in text choosing among them better than a scoring head does.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/legox/swe-lego-error-masking.png' | relative_url }}" alt="SWE-Lego error masking: an agent trajectory where the step that led to an execution error is excluded from the loss while correct steps receive gradient updates." width="1600" height="878" loading="lazy"></div>
    <figcaption>Step-level error masking in SWE-Lego: the model still sees the failed step and its error, but is not trained to imitate it. Figure from the <a href="https://www.legox.net/blog/swe-lego/">SWE-Lego blog</a>.</figcaption>
  </figure>

  <p><strong>For reinforcement learning, the trainer must see what the agent actually did.</strong> Lego-RL trains inside the real, unmodified harness. Harnesses rewrite their own history by compacting context, re-serializing tool calls and running sub-agents, so a saved transcript is not the token sequence that was sampled. An in-process proxy records tokens, probabilities and mixture-of-experts routing at generation time, and the routing is replayed during training. Mismatches here make no noise: training runs and curves move, which is exactly why they have to be checked explicitly.</p>
  <p><strong>The runs themselves taught two more lessons.</strong> Tasks the model always or never solves teach it nothing, so the useful difficulty band has to follow the policy as it improves. And a falling reward can mean a broken parser or failed environment setups rather than a worse policy, so dashboards that break down how every attempt ended are part of the method, not an extra. After training, the agents read more code before editing, reread their own edits and run tests more often, at the cost of longer sessions.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/legox/lego-rl-infrastructure.png' | relative_url }}" alt="Lego-RL infrastructure: unmodified harnesses run in sandboxes, an in-process proxy captures tokens and routing, a rollout engine and trainer exchange trajectories and weights with synchronous, asynchronous and partial-rollout modes." width="1600" height="992" loading="lazy"></div>
    <figcaption>Lego-RL connects unmodified harnesses to a trainer through an in-process proxy. Figure from the <a href="https://www.legox.net/blog/lego-rl/">Lego-RL blog</a>.</figcaption>
  </figure>

  <p>Two follow-ups extend the recipe. <a href="https://www.legox.net/blog/lego-rl-cross-harness/">Training one model on a mix of harnesses</a> came close to the average of separately trained models while narrowing some of the gaps between harnesses. <a href="https://www.legox.net/blog/lego-rl-sao/">Single-rollout optimization</a> learns from one attempt per task with a learned critic instead of comparing many attempts, which saves most of the sampling but only works once the critic has been warmed up and the advantages normalized; without that, the policy collapsed into repeating its "think" tool. For tasks without a single checkable answer, <a href="https://arxiv.org/abs/2601.18533">RLVRR</a> builds a chain of rewards from good reference answers, covering content and style, and <a href="https://arxiv.org/abs/2601.21968">OVD</a> learns from a teacher's text feedback on the student's own partial attempts, keeping good beginnings and replacing weak continuations.</p>

  <h3 id="checking">Checking: review and evaluation</h3>
  <p><a href="https://arxiv.org/abs/2607.06065">SWE-Review</a> trains a reviewer agent that explores the repository on its own, works out the root cause, compares it with a submitted patch and writes structured feedback, turning one-shot generation into generate, review and revise. Two results matter beyond the paper: review data also makes models better at fixing issues, and because choosing among a few attempts is cheaper than producing many more, a good reviewer makes test-time compute go further. <a href="https://arxiv.org/abs/2505.23932">SwingArena</a> puts models into a continuous-integration loop as both patch submitters and test-writing reviewers across several languages, and <a href="https://arxiv.org/abs/2604.06861">REAgent</a> checks and improves the issue description itself before any patch is written.</p>
  <p class="research-readmore">Read more: <a href="https://www.legox.net/blog/legoflow-experiments/">Lessons learned from LegoFlow-SWE</a> · <a href="https://www.legox.net/blog/lego-rl/">Lego-RL blog</a> · <a href="https://www.legox.net/blog/swe-review/">SWE-Review blog</a></p>

  <h2 id="multimodal">2. Beyond code: multimodal reasoning and the physical world</h2>
  <p><strong>Code is a forgiving environment: everything is text and every result can be checked.</strong> Our multimodal work asks what the loop needs when the agent has to look. In <a href="https://arxiv.org/abs/2408.09511">NAVERO</a>, we found that video-language models often can't tell who did what to whom, matching a video to a caption even when the action or relation is wrong; training on such near-miss descriptions taught the model to separate similar actions. <a href="https://arxiv.org/abs/2505.15929">PhyX</a> shows models answering physics questions about images from memorized formulas and surface patterns rather than understanding the situation. <a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a> builds search tasks whose answers depend on small visual clues carried through several rounds of retrieval; tools to mark, crop and zoom change what the agent can find, and most failures come from not locating the right evidence rather than from the last reasoning step.</p>
  <p>On training, the <a href="https://arxiv.org/abs/2507.07562">synergy dilemma</a> study found that long chain-of-thought SFT and RL help reasoning VLMs in different places, and that combining them tends to trade one benefit for the other. <a href="https://arxiv.org/abs/2506.01713">SRPO</a> first shows the model what a useful reflection looks like, then rewards reflections that actually change its reasoning. <a href="https://arxiv.org/abs/2402.16117">RoboCodeX</a> turns instructions into object-level actions with grasping and safety constraints written as code, so code plays for a robot the role a harness plays for a software agent. Our <a href="https://arxiv.org/abs/2411.05902">survey of autoregressive models in vision</a> maps how visual generation and understanding are converging, and its paper list has become a widely used reference.</p>
  <p><strong>Across these projects, the failure usually starts before the reasoning</strong>, at seeing the right detail or finding the right evidence. That is the part of the loop that agents, unlike fixed models, can go back and fix.</p>

  <h2 id="at-a-glance">At a glance</h2>
  <p class="research-works-note">All work in this table is by Chaofan Tao and collaborators.</p>
  <div class="research-table-wrap">
    <table>
      <thead><tr><th>Stage</th><th>Work</th><th>What we showed</th></tr></thead>
      <tbody>
        <tr><td rowspan="2">Environment</td><td><a href="https://arxiv.org/abs/2608.17393">Lego-RL</a> <span class="research-venue">(arXiv 2026)</span></td><td>The harness is part of the environment; train inside the real, unmodified harness</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a> <span class="research-venue">(ICLR 2026)</span> · <a href="https://arxiv.org/abs/2402.16117">RoboCodeX</a> <span class="research-venue">(ICML 2024)</span></td><td>Tools decide what evidence an agent can use; code is the interface to robots</td></tr>
        <tr><td rowspan="3">Experience</td><td><a href="https://www.legox.net/blog/legoflow/">LegoFlow</a> <span class="research-venue">(LegoX blog, 2026)</span></td><td>Real pull requests become tasks only when tests prove them; the pipeline is operable by agents</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2601.01426">SWE-Lego</a> <span class="research-venue">(arXiv 2026)</span></td><td>Real tasks for depth, synthetic tasks for scale; shortcuts removed from the environment</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2606.03461">Terminal-Lego</a> <span class="research-venue">(arXiv 2026)</span></td><td>Grounded traces teach better than stronger solvers</td></tr>
        <tr><td rowspan="4">Signal</td><td><a href="https://arxiv.org/abs/2601.01426">SWE-Lego</a> <span class="research-venue">(arXiv 2026)</span></td><td>Error masking, curriculum and a text verifier make SFT-only coding agents strong</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2608.17393">Lego-RL</a> <span class="research-venue">(arXiv 2026)</span></td><td>Faithful RL inside real harnesses; difficulty follows the policy</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2601.18533">RLVRR</a> <span class="research-venue">(ICLR 2026)</span> · <a href="https://arxiv.org/abs/2601.21968">OVD</a> <span class="research-venue">(arXiv 2026)</span></td><td>Rewards from references; learning from text feedback on partial attempts</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2506.01713">SRPO</a> <span class="research-venue">(NeurIPS 2025)</span> · <a href="https://arxiv.org/abs/2507.07562">Synergy dilemma</a> <span class="research-venue">(TMLR 2025)</span></td><td>Useful reflection over long reflection; SFT and RL help in different places</td></tr>
        <tr><td rowspan="3">Evaluation</td><td><a href="https://arxiv.org/abs/2607.06065">SWE-Review</a> <span class="research-venue">(arXiv 2026)</span></td><td>Independent review; review data improves fixing; choosing is cheaper than generating</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2505.23932">SwingArena</a> <span class="research-venue">(ICLR 2026 Oral)</span> · <a href="https://arxiv.org/abs/2604.06861">REAgent</a> <span class="research-venue">(ICSE 2027)</span></td><td>Evaluation inside CI; requirements checked before patching</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2505.15929">PhyX</a> <span class="research-venue">(TMLR 2026)</span> · <a href="https://arxiv.org/abs/2408.09511">NAVERO</a> <span class="research-venue">(arXiv 2024)</span></td><td>Physical reasoning and fine-grained video relations expose perception failures</td></tr>
      </tbody>
    </table>
  </div>

  <h2 id="lessons">What we learned</h2>
  <ol class="research-insights">
    <li><strong>The strongest model is rarely the best teacher.</strong> What transfers is behavior the student can see and imitate: looking, acting on what was found, checking. The same mismatch between teacher strength and student learnability shows up in our <a href="{{ '/research/efficient-ml-ai-infrastructure/#transfer' | relative_url }}">distillation work</a>.</li>
    <li><strong>Reliable judgment is the scarce resource.</strong> Verified tasks, verifiers, reviewers and CI-based arenas are all ways of producing judgments we can trust. Generating attempts is cheap; choosing between them reliably is what scales.</li>
    <li><strong>The trainer must see what the agent actually did.</strong> In agent RL, systems details such as token alignment and routing replay decide whether learning optimizes the right thing.</li>
    <li><strong>Stronger agents find more shortcuts.</strong> Git history, upstream patches, visual questions answerable from text alone: honesty has to be built into the environment and the benchmark.</li>
    <li><strong>Depth beats coverage.</strong> Careful reasoning where it is needed, useful reflection over long reflection, and evidence over verbosity.</li>
  </ol>

  <h2 id="outlook">Some thoughts on the future</h2>
  <p>These are personal views. Each starts from a problem we have already met in small form in the work above.</p>

  <h3 id="long-horizon">Very long-horizon agents: from hours of work to weeks</h3>
  <p>Agents are moving from tasks of hours to tasks of weeks: building a feature, migrating a codebase, running a research project. At that length, four problems we have seen in small form become central:</p>
  <ul>
    <li><strong>The goal drifts.</strong> <a href="https://arxiv.org/abs/2604.06861">REAgent</a> showed that a vague issue misleads agents even on short tasks; a week-long task has to revisit its requirements as it goes.</li>
    <li><strong>One verdict at the end is too little feedback.</strong> Progress needs checking at milestones, the way <a href="https://arxiv.org/abs/2607.06065">SWE-Review</a> checks a patch before it is accepted.</li>
    <li><strong>Credit is hard to assign.</strong> In single-rollout optimization, the critic's estimate tended to jump when new tool feedback arrived, a hint that credit can be anchored to meaningful checkpoints.</li>
    <li><strong>Environments will break.</strong> State has to survive failures, the lesson behind Lego-RL's failure dashboards and our <a href="{{ '/research/efficient-ml-ai-infrastructure/#serve' | relative_url }}">fault-tolerant serving work</a>.</li>
  </ul>
  <p>My guess is that such agents will work by milestones: at each one, re-read the goal, verify progress, record what was learned with its conditions, and save state.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/milestone-loop.svg' | relative_url }}" alt="A weeks-long task split by milestones. At every milestone the agent re-reads the goal (cf. REAgent), verifies progress (cf. SWE-Review), records lessons with their conditions and saves its state (cf. AnchorTP and partial rollout), then continues until a verified result." width="900" height="360" loading="lazy"></div>
    <figcaption>Working by milestones. A direction I expect, built from lessons in our work, not a finished system.</figcaption>
  </figure>

  <p><strong>Recording lessons is the subtle step.</strong> I think experience should be kept at three levels: habits in the weights, procedures as reusable skills and tools (LegoFlow's blocks are a small example), and task-specific facts in memory, each tagged with the data, code version and settings under which it held.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/experience-layers.svg' | relative_url }}" alt="Experience from attempts, failures and reviews is kept at three levels: stable habits in weights, reusable procedures as skills and tools, and task-specific facts in memory together with the conditions under which they hold." width="900" height="380" loading="lazy"></div>
    <figcaption>Keeping experience at three levels. Memory entries carry their conditions so they can be re-checked when those conditions change.</figcaption>
  </figure>

  <h3 id="multi-agent">Teams of agents: extra agents help only when they add independent evidence</h3>
  <p>SWE-Review works because the reviewer explores the repository on its own instead of re-reading the generator's reasoning, and SwingArena separates the agent that writes a patch from the one that writes the tests. Two agents with the same context tend to miss the same bug. So I think useful teams will divide verification, not just labor, and share a memory of evidence and provenance rather than only conclusions. Studies of why <a href="https://arxiv.org/abs/2503.13657">multi-agent systems fail</a> point the same way.</p>

  <h3 id="evaluation-trust">Evaluation: treat it like a security boundary</h3>
  <p>Every capability gain we saw came with a gain in exploiting the environment: stronger teachers cheated more, and every sandbox phase needed defenses. Benchmarks for strong agents need locked-down networks, clean re-grading, held-out tasks and regular refreshes. Training records should tell apart attempts that failed, were never scored, or "succeeded" by a route we would not accept.</p>

  <h3 id="ai-for-ai">AI for AI: judgment will be the weakest link</h3>
  <p><a href="https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/">AlphaEvolve</a> shows that AI can already propose and test improvements to algorithms and infrastructure; LegoFlow's agent-run iterations are a small instance. Generating candidates is easy; deciding which are real is hard. So a self-improving loop should propose, select and confirm on separate information, keep fresh tasks out of the search, and compare at equal total budget. The gains most likely to compound are to the loop's own pipelines, environments and verifiers.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/verification-and-improvement.svg' | relative_url }}" alt="Left: a team organized around verification, with a proposer, tester and reviewer that see different information and share a memory of claims, evidence and provenance. Right: a self-improvement loop that proposes on search tasks, selects on separate tasks, confirms on fresh tasks and inherits improved pipelines, environments and verifiers, compared at equal total budget." width="960" height="400" loading="lazy"></div>
    <figcaption>Left: a team organized around verification. Right: a self-improvement loop that keeps proposing, selecting and confirming separate.</figcaption>
  </figure>

  <h3 id="ai-for-science">AI for Science: the longest horizon, with the weakest verifier</h3>
  <p>Science stretches everything above: horizons of months, goals that shift as you learn, and rarely a unit test for a claim. Simulators, analysis sandboxes and programmable labs will play the role that harnesses and tests play for code; AI for AI moves first because its lab is a compute cluster.</p>
  <p>Two links to our work are direct. <a href="https://arxiv.org/abs/2505.15929">PhyX</a> shows that multimodal models still lean on memorized formulas rather than physical understanding. Our <a href="{{ '/research/efficient-ml-ai-infrastructure/#compress' | relative_url }}">vocabulary scaling study</a> trusted its conclusion only after three independent methods agreed, the replication habit a science agent should have by default. And since the scientific form of reward hacking is cherry-picking runs, I expect useful science agents to log every experiment, not just the successes, and confirm findings on settings never used in the search.</p>

  <h2 id="open-questions">Open questions</h2>
  <ul class="research-questions">
    <li><strong>Can an agent trained across several harnesses do well in one it has never seen?</strong> Our mixed-harness training shows skills can be shared, not that they transfer. <span class="research-test">How we might test it: hold one harness out of training and evaluate on it, rotating which one.</span></li>
    <li><strong>How do we assign credit when one result arrives after days?</strong> The critic's jumps at turn boundaries hint at milestone-level credit. <span class="research-test">How we might test it: on the same long tasks and compute, compare rewards at verified milestones with a single final reward.</span></li>
    <li><strong>How should a long task keep its goal right?</strong> REAgent fixes the requirement up front, but in long projects it changes. <span class="research-test">How we might test it: change the requirement partway through and measure whether, and how soon, agents notice.</span></li>
    <li><strong>What belongs in weights, skills and memory?</strong> Each choice ages differently when the base model changes. <span class="research-test">How we might test it: store the same lesson all three ways, switch to a newer base model, and see which still helps.</span></li>
    <li><strong>How can a self-improving loop show it got better at improving?</strong> Fresh tasks get used up and equal-budget comparisons are costly. <span class="research-test">How we might test it: track the budget each round needs to find an improvement confirmed on an untouched task pool; it should shrink.</span></li>
    <li><strong>What is the unit test for a scientific claim?</strong> Simulations can be gamed and experiments are slow. <span class="research-test">How we might test it: start where simulation and cheap experiments can cross-check, and measure how often simulator-confirmed findings survive the real check.</span></li>
  </ul>

  <h2 id="resources">Project resources and papers</h2>
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
