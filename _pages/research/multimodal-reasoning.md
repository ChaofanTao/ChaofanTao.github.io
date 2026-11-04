---
layout: default
title: "Multimodal Reasoning and Agents"
description: "Chaofan Tao's research on multimodal LLMs: post-training insights for reasoning VLMs, self-reflection, benchmarks for physical reasoning and multimodal search, and code generation for robots."
permalink: /research/multimodal-reasoning/
research_lang: en
last_modified_at: 2026-11-04
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
  - q: "Should reasoning VLMs be trained with long chain-of-thought SFT or with RL?"
    a: "They help in different places. Long chain-of-thought SFT helps on hard problems but makes answers verbose and can hurt easy ones, while RL improves more broadly and keeps answers concise. Combining them through staged, interleaved or progressive training, data mixing or model merging tends to trade one benefit for another rather than add them up, which the paper calls the synergy dilemma."
  - q: "What is PhyX?"
    a: "PhyX is a benchmark for physics-grounded reasoning in images across six physics domains. It shows that current multimodal models lean on memorized formulas and surface visual patterns rather than physical understanding, and remain well below human experts."
  - q: "What is MMSearch-Plus?"
    a: "MMSearch-Plus is a benchmark and agent framework for multimodal browsing, where answers depend on fine-grained visual cues that must be cross-checked through image and text search. It provides a set-of-mark tool that lets agents crop, zoom and launch targeted searches."
  - q: "Does Chaofan Tao work on embodied AI?"
    a: "His main focus is coding agents and efficient LLMs. Embodied-related contributions include RoboCodeX (ICML), which generates robot behavior as code from multimodal input, and PhyX, a benchmark for the physical reasoning such agents need."
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

  <p class="research-lead"><strong>This work studies how vision-language models reason, search and act, and builds the evaluations that show where they still fall short.</strong> The contributions are post-training insights for reasoning models, a method for teaching self-reflection, benchmarks that expose real gaps, and a step from multimodal reasoning toward embodied agents.</p>

  <ul class="research-highlights">
    <li><strong>Post-training insight</strong>When long chain-of-thought SFT helps, when RL helps, and why combining them is hard.</li>
    <li><strong>Self-reflection</strong>Teaching multimodal models to check and correct their own reasoning.</li>
    <li><strong>Evaluations that expose gaps</strong>Physical reasoning in images, and search that must rely on visual evidence.</li>
    <li><strong>Toward embodied agents</strong>Turning instructions and perception into robot behavior expressed as code.</li>
  </ul>

  <h2 id="sft-rl">Should reasoning VLMs be trained with long-CoT SFT or with RL?</h2>
  <p>It depends on what you need, and combining them is harder than it looks. Fine-tuning on long chains of thought helps on hard problems but makes answers verbose and can hurt easy ones; RL improves more broadly and keeps answers concise. Staged, interleaved and progressive training, data mixing and model merging all tend to trade one benefit for another rather than add them up. The <a href="https://arxiv.org/abs/2507.07562">synergy dilemma</a> study maps these trade-offs so practitioners can choose by target difficulty and answer-length budget.</p>

  <h2 id="reflection">How can multimodal models learn to reflect?</h2>
  <p>By learning from good reflections first, then being rewarded for useful ones. <a href="https://arxiv.org/abs/2506.01713">SRPO</a> (NeurIPS) builds a reflection-focused dataset in which a stronger model critiques initial answers, so the policy learns both to reason and to reflect. RL then rewards reflection that is short and meaningful, and discourages redundant self-talk.</p>

  <h2 id="gaps">Where do multimodal models still fall short?</h2>
  <p>In physical understanding and in using visual evidence. <a href="https://arxiv.org/abs/2505.15929">PhyX</a> tests physics-grounded reasoning in images across six physics domains and finds that models lean on memorized formulas and surface patterns. <a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a> (ICLR) asks questions whose answers depend on fine-grained visual cues that must be cross-checked through search; the most common failures are finding the right page and telling apart visually similar events. <a href="https://arxiv.org/abs/2408.09511">NAVERO</a> targets fine-grained compositional understanding in video-language models.</p>

  <h2 id="embodied">From multimodal reasoning to embodied agents</h2>
  <p><a href="https://arxiv.org/abs/2402.16117">RoboCodeX</a> (ICML) breaks a human instruction into object-centric manipulation steps with affordance and safety constraints and expresses them as code, which lets one model generalize across robot platforms. The <a href="https://arxiv.org/abs/2411.05902">survey of autoregressive models in vision</a> (TMLR, with a widely used <a href="https://github.com/ChaofanTao/Autoregressive-Models-in-Vision-Survey">paper list on GitHub</a>) covers applications including embodied AI. For efficient vision-language Transformers, see token ensembling (<a href="https://arxiv.org/abs/2305.17455">CrossGET</a>) and progressive pruning (<a href="https://arxiv.org/abs/2301.13741">UPop</a>).</p>

  {% include research/paper-list.liquid topic="multimodal" lang="en" %}

  {% include research/faq.liquid %}

  <p>Related: <a href="{{ '/research/coding-agents/' | relative_url }}">Coding agents and agentic RL</a> · <a href="{{ '/research/efficient-llm/' | relative_url }}">Efficient LLM training and inference</a></p>
</div>
