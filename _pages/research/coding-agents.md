---
layout: default
title: "Coding Agents, Agentic Data and Agentic RL"
description: "Chaofan Tao's open research on training LLM coding agents end to end at LegoX: verified task data, SFT and RL recipes, trajectory know-how, evaluation, and open infrastructure."
permalink: /research/coding-agents/
research_lang: en
last_modified_at: 2026-11-04
og_image: /assets/img/og-image.png
about:
  - Coding agents
  - Software engineering agents
  - Agentic reinforcement learning
  - Terminal agents
  - Agentic data
faq:
  - q: "What is SWE-Lego?"
    a: "SWE-Lego is an open supervised fine-tuning recipe for software issue resolution. It shows that a lightweight SFT-only pipeline can train strong open coding agents when the data is right: real and synthetic tasks combined, erroneous steps masked out, training ordered by difficulty, and trajectories that copy answers from Git history removed."
  - q: "What is Lego-RL?"
    a: "Lego-RL is LegoX's framework for reinforcement learning inside the unmodified agent harness the model will actually run in, such as OpenHands, Claude Code or OpenCode. It keeps the exact tokens generated during rollout, replays mixture-of-experts routing, trains asynchronously, and makes every trajectory inspectable."
  - q: "Are the LegoX datasets, code and models open source?"
    a: "Yes. Code is on GitHub under LegoX and SWE-Lego, and datasets and models are on Hugging Face under the Lego-X and SWE-Lego organizations."
  - q: "Do stronger coding agents make better teachers?"
    a: "Not necessarily. The Terminal-Lego study found that trajectories which visibly inspect the environment, act on what they saw and verify the result teach students best, even when they come from a weaker agent. Strong agents that jump straight to the answer leave little behavior worth imitating."
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

  <p class="research-lead"><strong>Chaofan Tao works on how to train open LLM coding agents end to end, at <a href="https://www.legox.net/">LegoX</a>.</strong> The focus is the part of the stack that usually stays private: where verified training tasks come from, which agent trajectories are worth learning from, how fine-tuning and reinforcement learning fit the agent tools people actually use, and how agents should be evaluated. The outputs are reusable recipes, open data and infrastructure rather than one-off models.</p>

  <ul class="research-highlights">
    <li><strong>Verified data at scale</strong>Real pull requests and community Q&amp;A turned into executable tasks that the environment itself can check.</li>
    <li><strong>Training recipes</strong>Fine-tuning that teaches good debugging habits, and RL that runs inside real agent harnesses.</li>
    <li><strong>Experimental know-how</strong>What makes a trajectory worth imitating, and why the strongest agent is not always the best teacher.</li>
    <li><strong>Open infrastructure</strong>Agent-operable pipelines, sandboxed environments and dashboards, released as code and data.</li>
  </ul>

  <h2 id="why">Why does this matter?</h2>
  <p>Coding agents are now judged by whether they can fix real software, but most strong systems are trained with pipelines that are hard to reproduce: data, environments, training and evaluation are tightly coupled and rarely released. This work breaks that pipeline into reusable blocks, so that others can rebuild, audit and improve each part on its own.</p>

  <h2 id="data">Where does good training data come from?</h2>
  <p>From real software history, checked by execution. <a href="https://www.legox.net/blog/legoflow/">LegoFlow</a> mines merged pull requests and rewrites each one into a self-contained task with its own environment and tests. A task is kept only if the environment proves it: the original code must fail the tests and the reference fix must pass. <a href="https://www.legox.net/blog/terminal-lego/">Terminal-Lego</a> applies the same discipline to command-line work, turning community Q&amp;A into sandboxed tasks.</p>
  <p><strong>Know-how:</strong> only a tiny fraction of raw candidates survive verification, and filtering for verifiability and for real reasoning in the trajectories matters more than collecting more data.</p>

  <h2 id="training">How should coding agents be trained?</h2>
  <p><strong>Fine-tuning.</strong> <a href="https://arxiv.org/abs/2601.01426">SWE-Lego</a> shows that a lightweight, SFT-only recipe can be strong when the data is right: combine real and synthetic tasks, mask erroneous steps so the model does not imitate its mistakes, order training by difficulty, and drop trajectories that peek at Git history for the answer.</p>
  <p><strong>Reinforcement learning.</strong> <a href="https://www.legox.net/blog/lego-rl/">Lego-RL</a> trains inside the unmodified harness the agent will run in, such as OpenHands, Claude Code or OpenCode, because the harness decides what the model sees and does. The engineering that makes this work: keep the exact tokens generated during rollout, replay mixture-of-experts routing, run training asynchronously, and make every trajectory inspectable.</p>

  <h2 id="teachers">What makes a good teacher trajectory?</h2>
  <p>Visible grounding, not raw strength. The Terminal-Lego study found that trajectories which inspect the environment, act on what they saw and then verify the result transfer best to students, while strong agents that jump straight to the answer leave little to learn from.</p>
  <blockquote>“The best solver is the worst teacher.” — <a href="https://www.legox.net/blog/terminal-lego/">LegoX, Terminal-Lego</a></blockquote>
  <p>The practical takeaway is to design the interaction so that the trace contains behavior worth imitating, a shift the paper calls harness engineering.</p>

  <h2 id="evaluation">How should coding agents be evaluated?</h2>
  <p>Closer to how software is actually built. <a href="https://arxiv.org/abs/2505.23932">SwingArena</a> (ICLR Oral) puts models in a continuous-integration loop as both patch submitters and test-writing reviewers across several programming languages. <a href="https://arxiv.org/abs/2604.06861">REAgent</a> (ICSE) treats the issue text as a requirement to check and refine before patching. <a href="https://arxiv.org/abs/2601.18533">RLVRR</a> (ICLR) carries verifiable rewards beyond code to open-ended generation.</p>

  <h2 id="resources">Open code and data</h2>
  <ul>
    <li>LegoFlow: <a href="https://github.com/LegoX/LegoFlow">code</a> · <a href="https://huggingface.co/collections/Lego-X/legoflow">data</a> · <a href="https://www.legox.net/blog/legoflow/">overview</a></li>
    <li>Lego-RL: <a href="https://github.com/LegoX/Lego-RL">code</a> · <a href="https://huggingface.co/collections/Lego-X/lego-rl">models and data</a> · <a href="https://www.legox.net/blog/lego-rl/">overview</a></li>
    <li>Terminal-Lego: <a href="https://github.com/SWE-Lego/terminal-lego">code</a> · <a href="https://huggingface.co/datasets/SWE-Lego/Terminal-Lego-15k">data</a> · <a href="https://www.legox.net/blog/terminal-lego/">overview</a></li>
    <li>SWE-Lego: <a href="https://github.com/LegoX/SWE-Lego">code</a> · <a href="https://arxiv.org/abs/2601.01426">paper</a> · <a href="https://www.legox.net/blog/swe-lego/">overview</a></li>
  </ul>

  {% include research/paper-list.liquid topic="coding-agents" lang="en" %}

  {% include research/faq.liquid %}

  <details class="research-more">
    <summary>How to cite</summary>
<pre><code>@article{tao2026swelego,
  title   = {SWE-Lego: Pushing the Limits of Supervised Fine-tuning for Software Issue Resolving},
  author  = {Tao, Chaofan and Chen, Jierun and Jiang, Yuxin and Kou, Kaiqi and Wang, Shaowei and Wang, Ruoyu and Li, Xiaohui and Yang, Sidi and Du, Yiming and Dai, Jianbo and Mao, Zhiming and Wang, Xinyu and Shang, Lifeng and Bai, Haoli},
  journal = {arXiv preprint arXiv:2601.01426},
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
