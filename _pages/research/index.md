---
layout: default
title: "Research"
description: "Research by Chaofan Tao (陶超凡) in two themes: agentic intelligence, from multimodal reasoning to coding agents built in the open at LegoX; and efficient ML and AI infrastructure, from model compression to systems for training agents."
permalink: /research/
research_lang: en
last_modified_at: 2026-11-09
og_image: /assets/img/og-image.png
about:
  - Agentic intelligence
  - Coding agents
  - Efficient machine learning
  - AI infrastructure
  - Multi-agent systems
  - AI for AI
---

{% include research/styles.liquid %}
{% include research/jsonld.liquid %}

<div class="research-page">
  <nav class="research-breadcrumb" aria-label="Breadcrumb">
    <a href="{{ '/' | relative_url }}">Chaofan Tao</a><span aria-hidden="true">/</span>
    <span>Research</span>
    <span aria-hidden="true">·</span><a href="{{ '/zh/research/' | relative_url }}" lang="zh-Hans">中文版</a>
  </nav>

  <h1>Research</h1>
  <p class="research-lead">I study how AI systems can see what matters, act on it, learn from the result and be trusted, and how to make all of that affordable. My work has moved from compressing and scaling language models, through multimodal reasoning, to coding agents that we build in the open at <a href="https://www.legox.net/">LegoX</a>. The two essays below walk through that work and say where I think it leads: longer tasks, teams of agents, trustworthy evaluation, AI that helps improve AI, and the infrastructure that agentic data now demands.</p>

  <div class="research-cards">
    <article class="research-card">
      <h2><a href="{{ '/research/agentic-intelligence/' | relative_url }}">Agentic Intelligence</a></h2>
      <p>Multimodal reasoning, then coding agents as a laboratory: verified experience, SFT and RL inside real harnesses, and agentic review. My views on long-horizon memory, multi-agent collaboration, evaluation and AI for AI.</p>
    </article>
    <article class="research-card">
      <h2><a href="{{ '/research/efficient-ml-ai-infrastructure/' | relative_url }}">Efficient ML &amp; AI Infrastructure</a></h2>
      <p>Quantization and pruning, vocabulary scaling, KV caches, fast test-time scaling, distillation and resilient systems. My views on infrastructure for large-scale agentic data and measuring efficiency per trajectory.</p>
    </article>
  </div>

  <p>All {{ site.data.homepage.publications.size }} publications, with English and Chinese summaries, are on the <a href="{{ '/#all-publications' | relative_url }}">homepage</a>.</p>
</div>
