---
layout: default
title: "研究方向"
description: "陶超凡的研究笔记：面向长期任务、用户协作和完整项目构建，讨论智能体的学习、评测，以及计算和返工成本。"
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
  <p class="research-lead">我希望智能体能从完成一次修复，走向和用户一起完成一个长期项目：理解需求、持续实现、检查结果，并在需求变化时接着做下去。这需要更可靠的学习与评测，也需要负担得起的训练和运行成本。</p>
  <p>下面两篇文章围绕我和合作者的研究展开，也结合了我们在 <a href="https://www.legox.net/">LegoX</a> 开源项目中的实践。我想写清楚每项工作的出发点、实验带来的认识，以及仍然没有答案的部分。具体论文、代码和数据链接都放在相关讨论旁，方便继续查阅。</p>

  <div class="research-cards">
    <article class="research-card">
      <h2><a href="{{ '/zh/research/agentic-intelligence/' | relative_url }}">智能体编程、推理与评测</a></h2>
      <p>从数据、训练和评测出发，讨论智能体怎样理解变化中的需求、与用户协作，并把一个项目持续做完整。</p>
    </article>
    <article class="research-card">
      <h2><a href="{{ '/zh/research/efficient-ml-ai-infrastructure/' | relative_url }}">高效机器学习与 AI 基础设施</a></h2>
      <p>从词表、压缩、缓存到训练与服务，讨论长期项目的计算开销、用户时间和返工成本，以及它们之间的取舍。</p>
    </article>
  </div>

  <p>全部 {{ site.data.homepage.publications.size }} 篇论文及中英文摘要见<a href="{{ '/#all-publications' | relative_url }}">主页</a>。</p>
</div>
