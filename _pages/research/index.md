---
layout: default
title: "Research"
description: "Research by Chaofan Tao (陶超凡) in two themes: agentic coding, reasoning and evaluation; and efficient ML and AI infrastructure."
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
  <p class="research-lead"><strong>Chaofan Tao (陶超凡) is an AI researcher at <a href="https://www.legox.net/">LegoX</a> and Huawei Foundation Model Lab.</strong> His research follows two connected themes: how agents learn from acting in real environments and how to evaluate them, and how to make models cheaper to build, train and serve. He received his PhD from The University of Hong Kong, and his work on generative model quantization received an ACL 2022 Outstanding Paper Award.</p>

  <div class="research-cards">
    <article class="research-card">
      <h2><a href="{{ '/research/agentic-intelligence/' | relative_url }}">Agentic Coding, Reasoning and Evaluation</a></h2>
      <p>Agents learn from a loop of environment, experience, signal and evaluation. Coding agents built in the open, multimodal reasoning, and benchmarks that cannot be gamed.</p>
    </article>
    <article class="research-card">
      <h2><a href="{{ '/research/efficient-ml-ai-infrastructure/' | relative_url }}">Efficient ML &amp; AI Infrastructure</a></h2>
      <p>Most efficiency problems start with a broken assumption. Vocabulary design, compression, long-context memory, test-time compute, resilient serving and distillation.</p>
    </article>
  </div>

  <p>All {{ site.data.homepage.publications.size }} publications, with English and Chinese summaries, are on the <a href="{{ '/#all-publications' | relative_url }}">homepage</a>.</p>
</div>
