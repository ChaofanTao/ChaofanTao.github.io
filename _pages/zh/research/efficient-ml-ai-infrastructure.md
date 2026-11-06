---
layout: default
title: "高效机器学习与 AI 基础设施"
description: "从词表、压缩、缓存和训练系统出发，讨论长期协作项目的效率：计算开销、用户时间、验证成本，以及需求变化后的返工。"
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
  - 人机协作
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
  <p class="research-dek">如果智能体要和用户一起完成一个长期项目，效率就要算到最后：模型花了多少计算，用户投入了多少时间，需求变化后又有多少工作需要重做。这些问题把我过去的模型效率研究，与下一阶段的智能体系统连接起来。</p>
  <p class="research-meta">作者：<a href="{{ '/' | relative_url }}">陶超凡（Chaofan Tao）</a> · 最后更新 <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%Y-%m-%d" }}</time></p>

  <p>我的早期工作关注量化和剪枝：怎样让生成模型变小，同时尽量保留效果。后来研究词表、长上下文和智能体训练，问题逐渐连了起来。词表影响同样一段文本要处理多少 token；缓存影响过去的信息还剩多少；调度和故障恢复影响已经花掉的计算能否保留下来。</p>
  <p>这些工作没有一个通用的“越大越好”或“越少越好”的答案。更有用的做法，是先说明要保留什么能力，再找出计算、显存和时间具体花在了哪里。当任务延伸到从需求构建完整项目时，还需要把交流、验证和后续修改计入。这篇文章从已有工作出发，讨论怎样在给定质量要求下，降低持续完成项目的总成本。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/efficiency-lifecycle-zh.svg' | relative_url }}" alt="五类相互联系的效率问题：词表设计、模型压缩、上下文缓存、计算与服务，以及知识迁移。每一类都需要重新考虑资源如何分配。" width="960" height="300" loading="eager"></div>
    <figcaption>效率问题会沿着整个流程传递。一个环节省下的资源，只有在后续没有带来更大的损失时，才算真正节省。</figcaption>
  </figure>

  <p class="research-toc">本页内容：<a href="#design">词表设计</a> · <a href="#compress">模型压缩</a> · <a href="#remember">上下文与缓存</a> · <a href="#serve">训练与服务</a> · <a href="#transfer">知识蒸馏</a> · <a href="#long-horizon">长期协作的成本</a> · <a href="#insights">怎样衡量效率</a> · <a href="#open-questions">开放问题</a></p>

  <h2 id="design">1. 词表也在分配算力</h2>
  <p>比较两个模型处理了多少 token，前提是它们切分文本的方式可比。词表较大时，一段文本通常能切成更少的 token；但嵌入层和输出层也会变大，不常见的词条还需要足够数据才能学好。所以，词表大小与模型规模、数据量和计算预算应该一起考虑。</p>
  <p>在 <a href="https://arxiv.org/abs/2407.13623">Scaling Laws with Vocabulary</a> 中，我们把词表参数与网络其他参数分开，用字符数衡量数据量，并比较不同词表下的训练效果。一个具体结果是：在相同的 2.3 × 10<sup>21</sup> FLOPs 预算下，将词表从 32K 调整为 43K，ARC-Challenge 得分从 29.1 提高到 32.0。这个结果说明，预算的分配方式本身就会影响模型能力。</p>
  <p>论文给出的最优词表估计，基于其中的模型、数据和训练设置。它不等于今天所有模型都应该继续扩大词表。多语言、代码和工具调用会改变文本的分布；部署时，较大的输出层也有成本。<a href="https://huggingface.co/spaces/sail/scaling-with-vocab-demo">交互式计算器</a>适合作为设计起点，新的工作负载仍需要重新验证。</p>

  <h2 id="compress">2. 压缩之前，先看模型会失去什么</h2>
  <p>在 <a href="https://arxiv.org/abs/2203.10705">生成式预训练语言模型量化</a>工作中，我们研究了为什么对编码器有效的方法，直接用于生成模型时效果会明显下降。两个原因很关键：低精度下，不同词条的表示变得过于相似；不同模块的权重分布又有较大差别，统一的量化设置难以兼顾。</p>
  <p>对应的做法是，用 token 级对比蒸馏保留表示之间的区别，再为不同模块动态调整量化范围。这项工作获得了 ACL 2022 杰出论文奖。后续的<a href="https://aclanthology.org/2023.findings-acl.692/">结构化剪枝</a>进一步研究哪些网络结构可以删减，让可学习的掩码参与选择，而不只按固定比例裁剪。</p>
  <p>视觉语言模型里，资源也不适合平均分。<a href="https://arxiv.org/abs/2301.13741">UPop</a> 联合搜索视觉和语言部分的压缩比例，并逐步搜索、重新训练；<a href="https://arxiv.org/abs/2305.17455">CrossGET</a> 利用跨模态信息，在推理时合并相近的 token。这些方法处理的对象不同，共同关心的是怎样识别冗余，同时保留任务需要的差异。</p>
  <p>放到智能体上，还需要多问一步：压缩后的一点误差，会不会改变下一次工具调用？单轮回答的平均得分，可以用来筛选方案；但要确认实际收益，还应检查完整任务里的错误、重试和最终解决率。这是从已有压缩研究延伸出的评测要求，需要用交互任务来验证。</p>

  <h2 id="remember">3. 上下文很长，不代表关键证据还在</h2>
  <p>模型通过 KV 缓存保留先前 token 的中间表示，避免生成每个新 token 时都从头计算。长上下文会让这部分显存持续增长。<a href="https://arxiv.org/abs/2406.13035">D2O</a> 根据各层的注意力分布分配缓存预算，并通过相似度判断，对准备丢弃的信息进行召回或合并补偿。<a href="https://arxiv.org/abs/2410.03090">UNComp</a> 用矩阵熵分析信息分布，指导不同部分采用不同压缩程度。这些补偿机制有助于减少信息损失，并不意味着删掉的信息都能原样恢复。</p>
  <p><a href="https://arxiv.org/abs/2606.10537">Prefilling-dLLM</a> 面对的是扩散语言模型的重复计算：每轮去噪都重新处理长提示。它预先分块缓存，再选择与查询相关的块和 token 供解码使用。论文也分析了分块起始 token 对注意力的作用。这里节省的是重复读取前缀的计算，适用条件和自回归模型的缓存删减并不完全相同。</p>
  <p>智能体带来了一个更棘手的问题：当前看似无关的信息，可能在几十步后才有用。例如，一行测试输出排除了某个假设，之后保留这条依据，可能比保留很长的搜索结果更有价值。近期的 <a href="https://arxiv.org/abs/2609.31395">ActKV</a> 已经开始按信息对后续动作的作用来管理缓存；<a href="https://arxiv.org/abs/2610.28577">2026 年 10 月的 Cache Engineering for Agents</a> 则让智能体直接控制活跃缓存，并指出：经历不同缓存操作后，相同的 token 序列也可能对应不同的内部状态。</p>
  <p>这些新工作让早期缓存研究与智能体训练有了更直接的交点。如果运行时使用了缓存删减或位置调整，训练端只重放文本，是否还对应同一个策略？这是一个需要重新检查的问题，不能由已有的 token 对齐结果直接推出答案。</p>

  <h2 id="serve">4. 一次训练有多少时间，真正花在了模型更新上？</h2>
  <p><a href="https://www.legox.net/blog/lego-rl/">Lego-RL 的时间分析</a>中，一次 OpenHands SDK 尝试平均约 920 秒，91.3% 花在智能体执行阶段。这里同时包含模型推理和工具交互，不能理解成九成时间都在等待工具。重要的是，每次尝试长短不一，同步批次会被最慢的一项拖住；异步调度可以让空出的执行位置继续接收任务。</p>
  <p>异步也有代价：一条操作记录完成时，训练参数可能已经更新。调度需要控制记录与当前策略之间的差距；部分生成的暂停和恢复，则需要保存正确的状态。Lego-RL 报告的原始单步加速为 2.5 倍，校正两组 GPU 计算吞吐差异后，调度带来的加速估计约为 1.9 倍。把这两种比较分开，才能看清收益来自哪里。</p>
  <p><a href="https://www.legox.net/blog/lego-rl-sao/">单轨迹异步优化（SAO）</a>尝试减少另一笔成本：同一道题不必采样一组尝试，再相互比较，而是训练一个价值模型来提供基线。在报告的实验中，SAO 到自身最佳检查点使用的轨迹比 GSPO 少 73.7%，但 Verified 得分也从 GSPO 的 70.4% 变为 68.6%。这是有意义的成本与效果取舍，不能写成“同等准确率下省了 73.7%”。价值模型自身的计算和训练也需要计入。</p>
  <p>推理服务中有类似的取舍。<a href="https://arxiv.org/abs/2509.15148">ATTS</a> 针对草稿模型与目标模型之间的同步开销，利用在线校准和共形预测安排异步推理；统计控制的是相应的拒绝过程，并非保证任意输出都正确。<a href="https://arxiv.org/abs/2511.11617">AnchorTP</a> 则关注故障发生之后：通过独立进程保留可用 GPU 上的状态，调整张量并行的分配，并减少恢复时的数据搬运。它研究的是相应故障场景下的恢复，不是所有硬件故障下都能无损继续。</p>
  <p>这些结果让我更愿意把调度、缓存和可靠性一起看。减少等待很有价值，保存已经完成的工作也有价值；但前提是奖励、状态和策略更新仍然可信。更快地产生一批无法使用的训练记录，并不会让学习更高效。</p>

  <h2 id="transfer">5. 蒸馏要看学生学到了多少</h2>
  <p>知识蒸馏把教师的能力传给学生，但教师给出的内容要适合学生学习。<a href="https://arxiv.org/abs/2404.02657">我们对前向与反向 KL 散度的研究</a>发现，在所研究的蒸馏设置中，两者充分训练后趋向相同目标，实际差异更多体现在有限训练预算下：前向 KL 早期更关注高概率部分，反向 KL 更关注低概率部分。自适应 KL 据此调整两者的权重。</p>
  <p><a href="https://arxiv.org/abs/2510.10925">PerSyn</a> 把选择提前到数据生成之前：根据问题和学生的学习能力，先分配教师，再让教师生成相应数据，减少“所有教师都回答一遍，最后再筛选”的开销。与 <a href="{{ '/zh/research/agentic-intelligence/#experience' | relative_url }}">Terminal-Lego 的示范选择</a>放在一起看，一个值得继续检验的方向是：数据的价值，应由学生学完后的改善来衡量，而不能只看教师的排名或答案看起来有多完整。</p>

  <h2 id="long-horizon">6. 长期项目里，还要算上用户的时间</h2>
  <p>在完整项目中，一次模型请求便宜，并不意味着整个流程便宜。<a href="https://arxiv.org/abs/2610.09633">2026 年 10 月关于真实用户任务流程的研究</a>发现，真实会话会在问答、规划、执行、重构和审查之间切换；其 SWE-TaskFlow 试验中，把任务改为多步互动后，成本约翻倍，却没有稳定的解决率提升。这是特定试验的结果，但足以提醒我们：增加互动步骤不会自动带来更好的协作。</p>
  <p>下一步值得衡量三类不同的成本：模型与工具的计算开销、用户等待和参与的时间，以及需求变化后的返工。它们不必合成一个分数。少问一个关键问题可能节省一轮对话，却让后续实现全部重来；过早打断用户，也可能把智能体自己能查清的事情转嫁给人。比较方案时，需要固定最终质量与用户时间预算，再看计算和返工的变化。</p>
  <p>这也会改变记忆和恢复的设计目标。长期任务需要保留用户已经确认的要求、重要设计决定及其依据，并把测试结果对应到当时的代码版本。中断后恢复的不只是模型生成，还包括仓库状态、依赖环境和未完成的工作。AnchorTP 研究的是推理服务恢复，这里还需要项目层面的持久记录；两者不能直接画等号。</p>
  <p>我倾向于把阶段性验证也看成一种资源分配：尽早检查安装、模块间接口和主要功能，可能比完成全部代码后再集中检查更早发现方向错误。但检查也有成本。哪些节点值得验证、哪些决定值得请用户确认，以及缓存应该优先保留什么，都需要在长期项目中一起测量。</p>

  <h2 id="insights">我会怎样衡量下一步的效率改进</h2>
  <p>对一组固定任务，可以把所有尝试消耗的模型、工具、验证与恢复成本加起来，再除以通过独立检查的完成数。失败尝试也应计入；完成耗时、用户实际参与时间和后续修改成本则另行报告，避免把省算力、缩短等待和减少人工负担混为一谈。这个衡量方式是对上述工作的综合思考，并非这些论文已经统一采用的指标。</p>
  <ol class="research-insights">
    <li><strong>比较相同交付要求下的成本。</strong>如果一个方案更快却漏掉关键需求，就需要报告完整的取舍。SAO 的样本节省、缓存压缩的显存节省，都应与完整验收、旧功能保留和下一次修改的成本放在一起看。</li>
    <li><strong>让局部优化接受完整流程的检查。</strong>缓存压缩可能减少显存，却增加重新读取和重试；更密集的审查会增加单次开销，也可能减少后续失败。哪一种更划算，需要在相同任务、预算和评分规则下测量。</li>
    <li><strong>把运行状态纳入训练的一致性检查。</strong>文本、模型权重、缓存状态和工具环境共同影响下一步动作。近期缓存研究提出的新接口，也意味着训练和服务两端需要共同验证，而不能各自只检查本地是否更快。</li>
  </ol>

  <h2 id="open-questions">还想继续弄清楚的问题</h2>
  <ul>
    <li>把多语言、代码、工具输出和推理成本一起考虑时，词表应该怎样重新选择？</li>
    <li>长任务中，能否围绕已经验证的事实、尚未排除的假设和失败记录来管理记忆，而不只按 token 的近期使用情况删减？</li>
    <li>怎样在计算预算和用户参与时间都有限的情况下，安排澄清、实现与检查，让更多项目达到可交付状态？</li>
  </ul>

  <p class="research-readmore">复现与延伸阅读：<a href="https://github.com/sail-sg/scaling-with-vocab">词表研究代码</a> · <a href="https://huggingface.co/spaces/sail/scaling-with-vocab-demo">词表计算器</a> · <a href="https://github.com/LegoX/Lego-RL">Lego-RL 代码</a> · <a href="https://www.legox.net/blog/lego-rl-sao/">SAO 实验与取舍</a></p>

{% include research/paper-list.liquid group="efficient" lang="zh" %}

  <p>相关页面：<a href="{{ '/zh/research/agentic-intelligence/' | relative_url }}">智能体编程、推理与评测</a></p>
</div>
