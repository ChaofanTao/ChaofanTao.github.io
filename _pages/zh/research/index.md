---
layout: default
title: "研究方向"
description: "陶超凡（Chaofan Tao）的研究概览：大模型代码智能体与智能体强化学习、高效大模型训练与推理、多模态推理与智能体。"
permalink: /zh/research/
research_lang: zh
last_modified_at: 2026-11-03
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
      <p>可验证软件工程任务构建（LegoFlow）、监督微调配方（SWE-Lego）、终端智能体轨迹（Terminal-Lego），以及在 Claude Code、OpenHands、OpenCode 内原生训练的强化学习（Lego-RL，SWE-bench Verified 最高 70.4%）。</p>
    </article>
    <article class="research-card">
      <h2><a href="{{ '/zh/research/efficient-llm/' | relative_url }}">高效大模型训练与推理</a></h2>
      <p>词表规模扩展定律（NeurIPS 2024）、生成式模型量化（ACL 2022 杰出论文）、KV 缓存压缩、快速测试时扩展。</p>
    </article>
    <article class="research-card">
      <h2><a href="{{ '/zh/research/multimodal-reasoning/' | relative_url }}">多模态推理与智能体</a></h2>
      <p>推理型视觉语言模型的 RL 与长思维链后训练、物理推理（PhyX）、多模态搜索智能体、面向机器人的代码生成（RoboCodeX）。</p>
    </article>
  </div>

  <p>全部 {{ site.data.homepage.publications.size }} 篇论文及中英文摘要见<a href="{{ '/#all-publications' | relative_url }}">主页</a>。面向 AI 的机器可读摘要：<a href="{{ '/llms.txt' | relative_url }}">llms.txt</a>、<a href="{{ '/llms-full.txt' | relative_url }}">llms-full.txt</a>。</p>
</div>
