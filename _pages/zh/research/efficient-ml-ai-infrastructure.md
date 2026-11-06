---
layout: default
title: "高效机器学习与 AI 基础设施"
description: "陶超凡的高效机器学习研究：词表设计、模型压缩、长上下文记忆、测试时计算、容错服务与知识蒸馏，各自在哪个隐含假设失效时出问题，以及如何修复。"
permalink: /zh/research/efficient-ml-ai-infrastructure/
research_lang: zh
last_modified_at: 2026-11-06
og_image: /assets/img/og-image.png
figure: /assets/img/research/efficiency-lifecycle-zh.svg
about:
  - 高效机器学习
  - AI 基础设施
  - 扩展定律
  - 模型量化
  - KV 缓存压缩
  - 测试时扩展
  - 知识蒸馏
---

{% include research/styles.liquid %}
{% include research/jsonld.liquid group="efficient" %}

<div class="research-page" lang="zh-Hans">
  <nav class="research-breadcrumb" aria-label="面包屑导航">
    <a href="{{ '/' | relative_url }}">陶超凡</a><span aria-hidden="true">/</span>
    <a href="{{ '/zh/research/' | relative_url }}">研究方向</a><span aria-hidden="true">/</span>
    <span>高效机器学习与 AI 基础设施</span>
    <span aria-hidden="true">·</span><a href="{{ '/research/efficient-ml-ai-infrastructure/' | relative_url }}" lang="en">English</a>
  </nav>

  <h1>高效机器学习与 AI 基础设施</h1>
  <p class="research-dek">大多数效率问题，都始于一个悄悄失效的假设。本文沿着一个模型从设计到部署的生命周期，梳理我们的每项工作分别拆掉了哪个假设。</p>
  <p class="research-meta">作者：<a href="{{ '/' | relative_url }}">陶超凡（Chaofan Tao）</a>及合作者 · 最后更新 <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%Y-%m-%d" }}</time></p>

  <p>效率通常被看作一种交换：牺牲一些质量，换取更少的算力或显存。但在我们的经验里，更大的收益往往来自别处。一个方法之所以失效或浪费资源，常常是因为它依赖的某个假设在设计时合理、如今却不再成立：分词器可以在扩展之前固定下来；网络的每个部分对压缩的承受力都一样；缓存里每个 token 同样重要；同步没有成本；硬件不会故障；最强的教师教得最好。</p>
  <p>找到失效的假设往往比修复它更难；诊断一旦准确，修复通常很简单。本页按假设所在的模型生命周期阶段来组织。其中第二阶段的量化工作获得 ACL 2022 杰出论文奖。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/efficiency-lifecycle-zh.svg' | relative_url }}" alt="模型生命周期五个阶段的示意图：设计、压缩、记忆、计算与服务、迁移，每个阶段对应一个被我们的工作证明并不成立的默认假设，以及相关项目。" width="960" height="300" loading="eager"></div>
    <figcaption>贯穿模型生命周期的效率。每个阶段对应一个常见假设，以及揭示它在哪里失效的工作。</figcaption>
  </figure>

  <p class="research-toc">本页内容：<a href="#design">设计</a> · <a href="#compress">压缩</a> · <a href="#remember">记忆</a> · <a href="#serve">计算与服务</a> · <a href="#transfer">迁移</a> · <a href="#insights">贯穿全文的洞察</a> · <a href="#open-questions">开放问题</a></p>

  <h2 id="design">1. 设计：分词器不是随意的选择</h2>
  <p class="research-claim">词表大小是一个扩展维度，而多数模型在这上面投入不足。</p>
  <p>经典扩展定律描述损失如何随参数量和数据量变化，却把词表排除在外，于是规模相近的模型往往配着差异很大的词表。<a href="https://arxiv.org/abs/2407.13623">Scaling Laws with Vocabulary</a>（NeurIPS）把词表重新放回来：把词表参数从网络其余部分中拆出，用字符而非 token 衡量数据量以便公平比较不同分词器，并采用与词表大小无关的损失。IsoFLOPs 分析、基于导数的方法和损失函数参数拟合三种独立估计得出一致结论。</p>
  <p>最优词表背后的机制是一个权衡：词表越大，文本切分出的 token 越少、覆盖的概念越多；但算力有限时，罕见 token 的嵌入很难学好。随着算力增长，平衡点随之移动：词表应随模型增长，但增速慢于模型其余部分，而许多流行模型的词表仍然偏小。数据情况也很关键：数据稀缺时，更小的词表能避免罕见 token 过拟合；训练数据远超计算最优时，更大的词表更有利，同时词表变大也会增加推理开销。可以这样理解最优点：在固定算力预算下，它是让模型读到最多训练文本的那个词表大小。词表太小，同样的文本要切成更多 token，算力花在了 token 数上；词表太大，算力又花在了嵌入层和输出层上。<a href="https://huggingface.co/spaces/sail/scaling-with-vocab-demo">交互式计算器</a>把这些结论变成可直接使用的选择。</p>

  <h2 id="compress">2. 压缩：模型的各部分并不一样</h2>
  <p class="research-claim">压缩在模型最不均匀的地方失效，所以修复的关键是区别对待各个部分。</p>
  <p>对 BERT 类编码器有效的量化方法在 GPT 类生成模型上失效，而原因一度不清楚。<a href="https://arxiv.org/abs/2203.10705">Compression of Generative Pre-trained Language Models via Quantization</a>（ACL 2022 杰出论文）给出了两点诊断：低精度下词嵌入变得几乎相同，生成模型在选择下一个 token 时无法区分它们；不同模块的权重分布差异很大，同一套量化设置无法同时适配。token 级对比蒸馏让每个 token 的表示靠近全精度教师、并与其他 token 保持区分；模块级动态缩放为每个模块单独学习量化范围。<a href="https://doi.org/10.18653/v1/2023.findings-acl.692">结构化剪枝</a>把同样的思路用于“删减”，学习生成式模型中哪些组件可以移除。</p>
  <p>视觉语言模型让不均匀性更加明显，因为两种模态承载信息的方式不同。<a href="https://arxiv.org/abs/2301.13741">UPop</a> 在视觉和语言两部分上联合搜索更小的子网络，让每种模态的剪枝比例由学习决定而非人为设定，并交替进行搜索与重训练。<a href="https://arxiv.org/abs/2305.17455">CrossGET</a> 在推理时合并冗余 token，用一种模态引导另一种模态的匹配。</p>

  <h2 id="remember">3. 记忆：不是每个缓存 token 都重要，但要留后路</h2>
  <p class="research-claim">长上下文的记忆可以大幅压缩，前提是淘汰既要自适应，又要可回退。</p>
  <p>KV 缓存保存此前每个 token 的键和值，在长上下文推理中很快成为显存的主要开销。均匀地丢弃很浪费，因为各层并不相同：<a href="https://arxiv.org/abs/2406.13035">D2O</a> 根据各层注意力的集中程度为每层分配预算，并保留召回或合并“与保留内容相似的被丢弃 token”的机制，全程无需微调。<a href="https://arxiv.org/abs/2410.03090">UNComp</a> 从信息的角度提问，用矩阵熵作为不确定性信号找出可压缩的部分；同样的分析还揭示了负责信息检索的注意力头和层。</p>
  <p>扩散语言模型带来了这个问题的另一种形式：它们在每一步去噪时都要重新编码整个前缀。<a href="https://arxiv.org/abs/2606.10537">Prefilling-dLLM</a> 无需重新训练，把前缀分块缓存一次，解码时只使用与查询相关的块和 token。一个小细节很关键：每块开头的起始符（BOS）充当周期性的注意力锚点，有了它，稀疏预填充甚至可以优于稠密注意力。</p>

  <h2 id="serve">4. 计算与服务：协调比计算更昂贵</h2>
  <p class="research-claim">在大规模系统中，瓶颈通常是等待，风险通常是状态丢失。</p>
  <p>测试时扩展通过在生成时投入更多算力来提升答案质量，常见做法是小模型起草、大模型校验。<a href="https://arxiv.org/abs/2509.15148">ATTS</a> 分析了时间花在哪里，发现主要瓶颈是同步而不是计算本身。它用基于一致性预测在线校准的异步推理取代同步校验，同时在串行和并行两个维度上扩展，并对草稿被拒绝的频率保持统计上的控制。</p>
  <p>部署也有一个隐含假设：GPU 不会故障。在多 GPU 张量并行中，单卡故障就可能让整个服务中断。<a href="https://arxiv.org/abs/2511.11617">AnchorTP</a> 把权重和 KV 缓存保存在推理进程之外的守护进程中，在剩余 GPU 上以不等宽方式重新切分模型，并规划恢复所需的最少数据迁移。</p>
  <p><strong>智能体训练的基础设施。</strong>同样的两条经验，在用<a href="{{ '/zh/research/agentic-intelligence/#signal' | relative_url }}">原生 harness 强化学习</a>训练智能体时表现得更加明显。在 Lego-RL 中，一次训练尝试的几乎全部时间都花在智能体行动上：在沙箱里读文件、改代码、跑测试。尝试时长长且参差不齐，同步批次总要等最慢的那一个；异步调度让新的尝试在有空位时立即开始。训练器在尝试进行中更新权重时，部分 rollout 会暂停生成、加载新权重，并在同一个副本上从缓存的前缀继续，长时间的尝试因此不会作废。启动沙箱的时间主要花在构建镜像上，所以预构建任务镜像、挂载智能体运行时、按需拉取镜像，去掉了大部分等待。有一个刻意的例外：评分工具链被固化进每个镜像，尽管会多花一点时间，因为可复现的奖励比更快的奖励更有价值。智能体强化学习在很大程度上是一个效率与可靠性问题。</p>

  <h2 id="transfer">5. 迁移：最强的教师不是最好的教师</h2>
  <p class="research-claim">蒸馏效果最好的时候，是信号与学生能学会的东西相匹配，而不是教师最强的时候。</p>
  <p>在大模型蒸馏中，<a href="https://arxiv.org/abs/2404.02657">前向 KL 与反向 KL</a> 其实有相同的最优解，也都不表现出通常认为的“寻峰”或“求均值”特性。实际差别出现在训练早期：前向 KL 关注教师分布的头部，反向 KL 关注尾部；自适应 KL 据此为两者加权。<a href="https://arxiv.org/abs/2510.10925">PerSyn</a> 基于“更强的模型不一定是更好的教师”这一观察，在生成任何数据之前，先把每个提示分配给学生最容易学会的教师，而不是让所有教师都生成、事后再挑选。</p>
  <p>同样的结论在智能体训练中独立出现：来自较弱智能体、锚定环境的轨迹，比更强智能体给出的答案教得更好；而<a href="{{ '/zh/research/agentic-intelligence/#signal' | relative_url }}">黑盒教师的口头反馈</a>无需暴露 token 概率，也能指导学生。</p>

  <h2 id="insights">贯穿全文的洞察</h2>
  <ol class="research-insights">
    <li><strong>优化之前，先诊断失效的假设。</strong>这里的每个结果，都始于追问现有方法为什么失效，而不是尝试一个更快的变体。原因一旦清楚，修复通常很小。</li>
    <li><strong>不均匀才是常态。</strong>层、模块、模态、token、教师各不相同。按层、按模块、按模态、按提示自适应分配预算，在压缩、缓存和蒸馏中反复出现。</li>
    <li><strong>留好后路。</strong>可召回的淘汰、保存在可能崩溃的进程之外的状态、在权重更新时也不中断的 rollout，让激进的优化变得安全。</li>
    <li><strong>规模越大，协调越占主导。</strong>在测试时扩展、线上服务和智能体训练中，最大的收益都来自消除等待，而不是加速计算。</li>
    <li><strong>效率决定了什么能被学会。</strong>算力训练不好的罕见 token 嵌入、学生吸收不了的教师输出，都说明效率不只关乎成本，也关乎模型能学会什么。</li>
  </ol>

  <h2 id="open-questions">开放问题</h2>
  <ul>
    <li>当推理成本、多语言数据和代码都纳入目标后，词表该如何选择？</li>
    <li>对上下文主要由工具输出而非文本构成的智能体，长上下文记忆应该保留什么？</li>
    <li>在大部分时间花在“行动”而非计算梯度的智能体强化学习中，rollout 效率还能提升多少？</li>
    <li>部署中的容错思路，能否让长时间的训练同样稳健？</li>
  </ul>

  {% include research/paper-list.liquid group="efficient" lang="zh" %}

  <p>相关页面：<a href="{{ '/zh/research/agentic-intelligence/' | relative_url }}">智能体编程、推理与评测</a></p>
</div>
