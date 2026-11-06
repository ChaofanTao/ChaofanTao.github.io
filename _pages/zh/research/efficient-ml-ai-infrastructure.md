---
layout: default
title: "高效机器学习与 AI 基础设施"
description: "从量化、剪枝、词表和知识蒸馏到训练与推理系统，讨论高效学习，以及支持多智能体探索、AI for AI 和自我改进的基础设施。"
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
  - 长期任务
  - 多智能体协作
  - AI for AI
  - 递归自我改进
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
  <p class="research-dek">模型变小、生成变快之后，省下来的资源能用来做什么？可以多试几条思路、多做一次复验，也可能让原本做不起的训练成为可能。沿着模型压缩、词表、缓存和训练系统这些工作，效率问题逐渐连到了自主探索与 AI for AI。</p>
  <p class="research-meta">作者：<a href="{{ '/' | relative_url }}">陶超凡（Chaofan Tao）</a> · 最后更新 <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%Y-%m-%d" }}</time></p>

  <p>我的早期工作关注量化和剪枝，后来又研究词表、长上下文、知识蒸馏，以及训练和推理系统。这些工作跨越不同阶段和合作团队，也逐渐形成了一条共同的问题线索：哪些计算真正带来了能力，哪些信息必须保留，哪些重复工作可以省下来。</p>
  <p>当智能体开始长时间地试验，甚至参与改进 AI 系统，这些选择会累积起来。单次推理省一点显存，可能让更多候选同时运行；一次错误的压缩，也可能让后面十几步都建立在不完整的信息上。理解这种前后关系，有助于把局部的效率改进放回整个研究过程来看。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/efficiency-lifecycle-zh.svg' | relative_url }}" alt="词表设计、模型压缩、上下文缓存、计算与服务、知识迁移五类效率问题及相关工作。" width="960" height="300" loading="eager"></div>
    <figcaption>从模型表示到系统运行，每一步都在决定有限资源能够换来多少有效学习与探索。</figcaption>
  </figure>

  <p class="research-toc">本页内容：<a href="#design">词表</a> · <a href="#compress">压缩</a> · <a href="#remember">记忆与缓存</a> · <a href="#serve">训练与服务</a> · <a href="#transfer">能力迁移</a> · <a href="#long-horizon">自主研究的成本</a> · <a href="#insights">怎样比较进步</a> · <a href="#open-questions">开放问题</a></p>

  <h2 id="design">同样的文本，为什么要花不同的计算</h2>
  <p>一段文本切成多少 token，会影响模型需要处理多长的序列。词表较大时，序列通常更短，但嵌入层和输出层会变大，少见词条也需要足够数据才能学好。所以词表大小值得和模型规模、数据量一起考虑。</p>
  <p>在 <a href="https://arxiv.org/abs/2407.13623">Scaling Laws with Vocabulary</a> 中，我们把词表参数与其他参数分开，用字符数比较不同分词方式下的数据量。在一组相同计算预算的实验里，词表从 32K 调整为 43K，ARC-Challenge 得分从 29.1 提高到 32.0。这是一个很直接的例子：重新分配已有预算，也能改变模型学到的能力。</p>
  <p>到了多语言、代码和工具调用场景，词条的使用频率和序列长度都会变化；训练时合适的选择，部署时还要考虑输出层的成本。能否把整个使用周期一起纳入词表设计，是这项工作自然延伸出的一个问题。<a href="https://huggingface.co/spaces/sail/scaling-with-vocab-demo">交互式计算器</a>给出了基于论文设置的估计，<a href="https://github.com/sail-sg/scaling-with-vocab">代码</a>也可以用来进一步检查这些取舍。</p>

  <h2 id="compress">压缩要保住哪些区别</h2>
  <p>在<a href="https://arxiv.org/abs/2203.10705">生成式语言模型量化</a>研究中，我们遇到的一个关键问题是：低精度会让不同词条的表示过于相似，模型挑选下一个 token 时需要的区别被削弱了。另一个问题来自不同模块的权重分布，一套统一设置难以兼顾。我们用 token 级对比蒸馏保留表示之间的区别，并按模块动态调整量化范围。这项工作获得了 ACL 2022 杰出论文奖。</p>
  <p>后续的<a href="https://aclanthology.org/2023.findings-acl.692/">结构化剪枝</a>让模型学习哪些部分可以删减。视觉语言模型中的 <a href="https://arxiv.org/abs/2301.13741">UPop</a> 联合安排不同模态的压缩比例，<a href="https://arxiv.org/abs/2305.17455">CrossGET</a> 则利用图像与文字之间的信息合并相近 token。它们都需要识别哪些差异对任务有用。</p>
  <p>如果被压缩的是一个会行动的模型，这个问题还会延伸到后续步骤。一次工具选择的变化，可能影响它接下来能看到什么信息。能否在完整任务中检查这种影响，而不只比较单次回答的平均分数？这样的评测可以帮助判断，省下的计算有没有被额外重试抵消。</p>

  <h2 id="remember">该记住的，可能只有一行</h2>
  <p>长记录里不一定每一段都同样有用。某次实验的失败原因可能只有一行，却能防止后续反复走同一条路；一份很长的日志，在问题定位之后可能只需要保留其中几个结果。困难在于，当前不显眼的信息，往往要过很多步才派上用场。</p>
  <p>KV 缓存保存先前 token 的中间表示，避免反复计算，但它会随上下文增长而占用更多显存。<a href="https://arxiv.org/abs/2406.13035">D2O</a> 按不同层的注意力分布分配预算，并通过召回或合并补偿减少丢弃信息的损失；<a href="https://arxiv.org/abs/2410.03090">UNComp</a> 用矩阵熵分析信息分布，指导不同部分的压缩程度。<a href="https://arxiv.org/abs/2606.10537">Prefilling-dLLM</a> 则针对扩散语言模型，在多轮去噪之间复用分块缓存，减少对长前缀的重复计算。</p>
  <p>近期的 <a href="https://arxiv.org/abs/2609.31395">ActKV</a> 已经按信息对后续动作的作用管理缓存。<a href="https://arxiv.org/abs/2610.28577">Cache Engineering for Agents</a> 更进一步，让智能体直接操作活跃缓存，并指出相同文本可能因缓存操作历史不同而对应不同内部状态。这给训练带来了一个具体问题：若运行时使用了这些操作，只重放文本，能否复现当时的决策条件？</p>
  <p>多智能体共享记忆时，还会遇到另一层困难。一条“方法 A 更好”的记录，可能只在某个数据集和实验设置下成立。能否把结论、依据和适用条件一起保留，并在条件变化后重新检查？这里既涉及模型内部的缓存，也涉及系统外部的实验记录，两者需要分别研究。</p>

  <h2 id="serve">跑得起来之后，还要能连续跑下去</h2>
  <p><a href="https://www.legox.net/blog/lego-rl/">Lego-RL 的时间分析</a>中，一次 OpenHands SDK 尝试平均约 920 秒，91.3% 花在包含模型推理与工具交互的执行阶段。各次尝试长短不同，同步批次会等最慢的那一个。异步调度可以填上这些空闲时间，但也要处理一个新问题：记录送到训练端时，模型参数可能已经更新了。</p>
  <p>这组实验的原始单步加速为 2.5 倍，校正两组 GPU 计算吞吐差异后，调度收益估计约为 1.9 倍。<a href="https://www.legox.net/blog/lego-rl-sao/">SAO</a> 则减少同一任务的重复采样，用价值模型提供训练基线：到各自最佳检查点的轨迹数比 GSPO 少 73.7%，对应的 Verified 得分分别为 68.6% 和 70.4%。这两组结果展示了不同的效率来源，也展示了成本和能力之间具体的取舍。</p>
  <p>推理服务中，<a href="https://arxiv.org/abs/2509.15148">ATTS</a> 通过在线校准和共形预测减少草稿模型与目标模型之间的同步等待；<a href="https://arxiv.org/abs/2511.11617">AnchorTP</a> 通过保留可用 GPU 状态、重新分配计算和减少数据搬运来加快故障恢复。到了自主研究任务，恢复还涉及实验做到哪一步、哪些结果仍然有效。模型服务恢复了，一项长实验是否也能从正确的位置继续，需要另外验证。</p>

  <h2 id="transfer">发现了更好的方法，怎样让它留下来</h2>
  <p>知识蒸馏研究怎样把教师的能力传给学生。我们对<a href="https://arxiv.org/abs/2404.02657">前向与反向 KL 散度</a>的研究发现，在所研究的设置里，两者充分训练后趋向相同目标，有限训练预算下的学习重点却不同：前者早期更关注高概率部分，后者更关注低概率部分。自适应 KL 据此调整两者的权重。</p>
  <p><a href="https://arxiv.org/abs/2510.10925">PerSyn</a> 在生成数据之前，先按问题和学生的学习能力选择教师，减少所有教师都回答一遍再筛选的开销。这与 <a href="{{ '/zh/research/agentic-intelligence/#experience' | relative_url }}">Terminal-Lego 的示范选择</a>形成了联系：有价值的经验，还需要以适合学习的方式留下来。</p>
  <p>如果多个智能体共同发现了一种更好的搜索或实验方法，下一代系统应该怎样继承它？保留代码、存成技能、蒸馏进模型，可能有不同的成本与适用范围。又怎样确认继承的是有效方法，而不只是某批任务的答案？这是效率研究可以进一步连接到自我改进的地方。</p>

  <h2 id="long-horizon">自主研究的算力，应该花在哪一步</h2>
  <p>一轮自主研究可能同时运行多个候选方案，还需要安排筛选、复验和后续训练。并行可以缩短等待，也可能带来重复计算和更昂贵的汇总。<a href="https://arxiv.org/abs/2610.00980">Can AI Scientists Coordinate at Runtime?</a> 的探索性实验就发现，动态选择成员有收益，但继续加入更复杂的协作与验证机制，并没有在其预算设置下稳定改善结果。怎样把有限资源分给探索与检查，本身就是需要学习和评测的问题。</p>
  <p><a href="https://arxiv.org/abs/2608.20318">AI4AI-Bench</a> 把改进对象推进到训练算法：让智能体修改学习方法，再从头运行并由隐藏评测器检查结果。这使两个问题更容易分开：程序是否运行得更快，以及模型是否学得更好。前者可能让同样时间内尝试更多方案，后者则可能改变相同计算量能够得到的能力。</p>
  <p><a href="https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/">AlphaEvolve</a> 在算法与计算基础设施上的工作，也说明 AI 产生的改进可以反馈到 AI 的运行过程。接下来的开放问题是：这些节省能否持续支持更多有效探索和独立复验，进一步提高下一轮发现改进的效率？这正是模型效率与递归自我改进（RSI）相交的地方。</p>
  <p>单个模块的加速倍数还不足以回答这个问题。需要把所有候选的生成、失败尝试、评测、复验和最终部署一起计入，并检查收益是否还能在新的任务或模型上保留。若每轮只是用更大预算挑出一个更好的候选，就需要与同预算、固定研究方法的搜索作比较，才能判断研究过程本身有没有改善。</p>

  <h2 id="insights">可以怎样比较不同层次的进步</h2>
  <div class="research-table-wrap">
    <table>
      <thead><tr><th>研究对象</th><th>需要一起观察</th></tr></thead>
      <tbody>
        <tr><td>模型的一次计算</td><td>相同任务质量下的计算量、显存和耗时</td></tr>
        <tr><td>一次完整探索</td><td>所有尝试与验证的总成本，以及完成任务的比例</td></tr>
        <tr><td>多轮自我改进</td><td>累计研究成本、留出任务上的收益，以及下一轮发现改进的效率</td></tr>
      </tbody>
    </table>
  </div>
  <p>这三层可以帮助区分局部加速、任务完成和研究能力的提升。第三层尤其需要谨慎设计实验：更好的最终分数，可能来自更多试验、对评测的适应，也可能来自可迁移的方法改进。怎样把它们分开，是一个比单独报告吞吐量更有挑战、也更值得研究的问题。</p>

  <h2 id="open-questions">还可以继续探索的问题</h2>
  <ul>
    <li>多个智能体能否共享可复用的计算和实验结果，同时避免过早放弃不同的探索路线？</li>
    <li>当模型权重、工具和缓存策略都在变化时，怎样保留足够信息，支持正确的训练、复验与恢复？</li>
    <li>在固定的累计预算下，系统能否一轮比一轮更有效地发现改进？这种收益能否跨模型、跨任务保留下来？</li>
  </ul>

  <p class="research-readmore">代码与实验：<a href="https://github.com/sail-sg/scaling-with-vocab">词表研究</a> · <a href="https://huggingface.co/spaces/sail/scaling-with-vocab-demo">词表计算器</a> · <a href="https://github.com/LegoX/Lego-RL">Lego-RL</a> · <a href="https://www.legox.net/blog/lego-rl-sao/">SAO 实验</a></p>

{% include research/paper-list.liquid group="efficient" lang="zh" %}

  <p>相关页面：<a href="{{ '/zh/research/agentic-intelligence/' | relative_url }}">智能体的学习、协作与自我改进</a></p>
</div>
