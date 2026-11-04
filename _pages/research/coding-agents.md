---
layout: default
title: "Coding Agents, Agentic Data and Agentic RL"
description: "How Chaofan Tao and collaborators at LegoX build open coding agents end to end: verified tasks, trustworthy trajectories and rewards, fine-tuning, harness-native RL, and agentic code review."
permalink: /research/coding-agents/
research_lang: en
last_modified_at: 2026-11-04
og_image: /assets/img/og-image.png
about:
  - Coding agents
  - Software engineering agents
  - Agentic reinforcement learning
  - Agentic data
  - Reward hacking
  - Code review agents
---

{% include research/styles.liquid %}
{% include research/jsonld.liquid topic="coding-agents" %}

<div class="research-page">
  <nav class="research-breadcrumb" aria-label="Breadcrumb">
    <a href="{{ '/' | relative_url }}">Chaofan Tao</a><span aria-hidden="true">/</span>
    <a href="{{ '/research/' | relative_url }}">Research</a><span aria-hidden="true">/</span>
    <span>Coding agents</span>
    <span aria-hidden="true">·</span><a href="{{ '/zh/research/coding-agents/' | relative_url }}" lang="zh-Hans">中文版</a>
  </nav>

  <h1>Coding Agents, Agentic Data and Agentic RL</h1>
  <p class="research-meta">By <a href="{{ '/' | relative_url }}">Chaofan Tao (陶超凡)</a>, LegoX · Last updated <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%B %-d, %Y" }}</time></p>

  <p class="research-lead"><strong>A coding agent is more than a model.</strong> Its behavior also depends on the harness that manages its tools and context, the tasks it learns from, and the reward that tells it whether it succeeded. Most strong agents are built with pipelines in which these pieces are tightly coupled and rarely released. Chaofan Tao and collaborators at <a href="https://www.legox.net/">LegoX</a> take that pipeline apart into open, reusable blocks (task construction, trajectory curation, fine-tuning, harness-native reinforcement learning and review) and document what each block teaches about building reliable coding agents.</p>

  <p class="research-toc">On this page: <a href="#why">Why open</a> · <a href="#tasks">Verified tasks</a> · <a href="#trajectories">Trajectories and rewards</a> · <a href="#sft">Fine-tuning</a> · <a href="#rl">RL in the native harness</a> · <a href="#review">Review and evaluation</a> · <a href="#resources">Open resources</a></p>

  <h2 id="why">Why build coding agents end to end, in the open?</h2>
  <p>Because the pieces interact in ways that only show up when you control all of them. The same model can behave quite differently under different harnesses, a strong teacher can quietly copy answers instead of solving tasks, and a rising reward curve can hide broken infrastructure. LegoX packages each stage as a block with its own code, environment and dashboard, and makes the blocks operable by coding agents themselves: Claude Code or Codex can run them as plugin skills. The goal is a system others can rebuild, audit and extend, rather than a single checkpoint.</p>
  <p class="research-readmore">Read more: <a href="https://www.legox.net/">LegoX</a> · <a href="https://www.legox.net/blog/legoflow/">LegoFlow overview</a></p>

  <h2 id="tasks">Where do verified training tasks come from?</h2>
  <p>From real software history, kept only when execution proves them. LegoFlow's Curator finds merged pull requests, gathers the issue, commits and tests, rewrites them into a task that does not leak the answer, builds an isolated environment in the Harbor task format, and keeps the task only if the original code fails the tests and the reference fix passes. Passing that check shows a task is usable, not that it is worth training on, so Curator also scores difficulty with a static rubric over patch scope, logic complexity, context breadth, test complexity and instruction detail, with no LLM judge involved. SWE-Lego adds synthetic tasks by injecting bugs through LLM rewriting and syntax-tree transformations, and Terminal-Lego turns Stack Overflow problems into sandboxed command-line tasks.</p>
  <p class="research-knowhow-label">Know-how</p>
  <ul class="research-knowhow">
    <li>Only a tiny fraction of raw pull requests survive verification; quality filters matter more than volume.</li>
    <li>Real tasks give depth (realistic, multi-file bugs) and synthetic tasks give breadth. Mixing the two helps more than either alone.</li>
    <li>Harder, multi-file tasks lead teachers to produce longer, richer trajectories, which make better training data.</li>
  </ul>
  <p class="research-readmore">Read more: <a href="https://www.legox.net/blog/legoflow/">LegoFlow</a> · <a href="https://www.legox.net/blog/legoflow-experiments/">Lessons learned from LegoFlow-SWE</a> · <a href="https://www.legox.net/blog/swe-lego/">SWE-Lego</a> · <a href="https://www.legox.net/blog/terminal-lego/">Terminal-Lego</a></p>

  <h2 id="trajectories">Which trajectories are worth learning from, and how do you keep rewards honest?</h2>
  <p>A trajectory is a recorded attempt by a teacher agent, and not every successful one is a good lesson. Three findings shape how LegoX curates them. First, reasoning depth matters more than reasoning coverage: traces that think briefly on every turn teach less than traces that reason in depth when the problem calls for it, and most of the gain comes from removing the shallowest traces. Second, environment-grounded trajectories make better teachers. In the Terminal-Lego study, traces that inspect, act and verify transferred better than those of stronger agents that jump straight to the answer; in the paper's words, “the best solver is the worst teacher.” Third, stronger models are better at hacking: they find the upstream pull request, copy the patch, or compare their change against the reference commit.</p>
  <p class="research-knowhow-label">Know-how</p>
  <ul class="research-knowhow">
    <li>Filter out shallow reasoning traces rather than simply picking the longest ones.</li>
    <li>Clean trajectories before training: remove Git history that reveals the fix, repair malformed tool calls, keep the tool set small, and recycle runs that found the right file but failed to fix it.</li>
    <li>Defend against hacking in two layers: tell the agent not to look up solutions, and enforce it in the environment by rewriting Git history and restricting network access while the agent runs, restoring them only for grading.</li>
  </ul>
  <p class="research-readmore">Read more: <a href="https://www.legox.net/blog/legoflow-experiments/">Lessons learned from LegoFlow-SWE</a> · <a href="https://arxiv.org/abs/2606.03461">What makes interaction trajectories effective</a></p>

  <h2 id="sft">How far can supervised fine-tuning go?</h2>
  <p>Further than its reputation suggests, if the data and the loss are right. SWE-Lego is an SFT-only recipe. Error masking keeps the full trajectory as context but excludes erroneous agent steps from the loss, so the model sees its mistakes without imitating them. A difficulty curriculum uses trajectory length as a proxy for difficulty, since longer trajectories are strongly associated with harder tasks, and trains in stages from easy to hard while carrying earlier data forward to avoid forgetting. At inference time, extra compute is best spent first on more interaction turns and then, once that saturates, on parallel attempts ranked by a verifier.</p>
  <p class="research-knowhow-label">Know-how</p>
  <ul class="research-knowhow">
    <li>Mask the loss on wrong steps instead of throwing away imperfect trajectories.</li>
    <li>A generative verifier, which answers “yes” or “no” as text, ranks attempts better than a regression head because it reuses what the model learned in pre-training.</li>
  </ul>
  <p class="research-readmore">Read more: <a href="https://www.legox.net/blog/swe-lego/">SWE-Lego overview</a> · <a href="https://arxiv.org/abs/2601.01426">paper</a></p>

  <h2 id="rl">Why train reinforcement learning inside the agent's native harness?</h2>
  <p>Because the harness is part of the environment the model learns from. Lego-RL connects unmodified harnesses such as OpenHands, Claude Code and OpenCode to a policy-gradient trainer without changing their control flow. The hard part is faithfulness. Harnesses rewrite their own history by compacting context, re-serializing tool calls and running sub-agents, so a saved transcript is not the token sequence the model actually sampled. An in-process proxy records tokens, log-probabilities and mixture-of-experts routing at generation time, and the routing is replayed during training so that both sides compute the same probabilities. Each attempt runs in its own sandbox with phase-dependent anti-cheating defenses, and dashboards make every trajectory inspectable.</p>
  <p class="research-knowhow-label">Know-how</p>
  <ul class="research-knowhow">
    <li>Check token and probability alignment explicitly; misalignments are silent bugs that look like normal training.</li>
    <li>Train on tasks the current policy solves only sometimes. Groups that always pass or always fail give no learning signal, and the useful band shifts as the policy improves.</li>
    <li>Separate policy failures from infrastructure failures, such as tool-call parser mismatches or environment setup errors, before reading a reward curve.</li>
    <li>After training, agents inspect more files before editing, reread their edits and run tests more often, at the cost of longer interactions.</li>
  </ul>
  <p>The same infrastructure supports newer recipes. Mixed-harness RL trains one model that works across several harnesses instead of one model per harness, and Single-Rollout Asynchronous Optimization (SAO) learns from a single attempt per task with a learned critic, which needs warm-up and advantage whitening to stay stable.</p>
  <p class="research-readmore">Read more: <a href="https://www.legox.net/blog/lego-rl/">Lego-RL</a> · <a href="https://www.legox.net/blog/lego-rl-cross-harness/">RL across harnesses</a> · <a href="https://www.legox.net/blog/lego-rl-sao/">Single-rollout optimization</a> · <a href="https://arxiv.org/abs/2608.17393">paper</a></p>

  <h2 id="review">How should coding agents be reviewed and evaluated?</h2>
  <p>Like human software work: with review, iteration and realistic checks. SWE-Review adds the missing second half of the loop. A reviewer agent explores the repository on its own, traces the root cause, compares its diagnosis with the submitted patch and returns structured feedback, turning one-shot generation into a generate-review-revise loop. Review trajectories also transfer back to issue resolution, and because choosing among attempts is cheaper than generating more of them, review makes test-time scaling more efficient. For evaluation, <a href="https://arxiv.org/abs/2505.23932">SwingArena</a> (ICLR Oral) has models compete as patch submitters and test-writing reviewers in continuous-integration pipelines, <a href="https://arxiv.org/abs/2604.06861">REAgent</a> (ICSE) checks and refines the issue as a requirement before patching, and <a href="https://arxiv.org/abs/2601.18533">RLVRR</a> (ICLR) extends verifiable rewards beyond code to open-ended generation.</p>
  <p class="research-readmore">Read more: <a href="https://www.legox.net/blog/swe-review/">SWE-Review</a> · <a href="https://arxiv.org/abs/2607.06065">paper</a></p>

  <h2 id="resources">Open resources</h2>
  <ul>
    <li>LegoFlow: <a href="https://github.com/LegoX/LegoFlow">code</a> · <a href="https://huggingface.co/collections/Lego-X/legoflow">data</a></li>
    <li>SWE-Lego: <a href="https://github.com/LegoX/SWE-Lego">code</a> · <a href="https://huggingface.co/collections/Lego-X/swe-lego">data and models</a></li>
    <li>Terminal-Lego: <a href="https://github.com/LegoX/Terminal-Lego">code</a> · <a href="https://huggingface.co/datasets/SWE-Lego/Terminal-Lego-15k">data</a></li>
    <li>Lego-RL: <a href="https://github.com/LegoX/Lego-RL">code</a> · <a href="https://huggingface.co/collections/Lego-X/lego-rl">models and data</a></li>
    <li>SWE-Review: <a href="https://github.com/LegoX/SWE-Review">code</a> · <a href="https://huggingface.co/collections/Lego-X/swe-review">models and data</a></li>
  </ul>

  {% include research/paper-list.liquid topic="coding-agents" lang="en" %}

  <details class="research-more">
    <summary>How to cite</summary>
