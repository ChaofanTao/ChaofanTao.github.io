---
layout: default
title: "研究方向"
description: "陶超凡不同阶段的研究：高效机器学习、多模态推理与智能体，以及多智能体协作、AI for AI 和递归自我改进的开放问题。"
permalink: /zh/research/
research_lang: zh
last_modified_at: 2026-11-06
og_image: /assets/img/og-image.png
about:
  - 智能体
  - 代码智能体
  - 高效机器学习
  - AI 基础设施
  - 多智能体协作
  - AI for AI
  - 递归自我改进
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
  <p class="research-lead">我的研究关注智能体如何理解环境、从行动中学习，并逐步具备更强的自主探索能力。再往前，值得追问的是：多个智能体能否协同解决复杂问题，甚至参与改进模型、训练方法和它们自身的研究过程？</p>
  <p>这里串起了我在不同阶段与不同团队合作的研究：从模型压缩与高效学习，到多模态推理、机器人，以及智能体的数据、训练和评测。近期在 <a href="https://www.legox.net/">LegoX</a> 的开源实践是其中一部分。两篇文章既回顾已有结果，也把多智能体、AI for AI 和递归自我改进放在开放问题中继续讨论。</p>

  <div class="research-cards">
    <article class="research-card">
      <h2><a href="{{ '/zh/research/agentic-intelligence/' | relative_url }}">智能体的学习、协作与自我改进</a></h2>
      <p>从多模态推理与环境交互出发，讨论经验、验证、多智能体协作，以及 AI 如何参与自身改进。</p>
    </article>
    <article class="research-card">
      <h2><a href="{{ '/zh/research/efficient-ml-ai-infrastructure/' | relative_url }}">高效机器学习与 AI 基础设施</a></h2>
      <p>从模型压缩、词表与知识蒸馏，到缓存、训练和推理系统，讨论有限资源怎样支持更多有效学习与自主探索。</p>
    </article>
  </div>

  <p>全部 {{ site.data.homepage.publications.size }} 篇论文及中英文摘要见<a href="{{ '/#all-publications' | relative_url }}">主页</a>。</p>
</div>
