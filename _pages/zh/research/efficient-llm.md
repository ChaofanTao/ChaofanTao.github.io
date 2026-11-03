---
layout: default
title: "高效大模型训练与推理"
description: "陶超凡的高效大模型研究：词表规模扩展定律、生成式模型量化与剪枝、KV 缓存压缩、快速测试时扩展与知识蒸馏。"
permalink: /zh/research/efficient-llm/
research_lang: zh
last_modified_at: 2026-11-03
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
  - q: "大模型的计算最优词表应该多大？"
    a: "最优词表随计算预算增长，模型越大，词表应越大。Scaling Laws with Vocabulary（NeurIPS 2024）预测 Llama2-70B 的词表至少应为 21.6 万，是其实际 3.2 万的 7 倍。在 2.3e21 FLOPs 固定预算下，把 3B 模型词表从 3.2 万增至 4.3 万，ARC-Challenge 准确率从 29.1 提升到 32.0。"
  - q: "陶超凡哪篇论文获得了 ACL 2022 杰出论文奖？"
    a: "Compression of Generative Pre-trained Language Models via Quantization（ACL 2022）。论文发现以往量化方法在生成式模型上失效，原因是词嵌入同质化和各模块权重分布差异大；通过 token 级对比蒸馏和模块级动态缩放解决，在 GPT-2 和 BART 上分别实现 14.4 倍和 13.4 倍压缩，性能接近全精度。"
  - q: "KV 缓存压缩在长上下文推理中能省多少？"
    a: "UNComp（EMNLP 2025）用不确定性指导压缩，把 KV 缓存降到原来的 4.74%，吞吐提升 6.4 倍。D2O 按层分配缓存并按相似度召回被丢弃的 token，无需微调即可把推理吞吐提升 3 倍以上。"
  - q: "词表扩展定律有代码或 demo 吗？"
    a: "有。代码在 github.com/sail-sg/scaling-with-vocab，预测最优词表大小的交互式 demo 在 Hugging Face Spaces：huggingface.co/spaces/sail/scaling-with-vocab-demo。"
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

  <p class="research-lead"><strong>这条研究线关注如何让每一份算力和每一字节显存换来更多能力。</strong>内容包括计算最优的词表规模、生成式语言模型的量化与结构化剪枝、长上下文推理的 KV 缓存压缩、更快的测试时扩展、知识蒸馏，以及容错的分布式推理。其中量化论文获得 ACL 2022 杰出论文奖。</p>

  <h2 id="key-results">核心结果</h2>
  <div class="research-table-wrap">
    <table>
      <thead>
        <tr><th>论文</th><th>问题</th><th>结果</th></tr>
      </thead>
      <tbody>
        <tr><td><a href="https://arxiv.org/abs/2407.13623">Scaling Laws with Vocabulary</a>（NeurIPS 2024）</td><td>计算最优词表规模</td><td>Llama2-70B 应使用 ≥21.6 万词表（实际 3.2 万的 7 倍）；3.2 万 → 4.3 万使 ARC-Challenge 29.1 → 32.0（2.3e21 FLOPs）</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2203.10705">生成式预训练模型量化压缩</a>（ACL 2022 杰出论文）</td><td>低比特生成式模型</td><td>GPT-2 压缩 14.4 倍、BART 压缩 13.4 倍，性能接近全精度</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2410.03090">UNComp</a>（EMNLP 2025）</td><td>KV 缓存压缩</td><td>缓存降至原来的 4.74%，吞吐提升 6.4 倍</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2406.13035">D2O</a></td><td>无需微调的 KV 缓存淘汰</td><td>推理吞吐提升 3 倍以上</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2509.15148">ATTS</a>（ICLR 2026）</td><td>测试时扩展延迟</td><td>测试时扩展最高加速 56.7 倍、吞吐提升 4.14 倍，准确率无损</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2606.10537">Prefilling-dLLM</a>（EMNLP 2026）</td><td>长上下文扩散语言模型</td><td>8K–32K 上下文加速 9.1–28.0 倍，无需训练</td></tr>
      </tbody>
    </table>
  </div>

  <h2 id="vocabulary">大模型的词表应该多大？</h2>
  <p>比现在大多数模型用的更大。<a href="https://arxiv.org/abs/2407.13623">Scaling Laws with Vocabulary</a> 训练了 3300 万到 30 亿参数、最多 5000 亿字符的模型，用 IsoFLOPs 分析、导数估计和损失函数参数拟合三种方法推导计算最优词表，三者结论一致：最优词表随算力增长。多数开源大模型词表偏小，例如 Llama2-70B 应使用至少 21.6 万而非 3.2 万。可以试用<a href="https://huggingface.co/spaces/sail/scaling-with-vocab-demo">交互式 demo</a> 或查看<a href="https://github.com/sail-sg/scaling-with-vocab">代码</a>。</p>

  <h2 id="quantization">如何量化生成式语言模型而不破坏生成质量？</h2>
  <p>先解决词嵌入问题。对 BERT 有效的量化方法在 GPT-2 和 BART 上失效，原因是低比特词嵌入变得同质化、各模块权重分布差异大。token 级对比蒸馏让词嵌入保持可区分，模块级动态缩放让量化器适配不同模块，从而实现 14.4 倍和 13.4 倍压缩且质量接近全精度。后续工作用可学习掩码做<a href="https://doi.org/10.18653/v1/2023.findings-acl.692">生成式预训练模型的结构化剪枝</a>（Findings of ACL 2023）。</p>

  <h2 id="long-context">如何降低长上下文推理成本？</h2>
  <p>关键是判断 KV 缓存中哪些部分重要。D2O 根据注意力密度按层分配缓存预算，并召回与保留 token 相似的被丢弃 token。UNComp 用截断矩阵熵作为不确定性信号发现稀疏性，同时揭示检索头和检索层。Prefilling-dLLM 把预填充与解码分离引入扩散语言模型：前缀分块只缓存一次，解码时只使用最相关的块。</p>

  <h2 id="test-time">测试时扩展能做到又快又准吗？</h2>
  <p>能，前提是去掉同步。ATTS 发现投机式测试时扩展的主要瓶颈是同步而非计算，并用基于一致性预测的异步推理替代。在 MATH、AMC23、AIME24、AIME25 上最高加速 56.7 倍，同时控制拒绝率。</p>

  <h2 id="distillation">大模型蒸馏中什么最重要？</h2>
  <p>充分训练后，前向 KL 与反向 KL 表现相近，但早期分别侧重分布的头部和尾部；<a href="https://arxiv.org/abs/2404.02657">自适应 KL</a>（COLING 2024）结合两者。<a href="https://arxiv.org/abs/2510.10925">PerSyn</a>（ACL 2026）为每个提示选择学生最容易学会的教师，<a href="https://arxiv.org/abs/2601.21968">On-policy Verbal Distillation</a> 用轨迹级教师评分替代 token 级匹配。</p>

  <h2 id="systems">高效视觉语言模型与容错推理服务</h2>
  <p><a href="https://arxiv.org/abs/2305.17455">CrossGET</a>（ICML 2024）和 <a href="https://arxiv.org/abs/2301.13741">UPop</a>（ICML 2023）通过 token 集成和渐进式剪枝加速、压缩视觉语言 Transformer。<a href="https://arxiv.org/abs/2511.11617">AnchorTP</a>（DATE 2026）用状态保持的弹性张量并行，让大模型推理服务在单 GPU 故障时快速恢复。</p>

  <h2 id="papers">相关论文</h2>
  {% include research/paper-list.liquid topic="efficient-llm" lang="zh" %}

  {% include research/faq.liquid %}

  <p>相关页面：<a href="{{ '/zh/research/coding-agents/' | relative_url }}">代码智能体与智能体强化学习</a> · <a href="{{ '/zh/research/multimodal-reasoning/' | relative_url }}">多模态推理与智能体</a> · <a href="{{ '/llms.txt' | relative_url }}">llms.txt</a></p>
</div>