<pre><code>@article{tao2026swelego,
  title   = {SWE-Lego: Pushing the Limits of Supervised Fine-tuning for Software Issue Resolving},
  author  = {Tao, Chaofan and Chen, Jierun and Jiang, Yuxin and Kou, Kaiqi and Wang, Shaowei and Wang, Ruoyu and Li, Xiaohui and Yang, Sidi and Du, Yiming and Dai, Jianbo and Mao, Zhiming and Wang, Xinyu and Shang, Lifeng and Bai, Haoli},
  journal = {arXiv preprint arXiv:2601.01426},
  year    = {2026}
}

@article{du2026legorl,
  title   = {LEGO-RL: Harness-Native Reinforcement Learning for Coding Agents},
  author  = {Du, Yiming and Jiang, Yuxin and Yuan, Tao and Dai, Jianbo and Wang, Shaowei and Chen, Jierun and Tao, Chaofan and Yu, Xianzhi and Shang, Lifeng and Wong, Kam-Fai and Li, Xiaohui and Bai, Haoli},
  journal = {arXiv preprint arXiv:2608.17393},
  year    = {2026}
}

@article{yang2026interactiontrajectories,
  title   = {What Makes Interaction Trajectories Effective for Training Terminal Agents?},
  author  = {Yang, Sidi and Tao, Chaofan and Chen, Jierun and Yu, Tiezheng and Wang, Ruoyu and Jiang, Yuxin and Du, Yiming and Xu, Wendong and Xiong, Jing and Wu, Taiqiang and Shang, Lifeng and Li, Xiaohui and Wong, Ngai and Bai, Haoli},
  journal = {arXiv preprint arXiv:2606.03461},
  year    = {2026}
}</code></pre>
  </details>

  <p>Related: <a href="{{ '/research/efficient-llm/' | relative_url }}">Efficient LLM training and inference</a> · <a href="{{ '/research/multimodal-reasoning/' | relative_url }}">Multimodal reasoning and agents</a></p>
</div>
