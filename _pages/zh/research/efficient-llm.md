---
layout: default
title: "高效大模型训练与推理"
description: "陶超凡的高效大模型研究：词表规模选择、生成式模型量化、低成本长上下文推理、更快的测试时扩展、容错推理服务与知识蒸馏。"
permalink: /zh/research/efficient-llm/
research_lang: zh
last_modified_at: 2026-11-04
og_image: /assets/img/og-image.png
about:
  - 高效大语言模型
  - 扩展定律
  - 词表大小
  - 模型量化
  - KV 缓存压缩
  - 测试时扩展
  - 知识蒸馏
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

  <p class="research-lead"><strong>大模型在每个阶段都很昂贵：</strong>决定怎么构建、训练和压缩，以及部署给用户使用。这条研究线寻找那些花了算力和显存却没有带来回报的地方。共同的方法是“先诊断”：先弄清现有方法为什么在某个具体瓶颈上失效，再把这个解释转化为简单实用、开源可用的改进。其中量化工作获得 ACL 2022 杰出论文奖。</p>

  <p class="research-toc">本页内容：<a href="#vocabulary">词表</a> · <a href="#quantization">量化与剪枝</a> · <a href="#long-context">长上下文</a> · <a href="#test-time">测试时扩展与服务</a> · <a href="#distillation">蒸馏</a> · <a href="#vision-language">视觉语言模型效率</a></p>

  <h2 id="vocabulary">大模型的词表应该多大？</h2>
  <p>比多数模型现在用的更大，但增长速度要慢于模型其余部分。经典的扩展定律只改变参数量和数据量，不考虑分词器，因此规模相近的模型词表大小差异很大。<a href="https://arxiv.org/abs/2407.13623">Scaling Laws with Vocabulary</a>（NeurIPS）把词表参数从网络其余部分中单独拆出，用字符而非 token 衡量数据量，并采用与词表大小无关的损失，从而公平比较不同分词器。IsoFLOPs 分析、基于导数的方法和损失函数参数拟合三种独立估计得出相同结论。</p>
  <p class="research-knowhow-label">经验</p>
  <ul class="research-knowhow">
    <li>最优词表的存在源于一个权衡：词表越大，文本切分出的 token 越少；但算力有限时，罕见 token 的嵌入很难学好。</li>
    <li>词表参数应随模型规模增长，但增速要慢于模型其余部分；许多流行模型的词表仍然偏小。</li>
    <li>根据数据量调整：数据稀缺时用更小的词表，训练数据远超计算最优时用更大的词表，同时记得词表变大也会增加推理开销。</li>
  </ul>
  <p class="research-readmore">延伸阅读：<a href="https://arxiv.org/abs/2407.13623">论文</a> · <a href="https://huggingface.co/spaces/sail/scaling-with-vocab-demo">交互式计算器</a> · <a href="https://github.com/sail-sg/scaling-with-vocab">代码</a></p>

  <h2 id="quantization">量化为什么会破坏生成式模型，又该如何修复？</h2>
  <p>量化是用更少的比特存储权重。对 BERT 类编码器有效的方法在 GPT 类生成模型上失效，而原因一度不清楚。这篇 ACL 2022 杰出论文的诊断分为两点：低精度下，词嵌入变得几乎相同，模型在生成时无法区分不同 token；不同模块的权重分布差异很大，同一套量化设置无法同时适配。token 级对比蒸馏让每个 token 的表示靠近全精度教师、远离其他 token；模块级动态缩放为每个模块学习单独的量化范围。后续工作通过可学习掩码做结构化剪枝，学习应该移除哪些组件。</p>
  <p class="research-knowhow-label">经验</p>
  <ul class="research-knowhow">
    <li>量化生成式模型时，先检查词嵌入是否还可区分，它最先坍缩。</li>
    <li>分模块处理；全局统一的量化尺度会掩盖问题。</li>
  </ul>
  <p class="research-readmore">延伸阅读：<a href="https://arxiv.org/abs/2203.10705">量化论文</a> · <a href="https://doi.org/10.18653/v1/2023.findings-acl.692">结构化剪枝论文</a></p>

  <h2 id="long-context">长上下文推理如何更省显存？</h2>
  <p>KV 缓存保存了此前每个 token 的键和值，随上下文长度增长，很快成为显存的主要开销。关键问题是：哪些部分可以丢弃而不损失信息？<a href="https://arxiv.org/abs/2406.13035">D2O</a> 根据各层注意力的集中程度为每层分配不同的缓存预算，并保留召回或合并“与保留内容相似的被丢弃 token”的机制，全程无需微调。<a href="https://arxiv.org/abs/2410.03090">UNComp</a> 用矩阵熵作为不确定性信号找出低信息区域，同时揭示负责信息检索的注意力头和层。扩散语言模型在每一步去噪时都要重新编码整个前缀；<a href="https://arxiv.org/abs/2606.10537">Prefilling-dLLM</a> 把前缀分块缓存一次，解码时只使用最相关的块。</p>
  <p class="research-knowhow-label">经验</p>
  <ul class="research-knowhow">
    <li>不同层需求不同：浅层和深层需要不同的缓存预算。</li>
    <li>淘汰要留“后路”：让被丢弃的 token 可以被召回或合并。</li>
    <li>分块缓存时，每块开头的起始符（BOS）会充当注意力锚点；稀疏预填充甚至可以优于稠密注意力。</li>
  </ul>
  <p class="research-readmore">延伸阅读：<a href="https://github.com/AIoT-MLSys-Lab/D2O">D2O 代码</a> · <a href="https://github.com/menik1126/UNComp">UNComp 代码</a> · <a href="https://github.com/menik1126/Prefilling-dLLM">Prefilling-dLLM 代码</a></p>

  <h2 id="test-time">推理阶段的计算和线上服务如何更快、更稳？</h2>
  <p>测试时扩展通过在生成时投入更多算力来提升答案质量，常见做法是小模型起草、大模型校验。<a href="https://arxiv.org/abs/2509.15148">ATTS</a> 分析了时间花在哪里，发现主要瓶颈是同步而不是计算本身。它用基于一致性预测在线校准的异步推理取代同步校验，同时在串行和并行两个维度上扩展，并对草稿被拒绝的频率保持统计上的控制。在部署侧，单张 GPU 故障就可能让多 GPU 服务整体中断。<a href="https://arxiv.org/abs/2511.11617">AnchorTP</a> 把模型权重和 KV 缓存保存在推理进程之外的守护进程中，在剩余 GPU 上重新切分模型，并规划最少的数据迁移来恢复服务。</p>
  <p class="research-knowhow-label">经验</p>
  <ul class="research-knowhow">
    <li>优化前先测算术强度；延迟问题往往是协调问题。</li>
    <li>把状态（权重与缓存）和可能崩溃的进程分开。</li>
  </ul>
  <p class="research-readmore">延伸阅读：<a href="https://github.com/menik1126/Asynchronous-Test-Time-Scaling">ATTS 代码</a> · <a href="https://arxiv.org/abs/2511.11617">AnchorTP 论文</a></p>

  <h2 id="distillation">知识蒸馏中什么最重要？</h2>
  <p>蒸馏是用更强的教师训练更小的学生，一个反复出现的结论是：最“显然”的教师信号不一定最好。在大模型蒸馏中，前向 KL 与反向 KL 其实有相同的最优解，也都不表现出通常认为的“寻峰”或“求均值”特性；实际差别在于训练早期前向 KL 关注分布头部、反向 KL 关注尾部，<a href="https://arxiv.org/abs/2404.02657">自适应 KL</a> 结合了两者。<a href="https://arxiv.org/abs/2510.10925">PerSyn</a> 基于“更强的模型不一定是更好的教师”这一观察，先为每个提示选出学生最容易学会的教师，再生成数据。<a href="https://arxiv.org/abs/2601.21968">On-policy Verbal Distillation</a> 适用于只返回文本的黑盒教师：用教师的评分给学生自己的部分尝试排序，保留好的前缀、替换较差的后续。</p>
  <p class="research-knowhow-label">经验</p>
  <ul class="research-knowhow">
    <li>按学生能学会什么来匹配教师，而不只看榜单强弱。同样的结论也出现在<a href="{{ '/zh/research/coding-agents/#trajectories' | relative_url }}">代码智能体的轨迹筛选</a>中。</li>
    <li>保留学生自己生成的好前缀，有助于保持探索、避免坍缩。</li>
  </ul>

  <h2 id="vision-language">视觉语言模型呢？</h2>
  <p>“先诊断再改进”的方法同样适用。<a href="https://arxiv.org/abs/2305.17455">CrossGET</a>（ICML）在推理时合并冗余 token，用一种模态的信息引导另一种模态的匹配，既适用于双编码器模型，也适用于多模态大模型。<a href="https://arxiv.org/abs/2301.13741">UPop</a>（ICML）在视觉和语言两部分上联合搜索更小的子网络，让各模态的剪枝比例由学习决定而非人为设定，并交替进行搜索与重训练以达到更高压缩率。</p>

  {% include research/paper-list.liquid topic="efficient-llm" lang="zh" %}

  <p>相关页面：<a href="{{ '/zh/research/coding-agents/' | relative_url }}">代码智能体与智能体强化学习</a> · <a href="{{ '/zh/research/multimodal-reasoning/' | relative_url }}">多模态推理与智能体</a></p>
</div>
