---
layout: default
title: "Research"
description: "Research overviews by Chaofan Tao (陶超凡): training open LLM coding agents, efficient LLM training and inference, and multimodal reasoning and agents."
permalink: /research/
research_lang: en
last_modified_at: 2026-11-04
og_image: /assets/img/og-image.png
about:
  - Large language models
  - Coding agents
  - Efficient LLMs
  - Multimodal LLMs
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
  <p class="research-lead"><strong>Chaofan Tao (陶超凡) is an AI researcher at <a href="https://www.legox.net/">LegoX</a> and Huawei Foundation Model Lab.</strong> His research spans three connected areas: training open LLM coding agents end to end, making LLMs cheaper to train and serve, and improving how multimodal models reason and act. He received his PhD from The University of Hong Kong, and his work on generative model quantization received an ACL 2022 Outstanding Paper Award.</p>

  <div class="research-cards">
    <article class="research-card">
      <h2><a href="{{ '/research/coding-agents/' | relative_url }}">Coding agents and agentic RL</a></h2>
      <p>Verified task data from real software history, fine-tuning and RL recipes that fit real agent tools, and know-how on which trajectories are worth learning from.</p>
    </article>
    <article class="research-card">
      <h2><a href="{{ '/research/efficient-llm/' | relative_url }}">Efficient LLM training and inference</a></h2>
      <p>Choosing vocabulary size, compressing generative models, cheaper long-context inference, and faster reasoning-time compute.</p>
    </article>
    <article class="research-card">
      <h2><a href="{{ '/research/multimodal-reasoning/' | relative_url }}">Multimodal reasoning and agents</a></h2>
      <p>Post-training insights for reasoning VLMs, self-reflection, benchmarks that expose real gaps, and code generation for robots.</p>
    </article>
  </div>

  <p>All {{ site.data.homepage.publications.size }} publications, with English and Chinese summaries, are on the <a href="{{ '/#all-publications' | relative_url }}">homepage</a>.</p>
</div>
