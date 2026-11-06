---
layout: default
title: "智能体的学习、协作与自我改进"
description: "从多模态推理、机器人和代码智能体出发，讨论学习与验证，以及多智能体协作、AI for AI 和递归自我改进的开放问题。"
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
  - 多智能体协作
  - AI for AI
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
  <p class="research-dek">模型能写出一个答案之后，还需要学会什么，才能自己探索、检验和改进？从多模态推理、机器人到代码智能体，我参与的工作从不同侧面触及这个问题。更远处，还有多智能体协作与 AI 改进 AI 的可能性。</p>
  <p class="research-meta">作者：<a href="{{ '/' | relative_url }}">陶超凡（Chaofan Tao）</a> · 最后更新 <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%Y-%m-%d" }}</time></p>

  <p>一张图里可能藏着搜索所需的线索，一次失败的测试可能推翻原来的判断，一段看起来正确的操作也可能依赖环境里根本不存在的条件。智能体要把事情做成，得不断处理这些落差：看清眼前的情况，决定下一步，再用结果修正自己。</p>
  <p>代码是研究这件事很方便的起点，因为动作、修改和测试结果都能留下记录。它与我此前参与的视觉理解、多模态推理和机器人研究也有共同的问题：行动依据从哪里来，错误能否被发现，经验能否用在下一次任务中。近期的 LegoX 项目把其中一些问题做成了可以运行和检查的系统；下文也会借助其他团队的研究，讨论这些经验怎样延伸到更广义的 agentic intelligence。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/agentic-loop-zh.svg' | relative_url }}" alt="智能体学习过程：环境、经验、训练信号与评测相互影响，图中列出研究各环节的相关工作。" width="760" height="480" loading="eager"></div>
    <figcaption>一次尝试留下经验，训练从经验中提取能力，评测再检查这种能力能否用到新任务上。</figcaption>
  </figure>

  <p class="research-toc">本页内容：<a href="#environment">行动的依据</a> · <a href="#physical">多模态与机器人</a> · <a href="#experience">值得学习的经验</a> · <a href="#signal">训练与反馈</a> · <a href="#evaluation">独立验证</a> · <a href="#long-horizon">多智能体协作</a> · <a href="#insights">AI for AI 与 RSI</a> · <a href="#open-questions">开放问题</a></p>

  <h2 id="environment">模型能做什么，也取决于它看到了什么</h2>
  <p>代码智能体通过运行框架（harness）接触环境。框架决定文件怎样读取、工具结果怎样呈现、历史记录何时压缩，以及命令失败后怎样继续。假如一条重要报错被截掉，模型就得在缺少这条信息的情况下做决定。这样的变化会影响最终表现。</p>
  <p><a href="https://www.legox.net/blog/lego-rl/">Lego-RL</a> 的一组评测中，同一个初始模型在三套框架下的得分相差 6.8 个百分点。我们因此选择在实际使用的框架中训练，并进一步尝试<a href="https://www.legox.net/blog/lego-rl-cross-harness/">混合多套框架训练同一个模型</a>。在所测的三套框架上，共享模型的平均表现接近分别训练三个模型。这支持在已知接口之间共享能力；换到从未见过的工具和环境后，哪些能力还能保留下来，仍是值得继续追问的问题。</p>

  <h3 id="physical">图像和机器人让这个问题更具体</h3>
  <p><a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a> 要求智能体抓住图像细节，经过多轮图文搜索和交叉核对找到答案。能否裁剪一处细节、沿着它继续搜索，会影响后面的推理。<a href="https://arxiv.org/abs/2505.15929">PhyX</a> 则要求把看到的现象与物理约束联系起来；<a href="https://arxiv.org/abs/2408.09511">NAVERO</a> 检查模型能否分清视频中相近的动作和关系。答错之后，先分清是没看见、没找对，还是推理出错，往往比笼统地要求“再想一遍”更有帮助。</p>
  <p><a href="https://arxiv.org/abs/2402.16117">RoboCodeX</a> 把高层指令拆成针对具体物体的操作，再生成控制代码，让感知、约束和动作之间的联系更明确。走到真实环境里，反馈的代价也变了：命令可以重新运行，物理动作却未必能撤销。未来更自主的智能体，能否根据环境决定什么时候先观察、什么时候再行动？这也是把视觉生成与理解能力接入行动系统时需要回答的问题。关于这些视觉模型的背景，可以参考我们的<a href="https://arxiv.org/abs/2411.05902">视觉自回归模型综述</a>。</p>

  <h2 id="experience">训练材料要留下可学习的过程</h2>
  <p><a href="https://www.legox.net/blog/legoflow/">LegoFlow</a> 从真实代码修改中构造可运行的任务，检查原始版本无法通过相关测试、参考补丁可以通过。<a href="https://arxiv.org/abs/2601.01426">SWE-Lego</a> 再把真实任务与通过注入错误构造的任务结合起来，兼顾复杂度和规模。有了任务，接下来才是更难的选择：哪些操作记录值得拿来教模型？</p>
  <p><a href="https://arxiv.org/abs/2606.03461">Terminal-Lego</a> 提供了一个很好的例子。在所比较的教师与学生组合里，教师自己更会解题，并不意味着学生学完以后更强。明确展示“查看相关信息、据此行动、检查结果”的记录，迁移效果更好。对于学生，一串正确命令和一个能学会的方法之间，还差着每一步为什么这样做的依据。</p>
  <p>长度也不能代替这些依据。<a href="https://www.legox.net/blog/legoflow-experiments/">LegoFlow 的实验</a>中，按平均推理长度分组训练，最短的一组明显落后，后面几组的提升却很快趋缓。去掉分析不足的示范有帮助，继续增加文字则未必同样有效。真正值得检查的是关键判断有没有根据，以及新信息出现后，智能体有没有调整做法。</p>
  <p>数据发布中的细节同样重要。<a href="https://huggingface.co/datasets/Lego-X/LegoFlow-SWE">LegoFlow-SWE 数据卡</a>说明，发布的原始记录里，奖励为 0 同时包含测试失败和没有拿到评分的运行；奖励为 1 表示验证器给出了成功，也不等于完成了答案泄漏审查。如果未来让智能体自动收集数据、自动更新自身，这些区别该怎样保留下来？把环境故障当成推理错误，或者把找到现成答案当成学会解题，都可能让下一轮训练学偏。</p>

  <h2 id="signal">一次经历，怎样变成下一次的能力</h2>
  <p>监督微调（SFT）让模型学习示范，但示范中也会有错误。SWE-Lego 保留失败步骤作为上下文，同时不在这些步骤上计算模仿损失。这样，模型仍能看到尝试为什么失败、后来怎样修正。失败经历能提供信息，是否应该照着其中的动作学习，则是另一个需要处理的选择。</p>
  <p>强化学习（RL）根据结果调整行为，还要求训练时用到的信息对应当时的尝试。<a href="https://arxiv.org/abs/2608.17393">Lego-RL</a> 在生成时记录 token、概率和混合专家模型的路由，再检查训练端能否对应起来。框架重写历史仍会给还原带来困难。这类问题容易被训练曲线掩盖：程序正常运行，更新用到的却可能已经不是当时那次决策。</p>
  <p>在没有唯一答案的任务中，反馈还需要更细。<a href="https://arxiv.org/abs/2601.18533">RLVRR</a> 从参考答案中提取内容和风格要求；<a href="https://arxiv.org/abs/2601.21968">OVD</a> 用教师的文本评分评价学生生成的片段，保留较好的部分、替换较差的后续内容。多模态研究也显示，<a href="https://arxiv.org/abs/2507.07562">长思维链 SFT 与 RL</a> 的收益在所测组合中并未直接相加，而 <a href="https://arxiv.org/abs/2506.01713">SRPO</a> 专门训练简洁、有帮助的反思。这些工作把问题落得更具体：我们究竟希望模型改变哪一种行为，又有什么反馈能够指出这个变化？</p>

  <h2 id="evaluation">检查应该提供新的证据</h2>
  <p>一个补丁可能修好了示例，却漏掉边界情况；一份实验报告也可能解释得很顺，却没有排除另一种原因。<a href="https://arxiv.org/abs/2607.06065">SWE-Review</a> 让审查智能体自己查阅仓库、追查问题，再评价候选补丁。我们同时考察判断是否准确，以及反馈能否帮助后续修复。这里最有价值的部分，是审查过程能够补上生成时没检查的东西。</p>
  <p>两个智能体得出相同结论，并不自动意味着找到了两份独立证据。如果它们看的是同一段材料、沿用同一个假设，就可能一起漏掉错误。更进一步的协作能否围绕可复查的实验、反例和来源来组织？<a href="https://arxiv.org/abs/2505.23932">SwingArena</a> 中的测试与持续集成、<a href="https://arxiv.org/abs/2604.06861">REAgent</a> 对需求的整理，都提供了具体的检查对象。</p>
  <p>评测环境本身也需要经得起检查。<a href="https://arxiv.org/abs/2610.24206">SWE-Bench Pro V2</a> 修订任务，并在干净容器里重新应用补丁、重新评分。这与 LegoFlow 中遇到的答案泄漏问题相呼应。系统越能主动探索，就越可能触及原先没暴露的评分缺陷。到了自我改进场景，这个问题还会向前多走一步：如果智能体连评测方法都能修改，应该由什么来判断它真的进步了？</p>

  <h2 id="long-horizon">走向多智能体：分工能带来什么</h2>
  <p>更复杂的目标往往涉及多种活动：检索资料、提出假设、设计实验、实现方法、复核结果。它们可能需要不同的工具、上下文和工作节奏。多智能体系统可以让这些过程同时推进，也给了它们相互检查的机会。但怎样分工、共享什么、何时汇合，会直接影响结果。</p>
  <p><a href="https://arxiv.org/abs/2512.08296">Towards a Science of Scaling Agent Systems</a> 在控制工具和计算预算的比较中发现，协作收益取决于任务结构：适合拆开的任务能够受益，依赖严格先后顺序的任务则可能被协调开销拖累。<a href="https://arxiv.org/abs/2503.13657">多智能体失败分析</a>也把分工不清、智能体之间理解不一致，以及验证和停止条件的问题列为重要原因。前沿的问题因而可以更具体：团队怎样学会组织自己，什么时候并行探索，什么时候收拢到一个判断上？</p>
  <p>2026 年 10 月的 <a href="https://arxiv.org/abs/2610.24454">MELD</a> 把这个问题推进到了学习层面，同时更新团队协调者和个体研究智能体；它的执行模块保持固定。这让分工和个体能力之间的联系变得可以研究：协调者分配了什么任务，会决定每个成员获得什么经验；成员学会了什么，又会改变下一轮值得怎样分工。怎样判断一次提升来自更好的成员、更好的组织，还是更多计算，仍需要分开验证。</p>
  <p>共享记忆也有类似问题。一个成员说“这个方法有效”，其他成员需要知道它在哪个数据集、哪份代码和什么设置下有效。环境变化后，旧结论是否应该重新检查？团队能否共享必要的依据，同时保留不同的探索路线？这些问题把多模态感知、工具使用、记忆和验证连接了起来，远不只是在代码任务上多运行几个模型。</p>

  <h2 id="insights">AI for AI：改进能否进入下一轮</h2>
  <p>AI for AI 关注让 AI 参与设计数据、训练方法、评测和计算系统。<a href="https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/">AlphaEvolve</a> 把程序生成、自动评估和进化搜索结合起来，用于算法发现，也产生了计算基础设施方面的改进。<a href="https://sakana.ai/dgm/">Darwin Gödel Machine</a> 则直接修改智能体自身的代码，保留不同版本供后续探索。两者改进的对象不同，却都让“提出改动—运行验证—保留结果”成为可以持续执行的过程。</p>
  <p>递归自我改进（recursive self-improvement，RSI）还要追问：这轮得到的改进，能否提高下一轮发现改进的能力？2026 年 9 月的 <a href="https://arxiv.org/abs/2609.26457">AIDE²</a> 研究让智能体修改自己的研究代码，并把选中的版本用于后续轮次，报告了多轮改进及向留出任务的迁移。这样的结果让问题变得具体，也留下了进一步检验的空间：收益来自更好的搜索方法、记忆，还是对某一套任务越来越熟悉？</p>
  <p>如果评测也由智能体生成，反馈来源就成了研究的一部分。<a href="https://arxiv.org/abs/2610.04184">EvalResearchBench</a> 研究智能体能否构造更省成本的评测，并发现开发集上表现最好的评测器，未必在未公开的目标基准上仍然最好。一个值得继续探索的办法，是让提出改进、筛选候选和最终复验使用不同的信息，并持续加入没有参与搜索的新任务。怎样把这件事做得足够可靠、又不让验证成本吞掉全部收益，是 RSI 和<a href="{{ '/zh/research/efficient-ml-ai-infrastructure/#long-horizon' | relative_url }}">效率研究</a>共同面对的问题。</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/self-improvement-questions-zh.svg' | relative_url }}" alt="自我改进的研究问题：多个智能体提出和执行方案，经独立复验后保留可继承的改进，再用于下一轮探索；协调、验证与迁移分别需要检验。" width="960" height="320" loading="lazy"></div>
    <figcaption>一个用于讨论的自我改进循环。箭头表示需要验证的联系：能生成新版本，还需要证明它更有用，并能帮助下一轮探索。</figcaption>
  </figure>

  <h2 id="open-questions">沿着这些工作，还可以继续问什么</h2>
  <ul>
    <li>在相同总预算下，多智能体怎样提供单个智能体难以获得的证据与探索范围？能否学会根据任务动态调整分工？</li>
    <li>从一次成功到稳定的能力提升，经验应该进入模型权重、外部技能还是共享记忆？它们分别能迁移到哪些新环境？</li>
    <li>一个系统连续改进多轮后，怎样证明下一轮探索本身更有效，而不只是筛选过更多候选？新的评测任务和复验预算应该怎样安排？</li>
  </ul>

  <h2 id="resources">项目资源与论文</h2>
  <p>下面是文中近期项目的开源资源。不同时期的相关论文和完整作者名单列在后面，也可以查阅我的 <a href="https://scholar.google.com/citations?user=gjmfLroAAAAJ">Google Scholar</a>、<a href="https://github.com/ChaofanTao">GitHub</a> 和 <a href="https://huggingface.co/tcftrees">Hugging Face</a>。</p>
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
