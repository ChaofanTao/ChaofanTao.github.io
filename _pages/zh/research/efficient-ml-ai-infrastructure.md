---
layout: default
title: "高效机器学习与 AI 基础设施"
description: "陶超凡的高效机器学习研究：词表设计、模型压缩、长上下文、推理时计算、稳定的部署服务和知识蒸馏，各自卡在哪个“想当然”的假设上，又是怎么解决的。"
permalink: /zh/research/efficient-ml-ai-infrastructure/
research_lang: zh
last_modified_at: 2026-11-06
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
  <p class="research-dek">在我的经验里，大多数效率问题，都源于一个悄悄不再成立的假设。这篇文章跟着一个模型从设计走到上线，看看我们的每项工作分别推翻了哪个假设。</p>
  <p class="research-meta">作者：<a href="{{ '/' | relative_url }}">陶超凡（Chaofan Tao）</a> · 最后更新 <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%Y-%m-%d" }}</time></p>

  <p>提到效率，大家通常会想到一种交换：牺牲一点效果，省下一些算力或显存。但我见过的更大收益，往往来自另一个地方。一个方法之所以失效或浪费资源，常常是因为它依赖的某个假设，在当初设计时没问题，现在却不成立了。比如：分词器可以在扩大模型之前就定下来；网络的每个部分对压缩的承受能力都一样；缓存里每个 token 都同样重要；等待同步不花成本；GPU 不会坏；最强的老师教得最好。</p>
  <p>找出那个不成立的假设，往往是最难的一步；判断对了，解决办法通常很简单。这篇文章按模型的“一生”来组织，看每个假设藏在哪个阶段。其中第二部分的量化工作获得了 ACL 2022 杰出论文奖。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/efficiency-lifecycle-zh.svg' | relative_url }}" alt="模型一生五个阶段的示意图：设计、压缩、记忆、计算与服务、迁移，每个阶段对应一个被我们的工作推翻的默认假设，以及相关项目。" width="960" height="300" loading="eager"></div>
    <figcaption>模型一生中的效率问题。每个阶段对应一个常见假设，以及揭示它在哪里不成立的工作。</figcaption>
  </figure>

  <p class="research-toc">本页内容：<a href="#design">设计</a> · <a href="#compress">压缩</a> · <a href="#remember">记忆</a> · <a href="#serve">计算与服务</a> · <a href="#transfer">迁移</a> · <a href="#insights">几点体会</a> · <a href="#open-questions">还没解决的问题</a></p>

  <h2 id="design">1. 设计：分词器不能随便定</h2>
  <p>扩展定律告诉我们，增加参数和数据时损失会怎样变化，但它通常不考虑词表。结果在实际中就能看到：规模差不多的模型，词表大小却相差很大。在 <a href="https://arxiv.org/abs/2407.13623">Scaling Laws with Vocabulary</a>（NeurIPS）里，我们把词表大小当作一个独立的扩展维度来研究：把词表参数和网络其他部分分开；用字符而不是 token 来衡量数据量，这样不同分词器之间才能公平比较；并使用一个不受词表大小影响的损失。我们用三种互相独立的方法估计最合适的词表大小，分别基于 IsoFLOPs 分析、求导和直接拟合损失，结论完全一致：大多数模型的词表都偏小了。</p>
  <p>为什么会存在一个最合适的大小？关键在于取舍。词表越大，同样的文本切出来的 token 越少，能直接表示的概念也越多；但算力有限时，那些不常见的 token 根本练不好。随着算力增加，天平会往大词表倾斜，不过词表的增长应该比模型其他部分慢一些。数据量也很关键：数据少的时候，小一点的词表能避免把罕见 token 学偏；数据远多于“刚好够用”的量时，大一点的词表更划算，只是要记得词表变大也会让推理更贵。我很喜欢这样理解：在算力固定的情况下，最好的词表，就是能让模型读到最多文本的那一个。词表太小，同样的内容要花更多 token；词表太大，算力又都耗在了嵌入层和输出层上。<a href="https://huggingface.co/spaces/sail/scaling-with-vocab-demo">交互式计算器</a>可以直接帮你算出一个可用的数字。</p>

  <h2 id="compress">2. 压缩：模型的各个部分并不一样</h2>
  <p>对 BERT 这类编码器很好用的量化方法，用到 GPT 这类生成模型上就不灵了，而且有一阵子大家都说不清为什么。在 <a href="https://arxiv.org/abs/2203.10705">Compression of Generative Pre-trained Language Models via Quantization</a>（ACL 2022 杰出论文）中，我们找到了两个原因。一是在低精度下，词嵌入会挤成一团、变得几乎一样，生成模型在挑下一个 token 时，就分不清这些选项了。二是不同模块的权重分布差别很大，一套量化设置没法同时照顾到所有模块。解决办法顺着诊断就出来了：用 token 级的对比蒸馏，让每个 token 的表示既贴近全精度模型，又和其他 token 区分开；用按模块的动态缩放，给每个模块单独设定范围。<a href="https://doi.org/10.18653/v1/2023.findings-acl.692">结构化剪枝</a>把同样的思路用在“删减”上，让模型自己学出哪些部分可以去掉。</p>
  <p>在视觉语言模型里，这种不均匀更加明显，因为图像和文字承载信息的方式差别很大。<a href="https://arxiv.org/abs/2301.13741">UPop</a> 在视觉和语言两部分里一起寻找更小的网络，让模型自己学出每部分该剪多少，而不是靠我们拍脑袋定，并且一边搜索一边重新训练。<a href="https://arxiv.org/abs/2305.17455">CrossGET</a> 则在模型运行时合并重复的 token，用一种模态的信息来指导另一种模态里哪些 token 该合并。</p>

  <h2 id="remember">3. 记忆：不是每个 token 都要记，但要留后路</h2>
  <p>做长上下文推理时，KV 缓存要存下前面每个 token 的键和值，很快就会占掉大部分显存。平均地删减很浪费，因为不同层的情况不一样。<a href="https://arxiv.org/abs/2406.13035">D2O</a> 根据每一层注意力集中的程度，给它分配不同的缓存额度；对于删掉的 token，如果和保留下来的很像，还可以把它找回来或合并进去，整个过程都不需要微调。<a href="https://arxiv.org/abs/2410.03090">UNComp</a> 从信息量的角度看这个问题：用矩阵熵衡量不确定性，找出可以压缩的部分；同样的分析，还能指出哪些注意力头和层负责“查找”信息。</p>
  <p>扩散语言模型有自己的麻烦：每一步去噪都要把整段提示重新读一遍。<a href="https://arxiv.org/abs/2606.10537">Prefilling-dLLM</a> 不需要重新训练，它把提示分块缓存一次，之后只用和问题相关的块和 token。一个小细节起了很大作用：在每一块开头放一个序列起始 token（BOS），让注意力有个稳定的“落脚点”。有了它，稀疏的做法甚至能比完整的注意力效果更好。</p>

  <h2 id="serve">4. 计算与服务：花在等待上的成本，比计算本身更高</h2>
  <p>规模一大，瓶颈通常是等待，最大的风险通常是丢失状态。推理时扩展就是前一种情况的典型例子：它通过在生成时多花算力来提升答案质量，常见做法是小模型先写草稿、大模型来检查。我们在 <a href="https://arxiv.org/abs/2509.15148">ATTS</a> 里仔细看了时间都花在哪儿，发现主要成本是同步等待，而不是计算本身。ATTS 把同步检查改成异步推理，并用边运行边校准的共性预测（conformal prediction），把草稿被拒绝的比例控制在统计上可靠的范围内。它可以同时往两个方向扩展：想得更长，以及并行尝试更多。</p>
  <p>部署服务也有一个藏起来的假设：GPU 不会坏。在多卡张量并行里，坏掉一张卡就可能让整个服务停掉。<a href="https://arxiv.org/abs/2511.11617">AnchorTP</a> 把权重和 KV 缓存放在一个独立的进程里，推理进程崩溃了它也还在；然后把模型重新分配到剩下的 GPU 上，并规划出恢复服务所需的最少数据搬运。</p>
  <p><strong>训练智能体的基础设施。</strong>在用 <a href="{{ '/zh/research/agentic-intelligence/#signal' | relative_url }}">真实 harness 里的 RL</a> 训练智能体时，这两条经验表现得更加明显。在 Lego-RL 里，一次训练尝试几乎全部时间都是智能体在干活：在沙箱里读文件、改代码、跑测试。每次尝试时间长、长短差别也很大，同步训练的一批总得等最慢的那个；异步调度则让空出来的位置马上开始新的尝试。如果训练途中权重更新了，部分 rollout 会先暂停生成、加载新权重，再接着缓存的内容在同一台机器上继续，长时间的尝试就不会白费。启动沙箱的时间主要花在构建镜像上，所以预先构建好任务镜像、挂载智能体运行环境、按需拉取镜像，省掉了大部分等待。有一处我们是有意选了更慢的做法：每个镜像里都内置了评分工具，因为能复现的奖励，比快一点拿到的奖励更有价值。说到底，智能体 RL 很大程度上是一个效率和稳定性的问题。</p>

  <h2 id="transfer">5. 迁移：最强的老师不一定教得最好</h2>
  <p>知识蒸馏效果最好的时候，是信号正好适合学生去学，而不是老师越强越好。拿前向 KL 和反向 KL 的选择来说，常见的说法是一个只盯着老师最主要的答案，另一个会尽量覆盖所有可能的答案。<a href="https://arxiv.org/abs/2404.02657">我们发现</a>，在大模型蒸馏里这两种现象其实都没有出现，两者的最优解是一样的。真正的区别出现在训练早期：前向 KL 更关注老师最常给出的那些 token，反向 KL 更关注不常见的那些。自适应 KL 就是按这个规律给两者分配权重。<a href="https://arxiv.org/abs/2510.10925">PerSyn</a> 的出发点是“更强的模型不一定是更好的老师”：在生成数据之前，先为每个问题挑出最适合这个学生的老师，而不是让所有老师都答一遍、事后再筛选。</p>
  <p>智能体训练从另一个方向得出了同样的结论：来自较弱智能体、脚踏实地的轨迹，比更强模型直接给出的答案教得更好；而<a href="{{ '/zh/research/agentic-intelligence/#signal' | relative_url }}">黑盒老师给出的文字反馈</a>，不用暴露老师内部的概率，也能指导学生。</p>

  <h2 id="insights">几点体会</h2>
  <ol class="research-insights">
    <li><strong>先找出那个不成立的假设，再动手优化。</strong>这里的每个结果，都是从追问“现有方法为什么不行”开始的，而不是直接去试一个更快的版本。原因一旦弄清楚，解决办法往往很简单。</li>
    <li><strong>不均匀才是常态。</strong>层与层、模块与模块、图像与文字、token 与 token、老师与老师，都各不相同。按层、按模块、按模态、按问题分别分配资源，在压缩、缓存和蒸馏里一次次见效。</li>
    <li><strong>给自己留条后路。</strong>删掉的 token 还能找回来、崩溃后状态还在、权重更新时尝试不中断，正是这些设计让大胆的优化变得安全。</li>
    <li><strong>规模越大，等待越是真正的成本。</strong>无论是推理时扩展、部署服务还是智能体训练，最大的收益都来自减少等待，而不是算得更快。</li>
    <li><strong>效率决定了模型能学会什么。</strong>算力不够、练不好的罕见 token，学生消化不了的老师输出，都说明效率不只是成本问题，它还决定了模型到底能学会什么。</li>
  </ol>

  <h2 id="open-questions">还没解决的问题</h2>
  <ul>
    <li>如果把推理成本、多语言数据和代码都考虑进来，词表该怎么选？</li>
    <li>对智能体来说，上下文里大部分是工具输出而不是普通文字，长上下文的记忆应该留下什么？</li>
    <li>在智能体 RL 里，大部分时间花在“做事”而不是算梯度上，还能再快多少？</li>
    <li>部署服务里的容错思路，能不能让长时间的训练也同样稳定？</li>
  </ul>

  {% include research/paper-list.liquid group="efficient" lang="zh" %}

  <p>相关页面：<a href="{{ '/zh/research/agentic-intelligence/' | relative_url }}">智能体编程、推理与评测</a></p>
</div>
