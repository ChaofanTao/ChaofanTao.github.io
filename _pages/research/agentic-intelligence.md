---
layout: default
title: "Agentic Intelligence"
description: "Chaofan Tao's research on agentic intelligence: coding agents built in the open at LegoX (verified data, SFT and RL inside real harnesses, agentic review), multimodal reasoning, and his views on long-horizon memory, multi-agent collaboration, trustworthy evaluation and AI that improves AI."
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
  - Recursive self-improvement
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
  <p class="research-dek">An agent's ability doesn't live in the model alone. It lives in the loop around it: seeing the situation, acting, learning from what happened, and being checked. At LegoX we have been building that loop in the open for coding agents, and our multimodal work tests what it needs beyond code. This page walks through what we found, and where I think the loop has to go next.</p>
  <p class="research-meta">By <a href="{{ '/' | relative_url }}">Chaofan Tao (陶超凡)</a> · Last updated <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%B %-d, %Y" }}</time></p>

  <p>For a long time, progress in AI meant a better answer to a fixed question. Agents change the question. An agent has to notice the detail that matters, decide what to try, act, read what came back and adjust. Each of those steps can fail on its own, and each needs its own kind of evidence: whether the model saw the right thing, whether its actions were grounded in what the environment showed it, whether it learned the right lesson from an attempt, and whether we can trust the check that says it improved.</p>
  <p>Coding agents are where we study all of these at once. Code leaves a record of every action and every result, and tests give an outcome you can verify. At <a href="https://www.legox.net/">LegoX</a>, we build each part of this loop as open, reusable pieces: how verified experience is collected, how it becomes training signal, and how the result is checked. Our multimodal work asks the same questions where the environment is an image, a video, the web or a robot.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/agentic-loop.svg' | relative_url }}" alt="Diagram of the agent learning loop: the agent, a model plus its harness, sits at the center of four stages connected clockwise: environment, experience, signal and evaluation, each labeled with the projects that study it." width="760" height="480" loading="eager"></div>
    <figcaption>The agent learning loop. An attempt leaves experience, training turns it into capability, and evaluation checks whether that capability carries over to new tasks.</figcaption>
  </figure>

  <p class="research-toc">On this page: <a href="#coding">Coding agents as a laboratory</a> · <a href="#multimodal">Beyond code</a> · <a href="#at-a-glance">At a glance</a> · <a href="#lessons">What we learned</a> · <a href="#outlook">Where I think this is going</a> · <a href="#open-questions">Open questions</a></p>

  <h2 id="coding">1. Coding agents as a laboratory</h2>
  <p>A coding agent never sees a repository directly. It sees whatever its harness shows it: which files and tool outputs reach the context, when history is compacted, how errors are reported, what happens after a command fails. When we trained the same starting model inside three widely used harnesses (OpenHands, Claude Code and OpenCode) with <a href="https://www.legox.net/blog/lego-rl/">Lego-RL</a>, it already behaved differently in each before any training. The harness is part of the environment, not plumbing around the model. That observation shaped how we collect data, how we train, and how we check results.</p>

  <h3 id="data">Data: experience worth learning from</h3>
  <p><a href="https://www.legox.net/blog/legoflow/">LegoFlow</a> treats code-data engineering as a chain of blocks. Curator finds merged pull requests, gathers the issue, commits and tests, rewrites them into a task that does not leak the answer, builds an isolated environment and keeps the task only if the original code fails the tests and the reference fix passes. Because passing that check only makes a task usable, Curator also scores difficulty with a static rubric over the size of the patch, the logic it adds, how much of the codebase it touches, the tests and the detail of the instructions, with no LLM judge involved. Tracer rolls out trajectories in sandboxes and screens them, and Trainer and Evaluator close the loop. Every block is packaged as a plugin skill, so a coding agent such as Claude Code or Codex can run the pipeline itself, and each block has its own dashboard. In one experiment, an agent ran the whole pipeline end to end, read the evaluation, noticed that many teacher traces contained only shallow reasoning, changed the filter and trained a clearly better model in the next round.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/legox/legoflow-architecture.png' | relative_url }}" alt="LegoFlow architecture: a Root block orchestrates Curator, Tracer, Trainer and Evaluator blocks, each exposed as plugin skills with its own dashboard, producing tasks, trajectories, models and scores." width="1600" height="766" loading="lazy"></div>
    <figcaption>LegoFlow's blocks, from task curation to evaluation, each operable by a coding agent. Figure from the <a href="https://www.legox.net/blog/legoflow/">LegoFlow blog</a>.</figcaption>
  </figure>

  <p><a href="https://arxiv.org/abs/2601.01426">SWE-Lego</a> combines real tasks from resolved pull requests with synthetic ones created by injecting bugs, through LLM rewriting and syntax-tree transformations. Real tasks bring depth and realism; synthetic tasks bring scale, and for the same repositories, adding them keeps helping. <a href="https://arxiv.org/abs/2606.03461">Terminal-Lego</a> brings the same discipline to command-line work, turning Stack Overflow problems into Docker-verified tasks.</p>
  <p>The lessons that mattered most were about which trajectories to keep. Terminal-Lego found that the strongest solver is not necessarily the best teacher: traces that visibly inspect, act on what they found and then verify the result teach students better than traces from stronger agents that jump straight to the answer. LegoFlow found that reasoning depth matters more than coverage. Teachers that think a little on every turn teach less than teachers that think hard when the problem calls for it, and most of the benefit comes from removing the shallowest traces rather than keeping only the longest. SWE-Lego added practical cleaning rules: repair malformed tool calls, keep the tool set small, and recycle attempts that found the right file but failed to fix it.</p>
  <p>Experience also has an honesty problem. Stronger teachers are better at finding shortcuts: locating the upstream pull request, copying the patch, or reading the fix from Git history. A successful trajectory is not necessarily an honest one. What worked was two layers: tell the agent plainly not to look up solutions, and make it impossible anyway, by rewriting Git history, hiding test files and restricting the network while the agent works, then restoring them only for grading.</p>

  <h3 id="learning">Learning: turning experience into capability</h3>
  <p>SWE-Lego showed that plain supervised fine-tuning can produce a strong open coding agent when the loss gets as much care as the data. Error masking keeps the whole trajectory, mistakes included, in context but takes no gradient on the wrong steps, so the model learns from its errors without learning to repeat them. A curriculum uses trajectory length as a stand-in for difficulty and trains from easy to hard, carrying earlier data forward. At inference time, extra compute is best spent first on more interaction turns and, once that saturates, on parallel attempts, with a verifier that answers "yes" or "no" in text choosing among them better than a scoring head does.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/legox/swe-lego-error-masking.png' | relative_url }}" alt="SWE-Lego error masking: an agent trajectory where the step that led to an execution error is excluded from the loss while correct steps receive gradient updates." width="1600" height="878" loading="lazy"></div>
    <figcaption>Step-level error masking in SWE-Lego: the model still sees the failed step and its error, but is not trained to imitate it. Figure from the <a href="https://www.legox.net/blog/swe-lego/">SWE-Lego blog</a>.</figcaption>
  </figure>

  <p>For reinforcement learning, <a href="https://arxiv.org/abs/2608.17393">Lego-RL</a> trains inside the real, unmodified harness. The hard part is making sure the trainer sees what the agent actually did. Harnesses rewrite their own history by compacting context, re-serializing tool calls and running sub-agents, so a saved transcript is not the token sequence that was sampled. An in-process proxy records tokens, probabilities and mixture-of-experts routing at generation time, and the routing is replayed during training. Mismatches here make no noise: training runs and curves move, which is exactly why they have to be checked explicitly. Two more lessons came from the runs themselves. Tasks the model always or never solves teach it nothing, so the useful difficulty band has to follow the policy as it improves. And a falling reward can mean a broken parser or failed environment setups rather than a worse policy, so dashboards that break down how every attempt ended are part of the method, not an extra. After training, the agents read more code before editing, reread their own edits and run tests more often, at the cost of longer sessions.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/legox/lego-rl-infrastructure.png' | relative_url }}" alt="Lego-RL infrastructure: unmodified harnesses run in sandboxes, an in-process proxy captures tokens and routing, a rollout engine and trainer exchange trajectories and weights with synchronous, asynchronous and partial-rollout modes." width="1600" height="992" loading="lazy"></div>
    <figcaption>Lego-RL connects unmodified harnesses to a trainer through an in-process proxy. Figure from the <a href="https://www.legox.net/blog/lego-rl/">Lego-RL blog</a>.</figcaption>
  </figure>

  <p>Two follow-ups extend the recipe. Training one model on a mix of harnesses came close to the average of separately trained models while narrowing some of the gaps between harnesses. Single-rollout optimization learns from one attempt per task with a learned critic instead of comparing many attempts, which saves most of the sampling but only works once the critic has been warmed up and the advantages normalized; without that, the policy collapsed into repeating its "think" tool. For tasks without a single checkable answer, <a href="https://arxiv.org/abs/2601.18533">RLVRR</a> builds a chain of rewards from good reference answers, covering content and style, and <a href="https://arxiv.org/abs/2601.21968">OVD</a> learns from a teacher's text feedback on the student's own partial attempts, keeping good beginnings and replacing weak continuations.</p>

  <h3 id="checking">Checking: review and evaluation</h3>
  <p><a href="https://arxiv.org/abs/2607.06065">SWE-Review</a> trains a reviewer agent that explores the repository on its own, works out the root cause, compares it with a submitted patch and writes structured feedback, turning one-shot generation into generate, review and revise. Two results matter beyond the paper: review data also makes models better at fixing issues, and because choosing among a few attempts is cheaper than producing many more, a good reviewer makes test-time compute go further. <a href="https://arxiv.org/abs/2505.23932">SwingArena</a> (ICLR Oral) puts models into a continuous-integration loop as both patch submitters and test-writing reviewers across several languages, and <a href="https://arxiv.org/abs/2604.06861">REAgent</a> (ICSE) checks and improves the issue description itself before any patch is written.</p>
  <p class="research-readmore">Read more: <a href="https://www.legox.net/blog/legoflow-experiments/">Lessons learned from LegoFlow-SWE</a> · <a href="https://www.legox.net/blog/lego-rl-cross-harness/">RL across harnesses</a> · <a href="https://www.legox.net/blog/lego-rl-sao/">Single-rollout optimization</a> · <a href="https://www.legox.net/blog/swe-review/">SWE-Review</a></p>

  <h2 id="multimodal">2. Beyond code: multimodal reasoning and the physical world</h2>
  <p>Code is a forgiving environment: everything is text and every result can be checked. Our multimodal work asks what the loop needs when the agent has to look. In <a href="https://arxiv.org/abs/2408.09511">NAVERO</a>, we found that video-language models often can't tell who did what to whom, matching a video to a caption even when the action or relation is wrong; training on such near-miss descriptions taught the model to separate similar actions. <a href="https://arxiv.org/abs/2505.15929">PhyX</a> shows models answering physics questions about images from memorized formulas and surface patterns rather than understanding the situation. <a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a> builds search tasks whose answers depend on small visual clues carried through several rounds of retrieval; tools to mark, crop and zoom change what the agent can find, and most failures come from not locating the right evidence rather than from the last reasoning step.</p>
  <p>On training, the <a href="https://arxiv.org/abs/2507.07562">synergy dilemma</a> study found that long chain-of-thought SFT and RL help reasoning VLMs in different places, and that combining them tends to trade one benefit for the other. <a href="https://arxiv.org/abs/2506.01713">SRPO</a> first shows the model what a useful reflection looks like, then rewards reflections that actually change its reasoning. <a href="https://arxiv.org/abs/2402.16117">RoboCodeX</a> turns instructions into object-level actions with grasping and safety constraints written as code, so code plays for a robot the role a harness plays for a software agent. Our <a href="https://arxiv.org/abs/2411.05902">survey of autoregressive models in vision</a> maps how visual generation and understanding are converging, and its paper list has become a widely used reference. Across these projects, the failure usually starts before the reasoning, at seeing the right detail or finding the right evidence, which is the part of the loop that agents, unlike fixed models, can go and fix.</p>

  <h2 id="at-a-glance">At a glance</h2>
  <div class="research-table-wrap">
    <table>
      <thead><tr><th>Stage</th><th>Work</th><th>What we showed</th></tr></thead>
      <tbody>
        <tr><td rowspan="2">Environment</td><td>Lego-RL</td><td>The harness is part of the environment; train inside the real, unmodified harness</td></tr>
        <tr><td>MMSearch-Plus · RoboCodeX</td><td>Tools decide what evidence an agent can use; code is the interface to robots</td></tr>
        <tr><td rowspan="3">Experience</td><td>LegoFlow</td><td>Real pull requests become tasks only when tests prove them; the pipeline is operable by agents</td></tr>
        <tr><td>SWE-Lego</td><td>Real tasks for depth, synthetic tasks for scale; shortcuts removed from the environment</td></tr>
        <tr><td>Terminal-Lego</td><td>Grounded traces teach better than stronger solvers</td></tr>
        <tr><td rowspan="4">Signal</td><td>SWE-Lego</td><td>Error masking, curriculum and a text verifier make SFT-only coding agents strong</td></tr>
        <tr><td>Lego-RL</td><td>Faithful RL inside real harnesses; difficulty follows the policy</td></tr>
        <tr><td>RLVRR · OVD</td><td>Rewards from references; learning from text feedback on partial attempts</td></tr>
        <tr><td>SRPO · Synergy dilemma</td><td>Useful reflection over long reflection; SFT and RL help in different places</td></tr>
        <tr><td rowspan="3">Evaluation</td><td>SWE-Review</td><td>Independent review; review data improves fixing; choosing is cheaper than generating</td></tr>
        <tr><td>SwingArena · REAgent</td><td>Evaluation inside CI; requirements checked before patching</td></tr>
        <tr><td>PhyX · NAVERO</td><td>Physical reasoning and fine-grained video relations expose perception failures</td></tr>
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

  <h2 id="outlook">Where I think this is going</h2>
  <p>The projects above are, in a sense, small versions of problems the field now faces at much larger scale. Here is where I think they lead.</p>

  <h3 id="long-horizon">Longer tasks: the bottleneck shifts from collecting experience to keeping it</h3>
  <p>As tasks stretch from fixing one issue to building a feature or running a research project over days, more experience is not the hard part; keeping the right part of it is. Our data work already points this way: depth beats coverage, grounded traces beat confident ones, and partial successes and review notes still carry useful lessons. I think experience will have to be kept at three levels. Stable habits, such as checking your own edit, belong in the weights. Procedures, such as how to set up and verify an environment, belong in reusable skills and tools; LegoFlow's blocks are a small example. Task-specific facts belong in memory, and every entry should carry the conditions under which it was true: which data, which code version, which settings. Without those conditions, a long-running agent will keep reusing conclusions that have quietly expired.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/experience-layers.svg' | relative_url }}" alt="Experience from attempts, failures and reviews is kept at three levels: stable habits in weights, reusable procedures as skills and tools, and task-specific facts in memory together with the conditions under which they hold." width="900" height="380" loading="lazy"></div>
    <figcaption>Keeping experience at three levels. Memory entries carry their conditions so they can be re-checked when those conditions change.</figcaption>
  </figure>

  <h3 id="multi-agent">Teams of agents: extra agents help only when they add independent evidence</h3>
  <p>It is tempting to scale agents by running more of them in parallel. Our review work suggests a more specific condition. SWE-Review works because the reviewer explores the repository on its own instead of re-reading the generator's reasoning, and SwingArena separates the agent that writes a patch from the agent that writes the tests. Two agents with the same context and the same assumptions tend to miss the same bug. So I think useful teams will be organized around a division of verification rather than a division of labor alone: a proposer, a tester and a reviewer that see different information, with shared memory that records evidence and provenance rather than just conclusions. Studies of why <a href="https://arxiv.org/abs/2503.13657">multi-agent systems fail</a> point the same way: many failures come from unclear specifications, weak verification and agents not knowing when to stop.</p>

  <h3 id="evaluation-trust">Evaluation: it is becoming the main bottleneck, and it has to be treated like a security boundary</h3>
  <p>Every capability gain we saw came with a matching gain in the ability to exploit the environment. In LegoFlow, stronger teachers cheated more; in Lego-RL, we needed defenses at every phase of the sandbox; in multimodal benchmarks, questions could be answered without really looking. I expect this to get worse, not better. Benchmarks for strong agents need locked-down networks, clean re-grading of the final patch, held-out tasks that are never used during development, and regular refreshes. Training rewards need the same care: a record should say whether an attempt failed, was never scored, or succeeded by a route we would not accept, because a pipeline that confuses these teaches the next model the wrong lesson.</p>

  <h3 id="ai-for-ai">AI for AI: if AI is to improve AI, judgment will be the weakest link</h3>
  <p>Systems such as <a href="https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/">AlphaEvolve</a> show that AI can already propose and test improvements to algorithms and computing infrastructure. LegoFlow's agent-run iterations are a small instance of the same idea: an agent reads evaluation results, changes how training data is filtered, and the next model improves. What our experience says is that generating candidate improvements is the easy part; deciding which ones are real is hard. A self-improving loop should separate the information used to propose a change, to select it and to confirm it; keep fresh tasks that never took part in the search; and compare progress at the same total budget, so that "better" does not just mean "searched more". I also think the improvements most likely to compound are improvements to the loop's own tooling, its data pipelines, environments and verifiers, because each raises the quality of every later round.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/verification-and-improvement.svg' | relative_url }}" alt="Left: a team organized around verification, with a proposer, tester and reviewer that see different information and share a memory of claims, evidence and provenance. Right: a self-improvement loop that proposes on search tasks, selects on separate tasks, confirms on fresh tasks and inherits improved pipelines, environments and verifiers, compared at equal total budget." width="960" height="400" loading="lazy"></div>
    <figcaption>Left: a team organized around verification. Right: a self-improvement loop that keeps proposing, selecting and confirming separate.</figcaption>
  </figure>

  <h2 id="open-questions">Open questions</h2>
  <ul>
    <li>Can an agent trained across several harnesses do well in one it has never seen?</li>
    <li>When a single success or failure arrives after hours of actions, how do we tell which steps actually helped?</li>
    <li>What is the right split between weights, skills and memory for experience that should last?</li>
    <li>How can a self-improving loop show that later rounds discover improvements more efficiently, not just that it tried more candidates?</li>
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
