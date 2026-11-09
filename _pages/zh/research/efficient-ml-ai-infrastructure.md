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
  <p>我在这个方向的工作，是从<a href="https://arxiv.org/abs/2203.10705">量化生成式语言模型</a><span class="research-venue">（ACL 2022 杰出论文）</span>开始的。在 BERT 这类编码器上很好用的量化方法，搬到 GPT 这类生成模型上就失灵了，当时也没人说得清为什么。我们找到了两个原因。一是精度一低，词嵌入就挤成一团，彼此几乎没了差别，模型挑下一个 token 时便分不清该选哪个。二是不同模块的权重分布差得很远，一套量化设置顾不过来。对应的办法是：用 token 级的对比蒸馏让每个 token 的表示保持可区分，用按模块的动态缩放给每个模块单独定范围。比起方法本身，更有价值的是这个诊断：它说明了为什么生成比分类更难压缩。</p>
  <p><a href="https://doi.org/10.18653/v1/2023.findings-acl.692">生成模型的结构化剪枝</a><span class="research-venue">（Findings of ACL 2023）</span>把同样的思路用在“删”上，让模型自己学出哪些部分可以去掉。视觉语言模型里，图像和文字承载信息的方式很不一样：<a href="https://arxiv.org/abs/2301.13741">UPop</a><span class="research-venue">（ICML 2023）</span>在视觉和语言两边同时找更小的网络，让模型自己学出每边该剪多少；<a href="https://arxiv.org/abs/2305.17455">CrossGET</a><span class="research-venue">（ICML 2024）</span>在运行时把重复的 token 合并掉，用一种模态的信息来指导另一种模态怎么合。</p>
  <p>词表是一个不太容易想到的地方。扩展定律通常不考虑词表，所以规模差不多的模型，词表大小却能差出很多。在 <a href="https://arxiv.org/abs/2407.13623">Scaling Laws with Vocabulary</a><span class="research-venue">（NeurIPS 2024）</span>里，我们把词表大小当成一个独立的扩展维度来研究。三种互相独立的估计方法得出了一致的结论：最合适的词表会随算力变大，只是比模型其他部分长得慢，而大多数模型的词表都偏小。背后是一个取舍：词表越大，同样的文字用的 token 越少；但算力有限时，那些罕见的 token 根本练不好。这给近年来模型普遍改用更大词表提供了有根据的解释，配套的<a href="https://huggingface.co/spaces/sail/scaling-with-vocab-demo">交互式计算器</a>也能直接帮你算出合适的大小。</p>

  <h2 id="remember">2. 记忆与推理</h2>
  <p>做长上下文推理，KV 缓存很快就会占掉大半显存，而一刀切地平均删减很浪费，因为各层的情况并不一样。<a href="https://arxiv.org/abs/2406.13035">D2O</a><span class="research-venue">（ICLR 2025）</span>按每一层注意力的集中程度来分配缓存额度；删掉的 token 如果和留下的很像，还能找回来或者合并进去，整个过程不需要微调。<a href="https://arxiv.org/abs/2410.03090">UNComp</a><span class="research-venue">（EMNLP 2025）</span>从信息量的角度看同一个问题，用矩阵熵找出可以压缩的部分；同样的分析还能指出，哪些注意力头和层在负责“查找”信息。扩散语言模型每一步去噪都要把整段提示重读一遍，<a href="https://arxiv.org/abs/2606.10537">Prefilling-dLLM</a><span class="research-venue">（EMNLP 2026）</span>把提示分块缓存一次，之后只读相关的块。这里有个小细节很关键：在每块开头放一个序列起始 token（BOS），给注意力一个稳定的“落脚点”；有了它，稀疏的做法甚至能比完整注意力效果更好。</p>
  <p>推理时扩展，是在生成时多花算力来换更好的答案，常见做法是小模型先打草稿、大模型来把关。在 <a href="https://arxiv.org/abs/2509.15148">ATTS</a><span class="research-venue">（ICLR 2026）</span>里，我们仔细测了时间都花在了哪儿，发现大头是在等同步，而不是计算本身。ATTS 把同步检查改成异步推理，再用边跑边校准的共性预测（conformal prediction），把草稿被打回的比例控制在统计上靠得住的范围内。</p>

  <h2 id="transfer">3. 知识迁移：给学生找对老师</h2>
  <p>知识蒸馏，是把老师的本事传给一个更小的学生。流行的说法是：前向 KL 会尽量覆盖老师所有可能的答案，反向 KL 则只盯住最主要的那一个。<a href="https://arxiv.org/abs/2404.02657">我们发现</a><span class="research-venue">（COLING 2025）</span>，在大模型蒸馏里，这两种现象其实都没怎么出现，两者的最优解是同一个；真正的差别出在训练早期，前向 KL 更在意老师最常给出的那些 token，反向 KL 更在意不常见的那些。自适应 KL 就按这个规律给两者分配权重。<a href="https://arxiv.org/abs/2510.10925">PerSyn</a><span class="research-venue">（ACL 2026）</span>的出发点是“更强的模型不一定是更好的老师”：在生成数据之前，先给每个问题挑出最适合这个学生的老师。能传下去多少，取决于学生能吸收多少，这一点在我们的<a href="{{ '/zh/research/agentic-intelligence/#data' | relative_url }}">智能体轨迹工作</a>里又出现了一次。</p>

  <h2 id="serve">4. 系统与稳定性</h2>
  <p>部署服务里还藏着一个假设：GPU 不会坏。多卡张量并行时，坏一张卡就可能让整个服务停摆。<a href="https://arxiv.org/abs/2511.11617">AnchorTP</a><span class="research-venue">（DATE 2026）</span>把权重和 KV 缓存放在一个独立的进程里，推理进程崩了它还在；然后把模型重新分到剩下的 GPU 上，并规划出恢复所需的最少数据搬运。</p>
  <p>到了训练智能体，“等待”和“丢状态”这两个问题就更突出了。在 <a href="https://arxiv.org/abs/2608.17393">Lego-RL</a><span class="research-venue">（arXiv 2026）</span>里，一次训练尝试几乎全部时间都是智能体在沙箱里干活，而且每次尝试长短差别很大，同步训练的一批总得等最慢的那个；异步调度能把这些空档填上。训练途中权重更新了，部分 rollout 会先暂停生成、换上新权重，再接着缓存好的前缀往下走，长时间的尝试就不会白跑。启动沙箱的时间主要花在构建镜像上，提前构建好任务镜像、按需拉取，能省掉大部分等待；评分工具则特意内置在每个镜像里，因为能复现的奖励，比快一点拿到的奖励更值钱。看板会把每次尝试为什么结束拆开来看，让我们在误读奖励曲线之前，先分清是基础设施出了问题还是模型本身的问题。<a href="https://www.legox.net/blog/lego-rl-sao/">单 rollout 优化</a><span class="research-venue">（LegoX 博客，2026）</span>则从另一头省钱：用一个学出来的 critic 代替对同一任务的反复采样，训练所需的轨迹少了很多。</p>

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
  <p>对语言模型来说，数据就是文本；对智能体来说，数据是能跑起来、而且能检验结果的环境，大规模生产这种数据，主要是个基础设施问题。做 LegoFlow 和 Terminal-Lego 让我们看清了钱花在哪儿：找候选任务很便宜，真正费劲的是搭运行环境、用测试证明每个任务成立、跑出轨迹，再把答案泄露或推理太浅的筛掉，最后只有一小部分候选能留下来。我觉得智能体数据的扩展单位，是“经过验证、能够复现的环境”；评价一套基础设施，就看单位算力下它能搭出、验证并保持干净的环境有多少。这需要快速构建和缓存环境，需要隔离且网络可控的沙箱，需要每个任务、每条轨迹都能追溯来源，还需要让智能体自己就能操作的流水线，LegoFlow 的积木式设计已经往这个方向迈了一步。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/agentic-data-pipeline-zh.svg' | relative_url }}" alt="从候选任务到训练数据的流水线：搭建环境、验证任务、生成轨迹、筛掉答案泄露和推理过浅的轨迹；每一步留下的都更少，大部分成本集中在中间几步，由 LegoFlow 的 Curator 和 Tracer 负责。" width="960" height="340" loading="lazy"></div>
    <figcaption>智能体数据的成本花在哪里。找候选任务很便宜，真正费劲的是搭环境、验证、跑轨迹和筛选。</figcaption>
  </figure>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/legox/terminal-lego-pipeline.png' | relative_url }}" alt="Terminal-Lego 任务构建流程：筛选高质量的 Stack Overflow 问答，依次生成指令、环境、解答、Dockerfile 和测试，审查测试，再通过 Docker 往返验证，只保留通过验证的任务。" width="1600" height="892" loading="lazy"></div>
    <figcaption>一个具体例子：<a href="https://arxiv.org/abs/2606.03461">Terminal-Lego</a><span class="research-venue">（arXiv 2026）</span>只有在完整的 Docker 往返验证通过后，才会留下一个任务。图片来自 <a href="https://www.legox.net/blog/terminal-lego/">Terminal-Lego 博客</a>。</figcaption>
  </figure>
  <p>软件工程是最容易的情况，因为测试能给出干净的信号。下一波智能体数据会来自协作办公，我把它叫作 cowork 数据：文档、表格、邮件，以及横跨多个应用的工作流程，而且常常有人参与。在这些场景里，判断一件事有没有做好要难得多。它需要状态可以检查的模拟应用，需要反应真实的模拟用户，还需要能判断“做得好不好”、而不只是“做没做完”的检查器。我觉得，最后手握好数据的，会是把这套基础设施建起来的团队，而不是手里原始日志最多的团队。</p>

  <div class="research-table-wrap">
    <table>
      <thead><tr><th></th><th>代码数据</th><th>cowork 数据</th></tr></thead>
      <tbody>
        <tr><td>环境</td><td>容器里的代码仓库快照</td><td>文档、表格、邮件和多个应用，常常有人参与</td></tr>
        <tr><td>怎么检验结果</td><td>测试：原代码不过，修复后能过</td><td>可检查的应用状态，加上对完成质量的判断；通常没有单元测试</td></tr>
        <tr><td>主要难点</td><td>答案泄露、大规模搭环境、推理过浅的轨迹</td><td>模拟应用和人；判断“做得好不好”，而不只是“做没做完”</td></tr>
        <tr><td>需要的基础设施</td><td>快速构建与缓存、隔离沙箱、防泄露、来源可追溯</td><td>状态可检查的模拟应用、模拟用户、质量检查器、可回放的会话</td></tr>
      </tbody>
    </table>
  </div>

  <h3 id="trajectory-efficiency">效率应该按整条轨迹算，而不是按单次调用算</h3>
  <p>大多数效率方法，包括我们自己的不少工作，都是按一次回答来评估的。可对智能体来说，一次压缩或缓存的决定如果丢了一个细节，后面可能要多绕好几步，省下的那点成本也就搭进去了。我觉得智能体的效率要放在整个任务上算：拿到一个经过验证的结果，一共花了多少算力、显存和时间。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/trajectory-efficiency-zh.svg' | relative_url }}" alt="两条轨迹对比：保留完整上下文时，智能体几步就得到经过验证的结果；上下文丢了一个细节时，每次调用更便宜，但要多走几步去重读、重试、重新测试，整体更慢也更贵。" width="900" height="300" loading="lazy"></div>
    <figcaption>单次省下的，整体上又亏了回去。智能体的效率要按拿到验证结果的整条轨迹来算。</figcaption>
  </figure>

  <p>这也改变了记忆该留什么。智能体的上下文里大多是工具输出，而不是普通文字，所以 D2O 和 UNComp 背后的思路，也就是留下后面会用到的信息、给删掉的内容留条退路，应该用到观察结果和动作上，而不只是用在 token 上。</p>

  <h3 id="long-runs">超长程运行：几周的活，需要像部署服务一样的记忆和稳定性</h3>
  <p>当智能体接手要干上几天甚至几周的任务，智能体训练也动辄牵动成千上万个沙箱，两个老问题会以更大的规模回来。第一个是记忆。没有哪个上下文窗口装得下几周的工具输出，所以智能体的记忆得分层：手边是一段短的工作上下文，往后是对早先工作的压缩摘要，再往后是一个需要精确细节时可以检索的存档。D2O 的“删掉的还能找回来”、UNComp 对哪些部分真正承载信息的分析，都是 token 层面上的早期版本；Prefilling-dLLM 把长前缀缓存一次、之后只读相关块的做法，也是同一个思路。不均匀地分配、永远留条退路，这些原则应该能放大到整个项目的层面。</p>
  <p>第二个是稳定性。几周下来，机器会坏，沙箱会崩，模型也可能在任务中途更新。AnchorTP 让部署服务变稳的做法，即把状态和可能崩溃的进程分开、用最少的搬运恢复，还有部分 rollout 背后“从断点接着走，而不是从头再来”的思路，都应该成为长时间运行的标配。此外还需要足够精确的记录，让实验出了故障也能接着跑、结果依然可信；也需要按整个任务来记账，这样我们才知道一个智能体干一周活到底花了多少钱。</p>

  <h3 id="ai-for-ai-compute">在 AI 改进 AI 的循环里，算力应该更多地流向验证</h3>
  <p>AI 帮着改进 AI 的时候，每一轮都要把算力花在提出候选、运行候选、检验候选和确认最终结果上。我们做智能体的经验是，可不可靠，往往就看检验这一步。所以我觉得，这类循环的效率问题，与其说是“候选能生成多快”，不如说是“要花多少成本才能相信一个结果”。更便宜的审查者和验证器，比如 <a href="https://arxiv.org/abs/2607.06065">SWE-Review</a> 和 SWE-Lego 的验证器所指的那种，很可能是最大的杠杆。各轮之间的进展也应该在相同的总预算下比较，把失败的尝试和复现都算进去，免得把“花得更多”当成“循环变好了”。</p>

  <h3 id="ai-for-science">AI for Science：用便宜的算力，决定昂贵的实验往哪儿做</h3>
  <p>在科学研究里，最贵的一步通常不是模型，而是实验本身：一次长时间的模拟，一次湿实验，一段仪器机时。这让 ATTS 里“先打草稿、再把关”的模式显得特别合适：便宜的模型或快速的近似模拟先提出、筛选大量候选，昂贵的模拟或实验只用来检验最有希望的那几个，每一层筛掉多少，则用类似 ATTS 中共性预测那样经过校准的规则来控制。我还猜想，让词表成为一个扩展维度的那套道理，在科学数据上也成立：分子、序列或测量数据怎么切成 token，是一个应该随预算一起调整的设计选择，而不是一个固定的预处理步骤。实验很难重做，所以智能体数据那边的基础设施经验可以直接搬过来：每个结果都带着来源和设置，失败的实验留着别扔，一个发现只有在搜索时没用过的条件下复现出来，才算数。</p>

  <h2 id="open-questions">还没解决的问题</h2>
  <ul class="research-questions">
    <li><strong>协作办公场景下，经过验证、能够复现的环境应该长什么样？</strong>没有单元测试，结果只能靠应用状态和质量判断来检验，而我们还不知道怎么让这种检验既便宜又不容易被钻空子。</li>
    <li><strong>上下文大多是工具输出的智能体，词表和缓存该怎么设计？</strong>日志、文件列表、测试结果，和我们调分词器、调缓存策略时用的普通文字完全不是一回事。</li>
    <li><strong>智能体 RL 的成本能省到什么程度，才会开始伤到能力？</strong>异步调度、部分 rollout、单 rollout 训练都能省算力，但每一种都会让训练数据和当前模型之间的“新鲜度”发生变化。</li>
    <li><strong>一个要干几周的智能体，该怎么决定忘掉什么？</strong>在 token 层面，我们能看到注意力用了什么；到了项目层面，一个细节值不值得留，可能要过好几天才看得出来。</li>
    <li><strong>AI 改进 AI 的循环，该怎么在探索和验证之间分预算？</strong>检验太少，假的进步会混进来；检验太多，搜索又慢下来。这个平衡点该怎么定，我们还缺少有原则的方法。</li>
    <li><strong>什么时候能放心让便宜的近似模型来筛选科学实验？</strong>如果它恰好把那些本该带来意外发现的候选筛掉了，就失去了意义。校准有帮助，可科学最在意的，往往正是近似模型从没见过的情况。</li>
  </ul>

  <p class="research-readmore">代码与实验：<a href="https://github.com/sail-sg/scaling-with-vocab">词表研究</a> · <a href="https://huggingface.co/spaces/sail/scaling-with-vocab-demo">词表计算器</a> · <a href="https://github.com/LegoX/Lego-RL">Lego-RL</a> · <a href="https://github.com/LegoX/LegoFlow">LegoFlow</a></p>

  {% include research/paper-list.liquid group="efficient" lang="zh" %}

  <p>相关页面：<a href="{{ '/zh/research/agentic-intelligence/' | relative_url }}">智能体的学习、协作与自我改进</a></p>
</div>
