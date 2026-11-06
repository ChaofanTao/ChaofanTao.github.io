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
  <p class="research-dek">Agents learn from a loop, not a dataset. This is my attempt to walk through that loop, from the environment an agent works in to the tests that tell us whether it got better, and to share what building each piece in the open has taught us.</p>
  <p class="research-meta">By <a href="{{ '/' | relative_url }}">Chaofan Tao (陶超凡)</a> · Last updated <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%B %-d, %Y" }}</time></p>

  <p>Language models got good by reading text. Agents get good by doing things and watching what happens: a command fails, a test passes, a web page turns out to be the wrong one, a reviewer sends the patch back. Once you take that seriously, the hard problems move. The model still matters, of course. But so do four things around it: the <strong>environment</strong> it works in, the <strong>experience</strong> it collects there, the <strong>signal</strong> that turns that experience into learning, and the <strong>evaluation</strong> that tells us whether any of it worked.</p>
  <p>I find it helpful to read most of my recent work as a study of that loop. Some projects build one piece of it in the open: <a href="https://www.legox.net/blog/legoflow/">LegoFlow</a> and <a href="https://www.legox.net/blog/swe-lego/">SWE-Lego</a> for experience, <a href="https://www.legox.net/blog/lego-rl/">Lego-RL</a> for learning inside real environments, and <a href="https://www.legox.net/blog/swe-review/">SWE-Review</a> and <a href="https://arxiv.org/abs/2505.23932">SwingArena</a> for review and evaluation. Others ask what goes wrong when the loop runs on images, the web or the physical world. Each paper answers its own question. Put side by side, though, they say a few things none of them says alone: the strongest model is rarely the best teacher, checking answers is harder than producing them, and the more capable agents get, the less we can take the honesty of the loop for granted.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/agentic-loop.svg' | relative_url }}" alt="Diagram of the agent learning loop: the agent, a model plus its harness, sits at the center of four stages connected clockwise: environment, experience, signal and evaluation, each labeled with the projects that study it." width="760" height="480" loading="eager"></div>
    <figcaption>The agent learning loop. Every stage is a place where things can quietly go wrong, and each project on this page looks at one of them.</figcaption>
  </figure>

  <p class="research-toc">On this page: <a href="#environment">Environment</a> · <a href="#experience">Experience</a> · <a href="#signal">Signal</a> · <a href="#evaluation">Evaluation</a> · <a href="#physical">Beyond the terminal</a> · <a href="#insights">What ties it together</a> · <a href="#open-questions">Open questions</a></p>

  <h2 id="environment">1. The environment is part of the agent</h2>
  <p>It's easy to think of an agent as "the model", with the tooling around it as plumbing. That picture turned out to be wrong in a way that matters. A coding agent never looks at a repository directly. It sees whatever its harness decides to show it: which files and tool outputs make it into the context, when the conversation gets compacted, how errors are reported, what happens after a command fails. When we plugged the same starting model into three widely used harnesses (OpenHands, Claude Code and OpenCode) for Lego-RL, it already behaved noticeably differently in each one before we had trained anything. Change the harness and you have, in a real sense, a different agent.</p>
  <p>That shaped how we built the system. Lego-RL trains inside the real, unmodified harness instead of a simplified copy, and treats the harness as part of the environment rather than part of the model. The obvious follow-up was whether one model could serve several harnesses at once. Training on a mix of all three got close to the average of three separately trained models and narrowed some of the gaps between them. That's encouraging, but every harness in those runs was one the model had seen during training. How an agent copes with a harness it has never met is still an open question.</p>
  <p>The same thing shows up outside code. In multimodal search, the tools are the harness. <a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a> gives a browsing agent a set-of-mark tool for marking, cropping and zooming into an image before it searches, and that one design choice changes what evidence the agent can use at all. In robotics, <a href="https://arxiv.org/abs/2402.16117">RoboCodeX</a> uses code as the bridge between what the robot sees and what it does, which makes its behavior something you can read, check and move to another robot.</p>

  <h2 id="experience">2. Experience: what is worth learning from</h2>
  <p>Everything starts with tasks the environment can actually check. LegoFlow mines merged pull requests, rewrites each one so it doesn't give away the answer, builds an isolated environment for it, and keeps it only if the original code fails the tests and the reference fix passes. Passing that check tells you a task is usable. It doesn't tell you the task is worth training on, so we also score difficulty with a simple rubric: how big the patch is, how much new logic it adds, how much of the codebase it touches, how involved the tests are and how detailed the instructions are. SWE-Lego mixes real tasks, which bring realism and depth, with synthetic ones created by injecting bugs, which bring scale. Terminal-Lego does the same for command-line work, starting from Stack Overflow questions.</p>
  <p>The lessons that surprised us most were about trajectories, the recorded attempts a teacher agent makes on these tasks. The usual assumption is simple: pick the strongest agent you can afford as the teacher. <a href="https://arxiv.org/abs/2606.03461">Terminal-Lego</a> found that this can be backwards. Trajectories that visibly look around, act on what they found and then check the result taught students far better than trajectories from stronger agents that jump straight to the answer. The paper puts it bluntly: "the best solver is the worst teacher." LegoFlow found something similar inside the reasoning itself. A teacher that thinks a little on every turn teaches less than one that thinks hard on the turns that need it, and most of the benefit comes from throwing out the shallowest traces, not from keeping only the longest ones.</p>
  <p>There's also an honesty problem. Stronger teachers are better at finding shortcuts: tracking down the upstream pull request, copying the patch, or reading the fix straight out of Git history. A successful trajectory isn't necessarily an honest one. What worked for us was a combination: tell the agent plainly not to look up solutions, and then make it impossible anyway, by rewriting history and cutting off network access while the agent works and only restoring them for grading.</p>
  <p class="research-knowhow-label">What we took away</p>
  <ul class="research-knowhow">
    <li>Pick trajectories for how they reason and how closely they engage with the environment, not just for whether they succeeded.</li>
    <li>Treat answer leakage as something to remove from the environment, not something to ask the agent nicely to avoid.</li>
  </ul>
  <p class="research-readmore">Read more: <a href="https://www.legox.net/blog/legoflow-experiments/">Lessons learned from LegoFlow-SWE</a> · <a href="https://www.legox.net/blog/terminal-lego/">Terminal-Lego</a> · <a href="https://www.legox.net/blog/swe-lego/">SWE-Lego</a></p>

  <h2 id="signal">3. Signal: from imitation to verification</h2>
  <p>If experience is what the agent tries, the signal is what it learns from those tries. What I've come to believe is that different signals teach genuinely different things, and that a well-aimed signal beats simply having more of it.</p>
  <p><strong>Imitation, done carefully.</strong> SWE-Lego was our test of how far plain supervised fine-tuning can go if you treat the loss with as much care as the data. With error masking, the model still sees the whole trajectory, mistakes included, but gets no gradient on the wrong steps, so it learns from its errors without learning to repeat them. A curriculum uses trajectory length as a rough stand-in for difficulty and works from easy to hard, mixing earlier data back in so nothing is forgotten. And when it comes to picking the best of several attempts, a verifier that simply answers "yes" or "no" in text does better than one with a scoring head, because it can lean on what the model already learned during pre-training.</p>
  <p><strong>RL in the real environment.</strong> Rewards from running tests sound naturally honest. They are only honest, though, if what the trainer optimizes matches what the model actually did. Harnesses quietly rewrite their own history, so a saved transcript isn't the exact token sequence the model produced. Lego-RL records tokens, probabilities and mixture-of-experts routing at the moment of generation, and replays that routing during training. The unnerving part is that mismatches here make no noise: training runs, curves move, nothing errors out. Difficulty also turns out to be relative. Tasks the model always solves, or never solves, teach it nothing, and the useful middle shifts as the agent improves. After training, the agents read more code before editing, reread their own edits and run the tests more often, at the cost of longer sessions. A newer recipe, single-rollout optimization, learns from just one attempt per task with a learned critic, but only once that critic has been warmed up enough to give sensible guidance.</p>
  <p><strong>Beyond pass or fail.</strong> Lots of useful tasks don't have one checkable answer. <a href="https://arxiv.org/abs/2601.18533">RLVRR</a> swaps a single pass/fail check for a chain of smaller checks against good reference answers, covering both content and style, which brings some of the efficiency of supervised data into RL for open-ended writing. <a href="https://arxiv.org/abs/2601.21968">On-policy Verbal Distillation</a> works with teachers that only give text feedback: their scores rank the student's own partial attempts, the good beginnings are kept and the weak continuations replaced, so the student keeps exploring instead of just copying.</p>
  <p><strong>The same tension in vision.</strong> With vision-language models, long chain-of-thought SFT and RL help in different places. SFT helps most on hard, multi-step questions but makes answers long-winded; RL helps across the board and keeps answers short. Every way we tried to combine them traded one benefit for the other instead of adding them up, which is what the <a href="https://arxiv.org/abs/2507.07562">synergy dilemma</a> paper is about. <a href="https://arxiv.org/abs/2506.01713">SRPO</a> takes a more focused route: first show the model what a good reflection looks like, then reward reflections that are short and actually change its reasoning.</p>
  <p class="research-readmore">Read more: <a href="https://www.legox.net/blog/lego-rl/">Lego-RL</a> · <a href="https://www.legox.net/blog/lego-rl-cross-harness/">RL across harnesses</a> · <a href="https://www.legox.net/blog/lego-rl-sao/">Single-rollout optimization</a></p>

  <h2 id="evaluation">4. Evaluation and review: a mirror that's hard to fool</h2>
  <p>Here's the uncomfortable symmetry: the same skill that lets a teacher find shortcuts while we collect data lets an agent find shortcuts while we evaluate it. So as agents get stronger, I think benchmarks need to be built with the care of a security boundary, and ideally with more realism too. <a href="https://arxiv.org/abs/2505.23932">SwingArena</a> (ICLR Oral) moves evaluation into continuous integration. Models take turns submitting patches and acting as reviewers who write the tests, across several programming languages, with retrieval to help them cope with very large codebases. <a href="https://arxiv.org/abs/2604.06861">REAgent</a> (ICSE) starts one step earlier: it treats the issue description as a requirement that might be incomplete, and checks and improves it before trying to fix anything.</p>
  <p>Review is where evaluation stops being a final exam and becomes part of the loop. <a href="https://arxiv.org/abs/2607.06065">SWE-Review</a> trains a reviewer agent that explores the repository on its own, figures out the root cause, compares that with the submitted patch and writes back structured feedback. One-shot generation becomes generate, review, revise. Two things from that work stay with me. Review data turns out to make models better at fixing issues too. And because picking among a few attempts is cheaper than generating many more, a good reviewer makes it cheaper to spend extra compute at test time.</p>
  <p>Multimodal benchmarks have a shortcut of their own: questions you can answer without really looking. <a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a> is built so the answer depends on small visual clues that have to be carried through several rounds of search. Most failures there come from not finding the right page or confusing similar-looking events, not from the last reasoning step. <a href="https://arxiv.org/abs/2505.15929">PhyX</a> shows models leaning on memorized formulas and surface patterns rather than real physical understanding, and <a href="https://arxiv.org/abs/2408.09511">NAVERO</a> looks at how video-language models handle relationships that change over time.</p>

  <h2 id="physical">5. Beyond the terminal</h2>
  <p>When the environment becomes physical, the loop stays the same; what changes is the interface. RoboCodeX breaks a high-level instruction down, step by step, into actions on specific objects, each annotated with how the object can be grasped or moved and what is safe, and then writes those actions as code. Code plays the same role here that a harness plays for software agents: it's the layer where behavior becomes explicit, checkable and reusable from one robot to the next. PhyX measures the kind of physical reasoning these agents will need, and our <a href="https://arxiv.org/abs/2411.05902">survey of autoregressive models in vision</a> traces how visual generation, from pixels to tokens to multi-scale models, is starting to reach into embodied settings.</p>

  <h2 id="insights">What ties it together</h2>
  <ol class="research-insights">
    <li><strong>The strongest model is rarely the best teacher.</strong> Grounded traces beat stronger solvers in Terminal-Lego, stronger teachers cheat more in LegoFlow, and the same mismatch between how strong a teacher is and what a student can learn is behind our work on <a href="{{ '/research/efficient-ml-ai-infrastructure/#transfer' | relative_url }}">matching each prompt to the right teacher</a>. What transfers is behavior the student can see and copy.</li>
    <li><strong>Checking is the scarce resource.</strong> Verified tasks, verifiers that rank attempts, reviewers that diagnose patches, CI-based arenas: they're all ways of producing judgments we can trust. Generating attempts is cheap. Choosing between them reliably is what scales.</li>
    <li><strong>The trainer has to see what the agent actually did.</strong> If the tokens, probabilities or routing used for training differ from what happened, learning quietly optimizes the wrong thing. In agent RL, you can't separate the systems work from the learning.</li>
    <li><strong>Stronger agents find more shortcuts.</strong> Git history, upstream patches, visual questions you can answer from text alone: capable models find these more often. Honesty has to be built into the environment and the benchmark; a line in the prompt isn't enough.</li>
    <li><strong>Depth beats coverage.</strong> Thinking hard where it's needed beats thinking a little everywhere. A useful reflection beats a long one. And long chains of thought have a real cost; they aren't free.</li>
  </ol>

  <h2 id="open-questions">Open questions</h2>
  <ul>
    <li>Can an agent trained on several harnesses do well in one it has never seen?</li>
    <li>When a single pass or fail arrives after dozens of actions, how do we tell which actions actually helped?</li>
    <li>What changes when an agent has to ask the user questions and go back and forth, instead of closing a ticket on its own?</li>
    <li>Can supervised and reinforcement signals be combined so that their benefits add up instead of trading off?</li>
    <li>How do these lessons carry over to much longer tasks, like building a whole repository from a written specification?</li>
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
