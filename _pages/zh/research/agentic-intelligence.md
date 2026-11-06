---
layout: default
title: "智能体编程、推理与评测"
description: "从代码智能体的训练与评测出发，讨论长期任务、与用户协作，以及从自然语言需求构建完整项目还需要解决什么。"
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
  - 长期任务
  - 人机协作
  - 从需求构建项目
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
  <p class="research-dek">修好一个问题之后，智能体能否继续和用户一起，把一个项目做完整？我想从已有的训练、数据和评测工作出发，讨论长期任务里更难的部分：理解需求、保留关键依据，以及在变化中持续交付。</p>
  <p class="research-meta">作者：<a href="{{ '/' | relative_url }}">陶超凡（Chaofan Tao）</a> · 最后更新 <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%Y-%m-%d" }}</time></p>

  <p>修复一个描述清楚的问题，和从几句需求开始构建项目，面对的困难很不一样。后者需要智能体决定先做什么、模块怎样配合、哪些地方应该询问用户；做了一半，需求还可能改变。代码能运行只是其中一步，之前已经完成的功能也得继续有效。</p>
  <p>我把相关工作放在四个环节里看：提供什么样的<strong>环境</strong>，收集什么样的<strong>经验</strong>，用什么<strong>训练信号</strong>，以及怎样<strong>评测</strong>。<a href="https://www.legox.net/blog/legoflow/">LegoFlow</a>、<a href="https://www.legox.net/blog/swe-lego/">SWE-Lego</a>、<a href="https://www.legox.net/blog/lego-rl/">Lego-RL</a> 和 <a href="https://www.legox.net/blog/swe-review/">SWE-Review</a> 分别从这些环节入手。我把它们看作继续研究长期协作的基础。下面先讲已有实验带来的认识，再讨论从单次修复走向完整项目时，还缺少哪些能力。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/agentic-loop-zh.svg' | relative_url }}" alt="智能体学习过程示意图：模型与运行框架位于中央，周围是环境、经验、训练信号和评测四个相互影响的环节。" width="760" height="480" loading="eager"></div>
    <figcaption>环境影响智能体能积累什么经验，训练方法决定它从中学到什么，评测则帮助我们检查这些变化是否有用。</figcaption>
  </figure>

  <p class="research-toc">本页内容：<a href="#environment">运行环境</a> · <a href="#experience">训练经验</a> · <a href="#signal">训练方法</a> · <a href="#evaluation">评测与审查</a> · <a href="#physical">多模态与机器人</a> · <a href="#long-horizon">长期任务与用户协作</a> · <a href="#insights">下一步怎样验证</a> · <a href="#open-questions">开放问题</a></p>

  <h2 id="environment">1. 换了运行框架，模型面对的任务也会变</h2>
  <p>先解释一个经常出现的词：运行框架（harness）。它负责把模型接到工具和环境上，决定文件怎样读取、工具结果怎样呈现、历史记录何时压缩，以及命令失败后如何继续。这些选择会改变模型下一步能依据什么来行动。</p>
  <p><a href="https://www.legox.net/blog/lego-rl/">Lego-RL 的实验</a>提供了一个直接的例子：同一个 Qwen3.5-35B-A3B 初始模型，在 OpenHands SDK、Claude Code 和 OpenCode 下，SWE-bench Verified 的得分分别是 64.0%、62.4% 和 57.2%。这说明模型之外的运行方式会影响表现。它也解释了我们为什么选择在原有框架中训练，但这组对比本身并不能证明，原生训练一定优于重写框架后的训练。</p>
  <p>维护多个框架各自的模型并不轻松。我们进一步尝试<a href="https://www.legox.net/blog/lego-rl-cross-harness/">让同一个模型在三套框架中混合训练</a>，在所测基准上的平均表现接近分别训练、分别部署三个模型。不过，三套框架都参与了训练。要判断模型学到的是通用的做事方法，还是对这些接口的适应，需要留出它没见过的框架，再分别考察工具变化、历史压缩和新仓库带来的影响。</p>

  <h2 id="experience">2. 做对一道题，和留下一个好示范，是两回事</h2>
  <p>训练数据首先得站得住脚。<a href="https://www.legox.net/blog/legoflow/">LegoFlow</a> 从真实的代码合并请求中构造任务，还原运行环境，并检查原始代码无法通过相关测试、参考补丁可以通过。<a href="https://www.legox.net/blog/swe-lego/">SWE-Lego</a> 把真实任务和通过注入错误构造的任务结合起来，兼顾复杂度和数据规模。这样的检查能筛掉一批无效任务，但不能保证测试覆盖了需求的每一个细节。</p>
  <p>接下来要选的是操作记录，也就是“轨迹”：智能体看过什么、做过什么、怎样检查结果。<a href="https://arxiv.org/abs/2606.03461">Terminal-Lego</a> 中一个很有意思的结果是，在所比较的教师和学生组合里，教师自身的解题排名与学生学完后的表现并不一致。明确呈现“查看相关信息—据此行动—验证效果”的记录，迁移效果更好。学生需要看见动作背后的依据；一串正确命令，未必能教会它怎样处理下一道题。</p>
  <p><a href="https://www.legox.net/blog/legoflow-experiments/">LegoFlow 的数据实验</a>也提醒我们，不能把推理长度直接当作质量。去掉推理最简略的一组后，学生的表现明显改善；继续挑选更长的记录，收益却很快变小。这支持筛除缺少必要分析的示范，但不意味着把一段推理写长就能教得更好。更值得检查的是：它有没有解释关键决定，有没有根据新的信息调整做法。</p>
  <p>还有一种“成功”需要排除：从 Git 历史或上游网页找到现成补丁。这样的记录可能通过测试，却没有展示我们希望学生学会的排查过程。提示中的约束有帮助，环境也需要配合：移除能暴露答案的历史，在执行阶段限制外部访问，并让评分过程独立检查提交的修改。数据的可信度，最终要落实到这些具体条件上。</p>
  <p class="research-readmore">实验与资源：<a href="https://www.legox.net/blog/legoflow-experiments/">LegoFlow-SWE 经验总结</a> · <a href="https://huggingface.co/datasets/Lego-X/LegoFlow-SWE">任务与轨迹</a> · <a href="https://www.legox.net/blog/terminal-lego/">Terminal-Lego</a></p>

  <h2 id="signal">3. 训练信号要教会什么，也要记录准确</h2>
  <p>监督微调（SFT）让模型学习示范，但示范里的每一步并不都值得模仿。<a href="https://arxiv.org/abs/2601.01426">SWE-Lego</a> 的错误屏蔽保留了失败步骤作为上下文，同时不在这些步骤上计算模仿损失。模型仍能看见一次尝试为什么失败，以及后来如何修正。这里要区分的是“失败经历有学习价值”和“错误动作应该被照着学”。</p>
  <p>强化学习（RL）则让模型根据任务结果调整行为。困难之一在于，运行框架可能压缩或改写对话，事后保存的文本不一定能还原生成时的输入。<a href="https://arxiv.org/abs/2608.17393">Lego-RL</a> 在生成时记录 token、概率和混合专家模型的路由信息，再检查训练端是否能够对应起来。历史改写仍然给还原带来限制，概率相关性高也不等于每个数值都一致。训练曲线正常，并不能代替这些检查。</p>
  <p>并非所有任务都能用一次测试判定对错。<a href="https://arxiv.org/abs/2601.18533">RLVRR</a> 从参考答案中提取内容和风格要求，拆成更细的奖励；<a href="https://arxiv.org/abs/2601.21968">OVD</a> 则利用只能输出文本的教师，评价学生自己生成的片段，保留较好的部分，替换较差的后续内容。这些方法拓宽了反馈的来源，也带来一个需要单独检查的问题：模型是在学任务本身，还是主要在迎合参考答案和评价者的偏好？</p>
  <p>多模态推理进一步说明，训练方法的收益未必能简单相加。在<a href="https://arxiv.org/abs/2507.07562">长思维链 SFT 与 RL 的对比研究</a>中，SFT 更有利于困难问题，却容易让回答变长；RL 的提升更均衡、表达更简洁，所测试的组合方案仍存在取舍。<a href="https://arxiv.org/abs/2506.01713">SRPO</a> 则针对自我反思设计训练，鼓励简洁、有实际帮助的修正。这些结果支持针对具体行为设计反馈，而不是把更多训练阶段当作必然的进步。</p>

  <h2 id="evaluation">4. 评测要检查结果，也要检查得分的来路</h2>
  <p>“通过测试”是一条很有用的证据，但它的含义取决于测试是否完整、需求是否清楚，以及评分过程能否被绕过。<a href="https://arxiv.org/abs/2604.06861">REAgent</a> 从需求入手，先整理和补全问题描述，再生成补丁。<a href="https://arxiv.org/abs/2505.23932">SwingArena</a> 把提交补丁和编写审查测试放进持续集成流程，考察长上下文、多语言代码库中的问题解决。</p>
  <p><a href="https://arxiv.org/abs/2607.06065">SWE-Review</a> 关注的是提交之后发生什么。审查智能体自己查阅仓库、分析问题，再对照候选补丁给出诊断，让生成者据此修改。评价审查者时，既要看它是否判断准确，也要看反馈能否帮助修好问题。不过，独立查阅代码不代表没有共同盲点；审查者和生成者仍可能一起漏掉同一个边界情况。因此，审查反馈和独立测试需要相互补充。</p>
  <p>近期基准维护中的变化也很有启发。<a href="https://arxiv.org/abs/2610.24206">2026 年 10 月的 SWE-Bench Pro V2 论文</a>记录了任务修订和更严格的评分流程：限制网络访问，并在干净容器中重新应用补丁、重新评分。这与 LegoFlow 中遇到的答案泄漏问题相呼应。能力变强后，原先不容易触及的任务缺陷和评分漏洞也会被暴露，评测本身需要持续维护。</p>
  <p>分数变化还可能来自资源配置。<a href="https://www.anthropic.com/research/infrastructure-noise">Anthropic 在 2026 年 2 月公布的实验</a>中，仅改变 Terminal-Bench 2.0 的资源配置，得分就能相差 6 个百分点。这个数字属于它报告的实验条件，不能套用到所有基准；但它说明，比较两个系统时，CPU、内存、超时、网络规则和失败重试都应该交代清楚。否则，很难判断那几个百分点究竟来自模型还是运行条件。</p>

  <h2 id="physical">5. 从代码到图像、网页和机器人</h2>
  <p>换到多模态任务，问题会更具体：智能体是否真的看到了关键线索？<a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a> 要求从图像细节出发，经过多轮图文搜索和交叉核对找到答案，并提供标记、裁剪和定向搜索工具。<a href="https://arxiv.org/abs/2505.15929">PhyX</a> 考察模型能否把图像、物理知识和实际约束结合起来。<a href="https://arxiv.org/abs/2408.09511">NAVERO</a> 则用动作或关系被替换的文本，检查视频语言模型是否分得清相近描述。它们共同提醒我们：答错之后，需要分清是没看见、没找对，还是推理出错。</p>
  <p><a href="https://arxiv.org/abs/2402.16117">RoboCodeX</a> 把高层指令分解为针对具体物体的操作，再生成控制代码。这让计划、约束和执行之间的联系更明确。不过，软件里的重试经验不能直接搬到机器人上：真实动作未必能撤销，检查的时机也会影响结果。我们的<a href="https://arxiv.org/abs/2411.05902">视觉自回归模型综述</a>梳理了视觉表示与生成方法；怎样把这些能力接到可靠的长期行动上，仍需要进一步研究。</p>

  <h2 id="long-horizon">6. 下一步：和用户一起，把项目做完整</h2>
  <p>这不是把单次修复的运行时间拉长就能解决的问题。<a href="https://arxiv.org/abs/2512.12730">NL2Repo-Bench</a> 从一份需求文档和空目录开始，要求智能体完成架构、依赖与多模块实现，最终交付可以安装的项目；<a href="https://arxiv.org/abs/2605.15846">RoadmapBench</a> 则考察已有项目的多目标版本升级。两者分别把“从零构建”和“持续演进”变成可研究的任务，也让提前停止、跨文件不一致和计划失效这些问题更容易暴露。</p>
  <p><a href="https://arxiv.org/abs/2509.16198">RPG / ZeroRepo</a> 尝试用结构化规划，把功能、文件、数据流和函数联系起来。这提示了一条值得尝试的路线：长期记忆除了保存对话，还可以保存项目当前的状态——哪些需求已经确认、设计为什么这样选、哪些功能经过了验证、还有哪些假设没被排除。但计划本身也可能过时；每次用户修改需求或代码发生变化，都需要检查这些记录是否仍然成立。</p>
  <p>用户参与之后，“独立做完”也不再是唯一目标。<a href="https://arxiv.org/abs/2610.29822">2026 年 10 月的 UserSWE</a> 把动态模拟用户和逐轮执行检查引入代码修复，发现智能体的相对排名会随互动预算变化。它并不能代替真实用户实验，却说明单轮得分不足以刻画协作能力。我更想研究的是提问的时机：一个会改变整体设计的问题，尽早问清可能省下大量返工；一个可以通过读代码解决的问题，则未必值得打断用户。</p>
  <p>长期项目还会积累早期选择的代价。<a href="https://arxiv.org/abs/2603.24755">SlopCodeBench</a> 让智能体反复扩展自己先前写出的代码，跟踪冗余和复杂度的集中，观察到通过检查与代码结构变差可以同时发生。对下一阶段的智能体来说，交付不仅是让当前功能通过，还要让下一次需求修改仍然做得动。这也让 SWE-Review 式的审查有了更长远的问题：一次修改有没有破坏旧功能、遗忘用户已经确认的要求，或者让后续开发变得更困难？</p>

  <h2 id="insights">下一步怎样验证这些想法</h2>
  <p>以下是我希望继续检验的方向，尚不能当作现有工作的结论。</p>
  <ol class="research-insights">
    <li><strong>把“项目记忆”放到需求变化中测试。</strong>给同一任务设置几次需求调整，比较保留完整对话、压缩摘要，以及维护需求与验证记录的做法。除了最终解决率，还要看旧功能是否回归、已经确认的要求是否丢失，以及能否从中断处继续。</li>
    <li><strong>同时衡量提问的收益和用户的负担。</strong>在相同的用户时间预算下，比较主动澄清、直接尝试和阶段性展示结果。提问次数本身不能代表协作质量；更关键的是有没有减少误解和返工，以及用户是否需要反复解释同一件事。</li>
    <li><strong>用下一次修改检验这一次交付。</strong>项目通过独立验收后，再加入一个相关需求，观察修改成本、回归和结构变化。这样才能区分“这次碰巧能运行”和“留下了可以继续发展的项目”，也能与<a href="{{ '/zh/research/efficient-ml-ai-infrastructure/#long-horizon' | relative_url }}">长期任务的成本研究</a>对接。</li>
  </ol>

  <h2 id="open-questions">还想继续弄清楚的问题</h2>
  <ul>
    <li>最终结果经过了大量实现、测试与用户交流，怎样识别真正推动进展的动作，并用来训练模型？</li>
    <li>需求发生变化后，智能体怎样判断哪些已有决定需要重看，哪些工作可以继续复用？</li>
    <li>怎样让独立测试、代码审查和用户验收互相补充，同时避免把测试通过率误当成完整项目的交付质量？</li>
  </ul>

  <h2 id="resources">代码、数据与模型</h2>
  <p>论文提供方法和实验，代码与数据则方便进一步检查这些结果。完整论文目录也可以在 <a href="https://scholar.google.com/citations?user=gjmfLroAAAAJ">Google Scholar</a> 中查阅。</p>
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
