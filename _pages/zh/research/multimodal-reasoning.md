---
layout: default
title: "多模态推理与智能体"
description: "陶超凡的多模态大模型研究：推理型视觉语言模型的后训练经验、自我反思、物理推理与多模态搜索基准，以及面向机器人的代码生成。"
permalink: /zh/research/multimodal-reasoning/
research_lang: zh
last_modified_at: 2026-11-04
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
  - q: "推理型视觉语言模型该用长思维链 SFT 还是 RL 训练？"
    a: "两者擅长的地方不同。长思维链 SFT 对难题有帮助，但会让回答冗长并可能损害简单题；RL 提升更全面且回答更简洁。分阶段、交替、渐进式训练以及数据混合、模型合并，往往只是用一种收益换另一种，而不是叠加，论文称之为协同困境。"
  - q: "PhyX 是什么？"
    a: "PhyX 是一个考察图像中物理推理能力的基准，覆盖六个物理领域。它表明当前多模态模型依赖记忆的公式和表层视觉模式，而非真正的物理理解，与人类专家仍有明显差距。"
  - q: "MMSearch-Plus 是什么？"
    a: "MMSearch-Plus 是面向多模态浏览智能体的基准和框架，答案依赖图像中的细粒度视觉线索，必须通过图文检索交叉验证。它提供 set-of-mark 工具，让智能体可以标记、裁剪、放大并发起定向检索。"
  - q: "陶超凡做具身智能吗？"
    a: "他的主要方向是代码智能体和高效大模型。与具身相关的工作包括 RoboCodeX（ICML），根据多模态输入把机器人行为生成为代码；以及 PhyX，一个考察这类智能体所需物理推理能力的基准。"
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

  <p class="research-lead"><strong>这部分工作研究视觉语言模型如何推理、搜索和行动，并构建能揭示其不足的评测。</strong>贡献包括推理模型的后训练经验、教会模型自我反思的方法、揭示真实差距的基准，以及从多模态推理迈向具身智能体的探索。</p>

  <ul class="research-highlights">
    <li><strong>后训练经验</strong>长思维链 SFT 何时有用、RL 何时有用，以及为什么二者难以叠加。</li>
    <li><strong>自我反思</strong>教会多模态模型检查并修正自己的推理。</li>
    <li><strong>揭示差距的评测</strong>图像中的物理推理，以及必须依靠视觉证据的搜索。</li>
    <li><strong>迈向具身智能体</strong>把指令和感知转化为以代码表达的机器人行为。</li>
  </ul>

  <h2 id="sft-rl">推理型视觉语言模型该用长思维链 SFT 还是 RL？</h2>
  <p>取决于你的目标，而且二者结合比看上去难。长思维链微调对难题有帮助，但会让回答冗长并可能损害简单题；RL 提升更全面，回答也更简洁。分阶段、交替、渐进式训练以及数据混合、模型合并，往往只是用一种收益换另一种，而不是叠加。<a href="https://arxiv.org/abs/2507.07562">协同困境</a>研究梳理了这些权衡，方便实践者按目标难度和回答长度预算做选择。</p>

  <h2 id="reflection">多模态模型如何学会反思？</h2>
  <p>先从好的反思中学习，再因有用的反思获得奖励。<a href="https://arxiv.org/abs/2506.01713">SRPO</a>（NeurIPS）构建以反思为中心的数据集，由更强的模型评析初始回答，让策略模型同时学会推理和反思；随后的 RL 奖励简洁、有意义的反思，抑制冗余的自言自语。</p>

  <h2 id="gaps">多模态模型还差在哪里？</h2>
  <p>差在物理理解和对视觉证据的运用。<a href="https://arxiv.org/abs/2505.15929">PhyX</a> 在六个物理领域考察图像中的物理推理，发现模型依赖记忆的公式和表层模式。<a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a>（ICLR）的问题依赖必须通过检索交叉验证的细粒度视觉线索，最常见的失败是找不到正确网页、分不清视觉上相似的事件。<a href="https://arxiv.org/abs/2408.09511">NAVERO</a> 关注视频-语言模型的细粒度组合理解。</p>

  <h2 id="embodied">从多模态推理到具身智能体</h2>
  <p><a href="https://arxiv.org/abs/2402.16117">RoboCodeX</a>（ICML）把人类指令分解为带有可供性和安全约束、以物体为中心的操作步骤，并用代码表达，使同一个模型能跨机器人平台泛化。<a href="https://arxiv.org/abs/2411.05902">视觉自回归模型综述</a>（TMLR，配有被广泛使用的 <a href="https://github.com/ChaofanTao/Autoregressive-Models-in-Vision-Survey">GitHub 论文列表</a>）涵盖了具身智能等应用。高效视觉语言 Transformer 方面，可参见 token 集成（<a href="https://arxiv.org/abs/2305.17455">CrossGET</a>）和渐进式剪枝（<a href="https://arxiv.org/abs/2301.13741">UPop</a>）。</p>

  {% include research/paper-list.liquid topic="multimodal" lang="zh" %}

  {% include research/faq.liquid %}

  <p>相关页面：<a href="{{ '/zh/research/coding-agents/' | relative_url }}">代码智能体与智能体强化学习</a> · <a href="{{ '/zh/research/efficient-llm/' | relative_url }}">高效大模型训练与推理</a></p>
</div>
