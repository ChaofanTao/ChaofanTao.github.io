---
layout: default
title: "高效机器学习与 AI 基础设施"
description: "陶超凡在高效机器学习与 AI 基础设施方向的研究：量化与剪枝、词表扩展定律、KV 缓存压缩、快速的推理时扩展、知识蒸馏、稳定的训练与部署，以及他对大规模智能体数据基础设施和按任务轨迹衡量效率的判断。"
permalink: /zh/research/efficient-ml-ai-infrastructure/
research_lang: zh
last_modified_at: 2026-11-09
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
  - 智能体数据基础设施
  - AI 改进 AI
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
  <p class="research-dek">在我看来，效率就是留下真正重要的信息，去掉不必要的计算。我在这个方向的工作从压缩语言模型开始，逐渐走向训练智能体的系统。到了智能体时代，我认为衡量效率的单位不再是一次前向计算，而是一整条任务轨迹；生产智能体数据的基础设施，也变得和模型本身一样重要。</p>
  <p class="research-meta">作者：<a href="{{ '/' | relative_url }}">陶超凡（Chaofan Tao）</a> · 最后更新 <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%Y-%m-%d" }}</time></p>

  <p>我的大部分效率工作都是这样开始的：一个现有方法不好用，或者浪费资源，真正有价值的问题是“为什么”。答案往往是某个悄悄不再成立的假设：分词器可以在扩大模型之前就定下来；网络的每个部分对压缩的承受能力都一样；缓存里的每个 token 都重要；等待同步不花成本；GPU 不会坏；最强的老师教得最好。一旦弄清是哪个假设出了问题，解决办法往往很简单。</p>
  <p>这篇文章沿着模型的“一生”梳理这些问题，从设计、压缩、记忆、部署到知识迁移，最后落到训练智能体的基础设施上。我认为，最重要的效率问题现在正出现在最后这一部分。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/efficiency-lifecycle-zh.svg' | relative_url }}" alt="模型一生五个阶段的示意图：设计、压缩、记忆、计算与服务、迁移，每个阶段对应一个核心问题及相关项目。" width="960" height="300" loading="eager"></div>
    <figcaption>模型一生中的效率问题。每个阶段对应一个核心问题，以及回答它的工作。</figcaption>
  </figure>

  <p class="research-toc">本页内容：<a href="#compress">表示与压缩</a> · <a href="#remember">记忆与推理</a> · <a href="#transfer">知识迁移</a> · <a href="#serve">系统与稳定性</a> · <a href="#at-a-glance">一览</a> · <a href="#lessons">我们的体会</a> · <a href="#outlook">我对接下来的判断</a> · <a href="#open-questions">还没解决的问题</a></p>

  <h2 id="compress">1. 表示与压缩</h2>
  <p>我在这个方向的工作，是从<a href="https://arxiv.org/abs/2203.10705">量化生成式语言模型</a>开始的，这项工作获得了 ACL 2022 杰出论文奖。对 BERT 这类编码器很好用的量化方法，用到 GPT 这类生成模型上就不灵了，而且当时说不清为什么。我们找到了两个原因：一是在低精度下，词嵌入会挤成一团、变得几乎一样，模型在挑下一个 token 时就分不清这些选项；二是不同模块的权重分布差别很大，一套量化设置照顾不到所有模块。对应的办法是：用 token 级的对比蒸馏让每个 token 的表示保持区分度，用按模块的动态缩放给每个模块单独设定范围。比起方法本身，更重要的是这个诊断，它解释了为什么生成任务比分类任务更难压缩。</p>
  <p><a href="https://doi.org/10.18653/v1/2023.findings-acl.692">生成模型的结构化剪枝</a>把同样的思路用在“删减”上，让模型学出哪些部分可以去掉。对视觉语言模型来说，图像和文字承载信息的方式差别很大：<a href="https://arxiv.org/abs/2301.13741">UPop</a> 在视觉和语言两部分一起寻找更小的网络，让模型自己学出每部分该剪多少；<a href="https://arxiv.org/abs/2305.17455">CrossGET</a> 在模型运行时合并重复的 token，用一种模态的信息指导另一种模态的合并。</p>
  <p>词表是一个不太容易想到的地方。扩展定律通常不考虑词表，所以规模差不多的模型，词表大小却相差很大。在 <a href="https://arxiv.org/abs/2407.13623">Scaling Laws with Vocabulary</a>（NeurIPS）里，我们把词表大小当作一个独立的扩展维度来研究。三种互相独立的估计方法结论一致：最合适的词表随算力增长，但增长得比模型其他部分慢，而大多数模型的词表都偏小了。原因在于取舍：词表越大，同样的文本用的 token 越少；但算力有限时，那些不常见的 token 根本练不好。这为近年模型普遍采用更大词表提供了有依据的解释，<a href="https://huggingface.co/spaces/sail/scaling-with-vocab-demo">交互式计算器</a>也能直接帮你选出合适的大小。</p>

  <h2 id="remember">2. 记忆与推理</h2>
  <p>做长上下文推理时，KV 缓存很快会占掉大部分显存，而平均地删减很浪费，因为不同层的情况不一样。<a href="https://arxiv.org/abs/2406.13035">D2O</a> 根据每一层注意力的集中程度分配缓存额度；删掉的 token 如果和保留下来的很像，还能找回来或合并进去，整个过程不需要微调。<a href="https://arxiv.org/abs/2410.03090">UNComp</a> 从信息量的角度看同一个问题，用矩阵熵找出可以压缩的部分；同样的分析还能指出哪些注意力头和层负责“查找”信息。扩散语言模型每一步去噪都要把整段提示重新读一遍，<a href="https://arxiv.org/abs/2606.10537">Prefilling-dLLM</a> 把提示分块缓存一次，之后只用相关的块。这里有个小细节很关键：在每一块开头放一个序列起始 token（BOS），让注意力有个稳定的“落脚点”，有了它，稀疏的做法甚至能比完整的注意力效果更好。</p>
  <p>推理时扩展是在生成时多花算力来提升答案质量，常见做法是小模型先写草稿、大模型来检查。在 <a href="https://arxiv.org/abs/2509.15148">ATTS</a> 里，我们仔细测了时间都花在哪儿，发现主要成本是等待同步，而不是计算本身。ATTS 把同步检查改成异步推理，并用边运行边校准的共性预测（conformal prediction），把草稿被拒绝的比例控制在统计上可靠的范围内。</p>

  <h2 id="transfer">3. 知识迁移：为学生找到合适的老师</h2>
  <p>知识蒸馏是把老师的能力传给更小的学生。常见的说法是：前向 KL 会尽量覆盖老师的所有可能答案，反向 KL 则只盯着最主要的那个。<a href="https://arxiv.org/abs/2404.02657">我们发现</a>，在大模型蒸馏里这两种现象其实都没有出现，两者的最优解是一样的；真正的区别出现在训练早期，前向 KL 更关注老师最常给出的 token，反向 KL 更关注不常见的那些。自适应 KL 就按这个规律给两者分配权重。<a href="https://arxiv.org/abs/2510.10925">PerSyn</a> 的出发点是“更强的模型不一定是更好的老师”：在生成数据之前，先为每个问题挑出最适合这个学生的老师。能传下去什么，取决于学生能吸收什么，这一点在我们的<a href="{{ '/zh/research/agentic-intelligence/#data' | relative_url }}">智能体轨迹工作</a>里再次出现。</p>

  <h2 id="serve">4. 系统与稳定性</h2>
  <p>部署服务还藏着一个假设：GPU 不会坏。在多卡张量并行里，坏一张卡就可能让整个服务停掉。<a href="https://arxiv.org/abs/2511.11617">AnchorTP</a> 把权重和 KV 缓存放在一个独立的进程里，推理进程崩溃了它也还在；然后把模型重新分配到剩下的 GPU 上，并规划出恢复所需的最少数据搬运。</p>
  <p>训练智能体时，“等待”和“丢失状态”这两个问题表现得更加明显。在 <a href="https://www.legox.net/blog/lego-rl/">Lego-RL</a> 里，一次训练尝试几乎全部时间都是智能体在沙箱里干活，而且每次尝试长短差别很大，同步训练的一批总得等最慢的那个；异步调度就能把这些空档填上。如果训练途中权重更新了，部分 rollout 会先暂停生成、加载新权重，再接着缓存的内容继续，长时间的尝试就不会白费。启动沙箱的时间主要花在构建镜像上，预先构建任务镜像、按需拉取镜像省掉了大部分等待；而评分工具则有意内置在每个镜像里，因为能复现的奖励比快一点拿到的奖励更有价值。看板会拆解每次尝试是怎么结束的，帮我们在误读奖励曲线之前，先分清是基础设施出了问题还是模型本身的问题。<a href="https://www.legox.net/blog/lego-rl-sao/">单 rollout 优化</a>则从另一个角度降低成本：用一个学出来的 critic 代替对同一任务的反复采样，训练所需的轨迹大大减少。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/legox/lego-rl-workflow.png' | relative_url }}" alt="Lego-RL 闭环训练流程：数据准备（沙箱管理、镜像缓存、按需拉取、防作弊）、运行前校验、训练（沙箱执行、进程内代理、rollout 与训练器）、实时看板（失败原因拆解、轨迹查看）以及人工复核。" width="1600" height="878" loading="lazy"></div>
    <figcaption>Lego-RL 的工作流程：从数据准备、沙箱管理，到实时的失败诊断和人工复核。图片来自 <a href="https://www.legox.net/blog/lego-rl/">Lego-RL 博客</a>。</figcaption>
  </figure>

  <h2 id="at-a-glance">一览</h2>
  <div class="research-table-wrap">
    <table>
      <thead><tr><th>不再成立的假设</th><th>工作</th><th>诊断</th><th>解法</th></tr></thead>
      <tbody>
        <tr><td>分词器可以在扩大模型前定下来</td><td>词表扩展定律</td><td>最合适的词表随算力增长，但比模型其他部分慢</td><td>根据算力预算预测词表大小</td></tr>
        <tr><td>每个部分对低精度的承受能力一样</td><td>量化（ACL 2022 杰出论文）</td><td>词嵌入挤成一团；各模块权重分布差异大</td><td>token 级对比蒸馏；按模块动态缩放</td></tr>
        <tr><td>结构可以统一地剪</td><td>结构化剪枝 · UPop</td><td>不同组件、不同模态能承受的删减程度不同</td><td>可学习的掩码；按模态学习剪枝比例</td></tr>
        <tr><td>每个视觉 token 都必不可少</td><td>CrossGET</td><td>跨模态存在大量重复 token</td><td>跨模态引导的 token 合并</td></tr>
        <tr><td>缓存里每个 token 同样重要</td><td>D2O · UNComp</td><td>不同层、不同注意力头需要的信息不同</td><td>按层分配额度并可召回；按熵引导压缩</td></tr>
        <tr><td>每一步都要重读整段提示</td><td>Prefilling-dLLM</td><td>扩散模型在前缀上重复计算</td><td>分块缓存，加上序列起始 token 作锚点</td></tr>
        <tr><td>同步没有成本</td><td>ATTS</td><td>推理时扩展的主要开销是等待</td><td>基于共性预测的异步推理</td></tr>
        <tr><td>GPU 不会坏</td><td>AnchorTP</td><td>坏一张卡就会让整个服务停掉</td><td>状态放在进程之外；最少数据搬运恢复</td></tr>
        <tr><td>前向和反向 KL 表现不同</td><td>自适应 KL</td><td>最优解相同，只在训练早期侧重头部或尾部</td><td>自适应地为两者分配权重</td></tr>
        <tr><td>最强的老师教得最好</td><td>PerSyn</td><td>关键在于学生能学会什么</td><td>为每个问题挑选最合适的老师</td></tr>
        <tr><td>智能体 RL 的瓶颈在优化器</td><td>Lego-RL 基础设施</td><td>大部分时间花在智能体干活和等待上</td><td>异步调度、部分 rollout、预构建镜像</td></tr>
      </tbody>
    </table>
  </div>

  <h2 id="lessons">我们的体会</h2>
  <ol class="research-insights">
    <li><strong>先找出那个不成立的假设，再动手优化。</strong>这里的每个结果，都是从追问“现有方法为什么不行”开始的。原因一旦弄清楚，解决办法往往很简单。</li>
    <li><strong>不均匀才是常态。</strong>层、模块、模态、token、老师各不相同，按需分别分配资源，一次次见效。</li>
    <li><strong>给自己留条后路。</strong>删掉的 token 还能找回来、崩溃后状态还在、权重更新时尝试不中断，这些设计让大胆的优化变得安全。</li>
    <li><strong>规模越大，等待越是真正的成本。</strong>无论是推理时扩展、部署服务还是智能体训练，最大的收益都来自减少等待，而不是算得更快。</li>
    <li><strong>效率决定了模型能学会什么。</strong>算力不够、练不好的罕见 token，学生消化不了的老师输出，都说明效率关乎能力，而不只是成本。</li>
  </ol>

  <h2 id="outlook">我对接下来的判断</h2>

  <h3 id="agentic-data">大规模智能体数据的基础设施，是新的瓶颈</h3>
  <p>对语言模型来说，数据就是文本；对智能体来说，数据是可以运行、并且能检验结果的环境，而大规模生产这样的数据，主要是一个基础设施问题。做 LegoFlow 和 Terminal-Lego 让我们看清了成本花在哪里：找候选任务很便宜，真正费力的是搭建运行环境、用测试证明每个任务成立、生成轨迹，再筛掉有答案泄露或推理太浅的那些，最后只有一小部分候选能留下来。我认为智能体数据的扩展单位，是“经过验证、可以复现的环境”，衡量基础设施的标准，是单位算力下能搭建、验证并保持干净的环境有多少。这需要快速的环境构建和缓存、隔离且可控网络的沙箱、每个任务和轨迹都能追溯来源，以及让智能体自己就能操作的数据流水线，LegoFlow 的模块化设计已经朝这个方向迈出了一步。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/agentic-data-pipeline-zh.svg' | relative_url }}" alt="从候选任务到训练数据的流水线：搭建环境、验证任务、生成轨迹、筛掉答案泄露和推理过浅的轨迹；每一步留下的都更少，大部分成本集中在中间几步，由 LegoFlow 的 Curator 和 Tracer 负责。" width="960" height="340" loading="lazy"></div>
    <figcaption>智能体数据的成本花在哪里。找候选任务很便宜，真正费力的是搭环境、验证、生成轨迹和筛选。</figcaption>
  </figure>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/legox/terminal-lego-pipeline.png' | relative_url }}" alt="Terminal-Lego 任务构建流程：筛选高质量的 Stack Overflow 问答，依次生成指令、环境、解答、Dockerfile 和测试，审查测试，再通过 Docker 往返验证，只保留通过验证的任务。" width="1600" height="892" loading="lazy"></div>
    <figcaption>一个具体例子：Terminal-Lego 只有在完整的 Docker 往返验证通过后，才保留一个任务。图片来自 <a href="https://www.legox.net/blog/terminal-lego/">Terminal-Lego 博客</a>。</figcaption>
  </figure>
  <p>软件工程是最容易的情况，因为测试能给出清晰的信号。下一波智能体数据会来自协作办公，我把它叫作 cowork 数据：文档、表格、邮件和跨多个应用的工作流程，而且常常有人参与其中。在这些场景里，判断任务是否完成要难得多。它需要状态可以检查的模拟应用、反应真实的模拟用户，以及能判断“做得好不好”而不只是“做没做完”的检查器。我认为，真正拥有好的智能体数据的，会是那些建好了这套基础设施的团队，而不是手里原始日志最多的团队。</p>

  <div class="research-table-wrap">
    <table>
      <thead><tr><th></th><th>代码数据</th><th>cowork 数据</th></tr></thead>
      <tbody>
        <tr><td>环境</td><td>容器里的代码仓库快照</td><td>文档、表格、邮件和多个应用，常常有人参与其中</td></tr>
        <tr><td>如何检验结果</td><td>测试：原代码不通过，修复后通过</td><td>可检查的应用状态，加上对完成质量的判断；通常没有单元测试</td></tr>
        <tr><td>主要难点</td><td>答案泄露、大规模搭建环境、推理过浅的轨迹</td><td>模拟应用和人；判断“做得好不好”，而不只是“做没做完”</td></tr>
        <tr><td>需要的基础设施</td><td>快速构建与缓存、隔离沙箱、防泄露、来源可追溯</td><td>状态可检查的模拟应用、模拟用户、质量检查器、可回放的会话</td></tr>
      </tbody>
    </table>
  </div>

  <h3 id="trajectory-efficiency">效率应该按整条轨迹衡量，而不是按单次调用</h3>
  <p>大多数效率方法，包括我们的不少工作，都是按单次回答来评估的。但对智能体来说，一次压缩或缓存决策如果丢掉了一个细节，后面可能要多走好几步，省下的成本也就没了。我认为，智能体的效率要在整个任务的层面衡量：得到一个经过验证的结果，总共花了多少算力、显存和时间。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/trajectory-efficiency-zh.svg' | relative_url }}" alt="两条轨迹对比：保留完整上下文时，智能体几步就得到经过验证的结果；上下文丢了一个细节时，每次调用更便宜，但要多走几步去重读、重试、重新测试，整体更慢也更贵。" width="900" height="300" loading="lazy"></div>
    <figcaption>单次省下的成本，整体上又亏了回去。智能体的效率要按得到验证结果的整条轨迹来衡量。</figcaption>
  </figure>

  <p>这也改变了记忆应该保留什么。智能体的上下文里大部分是工具输出而不是普通文字，所以 D2O 和 UNComp 背后的思路，即留下后续步骤会用到的信息、给删掉的内容留一条退路，应该用到观察结果和动作上，而不只是 token 上。</p>

  <h3 id="ai-for-ai-compute">在 AI 改进 AI 的循环里，算力应该更多地流向验证</h3>
  <p>当 AI 帮助改进 AI 时，每一轮都要把算力花在提出候选、运行候选、检验候选和确认最终结果上。我们在智能体方面的工作表明，可靠与否往往取决于检验这一步。所以我认为，这类循环的效率问题，与其说是“候选能生成多快”，不如说是“要花多少成本才能相信一个结果”。更便宜的审查者和验证器，比如 SWE-Review 和 SWE-Lego 的验证器所指向的那种，很可能是最大的杠杆。各轮之间的进展也应该在相同的总预算下比较，把失败的尝试和复现都算进去，免得把“花得更多”误当成“循环变好了”。</p>

  <h3 id="long-runs">长时间运行的任务，需要和部署服务一样的稳定性</h3>
  <p>智能体训练和自主实验往往要跑上好几天，涉及成千上万个沙箱。让部署服务变稳的那些做法，比如把状态和可能崩溃的进程分开、用最少的数据搬运完成恢复，也应该成为这类长时间任务的标配；同时还需要足够精确的记录，让实验在出故障后能够接着跑，结果也依然可信。</p>

  <h2 id="open-questions">还没解决的问题</h2>
  <ul>
    <li>协作办公场景下，经过验证、可以复现的环境应该是什么样子？没有单元测试的任务，结果要怎么检验？</li>
    <li>对于上下文大多是工具输出的智能体，词表和缓存应该怎样设计？</li>
    <li>智能体 RL 的成本，靠更好的调度和更少的 rollout 能省掉多少，才会开始损失能力？</li>
    <li>一个 AI 改进 AI 的循环，应该怎样在探索和验证之间分配预算？</li>
  </ul>

  <p class="research-readmore">代码与实验：<a href="https://github.com/sail-sg/scaling-with-vocab">词表研究</a> · <a href="https://huggingface.co/spaces/sail/scaling-with-vocab-demo">词表计算器</a> · <a href="https://github.com/LegoX/Lego-RL">Lego-RL</a> · <a href="https://github.com/LegoX/LegoFlow">LegoFlow</a></p>

  {% include research/paper-list.liquid group="efficient" lang="zh" %}

  <p>相关页面：<a href="{{ '/zh/research/agentic-intelligence/' | relative_url }}">智能体的学习、协作与自我改进</a></p>
</div>
