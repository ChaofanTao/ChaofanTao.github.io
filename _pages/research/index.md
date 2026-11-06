---
layout: default
title: "Research"
description: "Research notes by Chaofan Tao on agents that work with users over long projects, and the learning, evaluation and infrastructure needed to make that practical."
permalink: /research/
research_lang: en
last_modified_at: 2026-11-06
og_image: /assets/img/og-image.png
about:
  - Agentic intelligence
  - Coding agents
  - Efficient machine learning
  - AI infrastructure
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
  <p class="research-lead">I want agents to grow from fixing one issue to working with a user on a whole project: understanding requirements, building and checking the result, and continuing when those requirements change. That calls for reliable learning and evaluation, together with affordable training and execution.</p>
  <p>These two essays connect research by my collaborators and me with our open-source work at <a href="https://www.legox.net/">LegoX</a>. I explain the questions behind the projects, what the experiments taught us, and what remains unresolved. Links to papers, code and data sit alongside the discussion so the evidence is easy to follow.</p>

  <div class="research-cards">
    <article class="research-card">
      <h2><a href="{{ '/research/agentic-intelligence/' | relative_url }}">Agentic Coding, Reasoning and Evaluation</a></h2>
      <p>From data, training and evaluation to agents that understand changing requirements, collaborate with users and sustain work on complete projects.</p>
    </article>
    <article class="research-card">
      <h2><a href="{{ '/research/efficient-ml-ai-infrastructure/' | relative_url }}">Efficient ML &amp; AI Infrastructure</a></h2>
      <p>From vocabulary, compression and caches to training and serving: the trade-offs between compute, user time and rework over long projects.</p>
    </article>
  </div>

  <p>All {{ site.data.homepage.publications.size }} publications, with English and Chinese summaries, are on the <a href="{{ '/#all-publications' | relative_url }}">homepage</a>.</p>
</div>
