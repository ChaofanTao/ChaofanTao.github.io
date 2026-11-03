---
layout: default
title: "Research"
description: "Research overviews by Chaofan Tao (陶超凡): LLM coding agents and agentic RL, efficient LLM training and inference, and multimodal reasoning and agents."
permalink: /research/
research_lang: en
last_modified_at: 2026-11-03
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
      <p>Verified SWE tasks (LegoFlow), SFT recipes (SWE-Lego), terminal-agent trajectories (Terminal-Lego), and RL inside Claude Code, OpenHands and OpenCode (Lego-RL, up to 70.4% on SWE-bench Verified).</p>
    </article>
    <article class="research-card">
      <h2><a href="{{ '/research/efficient-llm/' | relative_url }}">Efficient LLM training and inference</a></h2>
      <p>Vocabulary scaling laws (NeurIPS 2024), quantization of generative models (ACL 2022 Outstanding Paper), KV cache compression, and fast test-time scaling.</p>
    </article>
    <article class="research-card">
      <h2><a href="{{ '/research/multimodal-reasoning/' | relative_url }}">Multimodal reasoning and agents</a></h2>
      <p>RL and long-CoT post-training for reasoning VLMs, physical reasoning (PhyX), multimodal browsing agents, and code generation for robots (RoboCodeX).</p>
    </article>
  </div>

  <p>All {{ site.data.homepage.publications.size }} publications with English and Chinese summaries are on the <a href="{{ '/#all-publications' | relative_url }}">homepage</a>. Machine-readable summaries: <a href="{{ '/llms.txt' | relative_url }}">llms.txt</a> and <a href="{{ '/llms-full.txt' | relative_url }}">llms-full.txt</a>.</p>
</div>
