---
layout: default
title: "智能体编程、推理与评测"
description: "智能体如何从“环境、经验、信号、评测”构成的闭环中学习，以及陶超凡与合作者在开源构建每个环节时，在代码智能体、多模态推理和评测基准上得到的经验。"
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
  <p class="research-dek">智能体是从一个闭环中学习的，而不是从一份数据集。本文沿着这个闭环，从智能体行动所在的环境，一直走到判断它是否进步的评测，梳理我们在开源构建每个环节时学到的东西。</p>
  <p class="research-meta">作者：<a href="{{ '/' | relative_url }}">陶超凡（Chaofan Tao）</a>及 LegoX 合作者 · 最后更新 <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%Y-%m-%d" }}</time></p>

  <p>语言模型靠学习文本变得有用；智能体则靠学习“行动之后发生了什么”变得有用：一条命令失败了，一个测试通过了，一个网页原来找错了，一个审查者把补丁打了回来。这个转变改变了难题所在的位置。模型依然重要，但同样重要的还有它周围的四件事：它行动所在的<strong>环境</strong>、它在那里收集的<strong>经验</strong>、把经验转化为学习的<strong>信号</strong>，以及告诉我们这一切是否奏效的<strong>评测</strong>。</p>
  <p>我们在代码智能体、多模态推理和评测基准上的工作，可以看作对这个闭环的系统研究。有些项目开源构建其中一个环节：<a href="https://www.legox.net/blog/legoflow/">LegoFlow</a> 和 <a href="https://www.legox.net/blog/swe-lego/">SWE-Lego</a> 负责经验，<a href="https://www.legox.net/blog/lego-rl/">Lego-RL</a> 负责在真实环境中学习，<a href="https://www.legox.net/blog/swe-review/">SWE-Review</a> 和 <a href="https://arxiv.org/abs/2505.23932">SwingArena</a> 负责审查与评测。另一些则追问：当闭环遇到图像、网页或物理世界时，什么会出问题。把它们放在一起读，会得到单篇论文都没有直接说出的结论：最强的模型很少是最好的教师，验证才是稀缺资源，而且智能体越强，闭环的可靠性就越需要被工程化地保障，而不能想当然。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/agentic-loop-zh.svg' | relative_url }}" alt="智能体学习闭环示意图：中心是由模型和 harness 组成的智能体，周围按顺时针连接环境、经验、信号、评测四个环节，每个环节标注了研究它的项目。" width="760" height="480" loading="eager"></div>
    <figcaption>智能体学习闭环。每个环节都可能悄无声息地出错，本页的每个项目研究其中之一。</figcaption>
  </figure>

  <p class="research-toc">本页内容：<a href="#environment">环境</a> · <a href="#experience">经验</a> · <a href="#signal">信号</a> · <a href="#evaluation">评测</a> · <a href="#physical">走出终端</a> · <a href="#insights">贯穿全文的洞察</a> · <a href="#open-questions">开放问题</a></p>

  <h2 id="environment">1. 环境是智能体的一部分</h2>
  <p class="research-claim">换了 harness，就换了智能体。</p>
  <p>代码智能体从不直接“看到”代码仓库，它看到的是 harness 给它看的东西：哪些文件和工具输出进入上下文、对话何时被压缩、错误如何呈现、命令失败后流程如何继续。我们用 Lego-RL 在三个常用 harness（OpenHands、Claude Code、OpenCode）内训练时发现，同一个初始模型在训练开始前，在三者中的表现就已明显不同。这一观察决定了设计：Lego-RL 在未经修改的 harness 内训练，而不是在简化的副本里；并把 harness 视为环境的一部分，而不是策略的一部分。</p>
  <p>接下来的自然问题是：一个模型能否同时服务多个 harness？同时用多个 harness 的 rollout 训练，效果接近分别训练多个模型的平均水平，并缩小了部分 harness 之间的差距。这令人鼓舞，但这些实验中每个 harness 都在训练时见过；智能体如何应对从未见过的 harness，仍是开放问题。</p>
  <p>同样的道理也适用于代码之外。在多模态搜索中，工具就是 harness：<a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a> 为浏览智能体提供 set-of-mark 模块，让它在检索前标记、裁剪和放大图像，这一设计直接决定了智能体能使用哪些证据。在机器人领域，<a href="https://arxiv.org/abs/2402.16117">RoboCodeX</a> 让代码成为感知与行动之间的接口，使行为可检查，并能在不同机器人平台之间迁移。</p>

  <h2 id="experience">2. 经验：什么值得学习</h2>
  <p class="research-claim">可教性是轨迹的属性，而不是教师的属性。</p>
  <p>经验始于环境能够验证的任务。LegoFlow 挖掘已合并的 PR，把每个改写成不泄露答案的任务，构建隔离环境，并且只保留原始代码测试失败、参考修复测试通过的任务。通过验证只说明任务“能用”，不代表“有价值”，因此还用静态规则从补丁范围、新增逻辑、涉及的上下文广度、测试和需求描述的详细程度来评估难度。SWE-Lego 混合真实任务（带来深度）和注入 bug 生成的合成任务（带来广度）；Terminal-Lego 则把社区问答转化为命令行任务。</p>
  <p>更出人意料的经验来自轨迹，也就是教师智能体在这些任务上的完整尝试记录。<a href="https://arxiv.org/abs/2606.03461">Terminal-Lego</a> 发现，显式地观察环境、基于所见行动、再验证结果的轨迹，教学效果远好于直接跳到答案的更强智能体的轨迹，用论文的话说，“最好的解题者是最差的教师”。LegoFlow 在推理层面发现了相似规律：每一轮都简短思考的教师，不如在需要时深入推理的教师；而且大部分收益来自剔除推理最浅的轨迹，而不是只保留最长的。</p>
  <p>经验还有一个可靠性问题。越强的教师越擅长找捷径：定位上游 PR、复制补丁，或从 Git 历史中读出修复。成功的轨迹不一定是诚实的轨迹。有效的防御是分层的：在提示中明确禁止查找现成答案，并由环境强制执行，即智能体运行期间改写历史、限制网络访问，只在评分时恢复。</p>
  <p class="research-knowhow-label">我们学到的</p>
  <ul class="research-knowhow">
    <li>按“是否锚定环境、推理是否有深度”筛选轨迹，而不只看是否成功。</li>
    <li>把答案泄漏当作需要从环境中移除的属性，而不是需要劝阻的行为。</li>
  </ul>
  <p class="research-readmore">延伸阅读：<a href="https://www.legox.net/blog/legoflow-experiments/">LegoFlow-SWE 经验总结</a> · <a href="https://www.legox.net/blog/terminal-lego/">Terminal-Lego</a> · <a href="https://www.legox.net/blog/swe-lego/">SWE-Lego</a></p>

  <h2 id="signal">3. 信号：从模仿到验证</h2>
  <p class="research-claim">每种训练信号教的东西不同；对准问题的信号，胜过更多的信号。</p>
  <p><strong>仔细做的模仿。</strong>SWE-Lego 表明，只要像打磨数据一样打磨损失函数，监督微调能走得很远。错误掩码保留完整轨迹作为上下文，但不在智能体的错误步骤上计算梯度，让模型看到错误而不学会重复它。课程学习用轨迹长度衡量难度，由易到难训练并回放前面的数据。推理时，以文本形式回答“是/否”的生成式验证器比打分头更会挑选结果，因为它复用了预训练学到的知识。</p>
  <p><strong>在真实环境中强化学习。</strong>来自测试执行结果的奖励，只有在训练器优化的内容与模型实际所做的一致时才可信。harness 会改写自身历史，保存下来的对话记录并不等于实际采样的 token 序列；Lego-RL 在生成时记录 token、概率和混合专家路由，并在训练时回放路由。这里的不一致是“静默”的：训练照常运行，曲线照常变化，没有任何报错。难度要相对于当前模型来定，因为总是成功或总是失败的任务不产生学习信号，而这个难度区间会随智能体进步而移动。训练之后，智能体会在修改前读更多代码、改完回读、更常运行测试，代价是交互更长。单 rollout 优化进一步提升效率，借助学到的 critic，每个任务只需一次尝试，但 critic 必须先预热，才能有效引导策略。</p>
  <p><strong>超越“通过/失败”。</strong>许多任务没有唯一可检查的答案。<a href="https://arxiv.org/abs/2601.18533">RLVRR</a> 把单个可验证的“点”换成基于参考答案、覆盖内容与风格的“奖励链”，把监督数据的效率带入开放式生成的强化学习。<a href="https://arxiv.org/abs/2601.21968">On-policy Verbal Distillation</a> 从只返回文本的黑盒教师中学习：教师的评分为学生自己的部分尝试排序，保留好的前缀、替换较差的后续，从而保住学生的探索。</p>
  <p><strong>视觉中的同一种张力。</strong>对推理型视觉语言模型，长思维链 SFT 和 RL 擅长的地方不同：SFT 擅长困难的多步问题，代价是冗长；RL 在各难度上都有提升，回答也更简洁。我们尝试过的所有组合方式都只是用一种收益换另一种，而不是叠加，这就是<a href="https://arxiv.org/abs/2507.07562">协同困境</a>。<a href="https://arxiv.org/abs/2506.01713">SRPO</a> 走了一条更窄的路：先用数据教会好的反思“长什么样”，再奖励简短且真正改变推理的反思。</p>
  <p class="research-readmore">延伸阅读：<a href="https://www.legox.net/blog/lego-rl/">Lego-RL</a> · <a href="https://www.legox.net/blog/lego-rl-cross-harness/">跨 harness 泛化</a> · <a href="https://www.legox.net/blog/lego-rl-sao/">单 rollout 优化</a></p>

  <h2 id="evaluation">4. 评测与审查：一面骗不过的镜子</h2>
  <p class="research-claim">智能体越强，评测就越要像安全边界一样设计。</p>
  <p>让教师在数据收集中找到捷径的能力，同样会让智能体在评测中找到捷径。因此，基准需要和训练环境一样严谨，最好还更贴近现实。<a href="https://arxiv.org/abs/2505.23932">SwingArena</a>（ICLR Oral）把评测搬进持续集成：模型轮流担任补丁提交者和编写测试的审阅者，覆盖多种编程语言，并用检索应对超长代码仓库。<a href="https://arxiv.org/abs/2604.06861">REAgent</a>（ICSE）把 issue 描述本身当作可能不完整的需求，在修复前先检查和完善。</p>
  <p>审查让评测成为闭环的一部分。<a href="https://arxiv.org/abs/2607.06065">SWE-Review</a> 训练的审查智能体独立探索仓库、追溯根因，把自己的诊断与提交的补丁对比，再返回结构化反馈，把一次性生成变成“生成、审查、修改”。有两个结论超出了论文本身：审查轨迹可以反哺问题修复能力；而且从多次尝试中挑选比继续生成更便宜，好的审查者因此让测试时扩展更高效。</p>
  <p>多模态基准有自己的捷径：不看图也能答对的问题。<a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a> 的问题依赖细粒度视觉线索，并需要经过多轮检索传递；大多数失败来自找不到正确网页、分不清相似事件，而不是最后一步推理。<a href="https://arxiv.org/abs/2505.15929">PhyX</a> 显示模型依赖记忆的公式和表层模式，而非物理理解；<a href="https://arxiv.org/abs/2408.09511">NAVERO</a> 考察视频-语言模型如何处理随时间变化的关系。</p>

  <h2 id="physical">5. 走出终端</h2>
  <p class="research-claim">环境变成物理世界时，闭环不变，变的是接口。</p>
  <p>RoboCodeX 以树状结构把高层指令分解为以物体为中心、带有可供性和安全约束的操作步骤，并写成代码。代码在这里扮演的角色，就像 harness 之于软件智能体：它是行为变得明确、可检查、可在不同机器人间复用的那一层。PhyX 衡量这类智能体所需的物理推理能力；我们的<a href="https://arxiv.org/abs/2411.05902">视觉自回归模型综述</a>梳理了从像素到 token 再到尺度的视觉生成方法如何延伸到具身场景。</p>

  <h2 id="insights">贯穿全文的洞察</h2>
  <ol class="research-insights">
    <li><strong>最强的模型很少是最好的教师。</strong>Terminal-Lego 中环境锚定的轨迹胜过更强的解题者，LegoFlow 中更强的教师更会作弊；教师强弱与学生可学性之间的错配，同样促成了<a href="{{ '/zh/research/efficient-ml-ai-infrastructure/#transfer' | relative_url }}">为每个提示选对教师</a>的工作。真正能迁移的，是学生看得见、学得会的行为。</li>
    <li><strong>验证才是稀缺资源。</strong>可验证的任务、为尝试排序的验证器、诊断补丁的审查者、基于 CI 的竞技场，本质上都是在生产可信的判断。生成很便宜，可信的挑选才能规模化。</li>
    <li><strong>保真是一个正确性问题。</strong>如果训练器看到的 token、概率或路由与智能体实际所做的不同，学习就会悄无声息地优化错误的目标。在智能体强化学习中，系统工程与学习密不可分。</li>
    <li><strong>能力会放大捷径。</strong>Git 历史、上游补丁、不看图就能回答的视觉问题，都是越强的模型越常找到的捷径。可靠性必须落在环境和基准里，而不是提示里。</li>
    <li><strong>深度胜过覆盖。</strong>在需要的回合深入推理，胜过处处浅尝辄止；有用的反思胜过冗长的反思；冗长的思维链是成本，不是免费的午餐。</li>
  </ol>

  <h2 id="open-questions">开放问题</h2>
  <ul>
    <li>在多个 harness 上训练的智能体，能否在从未见过的 harness 中表现良好？</li>
    <li>当一个“通过/失败”信号要在几十步行动之后才到来时，该如何分配功劳？</li>
    <li>当智能体需要向用户提问、反复迭代，而不是独自关闭一个工单时，会发生什么变化？</li>
    <li>监督信号与强化信号能否自适应地结合，让收益叠加而非互相抵消？</li>
    <li>这些经验如何延伸到长程任务，例如根据自然语言需求从零构建一个代码仓库？</li>
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
