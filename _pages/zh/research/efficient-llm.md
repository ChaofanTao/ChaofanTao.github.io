---
layout: default
title: "高效大模型训练与推理"
description: "陶超凡的高效大模型研究：词表规模选择、生成式模型压缩、低成本长上下文推理、更快的测试时扩展与知识蒸馏。"
permalink: /zh/research/efficient-llm/
research_lang: zh
last_modified_at: 2026-11-04
og_image: /assets/img/og-image.png
about:
  - 高效大语言模型
  - 扩展定律
  - 词表大小
  - 模型量化
  - 结构化剪枝
  - KV 缓存压缩
  - 知识蒸馏
  - 测试时扩展
faq:
  - q: "大模型的词表应该多大？"
    a: "比现在多数模型用的更大。Scaling Laws with Vocabulary（NeurIPS）用三种独立方法估计计算最优词表规模，结论一致：最优词表随计算预算增长，模型越大，词表应越大。Hugging Face Spaces 上提供了交互式计算器。"
  - q: "陶超凡哪篇论文获得了 ACL 2022 杰出论文奖？"
    a: "Compression of Generative Pre-trained Language Models via Quantization。论文解释了为 BERT 类编码器设计的量化方法为什么在 GPT 类生成式模型上失效，并用 token 级对比蒸馏和模块级动态缩放解决了这一问题。"
  - q: "长上下文推理如何减少显存占用？"
    a: "只保留 KV 缓存中真正重要的部分。D2O 按层分配缓存预算并召回有用的被丢弃 token；UNComp 用不确定性信号判断哪些内容可以压缩；Prefilling-dLLM 把预填充与解码分离引入扩散语言模型。"
  - q: "这些方法有代码吗？"
    a: "有。本页多数论文都提供公开代码，包括词表扩展定律（sail-sg/scaling-with-vocab）、D2O、UNComp、ATTS 和 Prefilling-dLLM，链接见论文列表。"
---

{% include research/styles.liquid %}
{% include research/jsonld.liquid topic="efficient-llm" %}

<div class="research-page" lang="zh-Hans">
  <nav class="research-breadcrumb" aria-label="面包屑导航">
    <a href="{{ '/' | relative_url }}">陶超凡</a><span aria-hidden="true">/</span>
    <a href="{{ '/zh/research/' | relative_url }}">研究方向</a><span aria-hidden="true">/</span>
    <span>高效大模型</span>
    <span aria-hidden="true">·</span><a href="{{ '/research/efficient-llm/' | relative_url }}" lang="en">English</a>
  </nav>

  <h1>高效大模型训练与推理</h1>
  <p class="research-meta">作者：<a href="{{ '/' | relative_url }}">陶超凡（Chaofan Tao）</a> · 最后更新 <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%Y-%m-%d" }}</time></p>

  <p class="research-lead"><strong>这条研究线关注如何让每一份算力和显存换来更多能力，</strong>从训练前的设计选择，到模型如何压缩和部署。每个项目都从一个具体瓶颈出发，先解释现有方法为什么在这里失效，再把这个解释转化为实用的改进，并公开代码。其中量化工作获得 ACL 2022 杰出论文奖。</p>

  <ul class="research-highlights">
    <li><strong>训练前的设计</strong>把词表大小视为一个扩展维度，并给出有依据的选择方法。</li>
    <li><strong>不破坏生成的压缩</strong>解释 GPT 类模型为什么一量化就坏，以及如何修复。</li>
    <li><strong>更便宜的长上下文</strong>判断 KV 缓存中哪些部分真正重要。</li>
    <li><strong>更快的推理与服务</strong>去掉测试时扩展中的同步等待，并在 GPU 故障时保持服务。</li>
  </ul>

  <h2 id="vocabulary">大模型的词表应该多大？</h2>
  <p>比现在多数模型用的更大。扩展研究通常只改变参数量和数据量，而把分词器视为固定。<a href="https://arxiv.org/abs/2407.13623">Scaling Laws with Vocabulary</a>（NeurIPS）用三种独立方法估计计算最优词表规模，三者一致表明最优词表随算力增长：模型越大，词表应越大，而许多流行模型的词表偏小。<a href="https://huggingface.co/spaces/sail/scaling-with-vocab-demo">交互式计算器</a>把这一结论变成可直接使用的选择。</p>

  <h2 id="quantization">量化为什么会破坏生成式模型，又该如何修复？</h2>
  <p>对 BERT 类编码器有效的方法在 GPT 类生成模型上失效，原因有二：低比特词嵌入会彼此趋同，而不同模块的权重范围差异很大。<a href="https://arxiv.org/abs/2203.10705">token 级对比蒸馏</a>让词嵌入保持可区分，模块级动态缩放让每个量化器适配所在模块（ACL 2022 杰出论文）。后续工作通过<a href="https://doi.org/10.18653/v1/2023.findings-acl.692">结构化剪枝</a>学习该移除哪些组件。</p>

  <h2 id="long-context">长上下文推理如何更省显存？</h2>
  <p>只保留 KV 缓存中真正重要的部分。<a href="https://arxiv.org/abs/2406.13035">D2O</a> 根据各层注意力的分布情况分配缓存预算，并能召回与保留内容相似的被丢弃 token。<a href="https://arxiv.org/abs/2410.03090">UNComp</a> 用不确定性信号找出可压缩的部分，同时揭示负责信息检索的注意力头和层。<a href="https://arxiv.org/abs/2606.10537">Prefilling-dLLM</a> 无需重新训练，就把预填充与解码分离引入扩散语言模型。</p>

  <h2 id="test-time">推理阶段的计算如何更快？</h2>
  <p>去掉等待。<a href="https://arxiv.org/abs/2509.15148">ATTS</a> 指出，在小模型起草、大模型校验的测试时扩展中，主要瓶颈是同步而不是计算本身，并用有统计保证的异步推理取而代之。在部署侧，<a href="https://arxiv.org/abs/2511.11617">AnchorTP</a> 通过状态保持的弹性张量并行，让大模型服务在单 GPU 故障时继续运行。</p>

  <h2 id="distillation">知识蒸馏中什么最重要？</h2>
  <p>让学生匹配到合适的信号。充分训练后，前向 KL 与反向 KL 表现相近，但训练早期分别关注教师分布的不同部分；<a href="https://arxiv.org/abs/2404.02657">自适应 KL</a> 结合了两者的优势。<a href="https://arxiv.org/abs/2510.10925">PerSyn</a> 为每个提示选择学生最容易学会的教师，<a href="https://arxiv.org/abs/2601.21968">On-policy Verbal Distillation</a> 从整条轨迹的教师反馈中学习，而不是逐 token 匹配。</p>

  {% include research/paper-list.liquid topic="efficient-llm" lang="zh" %}

  {% include research/faq.liquid %}

  <p>相关页面：<a href="{{ '/zh/research/coding-agents/' | relative_url }}">代码智能体与智能体强化学习</a> · <a href="{{ '/zh/research/multimodal-reasoning/' | relative_url }}">多模态推理与智能体</a></p>
</div>
