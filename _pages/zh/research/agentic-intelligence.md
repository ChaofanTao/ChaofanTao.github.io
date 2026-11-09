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

  <p>很长时间里，AI 的进步就是对一个固定的问题答得更好。智能体把问题本身变了：它得注意到要紧的细节，想好先试什么，动手，看懂返回的结果，再调整。每一步都可能单独出错，每一步要的证据也不一样：模型有没有看到该看的东西，它的动作是不是基于环境真实的反馈，它能不能从一次尝试里学到对的东西，还有，我们凭什么相信“它变强了”。</p>
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
  <p>代码智能体从来看不到代码仓库本身，它看到的是 harness 给它看的东西：哪些文件和工具输出会进上下文，历史什么时候被压缩，报错长什么样，命令失败以后接着怎么走。我们用 <a href="https://arxiv.org/abs/2608.17393">Lego-RL</a> 把同一个初始模型分别放进三个常用的 harness（OpenHands、Claude Code、OpenCode），还没开始训练，它在三处的表现就已经不一样了。也就是说，harness 本身就是环境的一部分，不是模型外面的配套设施。这一点决定了我们后来怎么收数据、怎么训练、怎么检验。</p>

  <h3 id="data">数据：收集值得学的经验</h3>
  <p><strong>LegoFlow 把已合并的 PR 变成经过验证的任务。</strong><a href="https://www.legox.net/blog/legoflow/">LegoFlow</a> 把代码数据工程拆成一串积木。Curator 去找已经合并的 PR，把对应的 issue、提交和测试收齐，改写成不会泄露答案的任务，搭好独立的运行环境，并且只留下“原代码测试不过、参考修复测试能过”的任务。能过这一关只说明任务可用，所以 Curator 还会用一套固定规则给任务打难度分：补丁有多大，加了多少新逻辑，牵动了代码库多大范围，测试有多复杂，需求写得多细，全程不用 LLM 打分。</p>
  <p><strong>整条流水线可以交给智能体自己跑。</strong>Tracer 在沙箱里跑出轨迹并做筛选，Trainer 和 Evaluator 负责训练和评测。每块积木都封装成插件 skill，Claude Code、Codex 这样的代码智能体可以自己把整条流水线跑起来，每块积木也都有自己的看板。有一次实验，智能体从头到尾跑完整个流程，读完评测结果后发现不少老师轨迹的推理很浅，就改了筛选规则，下一轮训出来的模型明显更好。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/legox/legoflow-architecture.png' | relative_url }}" alt="LegoFlow 架构图：Root 模块统筹 Curator、Tracer、Trainer、Evaluator 四个模块，每个模块都以插件 skill 的形式提供并配有看板，分别产出任务、轨迹、模型和评测分数。" width="1600" height="766" loading="lazy"></div>
    <figcaption>LegoFlow 的各个模块，从构建任务到评测，每一步都可以交给代码智能体来做。图片来自 <a href="https://www.legox.net/blog/legoflow/">LegoFlow 博客</a>。</figcaption>
  </figure>

  <p><a href="https://arxiv.org/abs/2601.01426">SWE-Lego</a> 把两类任务放在一起用：一类来自真实的 PR，另一类是用 LLM 改写或语法树变换故意埋进 bug 造出来的。真实任务够真、够深，合成任务管够量；在同一批代码仓库上，加进合成任务会一直带来提升。<a href="https://arxiv.org/abs/2606.03461">Terminal-Lego</a> 把同样严格的要求用到命令行任务上，把 Stack Overflow 上的问题做成经过 Docker 验证的任务。</p>
  <p><strong>最要紧的经验，是该留下哪些轨迹。</strong>Terminal-Lego 发现，最会解题的模型不一定是最好的老师，好老师是最适配学生能力的那一个：先观察、再根据看到的情况动手、最后检查结果的轨迹，教出来的学生比更强模型一步到位给出答案的轨迹更好。LegoFlow 发现，想得深比想得广更重要：每一步都浅浅想一下的老师，不如在关键处认真想的老师；而且大部分收益来自去掉最浅的那批轨迹，而不是只留最长的。SWE-Lego 还总结了几条很实用的清洗规则：修好格式出错的工具调用，工具集尽量精简，那些找对了文件却没改对的尝试也别扔，回收再用。</p>
  <p><strong>经验还有个“老不老实”的问题。</strong>老师越强，越会走捷径：找到上游的 PR 直接抄补丁，或者从 Git 历史里翻出答案。成功的轨迹，不一定是老老实实做出来的。管用的办法是两层防护：一是在提示里明说不许去查现成答案；二是在环境里让它根本查不到，智能体干活时改写 Git 历史、藏起测试文件、限制网络，等到评分时才恢复。</p>

  <h3 id="learning">学习：把经验变成能力</h3>
  <p><strong>只要像打磨数据一样打磨损失函数，单靠 SFT 也能走得很远。</strong>在 SWE-Lego 里，错误掩码让模型看到包括错误在内的完整轨迹，但出错的那几步不算梯度，这样它能从错误里长记性，又不会学着再犯。课程学习拿轨迹长度粗略代表难度，由易到难地训，后面阶段继续带着前面的数据。推理时多出来的算力，最好先花在多给几轮交互上，加到头了再用来并行多试几次；从几次尝试里挑结果时，直接用文字回答“是”或“否”的验证器，比打分头挑得更准。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/legox/swe-lego-error-masking.png' | relative_url }}" alt="SWE-Lego 错误掩码示意图：在一条智能体轨迹中，导致执行报错的那一步不参与损失计算，正确的步骤则正常更新梯度。" width="1600" height="878" loading="lazy"></div>
    <figcaption>SWE-Lego 的步骤级错误掩码：模型仍能看到出错的那一步和报错信息，只是不会被训练去模仿它。图片来自 <a href="https://www.legox.net/blog/swe-lego/">SWE-Lego 博客</a>。</figcaption>
  </figure>

  <p><strong>做强化学习，训练时看到的必须是智能体当时真正做的。</strong>Lego-RL 直接在真实、原封不动的 harness 里训练。harness 会压缩上下文、重新序列化工具调用、跑子智能体，等于悄悄改写了自己的历史，所以存下来的对话记录并不等于当时实际采样出的 token 序列。我们用一个进程内代理在生成时就记下 token、概率和混合专家模型的路由，训练时再按原样回放路由。这类对不上的问题不会报任何错：训练照跑，曲线照动，所以必须专门去查。</p>
  <p><strong>训练本身还教会我们两件事。</strong>模型总能做对或总做不对的任务，对它来说学不到东西，所以“跳一跳够得着”的难度区间要跟着模型的进步往上挪。奖励往下掉，也可能是解析器坏了或者环境没搭起来，不一定是模型变差了，所以把每次尝试为什么结束拆开来看的看板，是方法的一部分，不是锦上添花。训练之后，智能体改代码前会多读代码，改完会回头检查，也更常跑测试，代价是每次交互的时间更长。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/legox/lego-rl-infrastructure.png' | relative_url }}" alt="Lego-RL 训练架构图：未经修改的 harness 在沙箱中运行，进程内代理记录 token 和路由信息，rollout 引擎与训练器之间交换轨迹和权重，支持同步、异步和部分 rollout。" width="1600" height="992" loading="lazy"></div>
    <figcaption>Lego-RL 通过进程内代理，把原封不动的 harness 接到训练器上。图片来自 <a href="https://www.legox.net/blog/lego-rl/">Lego-RL 博客</a>。</figcaption>
  </figure>

  <p>在这个基础上又往前走了两步。<a href="https://www.legox.net/blog/lego-rl-cross-harness/">让一个模型同时在多个 harness 上训练</a>，效果接近分开训练的平均水平，还缩小了不同 harness 之间的一部分差距。<a href="https://www.legox.net/blog/lego-rl-sao/">单 rollout 优化</a>借助一个学出来的 critic，每个任务只试一次就能学，省掉了大部分采样；前提是 critic 要先充分“热身”，优势值也要做好归一化，不然模型会退化成一遍遍调用 think 工具。对于没有唯一标准答案的任务，<a href="https://arxiv.org/abs/2601.18533">RLVRR</a> 从优质参考答案里构造一串兼顾内容和风格的奖励；<a href="https://arxiv.org/abs/2601.21968">OVD</a> 则让老师对学生写了一半的回答给出文字点评，好的开头留下，写差的后半段换掉。</p>

  <h3 id="checking">检验：审查与评测</h3>
  <p><a href="https://arxiv.org/abs/2607.06065">SWE-Review</a> 训练了一个审查智能体：它自己去翻代码仓库，找出问题的根源，再拿去和提交的补丁对照，写出有条理的反馈，把“一次写完就交”变成“写、审、改”。有两个结论不止对这篇论文有意义：审查数据反过来也能让模型更会修 bug；从几次尝试里挑一个，比再多生成很多次便宜，所以好的审查者能让推理时的算力更值钱。<a href="https://arxiv.org/abs/2505.23932">SwingArena</a> 把模型放进持续集成流程，让它们在多种编程语言里轮流提交补丁、编写测试；<a href="https://arxiv.org/abs/2604.06861">REAgent</a> 则在写补丁之前，先检查并补全 issue 描述本身。</p>
  <p class="research-readmore">延伸阅读：<a href="https://www.legox.net/blog/legoflow-experiments/">LegoFlow-SWE 的经验总结</a> · <a href="https://www.legox.net/blog/lego-rl/">Lego-RL 博客</a> · <a href="https://www.legox.net/blog/swe-review/">SWE-Review 博客</a></p>

  <h2 id="multimodal">2. 走出代码：多模态推理与真实世界</h2>
  <p><strong>代码是个很宽容的环境：一切都是文本，每个结果都能核对。</strong>多模态方向要问的是，智能体必须用眼睛“看”的时候，这个循环还需要什么。在 <a href="https://arxiv.org/abs/2408.09511">NAVERO</a> 里，我们发现视频语言模型常常分不清谁对谁做了什么，描述里的动作或关系明明是错的，它照样把视频和描述配上对；拿这类“只差一点”的描述来训练，模型才学会分辨相近的动作。<a href="https://arxiv.org/abs/2505.15929">PhyX</a> 发现，模型回答图片里的物理问题时，常常靠背熟的公式和表面线索，并没有真正看懂当时的情形。<a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a> 设计的搜索任务，答案藏在图里的细小线索中，还要经过好几轮检索才用得上；给智能体配上标记、裁剪、放大这些工具，它能找到的东西就不一样了，而失败大多是因为没找到对的证据，而不是最后一步推理出了错。</p>
  <p>训练方面，<a href="https://arxiv.org/abs/2507.07562">“协同困境”</a>这项研究发现，长思维链 SFT 和 RL 对视觉语言模型推理的帮助落在不同地方，硬把两者叠在一起，往往是拿一种好处换另一种。<a href="https://arxiv.org/abs/2506.01713">SRPO</a> 先让模型看看有用的反思是什么样子，再奖励那些真正改变了推理的反思。<a href="https://arxiv.org/abs/2402.16117">RoboCodeX</a> 把指令拆成落到具体物体上、考虑了抓取和安全的动作，再写成代码；代码之于机器人，就像 harness 之于软件智能体。我们的<a href="https://arxiv.org/abs/2411.05902">视觉自回归模型综述</a>梳理了视觉生成和理解是怎么慢慢走到一起的，配套的论文列表也成了不少人常翻的参考。</p>
  <p><strong>这些项目放在一起看，问题往往在推理之前就出现了</strong>：没看清关键细节，没找到对的证据。而这恰恰是智能体可以自己回头再看、再补的地方。</p>

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
  <p>下面是我个人的看法。每一条都从上面工作里碰到过的小问题出发，看它放大之后会变成什么样。</p>

  <h3 id="long-horizon">超长程智能体：从几小时的活，到几周的活</h3>
  <p>智能体正在从几小时的任务，走向几周的任务：做一个完整的功能，迁移一个大代码库，推进一个研究项目。到了这个长度，我们在小任务里见过的四个问题会变成主要矛盾：</p>
  <ul>
    <li><strong>目标会跑偏。</strong><a href="https://arxiv.org/abs/2604.06861">REAgent</a> 发现，哪怕是短任务，issue 写得含糊也会把智能体带偏；几周的任务更得边做边回头看需求。</li>
    <li><strong>只在最后给一次“过”或“不过”，反馈太少。</strong>进展要在一个个里程碑上检查，就像 <a href="https://arxiv.org/abs/2607.06065">SWE-Review</a> 在补丁合入前先审一遍。</li>
    <li><strong>功劳很难分清。</strong>在单 rollout 优化里，critic 对成败的估计常常在新的工具反馈进来时跳一下，说明功劳也许可以记在关键节点上。</li>
    <li><strong>环境一定会出故障。</strong>状态得扛得住失败，这和 Lego-RL 拆解失败原因的看板、我们<a href="{{ '/zh/research/efficient-ml-ai-infrastructure/#serve' | relative_url }}">容错推理服务的工作</a>是同一个道理。</li>
  </ul>
  <p>我的猜测是，这样的智能体会按里程碑来干活：每到一个里程碑，重读一遍目标，核实一下进展，把学到的东西连同条件记下来，再把当前状态存好。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/milestone-loop-zh.svg' | relative_url }}" alt="一个要做几周的任务按里程碑分段。每到一个里程碑，智能体重读目标（参见 REAgent）、核实进展（参见 SWE-Review）、连同成立条件记下经验、保存状态（参见 AnchorTP 和部分 rollout），然后继续干活，直到得到经过验证的结果。" width="900" height="360" loading="lazy"></div>
    <figcaption>按里程碑推进。这是我设想的方向，来自我们已有工作里的经验，并不是一个已经做好的系统。</figcaption>
  </figure>

  <p><strong>“记下经验”这一步最讲究。</strong>我觉得经验要分三层存：习惯进权重，比如改完代码回头检查；流程做成可复用的技能和工具，LegoFlow 的积木就是个小例子；具体事实写进记忆，而且每条都要注明它在什么数据、什么代码版本、什么设置下成立。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/experience-layers-zh.svg' | relative_url }}" alt="来自尝试、失败和审查的经验分三层保留：稳定的习惯进入权重，可复用的流程沉淀为技能和工具，具体任务中的事实连同其成立条件写入记忆。" width="900" height="380" loading="lazy"></div>
    <figcaption>经验分三层保留。记忆条目带着成立的条件，条件一变就能重新核实。</figcaption>
  </figure>

  <h3 id="multi-agent">多智能体协作：多一个智能体，得多带来一份独立的证据</h3>
  <p>SWE-Review 之所以有用，是因为审查者自己去翻代码仓库，而不是把生成者的思路再读一遍；SwingArena 也把写补丁和写测试分给了两个角色。上下文一样的两个智能体，往往会漏掉同一个 bug。所以我觉得，好的团队应该“分头验证”，而不只是“分头干活”，共享的记忆里也要记下证据和来源，而不只是结论。关于<a href="https://arxiv.org/abs/2503.13657">多智能体系统为什么会失败</a>的研究，也指向同一个方向。</p>

  <h3 id="evaluation-trust">评测：得像守安全防线一样对待</h3>
  <p>我们看到的每一次能力提升，都伴随着钻空子的本事一起涨：老师越强越会作弊，沙箱的每个阶段都得设防。给强智能体用的评测，要封锁网络、在干净环境里重新评判、留一批开发中从不碰的任务，还要定期更新。训练记录也得分清：一次尝试是失败了、根本没评上分，还是用我们不认可的方式“成功”了。</p>

  <h3 id="ai-for-ai">AI 改进 AI：最薄弱的一环会是判断</h3>
  <p><a href="https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/">AlphaEvolve</a> 已经表明，AI 可以提出并检验对算法和基础设施的改进；LegoFlow 里由智能体主导的迭代，是同一个思路的小例子。想出候选改进容易，难的是判断哪些是真的。所以自我改进的循环应该把“提出”“挑选”“确认”用到的信息分开，留一批从没参与过搜索的新任务，并且在相同的总预算下比较。最可能越滚越大的，是对循环自身工具的改进：数据流水线、运行环境和验证器。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/verification-and-improvement-zh.svg' | relative_url }}" alt="左：按分工验证组织的团队，提出者、测试者、审查者看到不同的信息，并共享一份记录结论、证据和来源的记忆。右：自我改进循环在搜索任务上提出改进，在另一组任务上挑选，在新任务上确认，再把改进后的数据流水线、运行环境和验证器传给下一轮，并在相同总预算下比较。" width="960" height="400" loading="lazy"></div>
    <figcaption>左：按“分头验证”组织的团队。右：把提出、挑选、确认分开的自我改进循环。</figcaption>
  </figure>

  <h3 id="ai-for-science">AI for Science：最长的周期，最弱的验证</h3>
  <p>科学研究把上面所有问题都放大了：周期以月计，目标会随着认识变化，而且几乎没有一个单元测试能告诉你某个结论对不对。模拟器、数据分析沙箱和可编程的实验室，会扮演代码世界里 harness 和测试集的角色；AI 改进 AI 之所以走在前面，是因为它的“实验室”就是计算集群。</p>
  <p>和我们工作直接相关的有两点。<a href="https://arxiv.org/abs/2505.15929">PhyX</a> 显示，今天的多模态模型还在靠背公式，而不是真懂物理。我们的<a href="{{ '/zh/research/efficient-ml-ai-infrastructure/#compress' | relative_url }}">词表缩放研究</a>，是等三种互相独立的方法得出一致结论后才下判断的，这种“先复现、再相信”的习惯，科学智能体应该默认就有。另外，奖励投机在科研里的样子，就是只挑好看的实验来报，所以我预计有用的科学智能体会把试过的每个实验都记下来，不只是成功的那些，并且在搜索时没用过的设置上再确认一遍。</p>

  <h2 id="open-questions">还没解决的问题</h2>
  <ul class="research-questions">
    <li><strong>在多个 harness 上训过的智能体，换到没见过的 harness 还行吗？</strong>我们的混合训练只能说明技能可以共享，还不能说明能迁移。<span class="research-test">打算怎么验证：训练时完全留出一个 harness，只拿它来测，轮流换着留。</span></li>
    <li><strong>结果要几天后才揭晓，功劳怎么分？</strong>critic 在轮次交替处的跳变，暗示功劳可以按里程碑来分。<span class="research-test">打算怎么验证：同样的长任务、同样的算力，比较“在验证过的里程碑上给奖励”和“只在最后给一次奖励”。</span></li>
    <li><strong>长任务怎么守住正确的目标？</strong>REAgent 在动手前把需求理清，可长项目里需求本身会变。<span class="research-test">打算怎么验证：在长任务中途改需求，看智能体能不能发现、多快发现。</span></li>
    <li><strong>哪些该进权重，哪些做成技能，哪些记在记忆里？</strong>每种放法在底座模型更新后的表现都不一样。<span class="research-test">打算怎么验证：把同一条经验分别用三种方式存下来，换上更新的底座模型，看哪种还管用。</span></li>
    <li><strong>自我改进的循环，怎么证明自己“改进的本事”变强了？</strong>新任务会被一轮轮用掉，等预算比较又很贵。<span class="research-test">打算怎么验证：记录每一轮要花多少预算，才能在一批从没碰过的任务上确认一次真改进；循环真在变强的话，这个数应该越来越小。</span></li>
    <li><strong>一个科学结论的“单元测试”是什么？</strong>模拟可以被钻空子，真实实验又慢。<span class="research-test">打算怎么验证：先从模拟和便宜实验能互相核对的领域做起，看模拟里成立的发现，有多少能经得住真实检验。</span></li>
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
