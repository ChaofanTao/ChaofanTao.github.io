---
layout: default
title: "智能体编程、推理与评测"
description: "智能体如何在“环境、经验、信号、评测”这个循环里学习，以及陶超凡和合作者在开源搭建每个环节时，关于代码智能体、多模态推理和评测的体会。"
permalink: /zh/research/agentic-intelligence/
research_lang: zh
last_modified_at: 2026-11-06
og_image: /assets/img/og-image.png
figure: /assets/img/research/agentic-loop-zh.svg
about:
  - 智能体
  - 代码智能体
  - 智能体强化学习
  - 智能体数据
  - 多模态推理
  - 智能体评测
  - 奖励作弊
---

{% include research/styles.liquid %}
{% include research/jsonld.liquid group="agentic" %}

<div class="research-page" lang="zh-Hans">
  <nav class="research-breadcrumb" aria-label="面包屑导航">
    <a href="{{ '/' | relative_url }}">陶超凡</a><span aria-hidden="true">/</span>
    <a href="{{ '/zh/research/' | relative_url }}">研究方向</a><span aria-hidden="true">/</span>
    <span>智能体编程、推理与评测</span>
    <span aria-hidden="true">·</span><a href="{{ '/research/agentic-intelligence/' | relative_url }}" lang="en">English</a>
  </nav>

  <h1>智能体编程、推理与评测</h1>
  <p class="research-dek">智能体不是从一份数据集里学会做事的，而是在一个不断循环的过程中学会的。这篇文章想顺着这个循环走一遍，从智能体工作的环境，一直到检验它有没有进步的评测，也聊聊我们在开源搭建每个环节时的体会。</p>
  <p class="research-meta">作者：<a href="{{ '/' | relative_url }}">陶超凡（Chaofan Tao）</a>，与 LegoX 的合作者们 · 最后更新 <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%Y-%m-%d" }}</time></p>

  <p>语言模型是靠读大量文本变强的；智能体则是靠动手做事、再看结果变强的：一条命令报错了，一个测试通过了，一个网页原来找错了，提交的补丁被审查者退了回来。认真想想这件事，难点就转移了。模型当然还重要，但它周围还有四件同样重要的事：它在什么<strong>环境</strong>里工作，在那里攒下了什么<strong>经验</strong>，用什么<strong>信号</strong>把经验变成学习，以及用什么<strong>评测</strong>来判断这一切到底有没有用。</p>
  <p>我习惯把自己最近的工作都放在这个循环里来看。有些项目是开源搭建其中的一环：<a href="https://www.legox.net/blog/legoflow/">LegoFlow</a> 和 <a href="https://www.legox.net/blog/swe-lego/">SWE-Lego</a> 负责经验，<a href="https://www.legox.net/blog/lego-rl/">Lego-RL</a> 负责在真实环境里训练，<a href="https://www.legox.net/blog/swe-review/">SWE-Review</a> 和 <a href="https://arxiv.org/abs/2505.23932">SwingArena</a> 负责审查和评测。还有一些在问：当这个循环换到图像、网页或者真实世界里，会出什么问题。每篇论文都在回答自己的问题，但把它们放在一起看，会发现几件单篇论文都没直接说出来的事：最强的模型往往不是最好的老师；判断答案对不对，比生成答案更难；智能体越强，我们越不能想当然地认为这个循环是“诚实”的。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/agentic-loop-zh.svg' | relative_url }}" alt="智能体学习循环示意图：中间是由模型和 harness 组成的智能体，周围按顺时针连着环境、经验、信号、评测四个环节，每个环节旁标出了相关项目。" width="760" height="480" loading="eager"></div>
    <figcaption>智能体的学习循环。每个环节都可能在不知不觉中出问题，本页的每个项目各自研究其中一环。</figcaption>
  </figure>

  <p class="research-toc">本页内容：<a href="#environment">环境</a> · <a href="#experience">经验</a> · <a href="#signal">信号</a> · <a href="#evaluation">评测</a> · <a href="#physical">走出终端</a> · <a href="#insights">几点体会</a> · <a href="#open-questions">还没解决的问题</a></p>

  <h2 id="environment">1. 环境本身就是智能体的一部分</h2>
  <p>人们很容易把智能体等同于“模型”，把周边的工具当成配套设施。但这个看法其实不太对。代码智能体从来没有直接看过代码仓库，它看到的只是 harness 让它看到的东西：哪些文件和工具输出会进入上下文，对话什么时候被压缩，报错怎么呈现，命令失败后接下来怎么走。我们在做 Lego-RL 时，把同一个初始模型分别接到三个常用的 harness（OpenHands、Claude Code、OpenCode）里，还没开始训练，它在三个环境里的表现就已经明显不同。换一个 harness，某种意义上就是换了一个智能体。</p>
  <p>这直接影响了我们的设计：Lego-RL 在真实、未改动的 harness 里训练，而不是在一个简化版里；harness 被当作环境的一部分，而不是模型的一部分。接下来自然会问：一个模型能不能同时用好几个 harness？把三个 harness 混在一起训练，效果接近分别训练三个模型的平均水平，还缩小了不同 harness 之间的部分差距。这个结果让人振奋，但这些 harness 都是训练时见过的。遇到一个从没见过的 harness 会怎样，目前还没有答案。</p>
  <p>代码之外也是一样。在多模态搜索里，工具就是 harness：<a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a> 给浏览智能体配了一个 set-of-mark 工具，可以在搜索前先在图上做标记、裁剪、放大，仅这一个设计，就决定了智能体能利用哪些线索。在机器人领域，<a href="https://arxiv.org/abs/2402.16117">RoboCodeX</a> 用代码连接“看到的”和“要做的”，这样机器人的行为就变得可以读懂、可以检查，也能搬到另一台机器人上用。</p>

  <h2 id="experience">2. 经验：什么样的经验值得学</h2>
  <p>一切从环境能自动检查的任务开始。LegoFlow 从已合并的 PR 中挖掘任务，把每个任务改写成不泄露答案的形式，为它搭建独立的运行环境，并且只保留“原代码测试不通过、参考修复测试通过”的任务。通过这一步只能说明任务能用，不代表值得拿来训练，所以我们还用一套简单的规则给任务打难度分：补丁有多大、加了多少新逻辑、牵涉代码库的范围有多广、测试有多复杂、需求写得有多详细。SWE-Lego 把真实任务和人为注入 bug 生成的任务混在一起：前者更真实、更有深度，后者数量更多、覆盖更广。Terminal-Lego 则从 Stack Overflow 上的问题出发，做命令行任务。</p>
  <p>最让我们意外的，是关于轨迹的发现。轨迹就是老师智能体在这些任务上的完整尝试记录。通常的想法很简单：能用多强的模型当老师，就用多强的。<a href="https://arxiv.org/abs/2606.03461">Terminal-Lego</a> 却发现，事情可能恰恰相反。那些先四处看看、根据看到的情况动手、最后再检查结果的轨迹，教出来的学生明显更好；而更强的模型常常直接给出答案，留给学生可学的东西反而很少。论文说得很直白：“最会解题的，往往是最差的老师。”LegoFlow 在推理过程中也发现了类似的规律：每一步都想一点的老师，不如在关键步骤上认真想的老师；而且大部分好处来自去掉最“浅”的那部分轨迹，而不是只留下最长的。</p>
  <p>经验还有一个“诚实”的问题。越强的老师越会走捷径：找到上游的 PR、直接复制补丁，或者从 Git 历史里翻出答案。成功的轨迹，不一定是老老实实解出来的。我们最后的做法是两手一起抓：一方面在提示里明确告诉智能体不要去查现成答案；另一方面在环境里让它根本查不到，智能体工作时改写 Git 历史、断开网络，只有评分时才恢复。</p>
  <p class="research-knowhow-label">我们的体会</p>
  <ul class="research-knowhow">
    <li>挑轨迹时，要看它怎么推理、有没有认真和环境打交道，而不只是看成没成功。</li>
    <li>防止答案泄露，要从环境上把路堵死，而不是指望智能体自觉。</li>
  </ul>
  <p class="research-readmore">延伸阅读：<a href="https://www.legox.net/blog/legoflow-experiments/">LegoFlow-SWE 的经验总结</a> · <a href="https://www.legox.net/blog/terminal-lego/">Terminal-Lego</a> · <a href="https://www.legox.net/blog/swe-lego/">SWE-Lego</a></p>

  <h2 id="signal">3. 信号：从模仿到验证</h2>
  <p>如果说经验是智能体做过的尝试，那么信号就是它从这些尝试里学到东西的方式。我越来越相信，不同的信号教会的东西确实不一样，而一个用对地方的信号，比单纯更多的信号更管用。</p>
  <p><strong>把模仿做细。</strong>SWE-Lego 想回答的是：如果像对待数据一样认真对待损失函数，单靠 SFT 能走多远。我们用了错误掩码：模型仍然能看到整条轨迹，包括其中的错误，但不在错误的步骤上计算梯度，这样它能从错误中吸取教训，却不会学着重复错误。课程学习用轨迹长度粗略代表难度，从易到难地训练，同时把前面的数据混进来，避免学了新的忘了旧的。在从多个尝试中挑出最好的那一个时，直接用文字回答“是”或“否”的验证器，比加一个打分头的效果更好，因为它能用上模型在预训练时学到的知识。</p>
  <p><strong>在真实环境里做 RL。</strong>跑测试得到的奖励，听起来天然可靠。但只有当训练时用的内容和模型当时真正做的完全一致，它才可靠。harness 会悄悄改写自己的历史记录，所以保存下来的对话并不等于模型当时生成的 token 序列。Lego-RL 在生成的那一刻就把 token、概率和混合专家模型的路由记录下来，训练时再按原样回放路由。最让人不安的是，这类不一致不会发出任何警告：训练照常进行，曲线照常变化，什么报错都没有。另外，任务难度是相对的：模型总能做对或总是做错的任务，对它来说什么也学不到，而“刚好够得着”的那部分任务，会随着智能体变强而不断移动。训练之后，智能体会在改代码前读更多代码，改完会回头再看，也更常跑测试，代价是每次交互的时间更长。还有一种更新的做法叫单 rollout 优化：借助一个学出来的 critic，每个任务只需尝试一次就能学习，但前提是 critic 先“热身”到能给出靠谱的判断。</p>
  <p><strong>不只是“对”或“错”。</strong>很多有用的任务并没有唯一可以核对的答案。<a href="https://arxiv.org/abs/2601.18533">RLVRR</a> 把一次性的对错判断，换成对照优质参考答案的一连串小检查，既看内容也看风格，把监督数据的高效带进了开放式写作的 RL。<a href="https://arxiv.org/abs/2601.21968">On-policy Verbal Distillation</a> 面对的是只会给文字反馈的老师：用老师的打分给学生自己写到一半的答案排序，保留写得好的开头，替换写得差的后半段，让学生在模仿之外还能继续自己探索。</p>
  <p><strong>视觉里也有同样的取舍。</strong>对视觉语言模型来说，长思维链 SFT 和 RL 擅长的地方不一样。SFT 在困难的多步问题上帮助最大，但回答会变得啰嗦；RL 各方面都有提升，回答也更简洁。我们试过的各种组合方式，都是用一种好处换另一种，而不是叠加，这正是<a href="https://arxiv.org/abs/2507.07562">“协同困境”</a>这篇论文讨论的问题。<a href="https://arxiv.org/abs/2506.01713">SRPO</a> 换了一个更聚焦的思路：先让模型看看好的反思长什么样，再奖励那些简短、而且真正改变了推理的反思。</p>
  <p class="research-readmore">延伸阅读：<a href="https://www.legox.net/blog/lego-rl/">Lego-RL</a> · <a href="https://www.legox.net/blog/lego-rl-cross-harness/">跨 harness 训练</a> · <a href="https://www.legox.net/blog/lego-rl-sao/">单 rollout 优化</a></p>

  <h2 id="evaluation">4. 评测与审查：一面不容易骗过的镜子</h2>
  <p>这里有一个让人不太舒服的对称：老师在我们收集数据时能找到捷径，智能体在我们评测时同样能找到捷径。所以我认为，智能体越强，评测就越要像设计安全防线那样认真，而且最好更贴近真实场景。<a href="https://arxiv.org/abs/2505.23932">SwingArena</a>（ICLR Oral）把评测搬进了持续集成流程：模型轮流扮演提交补丁的人和编写测试的审查者，覆盖多种编程语言，还用检索帮助它们应对超大的代码库。<a href="https://arxiv.org/abs/2604.06861">REAgent</a>（ICSE）则从更前面一步入手：把 issue 描述当成一份可能写得不完整的需求，先检查、补全，再动手修复。</p>
  <p>到了审查这一步，评测不再只是“期末考试”，而是成了循环的一部分。<a href="https://arxiv.org/abs/2607.06065">SWE-Review</a> 训练了一个审查智能体：它自己去翻代码仓库、找出问题的根源，再和提交的补丁对照，写出有条理的反馈。原本“一次写完就交”的流程，变成了“写、审、改”。这项工作有两点让我印象很深：审查数据反过来也能让模型更会修 bug；而且从几个尝试里挑一个，比再多生成很多个要便宜，所以一个好的审查者，能让推理时多花的算力更值。</p>
  <p>多模态评测也有自己的捷径：有些题不认真看图也能答对。<a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a> 专门让答案依赖图里的细小线索，而且这些线索要经过几轮搜索才能用上。在这类题上，失败大多是因为没找到对的网页，或者把相似的事件搞混了，而不是最后一步推理出了错。<a href="https://arxiv.org/abs/2505.15929">PhyX</a> 发现，模型常常靠背下来的公式和表面特征答题，而不是真正理解物理过程；<a href="https://arxiv.org/abs/2408.09511">NAVERO</a> 则考察视频语言模型能否理解随时间变化的关系。</p>

  <h2 id="physical">5. 走出终端</h2>
  <p>当环境变成真实世界，循环本身没有变，变的是接口。RoboCodeX 把一句高层指令一步步拆成针对具体物体的动作，每个动作都标明这个物体可以怎么拿、怎么推、什么是安全的，然后把这些动作写成代码。代码在这里的作用，和 harness 对软件智能体的作用一样：它让行为变得明确、可以检查，也能在不同机器人之间复用。PhyX 衡量的正是这类智能体需要的物理推理能力；我们的<a href="https://arxiv.org/abs/2411.05902">视觉自回归模型综述</a>，梳理了从像素、token 到多尺度的视觉生成方法，以及它们怎样一步步走进具身场景。</p>

  <h2 id="insights">几点体会</h2>
  <ol class="research-insights">
    <li><strong>最强的模型往往不是最好的老师。</strong>在 Terminal-Lego 里，脚踏实地的轨迹胜过更强的解题者；在 LegoFlow 里，更强的老师更会作弊；老师的强弱和学生能不能学会之间的错位，也促成了我们<a href="{{ '/zh/research/efficient-ml-ai-infrastructure/#transfer' | relative_url }}">为每个问题挑选合适老师</a>的工作。真正能传下去的，是学生看得见、学得来的做法。</li>
    <li><strong>真正稀缺的是“判断”。</strong>可验证的任务、给尝试排序的验证器、诊断补丁的审查者、基于持续集成的评测，本质上都是在产出可以信任的判断。生成答案很便宜，可靠地从中挑选，才是能做大的那部分。</li>
    <li><strong>训练时看到的，必须和智能体当时做的一致。</strong>只要训练用的 token、概率或路由和实际情况对不上，学习就会悄悄朝错误的方向走。在智能体 RL 里，系统工程和算法是分不开的。</li>
    <li><strong>越强的智能体，越会找捷径。</strong>Git 历史、上游补丁、不看图也能答对的视觉题，越强的模型越容易发现。要保证诚实，得靠环境和评测本身的设计，光在提示里写一句是不够的。</li>
    <li><strong>想得深比想得多更重要。</strong>在需要的地方认真想，胜过处处想一点；有用的反思胜过长篇的反思；冗长的思维链是有代价的，并不白给。</li>
  </ol>

  <h2 id="open-questions">还没解决的问题</h2>
  <ul>
    <li>在多个 harness 上训练过的智能体，换到一个从没见过的 harness 里，还能表现好吗？</li>
    <li>当“成功”或“失败”要在几十步之后才揭晓，我们怎么知道是哪一步真正起了作用？</li>
    <li>如果智能体需要向用户提问、来回沟通，而不是自己独立关掉一个工单，会有什么不同？</li>
    <li>SFT 和 RL 能不能组合得更聪明，让好处叠加，而不是此消彼长？</li>
    <li>这些经验能不能用到更长的任务上，比如根据一份书面需求从零搭建整个代码仓库？</li>
  </ul>

  <h2 id="resources">开源资源</h2>
  <ul>
    <li>LegoFlow：<a href="https://github.com/LegoX/LegoFlow">代码</a> · <a href="https://huggingface.co/collections/Lego-X/legoflow">数据</a></li>
    <li>SWE-Lego：<a href="https://github.com/LegoX/SWE-Lego">代码</a> · <a href="https://huggingface.co/collections/Lego-X/swe-lego">数据与模型</a></li>
    <li>Terminal-Lego：<a href="https://github.com/LegoX/Terminal-Lego">代码</a> · <a href="https://huggingface.co/datasets/SWE-Lego/Terminal-Lego-15k">数据</a></li>
    <li>Lego-RL：<a href="https://github.com/LegoX/Lego-RL">代码</a> · <a href="https://huggingface.co/collections/Lego-X/lego-rl">模型与数据</a></li>
    <li>SWE-Review：<a href="https://github.com/LegoX/SWE-Review">代码</a> · <a href="https://huggingface.co/collections/Lego-X/swe-review">模型与数据</a></li>
  </ul>

  {% include research/paper-list.liquid group="agentic" lang="zh" %}

  <p>相关页面：<a href="{{ '/zh/research/efficient-ml-ai-infrastructure/' | relative_url }}">高效机器学习与 AI 基础设施</a></p>
</div>
