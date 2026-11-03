---
layout: default
title: "Coding Agents, Agentic Data and Agentic RL"
description: "Chaofan Tao's open research on LLM coding agents at LegoX: verified SWE task construction, SFT recipes, terminal-agent trajectories, and RL inside Claude Code, OpenHands and OpenCode."
permalink: /research/coding-agents/
research_lang: en
last_modified_at: 2026-11-03
og_image: /assets/img/og-image.png
about:
  - Coding agents
  - Software engineering agents
  - SWE-bench
  - Agentic reinforcement learning
  - Terminal agents
  - Agentic data
faq:
  - q: "What is SWE-Lego?"
    a: "SWE-Lego is a supervised fine-tuning recipe for software issue resolution by Chaofan Tao and collaborators. It combines a dataset of 32k task instances and 18k validated trajectories with error masking and a difficulty-based curriculum. SWE-Lego-Qwen3-8B and SWE-Lego-Qwen3-32B reach 42.2% and 52.6% on SWE-bench Verified with SFT only, and 49.6% and 58.8% with verifier-based test-time scaling (TTS@16), evaluated without Git hacking."
  - q: "What is Lego-RL?"
    a: "Lego-RL is a harness-native reinforcement learning framework for coding agents from LegoX. It trains a policy inside an unmodified agent harness (OpenHands SDK, Claude Code or OpenCode) while preserving token-level fidelity and MoE rollout-routing replay. Starting from Qwen3.5-35B-A3B, one training run per harness improves SWE-bench Verified from 64.0, 62.4 and 57.2 to 70.4, 68.2 and 66.6."
  - q: "Are the LegoX datasets, models and code open source?"
    a: "Yes. Code is on GitHub (LegoX/SWE-Lego, LegoX/LegoFlow, LegoX/Lego-RL, SWE-Lego/terminal-lego), and datasets and models are on Hugging Face under the Lego-X and SWE-Lego organizations, including LegoFlow-SWE and Terminal-Lego-15k."
  - q: "Do stronger coding agents make better teachers for distillation?"
    a: "Not necessarily. In the Terminal-Lego study, Claude Opus 4.6 scores 69.4 on Terminal-Bench 2.0 but its trajectories train weaker Qwen3 students than those of DeepSeek-V3.2 (39.3). Trajectories that visibly inspect, act and verify through the harness transfer best, a property the paper calls environment-grounded supervision."
  - q: "How can I collaborate with Chaofan Tao or apply for an internship?"
    a: "Use the Email me button in the contact section of chaofantao.top, put [Interest] in the subject, and include a short introduction and one or two links to your work such as a paper, GitHub repository, blog or demo."
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

  <p class="research-lead"><strong>Chaofan Tao builds open training recipes for LLM software-engineering and terminal agents at <a href="https://www.legox.net/">LegoX</a>.</strong> The work covers the full loop: verified tasks mined from real GitHub pull requests (LegoFlow), supervised fine-tuning with error masking and a difficulty curriculum (SWE-Lego), environment-grounded trajectories for terminal agents (Terminal-Lego), and reinforcement learning inside unmodified agent harnesses such as OpenHands, Claude Code and OpenCode (Lego-RL). Code, data and models are open.</p>

  <h2 id="key-results">Key results</h2>
  <div class="research-table-wrap">
    <table>
      <thead>
        <tr><th>Project</th><th>Model and setting</th><th>Benchmark</th><th>Result</th><th>Source</th></tr>
      </thead>
      <tbody>
        <tr><td>Lego-RL</td><td>Qwen3.5-35B-A3B, one RL run per harness</td><td>SWE-bench Verified</td><td>OpenHands SDK 64.0 → 70.4<br>Claude Code 62.4 → 68.2<br>OpenCode 57.2 → 66.6</td><td><a href="https://www.legox.net/blog/lego-rl/">Blog</a></td></tr>
        <tr><td>LegoFlow</td><td>Qwen3.5-35B-A3B-Base, two agent-managed iterations, 512 trajectories</td><td>SWE-bench Verified</td><td>7.6% → 64.4%</td><td><a href="https://www.legox.net/blog/legoflow/">Blog</a></td></tr>
        <tr><td>LegoFlow-SWE</td><td>Qwen3.5-35B-A3B-Base, about 1K trajectories</td><td>SWE-bench Verified / Pro / Multilingual</td><td>70.2% / 48.8% / 57.0%</td><td><a href="https://www.legox.net/blog/legoflow/">Blog</a></td></tr>
        <tr><td>SWE-Lego</td><td>Qwen3-8B / Qwen3-32B, SFT only, hack-free evaluation</td><td>SWE-bench Verified</td><td>42.2% / 52.6%<br>TTS@16: 49.6% / 58.8%</td><td><a href="https://arxiv.org/abs/2601.01426">arXiv:2601.01426</a></td></tr>
        <tr><td>Terminal-Lego</td><td>Qwen3-32B, 15.3k trajectories</td><td>Terminal-Bench 2.0</td><td>24.3%, with about 30× less data than prior results</td><td><a href="https://arxiv.org/abs/2606.03461">arXiv:2606.03461</a></td></tr>
      </tbody>
    </table>
  </div>

  <h2 id="verified-tasks">How do you build verified coding-agent tasks at scale?</h2>
  <p>A task is only useful for training if the environment can prove it: the buggy version must fail the tests and the reference fix must pass them. LegoFlow's Curator block discovers merged pull requests, rewrites each one as a leak-free task, assembles it in the Harbor task format with an isolated environment, and keeps it only after this fail-then-pass check. Every block (Curator, Tracer, Trainer, Evaluator) is packaged as a plugin skill that a coding agent such as Claude Code or Codex can run.</p>
  <p>For the LegoFlow-SWE release, filtering started from more than 700K repositories and 12M candidate pull requests and kept 5,000 verified tasks across 8 programming languages and 20 task tags, or 0.0417% of the pool. GLM-5.2 produced 9,767 rollouts, of which 2,780 passed verification. Under the same teacher, scaffold and budget, LegoFlow-SWE beats SWE-rebench-v2 by 5.8, 1.9 and 1.0 points on SWE-bench Verified, Pro and Multilingual.</p>

  <h2 id="sft">Can supervised fine-tuning alone produce a strong SWE agent?</h2>
  <p>Yes, for open models of 8B to 32B parameters. SWE-Lego combines 32k executable task instances and 18k validated trajectories from real and synthetic sources, masks erroneous steps during training, and orders data by difficulty. In the ablation, the dataset adds 25.6 points, refined SFT adds 3.8, and test-time scaling with a trained verifier adds 6.2, lifting Qwen3-32B from 23.2% to 58.8% on SWE-bench Verified. Trajectories that recover solutions from Git history are filtered out, and results are reported on hack-free images.</p>

  <h2 id="harness-native-rl">Why train RL inside the agent's native harness?</h2>
  <p>Because the harness changes what the model learns from. The same Qwen3.5-35B-A3B checkpoint scores 64.0, 62.4 and 57.2 on SWE-bench Verified under OpenHands SDK, Claude Code and OpenCode, a 6.8-point spread from the harness alone. Lego-RL trains inside each harness without changing its control flow, keeps token-in/token-out fidelity and history alignment, and replays MoE routing from rollout. Train/inference sampled-token probabilities correlate at r ≥ 0.998, and asynchronous training runs 2.5× faster than synchronous (about 1.9× after compute-throughput correction).</p>
  <p>All three runs use the same 2,699 tasks and a 200k context budget for 126 steps. In sampled OpenHands SDK trajectories, the share of runs that reread an edited file rose from 73.6% to 98.1% after training.</p>

  <h2 id="teachers">Do stronger agents make better teachers?</h2>
  <p>No. In the Terminal-Lego study, Claude Opus 4.6 is the strongest solver on Terminal-Bench 2.0 (69.4), yet Qwen3-8B and Qwen3-32B students trained on its trajectories reach only 5.6 and 15.5. Students trained on DeepSeek-V3.2 (39.3) reach 10.5 and 20.6. The difference follows the share of actions backed by a relevant prior observation, not the teacher's score.</p>
  <blockquote>“The best solver is the worst teacher.” — <a href="https://www.legox.net/blog/terminal-lego/">LegoX, Terminal-Lego</a></blockquote>
  <p>Terminal-Lego turns Stack Overflow problems into more than 15,000 Docker-verified terminal tasks across 90+ technical domains in 13 categories.</p>

  <h2 id="evaluation">How should coding agents be evaluated?</h2>
  <p>Static pass/fail on a fixed set misses how software is actually built. <a href="https://arxiv.org/abs/2505.23932">SwingArena</a> (ICLR 2026 Oral) pairs LLMs as patch submitters and test-writing reviewers inside CI pipelines, over 400+ real GitHub issues in C++, Python, Rust and Go. <a href="https://arxiv.org/abs/2604.06861">REAgent</a> (ICSE 2027) treats the issue text itself as a requirement to be checked and refined before patching, and outperforms five baselines on three benchmarks. RL reward design beyond code is studied in <a href="https://arxiv.org/abs/2601.18533">RLVRR</a> (ICLR 2026), which turns a single verifiable reward into a chain of reference-based rewards.</p>

  <h2 id="resources">Code, data and models</h2>
  <ul>
    <li>LegoFlow: <a href="https://github.com/LegoX/LegoFlow">GitHub</a> · <a href="https://huggingface.co/collections/Lego-X/legoflow">Hugging Face</a> · <a href="https://www.legox.net/blog/legoflow/">overview</a></li>
    <li>Lego-RL: <a href="https://github.com/LegoX/Lego-RL">GitHub</a> · <a href="https://huggingface.co/collections/Lego-X/lego-rl">Hugging Face</a> · <a href="https://www.legox.net/blog/lego-rl/">overview</a></li>
    <li>Terminal-Lego: <a href="https://github.com/SWE-Lego/terminal-lego">GitHub</a> · <a href="https://huggingface.co/datasets/SWE-Lego/Terminal-Lego-15k">Terminal-Lego-15k</a> · <a href="https://www.legox.net/blog/terminal-lego/">overview</a></li>
    <li>SWE-Lego: <a href="https://github.com/LegoX/SWE-Lego">GitHub</a> · <a href="https://arxiv.org/abs/2601.01426">paper</a> · <a href="https://www.legox.net/blog/swe-lego/">overview</a></li>
  </ul>

  <h2 id="papers">Papers</h2>
  {% include research/paper-list.liquid topic="coding-agents" lang="en" %}

  {% include research/faq.liquid %}

  <h2 id="cite">How to cite</h2>
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

  <p>Related: <a href="{{ '/research/efficient-llm/' | relative_url }}">Efficient LLM training and inference</a> · <a href="{{ '/research/multimodal-reasoning/' | relative_url }}">Multimodal reasoning and agents</a> · <a href="{{ '/llms.txt' | relative_url }}">llms.txt</a></p>
</div>
