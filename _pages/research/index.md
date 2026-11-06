---
layout: default
title: "Research"
description: "Research by Chaofan Tao across efficient machine learning, multimodal reasoning and agents, with open questions about multi-agent systems, AI for AI and recursive self-improvement."
permalink: /research/
research_lang: en
last_modified_at: 2026-11-06
og_image: /assets/img/og-image.png
about:
  - Agentic intelligence
  - Coding agents
  - Efficient machine learning
  - AI infrastructure
  - Multi-agent systems
  - AI for AI
  - Recursive self-improvement
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
  <p class="research-lead">My research asks how agents can understand their environment, learn from acting in it, and become more capable of autonomous exploration. Further questions follow: can multiple agents work together on complex problems, and can AI help improve models, learning methods and the research process itself?</p>
  <p>The work here spans different stages of my research and different collaborations: model compression and efficient learning, multimodal reasoning, robotics, and agent data, training and evaluation. Recent open-source projects at <a href="https://www.legox.net/">LegoX</a> form one part of that history. These essays connect the findings with open questions about multi-agent systems, AI for AI and recursive self-improvement.</p>

  <div class="research-cards">
    <article class="research-card">
      <h2><a href="{{ '/research/agentic-intelligence/' | relative_url }}">Agentic Intelligence</a></h2>
      <p>Learning from interaction and multimodal evidence, verifying outcomes, coordinating multiple agents, and exploring how AI could contribute to its own improvement.</p>
    </article>
    <article class="research-card">
      <h2><a href="{{ '/research/efficient-ml-ai-infrastructure/' | relative_url }}">Efficient ML &amp; AI Infrastructure</a></h2>
      <p>From compression, vocabulary and distillation to caches, training and serving: how limited resources can support more useful learning and autonomous exploration.</p>
    </article>
  </div>

  <p>All {{ site.data.homepage.publications.size }} publications, with English and Chinese summaries, are on the <a href="{{ '/#all-publications' | relative_url }}">homepage</a>.</p>
</div>
