---
layout: default
title: "Multimodal Reasoning and Agents"
description: "Chaofan Tao's research on multimodal LLMs: RL and long-CoT post-training for reasoning VLMs, physical reasoning benchmarks, multimodal browsing agents, and code generation for robots."
permalink: /research/multimodal-reasoning/
research_lang: en
last_modified_at: 2026-11-03
og_image: /assets/img/og-image.png
about:
  - Multimodal large language models
  - Vision-language models
  - Multimodal reasoning
  - Reinforcement learning for VLMs
  - Physical reasoning
  - Multimodal search agents
  - Embodied AI
faq:
  - q: "Does combining long chain-of-thought SFT and RL help reasoning VLMs?"
    a: "Not additively. The Synergy Dilemma study (TMLR 2025) finds that long-CoT SFT helps on hard questions but adds verbosity and hurts easy ones, while RL improves all difficulty levels and shortens answers. Two-stage, interleaved and progressive training, data mixing and model merging all trade off accuracy, reasoning style and length instead of adding the benefits."
  - q: "What is PhyX?"
    a: "PhyX is a benchmark of 3K multimodal questions on physics-grounded reasoning, covering 6 physics domains and 25 sub-domains. GPT-4o, Claude 3.7 Sonnet and o4-mini reach 32.5%, 42.2% and 45.8%, more than 29 points below human experts."
  - q: "What is MMSearch-Plus?"
    a: "MMSearch-Plus is a 311-task benchmark for multimodal browsing agents that requires extracting fine-grained visual cues and cross-validating them through image and text search. The strongest system reaches 36.0% end-to-end accuracy, and the set-of-mark module adds up to 3.9 points."
  - q: "Does Chaofan Tao work on embodied AI?"
    a: "His main focus is coding agents and efficient LLMs. Embodied-related contributions include RoboCodeX (ICML 2024), a multimodal code generation framework for robotic behavior synthesis evaluated in simulation and on real robots, and PhyX, a physical reasoning benchmark for multimodal models."
---

{% include research/styles.liquid %}
{% include research/jsonld.liquid topic="multimodal" %}

<div class="research-page">
  <nav class="research-breadcrumb" aria-label="Breadcrumb">
    <a href="{{ '/' | relative_url }}">Chaofan Tao</a><span aria-hidden="true">/</span>
    <a href="{{ '/research/' | relative_url }}">Research</a><span aria-hidden="true">/</span>
    <span>Multimodal reasoning</span>
    <span aria-hidden="true">·</span><a href="{{ '/zh/research/multimodal-reasoning/' | relative_url }}" lang="zh-Hans">中文版</a>
  </nav>

  <h1>Multimodal Reasoning and Agents</h1>
  <p class="research-meta">By <a href="{{ '/' | relative_url }}">Chaofan Tao (陶超凡)</a> · Last updated <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%B %-d, %Y" }}</time></p>

  <p class="research-lead"><strong>This work studies how vision-language models reason, search and act.</strong> It covers reflection-aware RL for multimodal reasoning (SRPO), the interplay of long chain-of-thought SFT and RL in reasoning VLMs, physics-grounded evaluation (PhyX), provenance-aware multimodal browsing agents (MMSearch-Plus), compositional video-language understanding (NAVERO), and multimodal code generation for robot behavior (RoboCodeX).</p>

  <h2 id="key-results">Key results</h2>
  <div class="research-table-wrap">
    <table>
      <thead>
        <tr><th>Paper</th><th>Question</th><th>Finding</th></tr>
      </thead>
      <tbody>
        <tr><td><a href="https://arxiv.org/abs/2507.07562">Synergy Dilemma</a> (TMLR 2025)</td><td>Do long-CoT SFT and RL add up for VLMs?</td><td>No: five combination strategies all trade off accuracy, style and length</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2506.01713">SRPO</a> (NeurIPS 2025)</td><td>Can MLLMs learn to self-reflect?</td><td>Two-stage reflection-aware GRPO improves Qwen2.5-VL-7B/32B on MathVista, MathVision, MathVerse and MMMU-Pro</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2505.15929">PhyX</a> (TMLR 2026)</td><td>Can models reason about physics in images?</td><td>3K questions; best models 32.5–45.8%, over 29 points below human experts</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a> (ICLR 2026)</td><td>Can browsing agents use visual evidence?</td><td>311 tasks; best system 36.0%; set-of-mark adds up to 3.9 points</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2402.16117">RoboCodeX</a> (ICML 2024)</td><td>Can code generation drive robot behavior?</td><td>State of the art on four manipulation task types and one navigation task, in simulation and on real robots</td></tr>
      </tbody>
    </table>
  </div>

  <h2 id="sft-rl">Does RL or long-CoT SFT make vision-language models reason better?</h2>
  <p>They help in different places, and combining them does not simply add their gains. Long chain-of-thought SFT improves hard questions through structured reasoning but makes answers verbose and hurts easy questions. RL improves every difficulty level and keeps answers short, with smaller gains on the hardest problems. Two-stage, interleaved and progressive schedules, data mixing and model merging all land on a trade-off instead of a sum, which the paper calls the <a href="https://arxiv.org/abs/2507.07562">synergy dilemma</a>.</p>

  <h2 id="reflection">How can multimodal LLMs learn to self-reflect?</h2>
  <p><a href="https://arxiv.org/abs/2506.01713">SRPO</a> first builds a reflection-focused dataset in which a stronger MLLM critiques initial answers, so the policy learns both reasoning and reflection. It then adds a GRPO reward that favors short, meaningful reflection over redundant self-talk.</p>

  <h2 id="physics">Can multimodal models reason about physics?</h2>
  <p>Not yet at human level. <a href="https://arxiv.org/abs/2505.15929">PhyX</a> spans thermodynamics, electromagnetism, mechanics, modern physics, optics, and waves and acoustics. Failure analysis points to over-reliance on memorized formulas and surface-level visual pattern matching rather than physical understanding.</p>

  <h2 id="search">What makes multimodal search agents fail?</h2>
  <p>Locating the right web page and telling apart visually similar events. <a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a> builds questions whose answers depend on spatial and temporal cues inside an image, and gives agents a set-of-mark tool to crop, zoom and launch targeted searches.</p>

  <h2 id="embodied">From multimodal reasoning to embodied agents</h2>
  <p><a href="https://arxiv.org/abs/2402.16117">RoboCodeX</a> decomposes instructions into object-centric manipulation units with affordance and safety constraints and expresses them as code, which lets one model generalize across robot platforms. PhyX measures the physical reasoning such agents need, and the <a href="https://arxiv.org/abs/2411.05902">survey of autoregressive models in vision</a> (TMLR 2025, about 250 references, <a href="https://github.com/ChaofanTao/Autoregressive-Models-in-Vision-Survey">800+ GitHub stars</a>) covers applications including embodied AI.</p>

  <h2 id="papers">Papers</h2>
  {% include research/paper-list.liquid topic="multimodal" lang="en" %}

  {% include research/faq.liquid %}

  <p>Related: <a href="{{ '/research/coding-agents/' | relative_url }}">Coding agents and agentic RL</a> · <a href="{{ '/research/efficient-llm/' | relative_url }}">Efficient LLM training and inference</a> · <a href="{{ '/llms.txt' | relative_url }}">llms.txt</a></p>
</div>
