---
layout: default
title: "Agentic Intelligence"
description: "Chaofan Tao's research on agentic intelligence: multimodal reasoning, coding agents built in the open at LegoX (verified data, SFT and RL inside real harnesses, agentic review), and his views on long-horizon memory, multi-agent collaboration, trustworthy evaluation and AI that improves AI."
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
  <p class="research-dek">An agent's ability doesn't live in the model alone. It lives in the loop around it: seeing the situation, acting, learning from what happened, and being checked. My work has built and stress-tested that loop, first in multimodal reasoning and now in coding agents. This page walks through what we found, and where I think the loop has to go next.</p>
  <p class="research-meta">By <a href="{{ '/' | relative_url }}">Chaofan Tao (陶超凡)</a> · Last updated <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%B %-d, %Y" }}</time></p>

  <p>For a long time, progress in AI meant a better answer to a fixed question. Agents change the question. An agent has to notice the detail that matters, decide what to try, act, read what came back and adjust. Each of those steps can fail on its own, and each needs its own kind of evidence. When I look back at my work, most of it is about one of those steps: whether a model actually sees the relation in a video or the cue in an image, whether its actions are grounded in what the environment showed it, whether it learns the right lesson from an attempt, and whether we can trust the check that says it improved.</p>
  <p>Coding agents became the place where I could study all of these at once. Code leaves a record of every action and every result, and tests give an outcome you can verify. At <a href="https://www.legox.net/">LegoX</a>, we have been building the pieces of this loop in the open: how verified experience is collected, how it becomes training signal, and how the result is checked. What we learned there now shapes how I think about longer tasks, teams of agents, and AI that helps improve AI.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/agentic-loop.svg' | relative_url }}" alt="Diagram of the agent learning loop: the agent, a model plus its harness, sits at the center of four stages connected clockwise: environment, experience, signal and evaluation, each labeled with the projects that study it." width="760" height="480" loading="eager"></div>
    <figcaption>The agent learning loop. An attempt leaves experience, training turns it into capability, and evaluation checks whether that capability carries over to new tasks.</figcaption>
  </figure>

  <p class="research-toc">On this page: <a href="#seeing">Seeing before acting</a> · <a href="#coding">Coding agents as a laboratory</a> · <a href="#lessons">What we learned</a> · <a href="#outlook">Where I think this is going</a> · <a href="#open-questions">Open questions</a></p>

  <h2 id="seeing">1. Seeing before acting: multimodal reasoning</h2>
  <p>My route into agents went through vision. In <a href="https://arxiv.org/abs/2408.09511">NAVERO</a>, we asked a simple question about video-language models: can they tell who did what to whom? Often they can't. A model would match a video to a caption even when the action or the relation in the caption was wrong. We built a benchmark from such near-miss descriptions and trained the model on them directly, so it had to learn the difference between similar actions instead of matching on objects alone. That experience stayed with me: before a model can act correctly, it has to perceive the right distinction.</p>
  <p>The same theme runs through our later multimodal work. <a href="https://arxiv.org/abs/2505.15929">PhyX</a> tests whether models can connect what they see with physical constraints, and finds them leaning on memorized formulas and surface patterns rather than understanding the situation. <a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a> builds search tasks whose answers depend on small visual clues that have to be carried through several rounds of retrieval; giving the agent tools to mark, crop and zoom changes what it can find, and most failures come from not locating the right evidence rather than from the last reasoning step. Our <a href="https://arxiv.org/abs/2411.05902">survey of autoregressive models in vision</a> maps how visual generation, from pixels to tokens to multi-scale models, is converging with understanding, and its paper list has become a widely used reference.</p>
  <p>We also studied how post-training shapes multimodal reasoning. The <a href="https://arxiv.org/abs/2507.07562">synergy dilemma</a> study found that long chain-of-thought SFT and RL help in different places, SFT on hard multi-step problems and RL across the board with shorter answers, and that combining them tends to trade one benefit for the other. <a href="https://arxiv.org/abs/2506.01713">SRPO</a> teaches multimodal models what a useful reflection looks like and then rewards reflections that actually change the reasoning. Finally, <a href="https://arxiv.org/abs/2402.16117">RoboCodeX</a> turns instructions into object-level actions with grasping and safety constraints, written as code, so a robot's behavior can be read, checked and moved to another platform.</p>
  <p>Put together, these projects kept pointing to the same place: the failure usually starts before the reasoning, at seeing the right detail or finding the right evidence. That is what drew me to agents. An agent can go and look.</p>

  <h2 id="coding">2. Coding agents as a laboratory</h2>
  <p>A coding agent never sees a repository directly. It sees whatever its harness shows it: which files and tool outputs reach the context, when history is compacted, how errors are reported. When we trained the same starting model inside three widely used harnesses with <a href="https://www.legox.net/blog/lego-rl/">Lego-RL</a>, it already behaved differently in each one before any training. The harness is part of the environment, not plumbing around the model. That observation shaped everything that followed.</p>

  <h3 id="data">Data: collecting experience worth learning from</h3>
  <p><a href="https://www.legox.net/blog/legoflow/">LegoFlow</a> turns real merged pull requests into executable tasks, and keeps a task only when the environment proves it: the original code fails the tests and the reference fix passes. Each stage, from collecting tasks to rolling out trajectories, training and evaluating, is a block that a coding agent can operate itself, with its own dashboard. <a href="https://arxiv.org/abs/2601.01426">SWE-Lego</a>, which I led, combines real tasks with synthetic ones made by injecting bugs, because real tasks bring depth and synthetic ones bring scale. <a href="https://arxiv.org/abs/2606.03461">Terminal-Lego</a> does the same for command-line work.</p>
  <p>The most important lessons were about which trajectories to keep. Terminal-Lego found that the strongest solver is not necessarily the best teacher: traces that visibly inspect, act and then verify teach students better than traces from stronger agents that jump to the answer. LegoFlow found that reasoning depth matters more than coverage, and that most of the benefit comes from removing the shallowest traces. And stronger teachers are better at cheating: finding the upstream fix, copying a patch, reading the answer from Git history. A successful trajectory is not necessarily an honest one, so we remove those paths from the environment itself instead of only asking the agent to behave.</p>

  <h3 id="learning">Learning: turning experience into capability</h3>
  <p>SWE-Lego showed that plain supervised fine-tuning can produce a strong open coding agent when the loss is treated as carefully as the data. Error masking keeps the whole trajectory, mistakes included, in context but takes no gradient on the wrong steps; a curriculum moves from easy to hard; and a verifier that answers "yes" or "no" in text picks the best of several attempts better than a scoring head. We also found that extra compute at test time is best spent first on more interaction turns and only then on parallel attempts.</p>
  <p>For reinforcement learning, <a href="https://arxiv.org/abs/2608.17393">Lego-RL</a> trains inside the real, unmodified harness. The hard part is making sure the trainer sees what the agent actually did. Harnesses rewrite their own history, so Lego-RL records tokens, probabilities and mixture-of-experts routing at generation time and replays the routing during training; mismatches here make no noise, which is exactly why they are dangerous. Tasks the model always or never solves teach it nothing, so difficulty has to follow the policy as it improves. After training, agents read more before editing, reread their own edits and run tests more often. Two follow-ups extend the recipe: training one model across several harnesses at once, and single-rollout optimization, which learns from one attempt per task with a learned critic. For tasks without a single checkable answer, <a href="https://arxiv.org/abs/2601.18533">RLVRR</a> builds rewards from reference answers, and <a href="https://arxiv.org/abs/2601.21968">OVD</a> learns from a teacher's text feedback on the student's own partial attempts.</p>

  <h3 id="checking">Checking: review and evaluation</h3>
  <p><a href="https://arxiv.org/abs/2607.06065">SWE-Review</a> trains a reviewer agent that explores the repository on its own, works out the root cause and compares it with a submitted patch, turning one-shot generation into generate, review and revise. Two results matter beyond the paper: review data also makes models better at fixing issues, and because choosing among a few attempts is cheaper than producing many more, a good reviewer makes test-time compute go further. <a href="https://arxiv.org/abs/2505.23932">SwingArena</a> (ICLR Oral) puts models in a continuous-integration loop as both patch submitters and test-writing reviewers, and <a href="https://arxiv.org/abs/2604.06861">REAgent</a> (ICSE) checks and improves the issue description itself before any patch is written.</p>
  <p class="research-readmore">Read more: <a href="https://www.legox.net/blog/legoflow-experiments/">Lessons learned from LegoFlow-SWE</a> · <a href="https://www.legox.net/blog/lego-rl-cross-harness/">RL across harnesses</a> · <a href="https://www.legox.net/blog/lego-rl-sao/">Single-rollout optimization</a> · <a href="https://www.legox.net/blog/swe-review/">SWE-Review</a></p>

  <h2 id="lessons">What we learned</h2>
  <ol class="research-insights">
    <li><strong>The strongest model is rarely the best teacher.</strong> What transfers is behavior the student can see and imitate: looking, acting on what was found, checking. The same mismatch between teacher strength and student learnability shows up in our <a href="{{ '/research/efficient-ml-ai-infrastructure/#transfer' | relative_url }}">distillation work</a>.</li>
    <li><strong>Reliable judgment is the scarce resource.</strong> Verified tasks, verifiers, reviewers and CI-based arenas are all ways of producing judgments we can trust. Generating attempts is cheap; choosing between them reliably is what scales.</li>
    <li><strong>The trainer must see what the agent actually did.</strong> In agent RL, systems details such as token alignment and routing replay decide whether learning optimizes the right thing.</li>
    <li><strong>Stronger agents find more shortcuts.</strong> Git history, upstream patches, visual questions answerable from text alone: honesty has to be built into the environment and the benchmark.</li>
    <li><strong>Depth beats coverage.</strong> Careful reasoning where it is needed, useful reflection over long reflection, and evidence over verbosity.</li>
  </ol>

  <h2 id="outlook">Where I think this is going</h2>
  <p>The projects above are, in a sense, small versions of problems the field is now facing at much larger scale. Here is where I think they lead.</p>

  <h3 id="long-horizon">Longer tasks: the bottleneck shifts from collecting experience to keeping it</h3>
  <p>As tasks stretch from fixing one issue to building a feature or running a research project over days, more experience is not the hard part. Keeping the right part of it is. Our data work already points this way: depth beats coverage, grounded traces beat confident ones, and partially successful attempts and review notes still carry useful lessons. I think experience will have to be kept at three levels. Stable habits, such as checking your own edit, belong in the weights. Procedures, such as how to set up and verify an environment, belong in reusable skills and tools; LegoFlow's blocks are a small example of this. Task-specific facts belong in memory, and every memory entry should carry the conditions under which it was true: which data, which code version, which settings. Without those conditions, a long-running agent will keep reusing conclusions that have quietly expired.</p>

  <h3 id="multi-agent">Teams of agents: extra agents help only when they add independent evidence</h3>
  <p>It is tempting to scale agents by running more of them in parallel. Our review work suggests a more specific condition. SWE-Review works because the reviewer explores the repository on its own instead of re-reading the generator's reasoning, and SwingArena separates the agent that writes a patch from the agent that writes the tests. Two agents with the same context and the same assumptions tend to miss the same bug. So I think useful teams will be organized around a division of verification rather than a division of labor alone: a proposer, a tester and a reviewer that see different information, with shared memory that records evidence and provenance rather than just conclusions. Studies of why <a href="https://arxiv.org/abs/2503.13657">multi-agent systems fail</a> point the same way: many failures come from unclear specifications, poor verification and agents not knowing when to stop.</p>

  <h3 id="evaluation-trust">Evaluation: it is becoming the main bottleneck, and it has to be treated like a security boundary</h3>
  <p>Every capability gain we saw came with a matching gain in the ability to exploit the environment. In LegoFlow, stronger teachers cheated more; in Lego-RL, we needed defenses at every phase of the sandbox; in multimodal benchmarks, questions could be answered without really looking. I expect this to get worse, not better. Benchmarks for strong agents need locked-down networks, clean re-grading of the final patch, held-out tasks that are never used during development, and regular refreshes. Training rewards need the same care: a record should say whether an attempt failed, was never scored, or succeeded by a route we would not accept, because a pipeline that confuses these teaches the next model the wrong lesson.</p>

  <h3 id="ai-for-ai">AI for AI: if AI is to improve AI, judgment will be the weakest link</h3>
  <p>Systems such as <a href="https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/">AlphaEvolve</a> show that AI can already propose and test improvements to algorithms and computing infrastructure. In our own work, LegoFlow's agent-run iterations are a small instance of the same idea: an agent reads evaluation results, changes how training data is filtered, and the next model improves. What I take from our experience is that generating candidate improvements is the easy part. The hard part is deciding which ones are real. A self-improving loop should separate the information used to propose a change, to select it and to confirm it; keep fresh tasks that never took part in the search; and compare progress at the same total budget, so that "better" does not just mean "searched more". I also think the improvements most likely to compound are improvements to the loop's own tooling, its data pipelines, environments and verifiers, because each of those raises the quality of every later round.</p>

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
