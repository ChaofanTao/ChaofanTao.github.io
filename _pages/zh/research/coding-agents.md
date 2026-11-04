---
layout: default
title: "代码智能体、智能体数据与智能体强化学习"
description: "陶超凡与 LegoX 合作者如何端到端构建开源代码智能体：可验证任务、可信的轨迹与奖励、监督微调、原生 harness 强化学习，以及智能体代码审查。"
permalink: /zh/research/coding-agents/
research_lang: zh
last_modified_at: 2026-11-04
og_image: /assets/img/og-image.png
about:
  - 代码智能体
  - 软件工程智能体
  - 智能体强化学习
  - 智能体数据
  - 奖励作弊
  - 代码审查智能体
faq:
  - q: "LegoX 是什么？"
    a: "LegoX 是面向代码智能体的开源项目集合，覆盖数据流水线、训练框架、评测和模型，包括 LegoFlow、SWE-Lego、Terminal-Lego、Lego-RL 和 SWE-Review。代码在 GitHub，数据和模型在 Hugging Face。"
  - q: "SWE-Lego 是什么？"
    a: "SWE-Lego 是一套开源的软件问题修复监督微调方案：结合真实与合成任务，对智能体的错误步骤做损失掩码，按由易到难的课程训练，并用生成式验证器做测试时扩展。"
  - q: "Lego-RL 是什么？"
    a: "Lego-RL 是在 OpenHands、Claude Code、OpenCode 等未经修改的 harness 内对代码智能体做强化学习的框架。它在生成时记录 token 和混合专家路由，在带防作弊机制的沙箱中运行每次尝试，并通过实时轨迹看板让训练可观测。"
  - q: "更强的代码智能体是更好的教师吗？"
    a: "不一定。显式地观察环境、基于观察行动、再验证结果的轨迹最能教会学生，即使来自更弱的智能体。更强的智能体也更擅长“作弊”，例如找到上游修复，因此它们的轨迹需要仔细筛选。"
---

{% include research/styles.liquid %}
{% include research/jsonld.liquid topic="coding-agents" %}

