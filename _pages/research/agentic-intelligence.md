---
layout: default
title: "Agentic Coding, Reasoning and Evaluation"
description: "How agents learn from a loop of environment, experience, signal and evaluation, and what building each part in the open taught Chaofan Tao and collaborators about coding agents, multimodal reasoning and benchmarks."
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
  <p class="research-dek">Agents learn from a loop, not a dataset. This essay follows that loop, from the environment an agent acts in to the evaluation that tells us whether it improved, and collects what building each part in the open has taught us.</p>
  <p class="research-meta">By <a href="{{ '/' | relative_url }}">Chaofan Tao (陶超凡)</a> and collaborators at LegoX · Last updated <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%B %-d, %Y" }}</time></p>

  <p>Language models became useful by learning from text. Agents become useful by learning from what happens when they act: a command fails, a test passes, a web page turns out to be the wrong one, a reviewer sends a patch back. That shift moves the hard problems. The model still matters, but so do four things around it: the <strong>environment</strong> it acts in, the <strong>experience</strong> it collects there, the <strong>signal</strong> that turns experience into learning, and the <strong>evaluation</strong> that tells us whether any of it worked.</p>
  <p>Our work on coding agents, multimodal reasoning and benchmarks can be read as a study of that loop. Some projects build one part of it in the open: <a href="https://www.legox.net/blog/legoflow/">LegoFlow</a> and <a href="https://www.legox.net/blog/swe-lego/">SWE-Lego</a> for experience, <a href="https://www.legox.net/blog/lego-rl/">Lego-RL</a> for learning inside real environments, <a href="https://www.legox.net/blog/swe-review/">SWE-Review</a> and <a href="https://arxiv.org/abs/2505.23932">SwingArena</a> for review and evaluation. Others ask what breaks when the loop meets images, the web or the physical world. Read together, they point to conclusions no single paper states on its own: the strongest model is rarely the best teacher, verification is the scarce resource, and as agents grow more capable, the integrity of the loop has to be engineered rather than assumed.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/agentic-loop.svg' | relative_url }}" alt="Diagram of the agent learning loop: the agent, a model plus its harness, sits at the center of four stages connected clockwise: environment, experience, signal and evaluation, each labeled with the projects that study it." width="760" height="480" loading="eager"></div>
    <figcaption>The agent learning loop. Each stage is a place where the loop can quietly fail, and each project on this page studies one of them.</figcaption>
  </figure>

  <p class="research-toc">On this page: <a href="#environment">Environment</a> · <a href="#experience">Experience</a> · <a href="#signal">Signal</a> · <a href="#evaluation">Evaluation</a> · <a href="#physical">Beyond the terminal</a> · <a href="#insights">What ties it together</a> · <a href="#open-questions">Open questions</a></p>

  <h2 id="environment">1. The environment is part of the agent</h2>
  <p class="research-claim">Change the harness and you change the agent.</p>
  <p>A coding agent never sees a repository directly. It sees what its harness shows it: which files and tool outputs enter the context, when the conversation is compacted, how errors are reported and how the loop continues after a failed command. When we trained with Lego-RL inside three widely used harnesses (OpenHands, Claude Code and OpenCode), the same starting model already behaved noticeably differently in each, before any training. That observation shaped the design. Lego-RL trains inside the unmodified harness instead of a simplified copy, and treats the harness as part of the environment rather than part of the policy.</p>
  <p>A natural next question is whether one model can serve many harnesses. Training on rollouts from several harnesses at once came close to the average of separately trained models while narrowing some of the gaps between them. That is encouraging, but every harness in those runs was seen during training; how an agent copes with one it has never seen is still open.</p>
  <p>The same idea holds outside code. In multimodal search, the tools are the harness: <a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a> gives a browsing agent a set-of-mark module to mark, crop and zoom into an image before it searches, and that choice changes which evidence the agent can use at all. In robotics, <a href="https://arxiv.org/abs/2402.16117">RoboCodeX</a> makes code the interface between perception and action, which makes behavior inspectable and portable across robot platforms.</p>

  <h2 id="experience">2. Experience: what is worth learning from</h2>
  <p class="research-claim">Teachability is a property of the trajectory, not of the teacher.</p>
  <p>Experience starts with tasks the environment can check. LegoFlow mines merged pull requests, rewrites each into a task that does not leak its answer, builds an isolated environment, and keeps it only if the original code fails the tests and the reference fix passes. Passing that check makes a task usable, not valuable, so a static rubric also scores difficulty from the scope of the patch, the logic it adds, the breadth of context it touches, the tests and the detail of the instructions. SWE-Lego mixes real tasks, which bring depth, with synthetic ones made by injecting bugs, which bring breadth; Terminal-Lego turns community Q&amp;A into command-line tasks.</p>
  <p>The more surprising lessons concern trajectories, the recorded attempts a teacher agent makes on those tasks. <a href="https://arxiv.org/abs/2606.03461">Terminal-Lego</a> found that traces which visibly inspect the environment, act on what they saw and then verify the result teach students far better than traces from stronger agents that jump straight to the answer; in the paper's words, “the best solver is the worst teacher.” LegoFlow found a related pattern inside the reasoning itself: teachers that think briefly on every turn teach less than teachers that reason in depth when a problem calls for it, and most of the benefit comes from discarding the shallowest traces rather than keeping only the longest.</p>
  <p>Experience also has an integrity problem. Stronger teachers are better at finding shortcuts: locating the upstream pull request, copying the patch, or reading the fix from Git history. A successful trajectory is not necessarily an honest one. The defenses that worked were layered: an explicit instruction not to look up solutions, enforced by the environment, which rewrites history and restricts network access while the agent runs and restores both only for grading.</p>
  <p class="research-knowhow-label">What we learned</p>
  <ul class="research-knowhow">
    <li>Filter trajectories for grounding and depth, not just for success.</li>
    <li>Treat leakage as a property of the environment to be removed, not a behavior to be discouraged.</li>
  </ul>
  <p class="research-readmore">Read more: <a href="https://www.legox.net/blog/legoflow-experiments/">Lessons learned from LegoFlow-SWE</a> · <a href="https://www.legox.net/blog/terminal-lego/">Terminal-Lego</a> · <a href="https://www.legox.net/blog/swe-lego/">SWE-Lego</a></p>

  <h2 id="signal">3. Signal: from imitation to verification</h2>
  <p class="research-claim">Each training signal teaches something different, and a well-aimed signal beats a larger one.</p>
  <p><strong>Imitation, done carefully.</strong> SWE-Lego shows how far supervised fine-tuning goes when the loss is shaped as carefully as the data. Error masking keeps a whole trajectory in context but takes no gradient on the agent's wrong steps, so the model sees its mistakes without learning to repeat them. A curriculum uses trajectory length as a proxy for difficulty and moves from easy to hard while replaying earlier data. At inference time, a generative verifier that answers “yes” or “no” in text ranks attempts better than a scoring head, because it reuses what the model learned in pre-training.</p>
  <p><strong>Reinforcement in the real environment.</strong> Outcome rewards from executed tests are honest only if what the trainer optimizes matches what the model actually did. Harnesses rewrite their own history, so a saved transcript is not the token sequence that was sampled; Lego-RL records tokens, probabilities and mixture-of-experts routing at generation time and replays the routing during training. Misalignments here are silent: training runs, curves move, and nothing errors. Difficulty is relative to the current policy, because tasks that always pass or always fail produce no learning signal, and that band shifts as the agent improves. After training, agents read more before editing, reread their edits and run tests more often, at the price of longer interactions. Single-rollout optimization pushes efficiency further by learning from one attempt per task with a learned critic, which has to be warmed up before it can guide the policy.</p>
  <p><strong>Beyond pass or fail.</strong> Many tasks have no single checkable answer. <a href="https://arxiv.org/abs/2601.18533">RLVRR</a> replaces one verifiable “dot” with a chain of reference-based checks on content and style, bringing the efficiency of supervised data into reinforcement learning for open-ended generation. <a href="https://arxiv.org/abs/2601.21968">On-policy Verbal Distillation</a> learns from black-box teachers that only return text: their scores rank the student's own partial attempts, good prefixes are kept and weak continuations replaced, which preserves the student's exploration.</p>
  <p><strong>The same tension in vision.</strong> For reasoning vision-language models, long chain-of-thought SFT and RL turn out to help in different places: SFT on hard, multi-step questions at the cost of verbosity, RL across difficulty levels with concise answers. Every way of combining them that we tried traded one benefit for another instead of adding them, the <a href="https://arxiv.org/abs/2507.07562">synergy dilemma</a>. <a href="https://arxiv.org/abs/2506.01713">SRPO</a> takes a narrower path: first teach the form of good reflection with data, then reward reflections that are short and actually change the reasoning.</p>
  <p class="research-readmore">Read more: <a href="https://www.legox.net/blog/lego-rl/">Lego-RL</a> · <a href="https://www.legox.net/blog/lego-rl-cross-harness/">RL across harnesses</a> · <a href="https://www.legox.net/blog/lego-rl-sao/">Single-rollout optimization</a></p>

  <h2 id="evaluation">4. Evaluation and review: a mirror that cannot be gamed</h2>
  <p class="research-claim">As agents improve, evaluation has to be designed like a security boundary.</p>
  <p>The same capability that lets a teacher find shortcuts during data collection lets an agent find them during evaluation. Benchmarks therefore need the same discipline as training environments, and ideally more realism. <a href="https://arxiv.org/abs/2505.23932">SwingArena</a> (ICLR Oral) moves evaluation into continuous integration: models take turns as patch submitters and as reviewers who write the tests, across several programming languages, with retrieval to cope with long repositories. <a href="https://arxiv.org/abs/2604.06861">REAgent</a> (ICSE) treats the issue text itself as a requirement that can be incomplete, and checks and refines it before patching.</p>
  <p>Review is where evaluation becomes part of the loop. <a href="https://arxiv.org/abs/2607.06065">SWE-Review</a> trains a reviewer agent that explores the repository on its own, traces the root cause, compares its diagnosis with a submitted patch and returns structured feedback, turning one-shot generation into generate, review and revise. Two consequences matter beyond the paper: review trajectories transfer back to issue resolution, and because choosing among attempts is cheaper than generating more of them, a good reviewer makes test-time scaling cheaper.</p>
  <p>Multimodal benchmarks face their own shortcut: questions that can be answered without looking. <a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a> builds questions whose answers depend on fine-grained visual cues carried through repeated searches; most failures come from finding the right page and telling similar events apart, not from the final reasoning step. <a href="https://arxiv.org/abs/2505.15929">PhyX</a> shows models leaning on memorized formulas and surface patterns instead of physical understanding, and <a href="https://arxiv.org/abs/2408.09511">NAVERO</a> probes how video-language models handle relations that change over time.</p>

  <h2 id="physical">5. Beyond the terminal</h2>
  <p class="research-claim">The loop does not change when the environment becomes physical; the interface does.</p>
  <p>RoboCodeX decomposes a high-level instruction, in a tree, into object-centric manipulation steps annotated with affordances and safety constraints, and writes them as code. Code plays the role a harness plays for software agents: it is the layer where behavior becomes explicit, checkable and reusable across robots. PhyX measures the physical reasoning such agents need, and our <a href="https://arxiv.org/abs/2411.05902">survey of autoregressive models in vision</a> maps how visual generation, from pixels to tokens to scales, is reaching into embodied settings.</p>

  <h2 id="insights">What ties it together</h2>
  <ol class="research-insights">
    <li><strong>The strongest model is rarely the best teacher.</strong> Grounded traces beat stronger solvers in Terminal-Lego, stronger teachers hack more in LegoFlow, and the same mismatch between teacher strength and student learnability motivates <a href="{{ '/research/efficient-ml-ai-infrastructure/#transfer' | relative_url }}">routing prompts to the right teacher</a>. What transfers is behavior the student can see and imitate.</li>
    <li><strong>Verification is the scarce resource.</strong> Verified tasks, verifiers that rank attempts, reviewers that diagnose patches and CI-based arenas are all ways of producing trustworthy judgments. Generation is cheap; trustworthy selection is what scales.</li>
    <li><strong>Fidelity is a correctness problem.</strong> If the tokens, probabilities or routing the trainer sees differ from what the agent did, learning silently optimizes the wrong thing. Systems engineering and learning are not separable in agentic RL.</li>
    <li><strong>Capability amplifies shortcuts.</strong> Git history, upstream patches and text-only answers to visual questions are all shortcuts that stronger models find more often. Integrity has to live in the environment and the benchmark, not in the prompt.</li>
    <li><strong>Depth beats coverage.</strong> Deep reasoning on the turns that need it beats shallow reasoning everywhere; useful reflection beats long reflection; and verbose chains of thought are a cost, not a free lunch.</li>
  </ol>

  <h2 id="open-questions">Open questions</h2>
  <ul>
    <li>Can an agent trained across several harnesses work well in one it has never seen?</li>
    <li>How should credit be assigned across long trajectories, where a single pass or fail arrives after dozens of actions?</li>
    <li>What changes when agents must ask users questions and iterate, rather than close a ticket alone?</li>
    <li>Can supervised and reinforcement signals be combined adaptively, so their benefits add instead of trade off?</li>
    <li>How do these lessons extend to long-horizon tasks, such as building a repository from a natural-language specification?</li>
  </ul>

  <h2 id="resources">Open resources</h2>
  <ul>
    <li>LegoFlow: <a href="https://github.com/LegoX/LegoFlow">code</a> · <a href="https://huggingface.co/collections/Lego-X/legoflow">data</a></li>
    <li>SWE-Lego: <a href="https://github.com/LegoX/SWE-Lego">code</a> · <a href="https://huggingface.co/collections/Lego-X/swe-lego">data and models</a></li>
    <li>Terminal-Lego: <a href="https://github.com/LegoX/Terminal-Lego">code</a> · <a href="https://huggingface.co/datasets/SWE-Lego/Terminal-Lego-15k">data</a></li>
    <li>Lego-RL: <a href="https://github.com/LegoX/Lego-RL">code</a> · <a href="https://huggingface.co/collections/Lego-X/lego-rl">models and data</a></li>
    <li>SWE-Review: <a href="https://github.com/LegoX/SWE-Review">code</a> · <a href="https://huggingface.co/collections/Lego-X/swe-review">models and data</a></li>
  </ul>

  {% include research/paper-list.liquid group="agentic" lang="en" %}

  <p>Related: <a href="{{ '/research/efficient-ml-ai-infrastructure/' | relative_url }}">Efficient ML and AI infrastructure</a></p>
</div>
