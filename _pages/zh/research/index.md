---
layout: default
title: "研究方向"
description: "陶超凡（Chaofan Tao）的研究概览：端到端训练开源大模型代码智能体、高效大模型训练与推理、多模态推理与智能体。"
permalink: /zh/research/
research_lang: zh
last_modified_at: 2026-11-04
og_image: /assets/img/og-image.png
about:
  - 大语言模型
  - 代码智能体
  - 高效大模型
  - 多模态大模型
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
  <p class="research-lead"><strong>陶超凡（Chaofan Tao）是 <a href="https://www.legox.net/">LegoX</a> 与华为基础模型实验室（Huawei Foundation Model Lab）的 AI 研究员。</strong>研究覆盖三个相互关联的方向：端到端训练开源大模型代码智能体、降低大模型训练与推理成本、提升多模态模型的推理与行动能力。他博士毕业于香港大学，关于生成式模型量化的工作获得 ACL 2022 杰出论文奖。</p>

  <div class="research-cards">
    <article class="research-card">
      <h2><a href="{{ '/zh/research/coding-agents/' | relative_url }}">代码智能体与智能体强化学习</a></h2>
      <p>来自真实软件历史的可验证任务数据、适配真实智能体工具的微调与强化学习方案，以及哪些轨迹值得学习的经验。</p>
    </article>
    <article class="research-card">
      <h2><a href="{{ '/zh/research/efficient-llm/' | relative_url }}">高效大模型训练与推理</a></h2>
      <p>词表规模选择、生成式模型压缩、低成本长上下文推理，以及更快的推理阶段计算。</p>
    </article>
    <article class="research-card">
      <h2><a href="{{ '/zh/research/multimodal-reasoning/' | relative_url }}">多模态推理与智能体</a></h2>
      <p>推理型视觉语言模型的后训练经验、自我反思、揭示真实差距的基准，以及面向机器人的代码生成。</p>
    </article>
  </div>

  <p>全部 {{ site.data.homepage.publications.size }} 篇论文及中英文摘要见<a href="{{ '/#all-publications' | relative_url }}">主页</a>。</p>
</div>