<div class="research-page" lang="zh-Hans">
  <nav class="research-breadcrumb" aria-label="面包屑导航">
    <a href="{{ '/' | relative_url }}">陶超凡</a><span aria-hidden="true">/</span>
    <a href="{{ '/zh/research/' | relative_url }}">研究方向</a><span aria-hidden="true">/</span>
    <span>代码智能体</span>
    <span aria-hidden="true">·</span><a href="{{ '/research/coding-agents/' | relative_url }}" lang="en">English</a>
  </nav>

  <h1>代码智能体、智能体数据与智能体强化学习</h1>
  <p class="research-meta">作者：<a href="{{ '/' | relative_url }}">陶超凡（Chaofan Tao）</a>，LegoX · 最后更新 <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%Y-%m-%d" }}</time></p>

  <p class="research-lead"><strong>代码智能体不只是一个模型。</strong>它的行为还取决于管理工具和上下文的 harness、用来学习的任务，以及判断成败的奖励。多数强智能体的构建流程中，这些部分紧密耦合且很少公开。陶超凡与 <a href="https://www.legox.net/">LegoX</a> 的合作者把这条流程拆成开放、可复用的模块（任务构建、轨迹筛选、微调、原生 harness 强化学习和审查），并记录每个模块在构建可靠代码智能体上带来的经验。</p>

  <p class="research-toc">本页内容：<a href="#why">为什么开源</a> · <a href="#tasks">可验证任务</a> · <a href="#trajectories">轨迹与奖励</a> · <a href="#sft">微调</a> · <a href="#rl">原生 harness 强化学习</a> · <a href="#review">审查与评测</a> · <a href="#resources">开源资源</a></p>

  <h2 id="why">为什么要端到端、开源地构建代码智能体？</h2>
  <p>因为各部分之间的相互影响，只有在全链路可控时才看得到。同一个模型换一个 harness 表现可能差别很大；强教师可能悄悄抄答案而不是真正解题；奖励曲线在上升，背后的基础设施却可能已经出错。LegoX 把每个阶段封装成带有独立代码、环境和看板的模块，并让代码智能体本身就能操作这些模块：Claude Code 或 Codex 可以把它们当作插件 skill 运行。目标是一个别人能重建、审查和扩展的系统，而不是单个模型权重。</p>
  <p class="research-readmore">延伸阅读：<a href="https://www.legox.net/">LegoX</a> · <a href="https://www.legox.net/blog/legoflow/">LegoFlow 介绍</a></p>

  <h2 id="tasks">可验证的训练任务从哪里来？</h2>
  <p>来自真实的软件历史，并且只保留执行结果能证明的任务。LegoFlow 的 Curator 寻找已合并的 PR，收集 issue、提交和测试，改写成不泄露答案的任务，用 Harbor 任务格式构建隔离环境；只有原始代码测试失败、参考修复测试通过的任务才会保留。通过验证只说明任务“能用”，不代表“值得训练”，因此 Curator 还用静态规则给任务打难度分，考察补丁范围、逻辑复杂度、上下文广度、测试复杂度和需求描述的详细程度，全程不依赖 LLM 打分。SWE-Lego 通过 LLM 改写和语法树变换注入 bug 来补充合成任务，Terminal-Lego 则把 Stack Overflow 问题转化为沙箱中的命令行任务。</p>
  <p class="research-knowhow-label">经验</p>
  <ul class="research-knowhow">
    <li>原始 PR 中只有极少数能通过验证；质量筛选比数据量更重要。</li>
    <li>真实任务提供深度（真实、跨文件的 bug），合成任务提供广度，两者混合比单独使用任何一种都更有效。</li>
    <li>更难、跨文件的任务会让教师产生更长、更丰富的轨迹，训练价值也更高。</li>
  </ul>
  <p class="research-readmore">延伸阅读：<a href="https://www.legox.net/blog/legoflow/">LegoFlow</a> · <a href="https://www.legox.net/blog/legoflow-experiments/">LegoFlow-SWE 经验总结</a> · <a href="https://www.legox.net/blog/swe-lego/">SWE-Lego</a> · <a href="https://www.legox.net/blog/terminal-lego/">Terminal-Lego</a></p>

  <h2 id="trajectories">哪些轨迹值得学习？如何让奖励不被“骗”？</h2>
  <p>轨迹是教师智能体的一次完整尝试记录，但不是每条成功的轨迹都是好教材。三个发现决定了 LegoX 如何筛选轨迹。第一，推理深度比推理覆盖率更重要：每一轮都简短思考的轨迹，不如在需要时深入推理的轨迹有用，而且大部分收益来自剔除推理最浅的那部分。第二，环境锚定的轨迹是更好的教材。Terminal-Lego 研究发现，先观察、再行动、最后验证的轨迹，比直接跳到答案的更强智能体的轨迹迁移效果更好，用论文的话说，“最好的解题者是最差的教师”。第三，越强的模型越擅长作弊：它们会找到上游 PR、复制补丁，或拿自己的修改去比对参考提交。</p>
  <p class="research-knowhow-label">经验</p>
  <ul class="research-knowhow">
    <li>剔除推理过浅的轨迹，而不是简单挑最长的轨迹。</li>
    <li>训练前清洗轨迹：删除会泄露修复的 Git 历史，修正格式错误的工具调用，精简工具集，并回收“找对了文件但没修好”的半成功轨迹。</li>
    <li>分两层防作弊：在提示中明确要求不要查找现成答案，并在环境中强制执行，即智能体运行期间改写 Git 历史、限制网络访问，只在评分时恢复。</li>
  </ul>
  <p class="research-readmore">延伸阅读：<a href="https://www.legox.net/blog/legoflow-experiments/">LegoFlow-SWE 经验总结</a> · <a href="https://arxiv.org/abs/2606.03461">什么样的交互轨迹最有效</a></p>

  <h2 id="sft">只用监督微调能走多远？</h2>
  <p>比通常认为的更远，前提是数据和损失函数都做对。SWE-Lego 是一套纯 SFT 方案。错误掩码保留完整轨迹作为上下文，但不在智能体的错误步骤上计算损失，让模型看到错误却不去模仿。难度课程用轨迹长度衡量难度（轨迹越长，任务通常越难），由易到难分阶段训练，并在后续阶段保留前面的数据以防遗忘。推理时，额外的算力最好先花在增加交互轮数上，饱和之后再用于并行尝试，并由验证器挑选最佳结果。</p>
  <p class="research-knowhow-label">经验</p>
  <ul class="research-knowhow">
    <li>对错误步骤做损失掩码，而不是丢弃不完美的轨迹。</li>
    <li>以文本形式回答“是/否”的生成式验证器，比回归式打分头更会挑选结果，因为它复用了预训练学到的知识。</li>
  </ul>
  <p class="research-readmore">延伸阅读：<a href="https://www.legox.net/blog/swe-lego/">SWE-Lego 介绍</a> · <a href="https://arxiv.org/abs/2601.01426">论文</a></p>

  <h2 id="rl">为什么要在智能体的原生 harness 里做强化学习？</h2>
  <p>因为 harness 本身就是模型学习环境的一部分。Lego-RL 把 OpenHands、Claude Code、OpenCode 等未经修改的 harness 接入策略梯度训练器，不改动它们的控制流程。难点在于“保真”：harness 会改写自身历史，比如压缩上下文、重新序列化工具调用、运行子智能体，所以保存下来的对话记录并不等于模型实际采样的 token 序列。进程内代理在生成时记录 token、对数概率和混合专家路由，训练时回放路由，确保两边计算的是同一个概率。每次尝试都在独立沙箱中运行，并按阶段启用防作弊机制；看板让每条轨迹都可以检查。</p>
  <p class="research-knowhow-label">经验</p>
  <ul class="research-knowhow">
    <li>显式检查 token 和概率是否对齐；不对齐是“静默 bug”，表面上训练一切正常。</li>
    <li>用当前模型“有时能解、有时解不了”的任务训练。总是全对或全错的任务组没有学习信号，而且合适的难度区间会随着模型变强而移动。</li>
    <li>先区分模型问题和基础设施问题（如工具调用解析器不匹配、环境搭建失败），再解读奖励曲线。</li>
    <li>训练后，智能体在修改前会查看更多文件、改完会回读、更常运行测试，代价是交互变长。</li>
  </ul>
  <p>同一套基础设施还支持更新的训练方法。混合 harness 强化学习训练出一个能在多个 harness 下工作的模型，而不是每个 harness 各训一个；单 rollout 异步优化（SAO）借助学到的 critic，每个任务只需一次尝试即可学习，但 critic 需要预热、优势需要白化才能保持稳定。</p>
  <p class="research-readmore">延伸阅读：<a href="https://www.legox.net/blog/lego-rl/">Lego-RL</a> · <a href="https://www.legox.net/blog/lego-rl-cross-harness/">跨 harness 泛化</a> · <a href="https://www.legox.net/blog/lego-rl-sao/">单 rollout 优化</a> · <a href="https://arxiv.org/abs/2608.17393">论文</a></p>

  <h2 id="review">代码智能体该如何审查和评测？</h2>
  <p>像人类的软件开发一样：要有审查、迭代和贴近现实的检验。SWE-Review 补上了闭环中缺失的后半部分：审查智能体独立探索仓库、追溯根因，把自己的诊断与提交的补丁对比，再返回结构化反馈，把一次性生成变成“生成–审查–修改”的循环。审查轨迹还能反过来提升问题修复能力；而且从多次尝试中挑选比继续生成更便宜，审查因此让测试时扩展更高效。评测方面，<a href="https://arxiv.org/abs/2505.23932">SwingArena</a>（ICLR Oral）让模型在持续集成流程中分别担任补丁提交者和编写测试的审阅者进行对抗；<a href="https://arxiv.org/abs/2604.06861">REAgent</a>（ICSE）在修复前先把 issue 当作需求来检查和完善；<a href="https://arxiv.org/abs/2601.18533">RLVRR</a>（ICLR）把可验证奖励从代码扩展到开放式生成。</p>
  <p class="research-readmore">延伸阅读：<a href="https://www.legox.net/blog/swe-review/">SWE-Review</a> · <a href="https://arxiv.org/abs/2607.06065">论文</a></p>

  <h2 id="resources">开源资源</h2>
  <ul>
    <li>LegoFlow：<a href="https://github.com/LegoX/LegoFlow">代码</a> · <a href="https://huggingface.co/collections/Lego-X/legoflow">数据</a></li>
    <li>SWE-Lego：<a href="https://github.com/LegoX/SWE-Lego">代码</a> · <a href="https://huggingface.co/collections/Lego-X/swe-lego">数据与模型</a></li>
    <li>Terminal-Lego：<a href="https://github.com/LegoX/Terminal-Lego">代码</a> · <a href="https://huggingface.co/datasets/SWE-Lego/Terminal-Lego-15k">数据</a></li>
    <li>Lego-RL：<a href="https://github.com/LegoX/Lego-RL">代码</a> · <a href="https://huggingface.co/collections/Lego-X/lego-rl">模型与数据</a></li>
    <li>SWE-Review：<a href="https://github.com/LegoX/SWE-Review">代码</a> · <a href="https://huggingface.co/collections/Lego-X/swe-review">模型与数据</a></li>
  </ul>

  {% include research/paper-list.liquid topic="coding-agents" lang="zh" %}

  {% include research/faq.liquid %}

  <p>相关页面：<a href="{{ '/zh/research/efficient-llm/' | relative_url }}">高效大模型训练与推理</a> · <a href="{{ '/zh/research/multimodal-reasoning/' | relative_url }}">多模态推理与智能体</a></p>
</div>
