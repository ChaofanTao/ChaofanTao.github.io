---
layout: default
title: "多模态推理与智能体"
description: "陶超凡的多模态大模型研究：推理型视觉语言模型的 RL 与长思维链后训练、物理推理基准、多模态搜索智能体，以及面向机器人的代码生成。"
permalink: /zh/research/multimodal-reasoning/
research_lang: zh
last_modified_at: 2026-11-03
og_image: /assets/img/og-image.png
about:
  - 多模态大模型
  - 视觉语言模型
  - 多模态推理
  - 视觉语言模型强化学习
  - 物理推理
  - 多模态搜索智能体
  - 具身智能
faq:
  - q: "长思维链 SFT 和 RL 结合能提升推理型视觉语言模型吗？"
    a: "不能简单叠加。Synergy Dilemma 研究（TMLR 2025）发现，长思维链 SFT 提升难题表现，但让回答冗长并损害简单题；RL 在各难度上都有提升且回答更简洁。两阶段、交替、渐进式训练以及数据混合、模型合并，都只是在准确率、推理风格和长度之间权衡，而不是叠加收益。"
  - q: "PhyX 是什么？"
    a: "PhyX 是包含 3000 道多模态题目的物理推理基准，覆盖 6 个物理领域和 25 个子领域。GPT-4o、Claude 3.7 Sonnet、o4-mini 的准确率分别为 32.5%、42.2%、45.8%，比人类专家低 29 个点以上。"
  - q: "MMSearch-Plus 是什么？"
    a: "MMSearch-Plus 是面向多模态浏览智能体的 311 题基准，要求从图像中提取细粒度视觉线索，并通过图文检索交叉验证。最强系统端到端准确率为 36.0%，set-of-mark 模块最多带来 3.9 个点提升。"
  - q: "陶超凡做具身智能吗？"
    a: "他的主要方向是代码智能体和高效大模型。与具身相关的工作包括 RoboCodeX（ICML 2024），一个在仿真和真实机器人上验证的、面向机器人行为合成的多模态代码生成框架；以及多模态物理推理基准 PhyX。"
---

{% include research/styles.liquid %}
{% include research/jsonld.liquid topic="multimodal" %}

<div class="research-page" lang="zh-Hans">
  <nav class="research-breadcrumb" aria-label="面包屑导航">
    <a href="{{ '/' | relative_url }}">陶超凡</a><span aria-hidden="true">/</span>
    <a href="{{ '/zh/research/' | relative_url }}">研究方向</a><span aria-hidden="true">/</span>
    <span>多模态推理</span>
    <span aria-hidden="true">·</span><a href="{{ '/research/multimodal-reasoning/' | relative_url }}" lang="en">English</a>
  </nav>

  <h1>多模态推理与智能体</h1>
  <p class="research-meta">作者：<a href="{{ '/' | relative_url }}">陶超凡（Chaofan Tao）</a> · 最后更新 <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%Y-%m-%d" }}</time></p>

  <p class="research-lead"><strong>这部分工作研究视觉语言模型如何推理、搜索和行动。</strong>包括反思感知的多模态推理强化学习（SRPO）、推理型视觉语言模型中长思维链 SFT 与 RL 的相互作用、物理推理评测（PhyX）、可溯源的多模态浏览智能体（MMSearch-Plus）、视频-语言组合理解（NAVERO），以及面向机器人行为的多模态代码生成（RoboCodeX）。</p>

  <h2 id="key-results">核心结果</h2>
  <div class="research-table-wrap">
    <table>
      <thead>
        <tr><th>论文</th><th>问题</th><th>结论</th></tr>
      </thead>
      <tbody>
        <tr><td><a href="https://arxiv.org/abs/2507.07562">Synergy Dilemma</a>（TMLR 2025）</td><td>长思维链 SFT 与 RL 能叠加吗？</td><td>不能：五种组合策略都只是在准确率、风格和长度之间权衡</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2506.01713">SRPO</a>（NeurIPS 2025）</td><td>多模态大模型能学会自我反思吗？</td><td>两阶段反思感知 GRPO 提升 Qwen2.5-VL-7B/32B 在 MathVista、MathVision、MathVerse、MMMU-Pro 上的表现</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2505.15929">PhyX</a>（TMLR 2026）</td><td>模型能对图像做物理推理吗？</td><td>3000 题；最强模型 32.5%–45.8%，比人类专家低 29 个点以上</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a>（ICLR 2026）</td><td>浏览智能体会用视觉证据吗？</td><td>311 题；最强系统 36.0%；set-of-mark 最多提升 3.9 个点</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2402.16117">RoboCodeX</a>（ICML 2024）</td><td>代码生成能驱动机器人行为吗？</td><td>在仿真和真实机器人的四类操作任务和一类导航任务上取得领先</td></tr>
      </tbody>
    </table>
  </div>

  <h2 id="sft-rl">RL 和长思维链 SFT，哪个让视觉语言模型推理更好？</h2>
  <p>两者擅长的地方不同，组合起来也不会简单叠加。长思维链 SFT 通过结构化推理提升难题，但让回答冗长并损害简单题；RL 在所有难度上都有提升且回答简短，只是在最难的题上提升较小。两阶段、交替、渐进式训练以及数据混合、模型合并，最终都是权衡而非叠加，论文称之为<a href="https://arxiv.org/abs/2507.07562">协同困境</a>。</p>

  <h2 id="reflection">多模态大模型如何学会自我反思？</h2>
  <p><a href="https://arxiv.org/abs/2506.01713">SRPO</a> 先构建以反思为中心的数据集：由更强的多模态模型评析初始回答，让策略模型同时学习推理和反思；再在 GRPO 中加入奖励，鼓励简洁、有意义的反思，避免冗余的自言自语。</p>

  <h2 id="physics">多模态模型能做物理推理吗？</h2>
  <p>还远未达到人类水平。<a href="https://arxiv.org/abs/2505.15929">PhyX</a> 覆盖热学、电磁学、力学、近代物理、光学、波动与声学。错误分析显示，模型过度依赖记忆的公式和表层视觉模式匹配，而非真正的物理理解。</p>

  <h2 id="search">多模态搜索智能体为什么会失败？</h2>
  <p>主要是找不到相关网页、分不清视觉上相似的事件。<a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a> 构造的问题依赖图像中的空间和时间线索，并为智能体提供 set-of-mark 工具，用于标记、裁剪、放大并发起定向图文检索。</p>

  <h2 id="embodied">从多模态推理到具身智能体</h2>
  <p><a href="https://arxiv.org/abs/2402.16117">RoboCodeX</a> 把指令分解为带有可供性和安全约束的、以物体为中心的操作单元，并用代码表达，使同一个模型能跨机器人平台泛化。PhyX 衡量这类智能体所需的物理推理能力；<a href="https://arxiv.org/abs/2411.05902">视觉自回归模型综述</a>（TMLR 2025，约 250 篇参考文献，<a href="https://github.com/ChaofanTao/Autoregressive-Models-in-Vision-Survey">GitHub 800+ star</a>）也涵盖了具身智能等应用。</p>

  <h2 id="papers">相关论文</h2>
  {% include research/paper-list.liquid topic="multimodal" lang="zh" %}

  {% include research/faq.liquid %}

  <p>相关页面：<a href="{{ '/zh/research/coding-agents/' | relative_url }}">代码智能体与智能体强化学习</a> · <a href="{{ '/zh/research/efficient-llm/' | relative_url }}">高效大模型训练与推理</a> · <a href="{{ '/llms.txt' | relative_url }}">llms.txt</a></p>
</div>
