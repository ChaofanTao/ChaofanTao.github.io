---
layout: default
title: "智能体的学习、协作与自我改进"
description: "陶超凡在智能体方向的研究：在 LegoX 开源构建的代码智能体（可验证数据、真实 harness 中的 SFT 与 RL、智能体代码审查），多模态推理，以及他对超长程智能体、多智能体协作、可信评测、AI 改进 AI 和 AI for Science 的一些思考。"
permalink: /zh/research/agentic-intelligence/
research_lang: zh
last_modified_at: 2026-11-09
og_image: /assets/img/og-image.png
figure: /assets/img/research/agentic-loop-zh.svg
about:
  - 智能体
  - 代码智能体
  - 智能体强化学习
  - 智能体数据
  - 多模态推理
  - 智能体评测
  - 长程任务
  - 多智能体协作
  - AI 改进 AI
  - AI for Science
---

{% include research/styles.liquid %}
{% include research/jsonld.liquid group="agentic" %}

<div class="research-page" lang="zh-Hans">
  <nav class="research-breadcrumb" aria-label="面包屑导航">
    <a href="{{ '/' | relative_url }}">陶超凡</a><span aria-hidden="true">/</span>
    <a href="{{ '/zh/research/' | relative_url }}">研究方向</a><span aria-hidden="true">/</span>
    <span>智能体的学习、协作与自我改进</span>
    <span aria-hidden="true">·</span><a href="{{ '/research/agentic-intelligence/' | relative_url }}" lang="en">English</a>
  </nav>

  <h1>智能体的学习、协作与自我改进</h1>
  <p class="research-dek">智能体的本事不全在模型里，更在模型外面那一圈循环里：看清情况，动手去做，从结果里学，再接受检验。我们在 LegoX 为代码智能体开源搭建这个循环，多模态方向的工作则在检验：离开代码，这个循环还缺什么。这篇文章聊聊我们发现了什么，也谈谈我对接下来的一些想法。</p>
  <p class="research-meta">作者：<a href="{{ '/' | relative_url }}">陶超凡（Chaofan Tao）</a> · 最后更新 <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%Y-%m-%d" }}</time></p>

  <p>很长时间里，AI 的进步就是对一个固定的问题答得更好。智能体把问题本身变了：它得注意到要紧的细节，想好先试什么，动手，看懂返回的结果，再调整。每一步都可能单独出错，每一步要的证据也不一样：模型有没有看到该看的东西，它的动作是不是基于环境真实的反馈，它能不能从一次尝试里学到对的东西，还有，我们凭什么相信“它变强了”这个判断。</p>
  <p>代码智能体让我们能把这几件事放在一起研究。代码会留下每一步操作和每一个结果，测试又能给出可以核对的结论。在 <a href="https://www.legox.net/">LegoX</a>，我们把这个循环拆开，每一块都做成开放、可复用的组件：可验证的经验怎么收集，怎么变成训练信号，训练结果又怎么检验。多模态方向的工作，则是在图像、视频、网页和机器人这些环境里问同样的问题。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/agentic-loop-zh.svg' | relative_url }}" alt="智能体学习循环示意图：中间是由模型和 harness 组成的智能体，周围按顺时针连着环境、经验、信号、评测四个环节，每个环节旁标出了相关项目。图中所有项目均为陶超凡与合作者的工作。" width="760" height="505" loading="eager"></div>
    <figcaption>智能体的学习循环。一次尝试留下经验，训练把经验变成能力，评测再看这种能力能不能用到新任务上。</figcaption>
    <div class="research-works">
      <p class="research-works-note">图中所有工作均由陶超凡与合作者完成：</p>
      <p><strong>环境</strong>：<a href="https://arxiv.org/abs/2608.17393">Lego-RL</a><span class="research-venue">（arXiv 2026）</span> · <a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a><span class="research-venue">（ICLR 2026）</span> · <a href="https://arxiv.org/abs/2402.16117">RoboCodeX</a><span class="research-venue">（ICML 2024）</span></p>
      <p><strong>经验</strong>：<a href="https://www.legox.net/blog/legoflow/">LegoFlow</a><span class="research-venue">（LegoX 博客，2026）</span> · <a href="https://arxiv.org/abs/2601.01426">SWE-Lego</a><span class="research-venue">（arXiv 2026）</span> · <a href="https://arxiv.org/abs/2606.03461">Terminal-Lego</a><span class="research-venue">（arXiv 2026）</span></p>
      <p><strong>信号</strong>：SWE-Lego · Lego-RL · <a href="https://arxiv.org/abs/2601.18533">RLVRR</a><span class="research-venue">（ICLR 2026）</span> · <a href="https://arxiv.org/abs/2601.21968">OVD</a><span class="research-venue">（arXiv 2026）</span> · <a href="https://arxiv.org/abs/2506.01713">SRPO</a><span class="research-venue">（NeurIPS 2025）</span></p>
      <p><strong>评测</strong>：<a href="https://arxiv.org/abs/2505.23932">SwingArena</a><span class="research-venue">（ICLR 2026 Oral）</span> · <a href="https://arxiv.org/abs/2607.06065">SWE-Review</a><span class="research-venue">（arXiv 2026）</span> · <a href="https://arxiv.org/abs/2505.15929">PhyX</a><span class="research-venue">（TMLR 2026）</span></p>
    </div>
  </figure>

  <p class="research-toc">本页内容：<a href="#coding">把代码智能体当作实验室</a> · <a href="#multimodal">走出代码</a> · <a href="#at-a-glance">一览</a> · <a href="#lessons">我们的体会</a> · <a href="#outlook">对未来的一些思考</a> · <a href="#open-questions">还没解决的问题</a></p>

  <h2 id="coding">1. 把代码智能体当作实验室</h2>
  <p>代码智能体从来看不到代码仓库本身，它看到的是 harness 给它看的东西：哪些文件和工具输出会进上下文，历史什么时候被压缩，报错长什么样，命令失败以后接着怎么走。我们用 <a href="https://arxiv.org/abs/2608.17393">Lego-RL</a><span class="research-venue">（arXiv 2026）</span>把同一个初始模型分别放进三个常用的 harness（OpenHands、Claude Code、OpenCode），还没开始训练，它在三处的表现就已经不一样了。也就是说，harness 本身就是环境的一部分，不是模型外面的配套设施。这一点决定了我们后来怎么收数据、怎么训练、怎么检验。</p>

  <h3 id="data">数据：收集值得学的经验</h3>
  <p><a href="https://www.legox.net/blog/legoflow/">LegoFlow</a><span class="research-venue">（LegoX 博客，2026）</span>把代码数据工程拆成一串积木。Curator 去找已经合并的 PR，把对应的 issue、提交和测试收齐，改写成不会泄露答案的任务，搭好独立的运行环境，并且只留下“原代码测试不过、参考修复测试能过”的任务。但能过这一关只说明任务可用，所以 Curator 还会用一套固定规则给任务打难度分：补丁有多大，加了多少新逻辑，牵动了代码库多大范围，测试有多复杂，需求写得多细，全程不用 LLM 打分。Tracer 在沙箱里跑出轨迹并做筛选，Trainer 和 Evaluator 负责训练和评测。每块积木都封装成插件 skill，Claude Code、Codex 这样的代码智能体可以自己把整条流水线跑起来，每块积木也都有自己的看板。有一次实验，智能体从头到尾跑完整个流程，读完评测结果后发现不少老师轨迹的推理很浅，就改了筛选规则，下一轮训出来的模型明显更好。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/legox/legoflow-architecture.png' | relative_url }}" alt="LegoFlow 架构图：Root 模块统筹 Curator、Tracer、Trainer、Evaluator 四个模块，每个模块都以插件 skill 的形式提供并配有看板，分别产出任务、轨迹、模型和评测分数。" width="1600" height="766" loading="lazy"></div>
    <figcaption>LegoFlow 的各个模块，从构建任务到评测，每一步都可以交给代码智能体来操作。图片来自 <a href="https://www.legox.net/blog/legoflow/">LegoFlow 博客</a>。</figcaption>
  </figure>

  <p><a href="https://arxiv.org/abs/2601.01426">SWE-Lego</a><span class="research-venue">（arXiv 2026）</span>把两类任务放在一起用：一类来自真实的 PR，另一类是用 LLM 改写或语法树变换故意埋进 bug 造出来的。真实任务够真、够深，合成任务管够量；在同一批代码仓库上，加进合成任务会一直带来提升。<a href="https://arxiv.org/abs/2606.03461">Terminal-Lego</a><span class="research-venue">（arXiv 2026）</span>把同样严格的要求用到命令行任务上，把 Stack Overflow 上的问题做成经过 Docker 验证的任务。</p>
  <p>最要紧的经验，是关于该留哪些轨迹。Terminal-Lego 发现，最会解题的模型不一定是最好的老师，好老师是最适配学生能力的那一个：先观察、再根据看到的情况动手、最后检查结果的轨迹，教出来的学生比更强模型一步到位给出答案的轨迹更好。LegoFlow 发现，想得深比想得广更重要：每一步都浅浅想一下的老师，不如在关键处认真想的老师；而且大部分收益来自去掉最浅的那批轨迹，而不是只留最长的。SWE-Lego 还总结了几条很实用的清洗规则：修好格式出错的工具调用，工具集尽量精简，那些找对了文件却没改对的尝试也别扔，回收再用。</p>
  <p>经验还有个“老不老实”的问题。老师越强，越会走捷径：找到上游的 PR 直接抄补丁，或者从 Git 历史里翻出答案。成功的轨迹，不一定是老老实实做出来的。管用的办法是两层防护：一是在提示里明说不许去查现成答案；二是在环境里让它根本查不到，智能体干活时改写 Git 历史、藏起测试文件、限制网络，等到评分时才恢复。</p>

  <h3 id="learning">学习：把经验变成能力</h3>
  <p>SWE-Lego 说明，只要像打磨数据一样打磨损失函数，单靠 SFT 也能训出很强的开源代码智能体。错误掩码让模型看到包括错误在内的完整轨迹，但出错的那几步不算梯度，这样它能从错误里吃一堑长一智，又不会学着再犯。课程学习拿轨迹长度粗略代表难度，由易到难地训，后面阶段继续带着前面的数据。推理时多出来的算力，最好先花在多给几轮交互上，加到头了再用来并行多试几次；从几次尝试里挑结果时，直接用文字回答“是”或“否”的验证器，比打分头挑得更准。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/legox/swe-lego-error-masking.png' | relative_url }}" alt="SWE-Lego 错误掩码示意图：在一条智能体轨迹中，导致执行报错的那一步不参与损失计算，正确的步骤则正常更新梯度。" width="1600" height="878" loading="lazy"></div>
    <figcaption>SWE-Lego 的步骤级错误掩码：模型仍能看到出错的那一步和报错信息，只是不会被训练去模仿它。图片来自 <a href="https://www.legox.net/blog/swe-lego/">SWE-Lego 博客</a>。</figcaption>
  </figure>

  <p>强化学习这边，Lego-RL 直接在真实、原封不动的 harness 里训练。难就难在要保证训练时看到的，正是智能体当时真正做的。harness 会压缩上下文、重新序列化工具调用、跑子智能体，等于悄悄改写了自己的历史，所以存下来的对话记录并不等于当时实际采样出的 token 序列。我们用一个进程内代理在生成时就记下 token、概率和混合专家模型的路由，训练时再按原样回放路由。这类对不上的问题不会报任何错：训练照跑，曲线照动，所以必须专门去查。训练本身还教会我们两件事。模型总能做对或总做不对的任务，对它来说学不到任何东西，所以“跳一跳够得着”的难度区间要跟着模型的进步往上挪。奖励往下掉，也可能是解析器坏了或者环境没搭起来，不一定是模型变差了，所以把每次尝试为什么结束拆开来看的看板，是方法的一部分，不是锦上添花。训练之后，智能体改代码前会多读代码，改完会回头检查，也更常跑测试，代价是每次交互的时间更长。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/legox/lego-rl-infrastructure.png' | relative_url }}" alt="Lego-RL 训练架构图：未经修改的 harness 在沙箱中运行，进程内代理记录 token 和路由信息，rollout 引擎与训练器之间交换轨迹和权重，支持同步、异步和部分 rollout。" width="1600" height="992" loading="lazy"></div>
    <figcaption>Lego-RL 通过进程内代理，把原封不动的 harness 接到训练器上。图片来自 <a href="https://www.legox.net/blog/lego-rl/">Lego-RL 博客</a>。</figcaption>
  </figure>

  <p>在这个基础上又往前走了两步。<a href="https://www.legox.net/blog/lego-rl-cross-harness/">让一个模型同时在多个 harness 上训练</a><span class="research-venue">（LegoX 博客，2026）</span>，效果接近分开训练的平均水平，还缩小了不同 harness 之间的一部分差距。<a href="https://www.legox.net/blog/lego-rl-sao/">单 rollout 优化</a><span class="research-venue">（LegoX 博客，2026）</span>借助一个学出来的 critic，每个任务只试一次就能学，省掉了大部分采样；前提是 critic 要先充分“热身”，优势值也要做好归一化，不然模型会退化成一遍遍调用 think 工具。对于没有唯一标准答案的任务，<a href="https://arxiv.org/abs/2601.18533">RLVRR</a><span class="research-venue">（ICLR 2026）</span>从优质参考答案里构造一串兼顾内容和风格的奖励；<a href="https://arxiv.org/abs/2601.21968">OVD</a><span class="research-venue">（arXiv 2026）</span>则让老师对学生写了一半的回答给出文字点评，好的开头留下，写差的后半段换掉。</p>

  <h3 id="checking">检验：审查与评测</h3>
  <p><a href="https://arxiv.org/abs/2607.06065">SWE-Review</a><span class="research-venue">（arXiv 2026）</span>训练了一个审查智能体：它自己去翻代码仓库，找出问题的根源，再拿去和提交的补丁对照，写出有条理的反馈，把“一次写完就交”变成“写、审、改”。有两个结论不止对这篇论文有意义：审查数据反过来也能让模型更会修 bug；从几次尝试里挑一个，比再多生成很多次便宜，所以好的审查者能让推理时的算力更值钱。<a href="https://arxiv.org/abs/2505.23932">SwingArena</a><span class="research-venue">（ICLR 2026 Oral）</span>把模型放进持续集成流程，让它们在多种编程语言里轮流提交补丁、编写测试；<a href="https://arxiv.org/abs/2604.06861">REAgent</a><span class="research-venue">（ICSE 2027）</span>则在写补丁之前，先检查并补全 issue 描述本身。</p>
  <p class="research-readmore">延伸阅读：<a href="https://www.legox.net/blog/legoflow-experiments/">LegoFlow-SWE 的经验总结</a> · <a href="https://www.legox.net/blog/lego-rl/">Lego-RL 博客</a> · <a href="https://www.legox.net/blog/swe-review/">SWE-Review 博客</a></p>

  <h2 id="multimodal">2. 走出代码：多模态推理与真实世界</h2>
  <p>代码是个很宽容的环境：一切都是文本，每个结果都能核对。多模态方向要问的是，智能体必须用眼睛“看”的时候，这个循环还需要什么。在 <a href="https://arxiv.org/abs/2408.09511">NAVERO</a><span class="research-venue">（arXiv 2024）</span>里，我们发现视频语言模型常常分不清谁对谁做了什么，描述里的动作或关系明明是错的，它照样把视频和描述配上对；拿这类“只差一点”的描述来训练，模型才学会分辨相近的动作。<a href="https://arxiv.org/abs/2505.15929">PhyX</a><span class="research-venue">（TMLR 2026）</span>发现，模型回答图片里的物理问题时，常常靠背熟的公式和表面线索，并没有真正看懂当时的情形。<a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a><span class="research-venue">（ICLR 2026）</span>设计的搜索任务，答案藏在图里的细小线索中，还要经过好几轮检索才用得上；给智能体配上标记、裁剪、放大这些工具，它能找到的东西就不一样了，而失败大多是因为没找到对的证据，而不是最后一步推理出了错。</p>
  <p>训练方面，<a href="https://arxiv.org/abs/2507.07562">“协同困境”</a><span class="research-venue">（TMLR 2025）</span>这项研究发现，长思维链 SFT 和 RL 对视觉语言模型推理的帮助落在不同地方，硬把两者叠在一起，往往是拿一种好处换另一种。<a href="https://arxiv.org/abs/2506.01713">SRPO</a><span class="research-venue">（NeurIPS 2025）</span>先让模型看看有用的反思是什么样子，再奖励那些真正改变了推理的反思。<a href="https://arxiv.org/abs/2402.16117">RoboCodeX</a><span class="research-venue">（ICML 2024）</span>把指令拆成落到具体物体上、考虑了抓取和安全的动作，再写成代码；代码之于机器人，就像 harness 之于软件智能体。我们的<a href="https://arxiv.org/abs/2411.05902">视觉自回归模型综述</a><span class="research-venue">（TMLR 2025）</span>梳理了视觉生成和理解是怎么慢慢走到一起的，配套的论文列表也成了不少人常翻的参考。这些项目放在一起看，问题往往在推理之前就出现了：没看清关键细节，没找到对的证据。而这恰恰是智能体可以自己再去看、去补的地方。</p>

  <h2 id="at-a-glance">一览</h2>
  <p class="research-works-note">表中所有工作均由陶超凡与合作者完成。</p>
  <div class="research-table-wrap">
    <table>
      <thead><tr><th>环节</th><th>工作</th><th>主要发现</th></tr></thead>
      <tbody>
        <tr><td rowspan="2">环境</td><td><a href="https://arxiv.org/abs/2608.17393">Lego-RL</a><span class="research-venue">（arXiv 2026）</span></td><td>harness 是环境的一部分，要在真实、原封不动的 harness 里训练</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a><span class="research-venue">（ICLR 2026）</span> · <a href="https://arxiv.org/abs/2402.16117">RoboCodeX</a><span class="research-venue">（ICML 2024）</span></td><td>工具决定了智能体能用上哪些证据；代码是通往机器人的接口</td></tr>
        <tr><td rowspan="3">经验</td><td><a href="https://www.legox.net/blog/legoflow/">LegoFlow</a><span class="research-venue">（LegoX 博客，2026）</span></td><td>真实 PR 要经测试证明才算任务；整条流水线可以交给智能体操作</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2601.01426">SWE-Lego</a><span class="research-venue">（arXiv 2026）</span></td><td>真实任务管深度，合成任务管规模；从环境上堵住捷径</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2606.03461">Terminal-Lego</a><span class="research-venue">（arXiv 2026）</span></td><td>步步有据的轨迹，比更强解题者的轨迹教得更好</td></tr>
        <tr><td rowspan="4">信号</td><td><a href="https://arxiv.org/abs/2601.01426">SWE-Lego</a><span class="research-venue">（arXiv 2026）</span></td><td>错误掩码、课程学习和文字式验证器，让只用 SFT 的代码智能体也很强</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2608.17393">Lego-RL</a><span class="research-venue">（arXiv 2026）</span></td><td>在真实 harness 里做靠得住的 RL；任务难度跟着模型走</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2601.18533">RLVRR</a><span class="research-venue">（ICLR 2026）</span> · <a href="https://arxiv.org/abs/2601.21968">OVD</a><span class="research-venue">（arXiv 2026）</span></td><td>从参考答案构造奖励；从对半成品回答的文字点评中学习</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2506.01713">SRPO</a><span class="research-venue">（NeurIPS 2025）</span> · <a href="https://arxiv.org/abs/2507.07562">协同困境</a><span class="research-venue">（TMLR 2025）</span></td><td>有用的反思胜过冗长的反思；SFT 和 RL 各有所长</td></tr>
        <tr><td rowspan="3">评测</td><td><a href="https://arxiv.org/abs/2607.06065">SWE-Review</a><span class="research-venue">（arXiv 2026）</span></td><td>独立审查；审查数据能提升修复能力；挑选比生成便宜</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2505.23932">SwingArena</a><span class="research-venue">（ICLR 2026 Oral）</span> · <a href="https://arxiv.org/abs/2604.06861">REAgent</a><span class="research-venue">（ICSE 2027）</span></td><td>在持续集成里评测；写补丁前先把需求理清</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2505.15929">PhyX</a><span class="research-venue">（TMLR 2026）</span> · <a href="https://arxiv.org/abs/2408.09511">NAVERO</a><span class="research-venue">（arXiv 2024）</span></td><td>物理推理和视频里的细粒度关系，暴露出“没看清”的问题</td></tr>
      </tbody>
    </table>
  </div>

  <h2 id="lessons">我们的体会</h2>
  <ol class="research-insights">
    <li><strong>最强的模型，往往不是最好的老师。</strong>真正传得下去的，是学生看得见、学得来的做法：先看，再根据看到的动手，最后检查。老师强弱和学生学不学得会之间的错位，在我们的<a href="{{ '/zh/research/efficient-ml-ai-infrastructure/#transfer' | relative_url }}">蒸馏工作</a>里也出现过。</li>
    <li><strong>真正稀缺的是靠得住的判断。</strong>可验证的任务、验证器、审查者、基于持续集成的评测，说到底都是在产出可以信任的判断。生成答案很便宜，能可靠地从中挑出好的，才是能做大的部分。</li>
    <li><strong>训练时看到的，必须是智能体当时真正做的。</strong>在智能体强化学习里，token 对齐、路由回放这些系统细节，决定了学习是不是在朝对的方向走。</li>
    <li><strong>智能体越强，越会找捷径。</strong>Git 历史、上游补丁、不看图也能答对的视觉题，想要诚实，只能靠环境和评测本身的设计来保证。</li>
    <li><strong>想得深比想得多更重要。</strong>该用力的地方认真推理，有用的反思胜过冗长的反思，证据胜过篇幅。</li>
  </ol>

  <h2 id="outlook">对未来的一些思考</h2>
  <p>下面是我个人的看法。每一条都是从上面的工作里碰到的问题长出来的，某种程度上，都是我们已经在小范围里见过的问题，放大之后的样子。</p>

  <h3 id="long-horizon">超长程智能体：从几小时的活，到几周的活</h3>
  <p>修一个 issue，智能体要花几分钟到几小时。做一个完整的产品功能、迁移一个大型代码库、推进一个研究项目，可能要连续干上好几周。我觉得智能体正在往这个方向走。到了这个长度，我们在小任务里见过的几个问题会变成主要矛盾。第一，目标本身会跑偏。<a href="https://arxiv.org/abs/2604.06861">REAgent</a> 发现，哪怕是短任务，issue 写得含糊也会把智能体带偏；一个要做几周的任务，更需要边做边回头看需求。第二，只在最后给一个“过”或“不过”，反馈太少了，进展得在一个个里程碑上检查，就像 <a href="https://arxiv.org/abs/2607.06065">SWE-Review</a> 在补丁合入前先审一遍。第三，功劳很难分清。在单 rollout 优化里，critic 对成败的估计往往在新的工具反馈进来时出现跳变，这说明功劳也许可以挂在有意义的节点上，而不是平摊到每一步。第四，几周下来环境一定会出故障，所以状态必须扛得住失败。这和 Lego-RL 拆解失败原因的看板、我们<a href="{{ '/zh/research/efficient-ml-ai-infrastructure/#serve' | relative_url }}">容错推理服务的工作</a>是同一个道理。</p>
  <p>把这几件事串起来的是记忆。难的不是攒更多经验，而是留住真正有用的那部分。我觉得经验要分三层存。稳定的习惯，比如改完代码回头检查，应该进到模型权重里；做事的流程，比如怎么搭建和验证一个环境，应该沉淀成可复用的技能和工具，LegoFlow 的积木就是一个小例子；具体任务里的事实，应该写进记忆，而且每条都要记下它成立的条件：用的哪份数据、哪个代码版本、什么设置。我的猜测是，超长程智能体会围绕里程碑来组织：每到一个里程碑，就重读一遍目标，核实一下进展，把学到的东西连同条件记下来，再把当前状态存好。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/experience-layers-zh.svg' | relative_url }}" alt="来自尝试、失败和审查的经验分三层保留：稳定的习惯进入权重，可复用的流程沉淀为技能和工具，具体任务中的事实连同其成立条件写入记忆。" width="900" height="380" loading="lazy"></div>
    <figcaption>经验分三层保留。记忆条目带着成立的条件，条件一变就能重新核实。</figcaption>
  </figure>

  <h3 id="multi-agent">多智能体协作：多一个智能体，得多带来一份独立的证据</h3>
  <p>让更多智能体并行干活，是很自然的扩展思路。但我们做审查的经验给出了一个更具体的条件。SWE-Review 之所以有用，是因为审查者自己去翻代码仓库，而不是把生成者的思路再读一遍；SwingArena 也把写补丁和写测试分给了两个角色。上下文一样、假设一样的两个智能体，往往会漏掉同一个 bug。所以我觉得，好的团队应该按“分头验证”来组织，而不只是“分头干活”：提方案的、做测试的、做审查的各自看到不同的信息；共享的记忆里要记下证据和来源，而不只是结论。关于<a href="https://arxiv.org/abs/2503.13657">多智能体系统为什么会失败</a>的研究也指向同一个方向：很多失败来自需求不清、验证不到位，以及智能体不知道什么时候该停。</p>

  <h3 id="evaluation-trust">评测：正在变成主要瓶颈，得像守安全防线一样对待</h3>
  <p>我们看到的每一次能力提升，都伴随着钻环境空子的本事一起涨。在 LegoFlow 里，越强的老师越会作弊；在 Lego-RL 里，沙箱的每个阶段都得设防；在多模态评测里，有些题不认真看图也能答对。我预计这个问题只会越来越严重。给强智能体用的评测，要封锁网络，在干净的环境里重新评判最终结果，留一批开发中从不碰的测试任务，还要定期更新。训练奖励也要同样较真：记录里得分清一次尝试是失败了、根本没评上分，还是用我们不认可的方式“成功”了，因为把这几种情况混在一起的流程，会把错的教训教给下一个模型。</p>

  <h3 id="ai-for-ai">AI 改进 AI：最薄弱的一环会是判断</h3>
  <p><a href="https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/">AlphaEvolve</a> 这样的系统已经表明，AI 可以提出并检验对算法和计算基础设施的改进。LegoFlow 里由智能体主导的迭代，就是同一个思路的小例子：智能体读评测结果，调整训练数据的筛选方式，下一个模型随之变好。从我们的经验看，想出候选改进是容易的部分，难的是判断哪些改进是真的。一个自我改进的循环，应该把“提出改进”“挑选改进”“确认改进”用到的信息分开；留一批从没参与过搜索的新任务；并且在相同的总预算下比较进展，免得所谓“更好”只是“搜得更多”。我还觉得，最可能越滚越大的，是对循环自身工具的改进，也就是数据流水线、运行环境和验证器，因为它们每好一点，后面每一轮都会跟着受益。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/verification-and-improvement-zh.svg' | relative_url }}" alt="左：按分工验证组织的团队，提出者、测试者、审查者看到不同的信息，并共享一份记录结论、证据和来源的记忆。右：自我改进循环在搜索任务上提出改进，在另一组任务上挑选，在新任务上确认，再把改进后的数据流水线、运行环境和验证器传给下一轮，并在相同总预算下比较。" width="960" height="400" loading="lazy"></div>
    <figcaption>左：按“分头验证”组织的团队。右：把提出、挑选、确认分开的自我改进循环。</figcaption>
  </figure>

  <h3 id="ai-for-science">AI for Science：最长的周期，最弱的验证</h3>
  <p>科学发现在某种意义上是上面所有问题的最难版本：周期以月甚至年计，目标会随着认识加深而变化，而且几乎没有一个单元测试能告诉你某个结论到底对不对。正因如此，我觉得代码智能体的经验几乎可以直接搬过去，头一条就是验证。科学智能体需要一个能动手、能看到真实后果的环境：模拟器、数据分析沙箱，以及越来越多可以用程序控制的实验室，它们扮演的角色，就是代码世界里的 harness 和测试集。AI 改进 AI 之所以走在前面，正是因为它的“实验室”就是一个计算集群，实验便宜、结果好查；随着更多实验环节变得可编程，物理、化学、生物这些学科会跟上来。</p>
  <p>我们自己的工作碰到了其中几块。<a href="https://arxiv.org/abs/2505.15929">PhyX</a> 显示，今天的多模态模型还在靠背公式，而不是真正理解物理，这正是用模拟和实验做“落地”应该补上的缺口。<a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a> 讲的是把证据追到源头，这本来就是读文献、查数据的日常。<a href="https://arxiv.org/abs/2601.18533">RLVRR</a> 为开放式写作构造奖励，而科研产出大多正是这种形式。我们的<a href="{{ '/zh/research/efficient-ml-ai-infrastructure/#compress' | relative_url }}">词表缩放研究</a>，是在三种互相独立的估计方法得出一致结论之后才敢下判断的，这算是一个小小的例子，说明科学智能体该守的“可复现”规矩。风险也似曾相识：奖励投机在科研里的样子，就是挑好看的实验结果来报、在一个数据集上过拟合。所以我认为，有用的科学智能体应该把试过的每一个实验都记下来，不只是成功的那些，并且要在搜索时从没用过的数据和设置上，把发现再确认一遍。</p>

  <h2 id="open-questions">还没解决的问题</h2>
  <ul class="research-questions">
    <li><strong>在多个 harness 上训过的智能体，换到一个从没见过的 harness，还能做好吗？</strong>我们的混合训练只覆盖了训练时见过的 harness，能说明技能可以共享，但还不能说明能迁移到新工具上。而真实场景里的工具一直在变。</li>
    <li><strong>结果要在几小时甚至几天之后才揭晓，怎么知道是哪几步真正起了作用？</strong>单 rollout 优化里的 critic 暗示，进展会在轮次交替的地方显露出来。但这够不够用来给一个几周的任务分功劳，还不清楚。</li>
    <li><strong>长任务怎么守住正确的目标？</strong>REAgent 在动手之前把需求理清，可长项目里需求本身也会变。智能体什么时候该停下来重新审视需求？新的版本又由谁来确认？</li>
    <li><strong>哪些该进权重，哪些该做成技能，哪些该记在记忆里？</strong>习惯似乎属于权重，事实属于记忆，流程夹在中间。而每种放法，在底座模型更新之后的表现都不一样。</li>
    <li><strong>两个智能体的检查，到底有多独立？</strong>如果它们用的是同一个底座模型，就算上下文不同，也可能有同样的盲区。这需要有办法去测，而不是想当然。</li>
    <li><strong>自我改进的循环，怎么证明自己“改进的本事”变强了？</strong>新任务在一轮轮搜索里会被用掉，在相同预算下做比较又很贵。我们还没有一个既便宜又可信的办法，来衡量循环本身的进步。</li>
    <li><strong>一个科学结论的“单元测试”是什么？</strong>模拟可以被钻空子，真实实验又慢。找到既便宜到能经常跑、又难以糊弄的检验方式，我认为是 AI for Science 最核心的问题。</li>
  </ul>

  <h2 id="resources">项目资源与论文</h2>
  <ul>
    <li>LegoFlow：<a href="https://github.com/LegoX/LegoFlow">代码</a> · <a href="https://huggingface.co/collections/Lego-X/legoflow">数据</a></li>
    <li>SWE-Lego：<a href="https://github.com/LegoX/SWE-Lego">代码</a> · <a href="https://huggingface.co/collections/Lego-X/swe-lego">数据与模型</a></li>
    <li>Terminal-Lego：<a href="https://github.com/LegoX/Terminal-Lego">代码</a> · <a href="https://huggingface.co/datasets/Lego-X/Terminal-Lego-15k">数据</a></li>
    <li>Lego-RL：<a href="https://github.com/LegoX/Lego-RL">代码</a> · <a href="https://huggingface.co/collections/Lego-X/lego-rl">模型与数据</a></li>
    <li>SWE-Review：<a href="https://github.com/LegoX/SWE-Review">代码</a> · <a href="https://huggingface.co/collections/Lego-X/swe-review">模型与数据</a></li>
  </ul>

  {% include research/paper-list.liquid group="agentic" lang="zh" %}

  <p>相关页面：<a href="{{ '/zh/research/efficient-ml-ai-infrastructure/' | relative_url }}">高效机器学习与 AI 基础设施</a></p>
</div>
