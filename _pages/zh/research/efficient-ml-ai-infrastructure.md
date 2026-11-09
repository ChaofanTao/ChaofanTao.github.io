---
layout: default
title: "高效机器学习与 AI 基础设施"
description: "陶超凡在高效机器学习与 AI 基础设施方向的研究：量化与剪枝、词表扩展定律、KV 缓存压缩、快速的推理时扩展、知识蒸馏、稳定的训练与部署，以及他对大规模智能体数据基础设施、按任务轨迹衡量效率、超长程运行和 AI for Science 的一些思考。"
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
  - AI for Science
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
  <p class="research-dek">在我看来，效率就是把要紧的信息留下，把不必要的计算省掉。我在这个方向的工作从压缩语言模型起步，慢慢走到了训练智能体的系统上。到了智能体时代，我觉得衡量效率的单位已经不是一次前向计算，而是一整条任务轨迹；生产智能体数据的基础设施，也变得和模型本身一样重要。</p>
  <p class="research-meta">作者：<a href="{{ '/' | relative_url }}">陶超凡（Chaofan Tao）</a> · 最后更新 <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%Y-%m-%d" }}</time></p>

  <p>我的大部分效率工作，开头都差不多：某个现成的方法不好使，或者白白浪费资源，而真正值得问的是“为什么”。答案往往是某个早已悄悄失效的假设：分词器可以在模型做大之前就定下来；网络的每个部分都一样扛得住压缩；缓存里的每个 token 都重要；等同步不花钱；GPU 不会坏；最强的老师教得最好。一旦找准是哪个假设出了问题，解法常常并不复杂。</p>
  <p>这篇文章顺着一个模型的“一生”来讲这些问题：从设计、压缩、记忆、部署到知识迁移，最后落到训练智能体的基础设施上。我觉得眼下最重要的效率问题，恰恰出在最后这一段。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/efficiency-lifecycle-zh.svg' | relative_url }}" alt="模型一生五个阶段的示意图：设计、压缩、记忆、计算与服务、迁移，每个阶段对应一个核心问题及相关项目。图中所有项目均为陶超凡与合作者的工作。" width="960" height="325" loading="eager"></div>
    <figcaption>模型一生中的效率问题。每个阶段对应一个核心问题，以及回答它的工作。</figcaption>
    <div class="research-works">
      <p class="research-works-note">图中所有工作均由陶超凡与合作者完成：</p>
      <p><strong>设计</strong>：<a href="https://arxiv.org/abs/2407.13623">词表扩展定律</a><span class="research-venue">（NeurIPS 2024）</span></p>
      <p><strong>压缩</strong>：<a href="https://arxiv.org/abs/2203.10705">生成式语言模型量化</a><span class="research-venue">（ACL 2022 杰出论文）</span> · <a href="https://doi.org/10.18653/v1/2023.findings-acl.692">结构化剪枝</a><span class="research-venue">（Findings of ACL 2023）</span> · <a href="https://arxiv.org/abs/2301.13741">UPop</a><span class="research-venue">（ICML 2023）</span> · <a href="https://arxiv.org/abs/2305.17455">CrossGET</a><span class="research-venue">（ICML 2024）</span></p>
      <p><strong>记忆</strong>：<a href="https://arxiv.org/abs/2406.13035">D2O</a><span class="research-venue">（ICLR 2025）</span> · <a href="https://arxiv.org/abs/2410.03090">UNComp</a><span class="research-venue">（EMNLP 2025）</span> · <a href="https://arxiv.org/abs/2606.10537">Prefilling-dLLM</a><span class="research-venue">（EMNLP 2026）</span></p>
      <p><strong>计算与服务</strong>：<a href="https://arxiv.org/abs/2509.15148">ATTS</a><span class="research-venue">（ICLR 2026）</span> · <a href="https://arxiv.org/abs/2511.11617">AnchorTP</a><span class="research-venue">（DATE 2026）</span> · <a href="https://arxiv.org/abs/2608.17393">Lego-RL</a><span class="research-venue">（arXiv 2026）</span></p>
      <p><strong>迁移</strong>：<a href="https://arxiv.org/abs/2404.02657">自适应 KL</a><span class="research-venue">（COLING 2025）</span> · <a href="https://arxiv.org/abs/2510.10925">PerSyn</a><span class="research-venue">（ACL 2026）</span></p>
    </div>
  </figure>

  <p class="research-toc">本页内容：<a href="#compress">表示与压缩</a> · <a href="#remember">记忆与推理</a> · <a href="#transfer">知识迁移</a> · <a href="#serve">系统与稳定性</a> · <a href="#at-a-glance">一览</a> · <a href="#lessons">我们的体会</a> · <a href="#outlook">对未来的一些思考</a> · <a href="#open-questions">还没解决的问题</a></p>

  <h2 id="compress">1. 表示与压缩</h2>
  <p><strong>生成比分类更难压缩，原因藏在表示里。</strong>我在这个方向的工作，是从<a href="https://arxiv.org/abs/2203.10705">量化生成式语言模型</a>开始的，这项工作拿到了 ACL 2022 杰出论文奖。在 BERT 这类编码器上很好用的量化方法，搬到 GPT 这类生成模型上就失灵了，当时也没人说得清为什么。我们找到了两个原因。一是精度一低，词嵌入就挤成一团，彼此几乎没了差别，模型挑下一个 token 时便分不清该选哪个。二是不同模块的权重分布差得很远，一套量化设置顾不过来。对应的办法是：用 token 级的对比蒸馏让每个 token 的表示保持可区分，用按模块的动态缩放给每个模块单独定范围。</p>
  <p><a href="https://doi.org/10.18653/v1/2023.findings-acl.692">生成模型的结构化剪枝</a>把同样的思路用在“删”上，让模型自己学出哪些部分可以去掉。视觉语言模型里，图像和文字承载信息的方式很不一样：<a href="https://arxiv.org/abs/2301.13741">UPop</a> 在视觉和语言两边同时找更小的网络，让模型自己学出每边该剪多少；<a href="https://arxiv.org/abs/2305.17455">CrossGET</a> 在运行时把重复的 token 合并掉，用一种模态的信息来指导另一种模态怎么合。</p>
  <p><strong>词表是一个不太容易想到的地方。</strong>扩展定律通常不考虑词表，所以规模差不多的模型，词表大小却能差出很多。在 <a href="https://arxiv.org/abs/2407.13623">Scaling Laws with Vocabulary</a> 里，我们把词表大小当成一个独立的扩展维度来研究。三种互相独立的估计方法得出了一致的结论：最合适的词表会随算力变大，只是比模型其他部分长得慢，而大多数模型的词表都偏小。背后是一个取舍：词表越大，同样的文字用的 token 越少；但算力有限时，那些罕见的 token 根本练不好。这给近年来模型普遍改用更大词表提供了有根据的解释，配套的<a href="https://huggingface.co/spaces/sail/scaling-with-vocab-demo">交互式计算器</a>也能直接帮你算出合适的大小。</p>

  <h2 id="remember">2. 记忆与推理</h2>
  <p><strong>做长上下文推理，KV 缓存很快就会占掉大半显存，而一刀切地平均删减很浪费，因为各层的情况并不一样。</strong><a href="https://arxiv.org/abs/2406.13035">D2O</a> 按每一层注意力的集中程度来分配缓存额度；删掉的 token 如果和留下的很像，还能找回来或者合并进去，整个过程不需要微调。<a href="https://arxiv.org/abs/2410.03090">UNComp</a> 从信息量的角度看同一个问题，用矩阵熵找出可以压缩的部分；同样的分析还能指出，哪些注意力头和层在负责“查找”信息。</p>
  <p>扩散语言模型每一步去噪都要把整段提示重读一遍，<a href="https://arxiv.org/abs/2606.10537">Prefilling-dLLM</a> 把提示分块缓存一次，之后只读相关的块。这里有个小细节很关键：在每块开头放一个序列起始 token（BOS），给注意力一个稳定的“落脚点”；有了它，稀疏的做法甚至能比完整注意力效果更好。</p>
  <p><strong>推理时扩展，是在生成时多花算力来换更好的答案</strong>，常见做法是小模型先打草稿、大模型来把关。在 <a href="https://arxiv.org/abs/2509.15148">ATTS</a> 里，我们仔细测了时间都花在了哪儿，发现大头是在等同步，而不是计算本身。ATTS 把同步检查改成异步推理，再用边跑边校准的共性预测（conformal prediction），把草稿被打回的比例控制在统计上靠得住的范围内。</p>

  <h2 id="transfer">3. 知识迁移：给学生找对老师</h2>
  <p>知识蒸馏，是把老师的本事传给一个更小的学生。流行的说法是：前向 KL 会尽量覆盖老师所有可能的答案，反向 KL 则只盯住最主要的那一个。<a href="https://arxiv.org/abs/2404.02657">我们发现</a>，在大模型蒸馏里，这两种现象其实都没怎么出现，两者的最优解是同一个；真正的差别出在训练早期，前向 KL 更在意老师最常给出的那些 token，反向 KL 更在意不常见的那些。自适应 KL 就按这个规律给两者分配权重。<a href="https://arxiv.org/abs/2510.10925">PerSyn</a> 的出发点是“更强的模型不一定是更好的老师”：在生成数据之前，先给每个问题挑出最适合这个学生的老师。能传下去多少，取决于学生能吸收多少，这一点在我们的<a href="{{ '/zh/research/agentic-intelligence/#data' | relative_url }}">智能体轨迹工作</a>里又出现了一次。</p>

  <h2 id="serve">4. 系统与稳定性</h2>
  <p><strong>部署服务里还藏着一个假设：GPU 不会坏。</strong>多卡张量并行时，坏一张卡就可能让整个服务停摆。<a href="https://arxiv.org/abs/2511.11617">AnchorTP</a> 把权重和 KV 缓存放在一个独立的进程里，推理进程崩了它还在；然后把模型重新分到剩下的 GPU 上，并规划出恢复所需的最少数据搬运。</p>
  <p><strong>到了训练智能体，“等待”和“丢状态”这两个问题就更突出了。</strong>在 <a href="https://arxiv.org/abs/2608.17393">Lego-RL</a> 里，一次训练尝试几乎全部时间都是智能体在沙箱里干活，而且每次尝试长短差别很大，同步训练的一批总得等最慢的那个；异步调度能把这些空档填上。训练途中权重更新了，部分 rollout 会先暂停生成、换上新权重，再接着缓存好的前缀往下走，长时间的尝试就不会白跑。</p>
  <p><strong>启动和排查，和调度一样重要。</strong>启动沙箱的时间主要花在构建镜像上，提前构建好任务镜像、按需拉取，能省掉大部分等待；评分工具则特意内置在每个镜像里，因为能复现的奖励，比快一点拿到的奖励更值钱。看板会把每次尝试为什么结束拆开来看，让我们在误读奖励曲线之前，先分清是基础设施出了问题还是模型本身的问题。<a href="https://www.legox.net/blog/lego-rl-sao/">单 rollout 优化</a>则从另一头省钱：用一个学出来的 critic 代替对同一任务的反复采样，训练所需的轨迹少了很多。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/legox/lego-rl-workflow.png' | relative_url }}" alt="Lego-RL 闭环训练流程：数据准备（沙箱管理、镜像缓存、按需拉取、防作弊）、运行前校验、训练（沙箱执行、进程内代理、rollout 与训练器）、实时看板（失败原因拆解、轨迹查看）以及人工复核。" width="1600" height="878" loading="lazy"></div>
    <figcaption>Lego-RL 的工作流程：从数据准备、沙箱管理，到实时的失败诊断和人工复核。图片来自 <a href="https://www.legox.net/blog/lego-rl/">Lego-RL 博客</a>。</figcaption>
  </figure>

  <h2 id="at-a-glance">一览</h2>
  <p class="research-works-note">表中所有工作均由陶超凡与合作者完成。</p>
  <div class="research-table-wrap">
    <table>
      <thead><tr><th>不再成立的假设</th><th>工作</th><th>诊断</th><th>解法</th></tr></thead>
      <tbody>
        <tr><td>分词器可以在模型做大前定下来</td><td><a href="https://arxiv.org/abs/2407.13623">词表扩展定律</a><span class="research-venue">（NeurIPS 2024）</span></td><td>最合适的词表随算力变大，但比模型其他部分长得慢</td><td>根据算力预算预测词表大小</td></tr>
        <tr><td>每个部分都一样扛得住低精度</td><td><a href="https://arxiv.org/abs/2203.10705">量化</a><span class="research-venue">（ACL 2022 杰出论文）</span></td><td>词嵌入挤成一团；各模块权重分布差异大</td><td>token 级对比蒸馏；按模块动态缩放</td></tr>
        <tr><td>结构可以一刀切地剪</td><td><a href="https://doi.org/10.18653/v1/2023.findings-acl.692">结构化剪枝</a><span class="research-venue">（Findings of ACL 2023）</span> · <a href="https://arxiv.org/abs/2301.13741">UPop</a><span class="research-venue">（ICML 2023）</span></td><td>不同组件、不同模态能承受的删减程度不同</td><td>可学习的掩码；按模态学剪枝比例</td></tr>
        <tr><td>每个视觉 token 都少不了</td><td><a href="https://arxiv.org/abs/2305.17455">CrossGET</a><span class="research-venue">（ICML 2024）</span></td><td>跨模态存在大量重复 token</td><td>跨模态引导的 token 合并</td></tr>
        <tr><td>缓存里每个 token 同样重要</td><td><a href="https://arxiv.org/abs/2406.13035">D2O</a><span class="research-venue">（ICLR 2025）</span> · <a href="https://arxiv.org/abs/2410.03090">UNComp</a><span class="research-venue">（EMNLP 2025）</span></td><td>不同层、不同注意力头要的信息不同</td><td>按层分配额度并可找回；按熵引导压缩</td></tr>
        <tr><td>每一步都得重读整段提示</td><td><a href="https://arxiv.org/abs/2606.10537">Prefilling-dLLM</a><span class="research-venue">（EMNLP 2026）</span></td><td>扩散模型在前缀上反复做重复计算</td><td>分块缓存，以序列起始 token 作锚点</td></tr>
        <tr><td>同步不花成本</td><td><a href="https://arxiv.org/abs/2509.15148">ATTS</a><span class="research-venue">（ICLR 2026）</span></td><td>推理时扩展的主要开销是等待</td><td>基于共性预测的异步推理</td></tr>
        <tr><td>GPU 不会坏</td><td><a href="https://arxiv.org/abs/2511.11617">AnchorTP</a><span class="research-venue">（DATE 2026）</span></td><td>坏一张卡就让整个服务停摆</td><td>状态放在进程之外；最少数据搬运恢复</td></tr>
        <tr><td>前向和反向 KL 表现不同</td><td><a href="https://arxiv.org/abs/2404.02657">自适应 KL</a><span class="research-venue">（COLING 2025）</span></td><td>最优解相同，只在训练早期各有侧重</td><td>自适应地给两者分配权重</td></tr>
        <tr><td>最强的老师教得最好</td><td><a href="https://arxiv.org/abs/2510.10925">PerSyn</a><span class="research-venue">（ACL 2026）</span></td><td>关键在于学生能学会什么</td><td>为每个问题挑最合适的老师</td></tr>
        <tr><td>智能体 RL 的瓶颈在优化器</td><td><a href="https://arxiv.org/abs/2608.17393">Lego-RL</a> 基础设施<span class="research-venue">（arXiv 2026）</span></td><td>大部分时间花在智能体干活和等待上</td><td>异步调度、部分 rollout、预构建镜像</td></tr>
      </tbody>
    </table>
  </div>

  <h2 id="lessons">我们的体会</h2>
  <ol class="research-insights">
    <li><strong>先找出那个不成立的假设，再动手优化。</strong>这里的每个结果，都是从追问“现有方法为什么不行”开始的。原因一旦弄清，解法往往很简单。</li>
    <li><strong>不均匀才是常态。</strong>层、模块、模态、token、老师各不相同，给它们分别分配资源，屡试不爽。</li>
    <li><strong>给自己留条后路。</strong>删掉的 token 还能找回来，崩溃后状态还在，权重更新时尝试不中断，有了这些，大胆的优化才是安全的。</li>
    <li><strong>规模越大，等待越是真正的成本。</strong>不管是推理时扩展、部署服务还是智能体训练，最大的收益都来自少等，而不是算得更快。</li>
    <li><strong>效率决定了模型能学会什么。</strong>算力不够而练不好的罕见 token，学生消化不了的老师输出，都说明效率关乎能力，而不只是成本。</li>
  </ol>

  <h2 id="outlook">对未来的一些思考</h2>
  <p>下面是我个人的看法，每一条都是从上面的工作里延伸出来的。</p>

  <h3 id="agentic-data">大规模智能体数据的基础设施，是新的瓶颈</h3>
  <p><strong>对智能体来说，数据是能跑起来、而且能检验结果的环境。</strong>做 LegoFlow 和 Terminal-Lego 让我们看清了钱花在哪儿：找候选任务很便宜，真正费劲的是搭运行环境、用测试证明每个任务成立、跑出轨迹再做筛选，最后只有一小部分候选能留下来。我觉得智能体数据的扩展单位，是“经过验证、能够复现的环境”；评价一套基础设施，就看单位算力下它能搭出、验证并保持干净的环境有多少。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/agentic-data-pipeline-zh.svg' | relative_url }}" alt="从候选任务到训练数据的流水线：搭建环境、验证任务、生成轨迹、筛掉答案泄露和推理过浅的轨迹；每一步留下的都更少，大部分成本集中在中间几步，由 LegoFlow 的 Curator 和 Tracer 负责。" width="960" height="340" loading="lazy"></div>
    <figcaption>智能体数据的成本花在哪里。找候选任务很便宜，真正费劲的是搭环境、验证、跑轨迹和筛选。</figcaption>
  </figure>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/legox/terminal-lego-pipeline.png' | relative_url }}" alt="Terminal-Lego 任务构建流程：筛选高质量的 Stack Overflow 问答，依次生成指令、环境、解答、Dockerfile 和测试，审查测试，再通过 Docker 往返验证，只保留通过验证的任务。" width="1600" height="892" loading="lazy"></div>
    <figcaption>一个具体例子：<a href="https://arxiv.org/abs/2606.03461">Terminal-Lego</a> 只有在完整的 Docker 往返验证通过后，才会留下一个任务。图片来自 <a href="https://www.legox.net/blog/terminal-lego/">Terminal-Lego 博客</a>。</figcaption>
  </figure>
  <p>软件工程是最容易的情况，因为测试能给出干净的信号。下一波会是 cowork 数据：文档、表格、邮件，以及横跨多个应用的工作流程，而且常常有人参与，判断一件事有没有做好要难得多。我觉得，最后手握好数据的，会是把这套基础设施建起来的团队，而不是手里原始日志最多的团队。</p>

  <div class="research-table-wrap">
    <table>
      <thead><tr><th></th><th>代码数据</th><th>cowork 数据</th></tr></thead>
      <tbody>
        <tr><td>环境</td><td>容器里的代码仓库快照</td><td>文档、表格、邮件和多个应用，常常有人参与</td></tr>
        <tr><td>怎么检验结果</td><td>测试：原代码不过，修复后能过</td><td>可检查的应用状态，加上对完成质量的判断；通常没有单元测试</td></tr>
        <tr><td>主要难点</td><td>答案泄露、大规模搭环境、推理过浅的轨迹</td><td>模拟应用和人；判断“做得好不好”，而不只是“做没做完”</td></tr>
        <tr><td>需要的基础设施</td><td>快速构建与缓存、隔离沙箱、防泄露、来源可追溯</td><td>模拟应用和用户、质量检查器、可回放的会话</td></tr>
      </tbody>
    </table>
  </div>

  <h3 id="trajectory-efficiency">效率应该按整条轨迹算，而不是按单次调用算</h3>
  <p>大多数效率方法，包括我们自己的不少工作，都是按一次回答来评估的。可对智能体来说，丢掉一个细节，后面可能要多绕好几步。所以效率要按整个任务来算：拿到一个经过验证的结果，一共花了多少算力、显存和时间。D2O 和 UNComp 背后“留下后面要用的、给删掉的留条退路”的思路，也应该用到观察结果和动作上，而不只是 token 上。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/trajectory-efficiency-zh.svg' | relative_url }}" alt="两条轨迹对比：保留完整上下文时，智能体几步就得到经过验证的结果；上下文丢了一个细节时，每次调用更便宜，但要多走几步去重读、重试、重新测试，整体更慢也更贵。" width="900" height="300" loading="lazy"></div>
    <figcaption>单次省下的，整体上又亏了回去。智能体的效率要按拿到验证结果的整条轨迹来算。</figcaption>
  </figure>

  <h3 id="long-runs">超长程运行：需要分层的记忆和能接着跑的状态</h3>
  <p>没有哪个上下文窗口装得下几周的工具输出，所以记忆得分层：手边一段短的工作上下文，往后是早先工作的压缩摘要，再往后是一个需要精确细节时可以检索的存档，相当于把 D2O“删掉的还能找回来”放大到项目层面。几周下来，机器和沙箱一定会出故障，所以 AnchorTP 把状态和会崩的进程分开、部分 rollout“从断点接着走”的做法，都应该成为标配。</p>

  <h3 id="verification-compute">AI 改进 AI 与 AI for Science：算力应该更多地花在验证上</h3>
  <p>在 AI 改进 AI 的循环里，可不可靠就看检验这一步，所以像 <a href="https://arxiv.org/abs/2607.06065">SWE-Review</a> 这样更便宜的审查者和验证器，很可能是最大的杠杆。科研把这一点放得更大，因为最贵的不是模型，而是实验本身。ATTS 里“先打草稿、再把关”的模式正好用得上：便宜的模型或快速的近似模拟先筛一大批候选，昂贵的模拟或实验只检验最有希望的几个，每层筛掉多少由校准过的规则来定。失败的实验也要连同设置一起留着，别扔。</p>

  <h2 id="open-questions">还没解决的问题</h2>
  <ul class="research-questions">
    <li><strong>cowork 任务的可验证环境，应该长什么样？</strong>没有单元测试，只能看应用状态和质量判断。<span class="research-test">打算怎么验证：先请人给一小批 cowork 任务打分，再看自动检查器和人有多一致、多容易被智能体糊弄。</span></li>
    <li><strong>上下文大多是工具输出时，词表和缓存该怎么设计？</strong><span class="research-test">打算怎么验证：在智能体轨迹上比较不同的分词器和缓存策略，按“拿到验证结果的总成本”来打分。</span></li>
    <li><strong>智能体 RL 的成本能省到什么程度，才会开始伤到能力？</strong>每一种省法，都会让训练数据比当前模型更“旧”一点。<span class="research-test">打算怎么验证：系统地调整数据的新旧程度和 rollout 数量，在相同算力和相同耗时下比较。</span></li>
    <li><strong>一个要干几周的智能体，该忘掉什么？</strong><span class="research-test">打算怎么验证：用不同的遗忘策略重放长轨迹，数一数每种策略要多走多少步，才能拿到同样的验证结果。</span></li>
    <li><strong>循环该怎么在探索和验证之间分预算？</strong>在科研里，近似模型可能恰好把最出人意料的候选筛掉了。<span class="research-test">打算怎么验证：逐步调整花在验证上的比例，在留出的数据上看每单位算力能确认多少真进步。</span></li>
  </ul>

  <p class="research-readmore">代码与实验：<a href="https://github.com/sail-sg/scaling-with-vocab">词表研究</a> · <a href="https://huggingface.co/spaces/sail/scaling-with-vocab-demo">词表计算器</a> · <a href="https://github.com/LegoX/Lego-RL">Lego-RL</a> · <a href="https://github.com/LegoX/LegoFlow">LegoFlow</a></p>

  {% include research/paper-list.liquid group="efficient" lang="zh" %}

  <p>相关页面：<a href="{{ '/zh/research/agentic-intelligence/' | relative_url }}">智能体的学习、协作与自我改进</a></p>
</div>
