---
layout: default
title: "研究方向"
description: "陶超凡（Chaofan Tao）的两个研究主题：智能体编程、推理与评测；高效机器学习与 AI 基础设施。"
permalink: /zh/research/
research_lang: zh
last_modified_at: 2026-11-06
og_image: /assets/img/og-image.png
about:
  - 智能体
  - 代码智能体
  - 高效机器学习
  - AI 基础设施
---

{% include research/styles.liquid %}
{% include research/jsonld.liquid %}

<div class="research-page" lang="zh-Hans">
  <nav class="research-breadcrumb" aria-label="面包屑导航">
    <a href="{{ '/' | relative_url }}">陶超凡</a><span aria-hidden="true">/</span>
    <span>研究方向</span>
    <span aria-hidden="true">·</span><a href="{{ '/research/' | relative_url }}" lang="en">English</a>
  </nav>

  <h1>研究方向</h1>
  <p class="research-lead"><strong>陶超凡（Chaofan Tao）是 <a href="https://www.legox.net/">LegoX</a> 与华为基础模型实验室（Huawei Foundation Model Lab）的 AI 研究员。</strong>他的研究围绕两个相互关联的主题：智能体如何在真实环境中通过行动来学习、又该如何评测它们；以及如何让模型的构建、训练和部署更便宜。他博士毕业于香港大学，关于生成式模型量化的工作获得 ACL 2022 杰出论文奖。</p>

  <div class="research-cards">
    <article class="research-card">
      <h2><a href="{{ '/zh/research/agentic-intelligence/' | relative_url }}">智能体编程、推理与评测</a></h2>
      <p>智能体从“环境、经验、信号、评测”构成的闭环中学习。开源构建的代码智能体、多模态推理，以及骗不过的评测基准。</p>
    </article>
    <article class="research-card">
      <h2><a href="{{ '/zh/research/efficient-ml-ai-infrastructure/' | relative_url }}">高效机器学习与 AI 基础设施</a></h2>
      <p>大多数效率问题始于一个失效的假设。词表设计、模型压缩、长上下文记忆、测试时计算、容错服务与知识蒸馏。</p>
    </article>
  </div>

  <p>全部 {{ site.data.homepage.publications.size }} 篇论文及中英文摘要见<a href="{{ '/#all-publications' | relative_url }}">主页</a>。</p>
</div>
