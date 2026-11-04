---
layout: default
title: "多模态推理与智能体"
description: "陶超凡的多模态大模型研究：后训练如何塑造推理型视觉语言模型、教会模型自我反思、揭示真实差距的基准，以及把多模态推理转化为机器人行为。"
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

  <p class="research-lead"><strong>视觉语言模型能描述图像、解视觉数学题，但它们何时真正基于所见进行推理，仍不清楚。</strong>这条研究线研究后训练如何塑造它们的推理，教会它们检查自己的答案，并构建揭示其失败之处的基准，从图像中的物理到依赖视觉证据的搜索；进而迈向在物理世界中行动的智能体。</p>

  <p class="research-toc">本页内容：<a href="#post-training">后训练</a> · <a href="#reflection">自我反思</a> · <a href="#gaps">模型的不足</a> · <a href="#embodied">迈向具身智能体</a></p>

  <h2 id="post-training">推理型视觉语言模型该用长思维链 SFT 还是 RL 训练？</h2>
  <p>两者擅长的地方不同，而且结合起来比看上去难。<a href="https://arxiv.org/abs/2507.07562">协同困境</a>研究（TMLR）在多个多模态推理基准上比较了两者。长思维链 SFT 教会模型结构化、深入的推理，对难题有帮助，但会让回答冗长并损害简单题。RL 提升泛化能力、让回答简洁，在各难度上都有稳定提升，只是在最难的题上提升较小。在纯语言模型中两者通常可以叠加；但对视觉语言模型，所有尝试过的组合方式（两阶段、交替、渐进式训练，以及数据混合和模型合并）都只是在准确率、推理风格和回答长度之间互相权衡，而不是收益相加。</p>
  <p class="research-knowhow-label">经验</p>
  <ul class="research-knowhow">
    <li>按目标选择：困难的多步问题用长思维链 SFT；追求广泛稳健和简洁回答用 RL。</li>
    <li>不要默认纯文本推理模型的训练方案能迁移到视觉语言模型；如何自适应地结合两者仍是开放问题。</li>
  </ul>
  <p class="research-readmore">延伸阅读：<a href="https://arxiv.org/abs/2507.07562">论文</a> · <a href="https://github.com/JierunChen/SFT-RL-SynergyDilemma">代码</a></p>

  <h2 id="reflection">多模态模型如何学会反思？</h2>
  <p>自我反思，即发现并纠正自己的错误，在多模态模型中比纯文本模型更弱，而仅靠提示无法补上模型不具备的知识。<a href="https://arxiv.org/abs/2506.01713">SRPO</a>（NeurIPS）分两个阶段：首先由更强的多模态模型评析策略模型的初始回答，构建以反思为中心的数据集，让模型学会“怎么反思”，而不只是“答什么”；然后在 GRPO 式强化学习中，用奖励鼓励简洁、真正改进推理的反思，抑制冗余的自言自语。</p>
  <p class="research-knowhow-label">经验</p>
  <ul class="research-knowhow">
    <li>先用数据教会好的反思“长什么样”，再用 RL 奖励它。</li>
    <li>奖励反思是否有用，而不是反思有多长。</li>
  </ul>
  <p class="research-readmore">延伸阅读：<a href="https://arxiv.org/abs/2506.01713">论文</a> · <a href="https://github.com/SUSTechBruce/SRPO_MLLMs">代码</a></p>

  <h2 id="gaps">多模态模型还差在哪里？</h2>
  <p>基准只有在无法靠捷径解决时才有价值，以下三个评测分别针对特定盲区。<a href="https://arxiv.org/abs/2505.15929">PhyX</a> 在六个物理领域考察视觉场景中的物理推理，错误分析显示模型依赖记忆的教科书知识、过度依赖数学公式、匹配表层视觉模式，而不是理解物理情境。<a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a>（ICLR）针对“只看文字就能答对”的浏览基准：它的问题要求提取空间细节、时间痕迹等细粒度视觉线索，并通过多轮图文检索推断出图像之外的事实，例如事件或地点；其智能体框架加入 set-of-mark 模块，可在检索前标记、裁剪和放大。<a href="https://arxiv.org/abs/2408.09511">NAVERO</a> 关注视频中随时间变化的物体与动作关系，构建了基于反例描述的基准，并提出从反例中学习的训练方法。</p>
  <p class="research-knowhow-label">经验</p>
  <ul class="research-knowhow">
    <li>设计“忽略图像就答不对”的问题。</li>
    <li>搜索智能体的大多数失败来自找不到正确网页、分不清视觉上相似的事件，而不是最后一步推理。</li>
  </ul>
  <p class="research-readmore">延伸阅读：<a href="https://github.com/killthefullmoon/PhyX">PhyX</a> · <a href="https://github.com/mmsearch-plus/MMSearch-Plus">MMSearch-Plus</a></p>

  <h2 id="embodied">多模态推理如何转化为机器人行为？</h2>
  <p>用代码作为感知与控制之间的桥梁。<a href="https://arxiv.org/abs/2402.16117">RoboCodeX</a>（ICML）以树状结构把高层指令分解为以物体为中心的操作单元，每个单元附带可供性、安全约束等物理偏好，再写成代码，使同一个模型能跨机器人平台泛化；它用多模态推理数据做预训练，并用迭代自我更新的方法做微调。<a href="https://arxiv.org/abs/2411.05902">视觉自回归模型综述</a>（TMLR）把视觉生成方法归纳为基于像素、token 和尺度三类，并涵盖具身智能等应用，其 <a href="https://github.com/ChaofanTao/Autoregressive-Models-in-Vision-Survey">GitHub 论文列表</a>被广泛使用。</p>
  <p class="research-knowhow-label">经验</p>
  <ul class="research-knowhow">
    <li>代码是感知与控制之间的好接口：可检查、可组合，并能在不同机器人之间迁移。</li>
  </ul>
  <p>如何让视觉语言 Transformer 运行得更便宜，见<a href="{{ '/zh/research/efficient-llm/#vision-language' | relative_url }}">高效大模型页面</a>中的 token 合并与联合剪枝。</p>

  {% include research/paper-list.liquid topic="multimodal" lang="zh" %}

  <p>相关页面：<a href="{{ '/zh/research/coding-agents/' | relative_url }}">代码智能体与智能体强化学习</a> · <a href="{{ '/zh/research/efficient-llm/' | relative_url }}">高效大模型训练与推理</a></p>
</div>
