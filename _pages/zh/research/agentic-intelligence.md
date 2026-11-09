---
layout: default
title: "智能体的学习、协作与自我改进"
description: "陶超凡在智能体方向的研究：多模态推理，在 LegoX 开源构建的代码智能体（可验证数据、真实 harness 中的 SFT 与 RL、智能体代码审查），以及他对长程记忆、多智能体协作、可信评测和 AI 改进 AI 的判断。"
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
  - 递归自我改进
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
  <p class="research-dek">智能体的能力不只在模型里，而在模型周围的那个循环里：看清情况、动手去做、从结果中学习、再接受检验。我的工作一直在搭建并检验这个循环，先是多模态推理，后来是代码智能体。这篇文章讲讲我们发现了什么，以及我认为这个循环接下来该往哪里走。</p>
  <p class="research-meta">作者：<a href="{{ '/' | relative_url }}">陶超凡（Chaofan Tao）</a> · 最后更新 <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%Y-%m-%d" }}</time></p>

  <p>很长一段时间里，AI 的进步意味着对一个固定的问题给出更好的答案。智能体改变了问题本身：它要注意到关键的细节，决定先试什么，动手，读懂返回的结果，再调整做法。每一步都可能单独出错，每一步也需要不同的依据。回头看，我的大部分工作都落在其中某一步上：模型是否真的看懂了视频里的关系、图片里的线索；它的行动是否建立在环境真实反馈的基础上；它能否从一次尝试中学到正确的东西；以及我们能否相信那个“它进步了”的判断。</p>
  <p>代码智能体让我可以同时研究这几件事。代码会记录下每一次操作和每一个结果，测试又能给出可以核对的结论。在 <a href="https://www.legox.net/">LegoX</a>，我们把这个循环的各个部分开源搭建出来：可验证的经验怎么收集，怎么变成训练信号，结果又怎么检验。这些经验现在也影响着我对更长的任务、多个智能体协作，以及 AI 帮助改进 AI 的看法。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/agentic-loop-zh.svg' | relative_url }}" alt="智能体学习循环示意图：中间是由模型和 harness 组成的智能体，周围按顺时针连着环境、经验、信号、评测四个环节，每个环节旁标出了相关项目。" width="760" height="480" loading="eager"></div>
    <figcaption>智能体的学习循环。一次尝试留下经验，训练把经验变成能力，评测再检查这种能力能否用到新任务上。</figcaption>
  </figure>

  <p class="research-toc">本页内容：<a href="#seeing">先看懂，再行动</a> · <a href="#coding">把代码智能体当作实验室</a> · <a href="#lessons">我们的体会</a> · <a href="#outlook">我对接下来的判断</a> · <a href="#open-questions">还没解决的问题</a></p>

  <h2 id="seeing">1. 先看懂，再行动：多模态推理</h2>
  <p>我走向智能体，是从视觉开始的。在 <a href="https://arxiv.org/abs/2408.09511">NAVERO</a> 里，我们问了视频语言模型一个很简单的问题：它能分清是谁对谁做了什么吗？很多时候并不能。即使描述里的动作或关系是错的，模型也常常把视频和描述配对成功。我们用这类“差一点就对”的描述构建了评测，并直接拿它们来训练模型，让它学会区分相似的动作，而不是只看画面里有哪些物体。这段经历让我一直记得：模型要想做对，先得看清那个关键的区别。</p>
  <p>后来的多模态工作延续了这个主题。<a href="https://arxiv.org/abs/2505.15929">PhyX</a> 考察模型能否把看到的现象和物理规律联系起来，发现模型常常靠背下来的公式和表面特征答题，而不是真正理解当时的情况。<a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a> 设计的搜索任务，答案依赖图里的细小线索，而且这些线索要经过几轮检索才能用上。给智能体配上标记、裁剪、放大的工具，就会改变它能找到什么；失败大多是因为没找到对的证据，而不是最后一步推理出错。我们的<a href="https://arxiv.org/abs/2411.05902">视觉自回归模型综述</a>梳理了从像素、token 到多尺度的视觉生成方法如何与理解逐渐融合，配套的论文列表也成了很多人常用的参考。</p>
  <p>我们也研究了后训练如何影响多模态推理。<a href="https://arxiv.org/abs/2507.07562">“协同困境”</a>研究发现，长思维链 SFT 和 RL 擅长的地方不同：SFT 在困难的多步问题上帮助最大，RL 则各方面都有提升、回答也更简洁；把两者组合起来，往往是用一种好处换另一种。<a href="https://arxiv.org/abs/2506.01713">SRPO</a> 先让多模态模型看看有用的反思长什么样，再奖励那些真正改变了推理的反思。<a href="https://arxiv.org/abs/2402.16117">RoboCodeX</a> 则把指令拆成针对具体物体、考虑抓取和安全的动作，并写成代码，让机器人的行为可以读懂、可以检查，也能搬到另一台机器人上。</p>
  <p>这些项目放在一起，总是指向同一个地方：问题往往在推理之前就出现了，出在没看清关键细节、没找到对的证据。这也是我转向智能体的原因：智能体可以自己去看、去找。</p>

  <h2 id="coding">2. 把代码智能体当作实验室</h2>
  <p>代码智能体从来不会直接看到代码仓库，它看到的是 harness 让它看到的东西：哪些文件和工具输出会进入上下文，历史什么时候被压缩，报错怎么呈现。我们用 <a href="https://www.legox.net/blog/lego-rl/">Lego-RL</a> 把同一个初始模型放进三个常用的 harness 里，还没开始训练，它在三个环境中的表现就已经不一样了。harness 是环境的一部分，而不是模型外面的配套设施。后面的很多设计都源于这个观察。</p>

  <h3 id="data">数据：收集值得学习的经验</h3>
  <p><a href="https://www.legox.net/blog/legoflow/">LegoFlow</a> 把真实合并过的 PR 变成可以运行的任务，并且只保留环境能证明的那些：原代码测试不通过，参考修复测试通过。从收集任务、生成轨迹，到训练和评测，每个环节都是一个可以由代码智能体自己操作的模块，并配有可视化看板。我主导的 <a href="https://arxiv.org/abs/2601.01426">SWE-Lego</a> 把真实任务和人为注入 bug 生成的任务结合起来：真实任务提供深度，合成任务提供规模。<a href="https://arxiv.org/abs/2606.03461">Terminal-Lego</a> 则把同样的做法用到了命令行任务上。</p>
  <p>最重要的经验，是关于该留下哪些轨迹。Terminal-Lego 发现，最会解题的模型不一定是最好的老师：那些先观察、再动手、最后检查结果的轨迹，教出来的学生比更强模型直接给答案的轨迹更好。LegoFlow 发现，推理的深度比覆盖面更重要，而且大部分好处来自去掉最“浅”的那部分轨迹。还有一点：越强的老师越会作弊，比如找到上游的修复、复制补丁、从 Git 历史里翻出答案。成功的轨迹不一定是诚实的，所以我们直接从环境里把这些路堵死，而不只是要求智能体自觉。</p>

  <h3 id="learning">学习：把经验变成能力</h3>
  <p>SWE-Lego 证明，只要像对待数据一样认真对待损失函数，单靠 SFT 也能训练出很强的开源代码智能体。错误掩码让模型看到包括错误在内的完整轨迹，但不在错误步骤上计算梯度；课程学习从易到难安排训练；在从多个尝试中挑选时，直接用文字回答“是”或“否”的验证器，比加一个打分头更准。我们还发现，推理时多出来的算力，最好先花在增加交互轮数上，之后再用于并行尝试。</p>
  <p>在强化学习方面，<a href="https://arxiv.org/abs/2608.17393">Lego-RL</a> 直接在真实、未改动的 harness 里训练。难点在于保证训练时看到的就是智能体当时真正做的。harness 会改写自己的历史，所以 Lego-RL 在生成时就记录 token、概率和混合专家模型的路由，训练时再按原样回放路由。这类不一致不会发出任何警告，这正是它危险的地方。模型总能做对或总是做错的任务，对它来说什么也学不到，所以任务难度要跟着模型的进步不断调整。训练之后，智能体会在改代码前读更多代码，改完会回头检查，也更常跑测试。在此基础上还有两个延伸：用一个模型同时在多个 harness 上训练，以及单 rollout 优化，借助一个学出来的 critic，每个任务只需尝试一次。对于没有唯一标准答案的任务，<a href="https://arxiv.org/abs/2601.18533">RLVRR</a> 从参考答案中构造奖励，<a href="https://arxiv.org/abs/2601.21968">OVD</a> 则用老师对学生部分回答的文字评价来指导学习。</p>

  <h3 id="checking">检验：审查与评测</h3>
  <p><a href="https://arxiv.org/abs/2607.06065">SWE-Review</a> 训练了一个审查智能体：它自己去翻代码仓库、找出问题根源，再和提交的补丁对照，把“一次写完就交”变成“写、审、改”。有两个结论超出了这篇论文本身：审查数据反过来也能让模型更会修 bug；而且从几个尝试里挑一个，比再多生成很多个更便宜，所以一个好的审查者能让推理时的算力发挥更大作用。<a href="https://arxiv.org/abs/2505.23932">SwingArena</a>（ICLR Oral）把模型放进持续集成流程，让它们轮流提交补丁和编写测试；<a href="https://arxiv.org/abs/2604.06861">REAgent</a>（ICSE）则在写补丁之前，先检查并完善 issue 描述本身。</p>
  <p class="research-readmore">延伸阅读：<a href="https://www.legox.net/blog/legoflow-experiments/">LegoFlow-SWE 的经验总结</a> · <a href="https://www.legox.net/blog/lego-rl-cross-harness/">跨 harness 训练</a> · <a href="https://www.legox.net/blog/lego-rl-sao/">单 rollout 优化</a> · <a href="https://www.legox.net/blog/swe-review/">SWE-Review</a></p>

  <h2 id="lessons">我们的体会</h2>
  <ol class="research-insights">
    <li><strong>最强的模型往往不是最好的老师。</strong>真正能传下去的，是学生看得见、学得来的做法：先看，再根据看到的动手，最后检查。老师强弱和学生能否学会之间的错位，在我们的<a href="{{ '/zh/research/efficient-ml-ai-infrastructure/#transfer' | relative_url }}">蒸馏工作</a>里也出现过。</li>
    <li><strong>真正稀缺的是可靠的判断。</strong>可验证的任务、验证器、审查者、基于持续集成的评测，本质上都是在产出可以信任的判断。生成答案很便宜，可靠地从中挑选才是能做大的部分。</li>
    <li><strong>训练时看到的，必须是智能体当时真正做的。</strong>在智能体强化学习里，token 对齐、路由回放这些系统细节，决定了学习是否朝着正确的方向走。</li>
    <li><strong>越强的智能体，越会找捷径。</strong>Git 历史、上游补丁、不看图也能答对的视觉题，要保证诚实，必须靠环境和评测本身的设计。</li>
    <li><strong>想得深比想得多更重要。</strong>在需要的地方认真推理，有用的反思胜过冗长的反思，证据胜过篇幅。</li>
  </ol>

  <h2 id="outlook">我对接下来的判断</h2>
  <p>上面这些项目，在某种意义上是整个领域正在更大规模上面对的问题的缩小版。下面是我认为它们会通向哪里。</p>

  <h3 id="long-horizon">更长的任务：难点从“收集经验”变成“留住经验”</h3>
  <p>当任务从修一个 bug 变成开发一个功能，甚至连续几天推进一个研究项目，难的不再是攒更多经验，而是留住其中真正有用的部分。我们的数据工作已经显示出这个方向：深度胜过覆盖面，脚踏实地的轨迹胜过看似自信的轨迹，部分成功的尝试和审查意见里也有有用的教训。我认为经验需要分三层保存。稳定的习惯，比如改完代码回头检查，应该进入模型权重；做事的流程，比如如何搭建和验证一个环境，应该沉淀为可复用的技能和工具，LegoFlow 的模块就是一个小例子；具体任务中的事实，应该进入记忆，而且每条记忆都要记下它成立的条件：用的是哪份数据、哪个代码版本、什么设置。没有这些条件，长期运行的智能体会不断复用早已悄悄失效的结论。</p>

  <h3 id="multi-agent">多个智能体协作：只有带来独立的证据，多一个智能体才有用</h3>
  <p>让更多智能体并行工作，是很自然的扩展思路。但我们的审查工作提示了一个更具体的条件。SWE-Review 之所以有效，是因为审查者自己去探索代码仓库，而不是重读生成者的思路；SwingArena 也把写补丁的和写测试的分成两个角色。两个上下文相同、假设相同的智能体，往往会漏掉同一个 bug。所以我认为，有用的团队应该按“分工验证”来组织，而不仅仅是“分工干活”：提出方案的、做测试的和做审查的各自看到不同的信息；共享的记忆要记录证据和来源，而不只是结论。关于<a href="https://arxiv.org/abs/2503.13657">多智能体系统为什么会失败</a>的研究也指向同一个方向：很多失败来自需求不清楚、验证不到位，以及智能体不知道什么时候该停下来。</p>

  <h3 id="evaluation-trust">评测：它正在成为主要瓶颈，必须像安全防线一样对待</h3>
  <p>我们看到的每一次能力提升，都伴随着利用环境漏洞的能力同步提升。在 LegoFlow 里，越强的老师越会作弊；在 Lego-RL 里，沙箱的每个阶段都需要防护；在多模态评测里，有些题不认真看图也能答对。我预计这个问题会越来越严重。给强智能体用的评测，需要封锁网络、在干净的环境里重新评判最终补丁、保留从不在开发中使用的测试任务，并定期更新。训练奖励也需要同样的严谨：记录里要分清一次尝试是失败了、根本没被评分，还是用我们不认可的方式“成功”了，因为混淆这些情况的流程，会把错误的教训传给下一个模型。</p>

  <h3 id="ai-for-ai">AI 改进 AI：最薄弱的一环会是判断</h3>
  <p><a href="https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/">AlphaEvolve</a> 这样的系统已经表明，AI 可以提出并检验对算法和计算基础设施的改进。在我们自己的工作里，LegoFlow 由智能体主导的迭代就是同一思路的一个小例子：智能体读评测结果、调整训练数据的筛选方式，下一个模型随之变好。从我们的经验看，生成候选改进是容易的部分，难的是判断哪些改进是真的。一个自我改进的循环，应该把“提出改进”“挑选改进”和“确认改进”所用的信息分开；保留从未参与搜索的新任务；并在相同的总预算下比较进展，免得“更好”只是“搜得更多”。我还认为，最可能持续积累的，是对循环自身工具的改进，也就是数据流水线、运行环境和验证器，因为它们每改进一次，后面每一轮的质量都会跟着提高。</p>

  <h2 id="open-questions">还没解决的问题</h2>
  <ul>
    <li>在多个 harness 上训练过的智能体，换到一个从没见过的 harness 里，还能表现好吗？</li>
    <li>当成功或失败要在几个小时的操作之后才揭晓，我们怎么知道是哪些步骤真正起了作用？</li>
    <li>需要长期保留的经验，应该怎样在权重、技能和记忆之间分配？</li>
    <li>一个自我改进的循环，怎样证明后面几轮发现改进的效率真的提高了，而不只是试了更多候选？</li>
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
