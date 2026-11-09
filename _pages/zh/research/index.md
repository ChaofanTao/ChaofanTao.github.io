---
layout: default
title: "研究方向"
description: "陶超凡（Chaofan Tao）的两个研究主题：智能体，从多模态推理到在 LegoX 开源构建的代码智能体；高效机器学习与 AI 基础设施，从模型压缩到训练智能体的系统。"
permalink: /zh/research/
research_lang: zh
last_modified_at: 2026-11-09
og_image: /assets/img/og-image.png
about:
  - 智能体
  - 代码智能体
  - 高效机器学习
  - AI 基础设施
  - 多智能体协作
  - AI 改进 AI
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
  <p class="research-lead">我关心的是：AI 系统怎样看清要紧的信息、据此行动、从结果里学习、并且值得信任，以及怎样让这一切花得起。我的工作从压缩和扩展语言模型开始，经过多模态推理，走到了我们在 <a href="https://www.legox.net/">LegoX</a> 开源构建的代码智能体。下面两篇文章梳理这些工作，也聊聊我对未来的一些思考：超长程任务、多智能体协作、可信的评测、AI 改进 AI、AI for Science，以及智能体数据对基础设施提出的新要求。</p>

  <div class="research-cards">
    <article class="research-card">
      <h2><a href="{{ '/zh/research/agentic-intelligence/' | relative_url }}">智能体的学习、协作与自我改进</a></h2>
      <p>从多模态推理，到把代码智能体当作实验室：可验证的经验、真实 harness 里的 SFT 与 RL、智能体代码审查；以及我对超长程智能体、多智能体协作、评测、AI 改进 AI 和 AI for Science 的一些思考。</p>
    </article>
    <article class="research-card">
      <h2><a href="{{ '/zh/research/efficient-ml-ai-infrastructure/' | relative_url }}">高效机器学习与 AI 基础设施</a></h2>
      <p>量化与剪枝、词表扩展定律、KV 缓存、快速的推理时扩展、知识蒸馏和稳定的系统；以及我对大规模智能体数据基础设施、按轨迹衡量效率、超长程运行和 AI for Science 的一些思考。</p>
    </article>
  </div>

  <p>全部 {{ site.data.homepage.publications.size }} 篇论文及中英文摘要见<a href="{{ '/#all-publications' | relative_url }}">主页</a>。</p>
</div>
