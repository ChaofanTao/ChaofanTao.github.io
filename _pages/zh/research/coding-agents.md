---
layout: default
title: "代码智能体、智能体数据与智能体强化学习"
description: "陶超凡在 LegoX 的开源代码智能体研究：可验证软件工程任务构建、监督微调配方、终端智能体轨迹，以及在 Claude Code、OpenHands、OpenCode 内原生训练的强化学习。"
permalink: /zh/research/coding-agents/
research_lang: zh
last_modified_at: 2026-11-03
og_image: /assets/img/og-image.png
about:
  - 代码智能体
  - 软件工程智能体
  - SWE-bench
  - 智能体强化学习
  - 终端智能体
  - 智能体数据
faq:
  - q: "SWE-Lego 是什么？"
    a: "SWE-Lego 是陶超凡等人提出的软件问题修复监督微调配方：包含 3.2 万个任务实例和 1.8 万条验证轨迹的数据集，配合错误掩码和按难度递进的课程学习。仅用 SFT，SWE-Lego-Qwen3-8B 和 SWE-Lego-Qwen3-32B 在 SWE-bench Verified 上分别达到 42.2% 和 52.6%；加上基于验证器的测试时扩展（TTS@16）后分别为 49.6% 和 58.8%，评测排除了 Git 历史泄漏。"
  - q: "Lego-RL 是什么？"
    a: "Lego-RL 是 LegoX 的原生 harness 强化学习框架：在不修改控制流的 OpenHands SDK、Claude Code 或 OpenCode 内直接训练策略，并保持 token 级一致性和 MoE 路由回放。以 Qwen3.5-35B-A3B 为起点，每个 harness 单次训练即把 SWE-bench Verified 从 64.0、62.4、57.2 提升到 70.4、68.2、66.6。"
  - q: "LegoX 的数据、模型和代码开源吗？"
    a: "开源。代码在 GitHub（LegoX/SWE-Lego、LegoX/LegoFlow、LegoX/Lego-RL、SWE-Lego/terminal-lego），数据集和模型在 Hugging Face 的 Lego-X 与 SWE-Lego 组织下，包括 LegoFlow-SWE 和 Terminal-Lego-15k。"
  - q: "更强的代码智能体是更好的蒸馏教师吗？"
    a: "不一定。Terminal-Lego 研究中，Claude Opus 4.6 在 Terminal-Bench 2.0 上得分 69.4，但用它的轨迹训练出的 Qwen3 学生弱于用 DeepSeek-V3.2（39.3）轨迹训练的学生。真正能迁移的是在 harness 中显式“观察-行动-验证”的轨迹，论文称之为环境锚定监督。"
  - q: "如何与陶超凡合作或申请实习？"
    a: "通过 chaofantao.top 联系区的 Email me 按钮发邮件，标题注明 [Interest]，附简短介绍和一到两个代表性链接，例如论文、GitHub 仓库、博客或 demo。"
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

  <p class="research-lead"><strong>陶超凡在 <a href="https://www.legox.net/">LegoX</a> 构建开源的大模型软件工程智能体与终端智能体训练方案。</strong>工作覆盖完整闭环：从真实 GitHub PR 中挖掘可验证任务（LegoFlow），带错误掩码与难度课程的监督微调（SWE-Lego），面向终端智能体的环境锚定轨迹（Terminal-Lego），以及在 OpenHands、Claude Code、OpenCode 等原生 harness 内直接做强化学习（Lego-RL）。代码、数据和模型均已开源。</p>

  <h2 id="key-results">核心结果</h2>
  <div class="research-table-wrap">
    <table>
      <thead>
        <tr><th>项目</th><th>模型与设置</th><th>基准</th><th>结果</th><th>出处</th></tr>
      </thead>
      <tbody>
        <tr><td>Lego-RL</td><td>Qwen3.5-35B-A3B，每个 harness 单次 RL 训练</td><td>SWE-bench Verified</td><td>OpenHands SDK 64.0 → 70.4<br>Claude Code 62.4 → 68.2<br>OpenCode 57.2 → 66.6</td><td><a href="https://www.legox.net/blog/lego-rl/">博客</a></td></tr>
        <tr><td>LegoFlow</td><td>Qwen3.5-35B-A3B-Base，智能体管理的两轮迭代，512 条轨迹</td><td>SWE-bench Verified</td><td>7.6% → 64.4%</td><td><a href="https://www.legox.net/blog/legoflow/">博客</a></td></tr>
        <tr><td>LegoFlow-SWE</td><td>Qwen3.5-35B-A3B-Base，约 1K 条轨迹</td><td>SWE-bench Verified / Pro / Multilingual</td><td>70.2% / 48.8% / 57.0%</td><td><a href="https://www.legox.net/blog/legoflow/">博客</a></td></tr>
        <tr><td>SWE-Lego</td><td>Qwen3-8B / Qwen3-32B，仅 SFT，无泄漏评测</td><td>SWE-bench Verified</td><td>42.2% / 52.6%<br>TTS@16：49.6% / 58.8%</td><td><a href="https://arxiv.org/abs/2601.01426">arXiv:2601.01426</a></td></tr>
        <tr><td>Terminal-Lego</td><td>Qwen3-32B，1.53 万条轨迹</td><td>Terminal-Bench 2.0</td><td>24.3%，数据量约为此前结果的 1/30</td><td><a href="https://arxiv.org/abs/2606.03461">arXiv:2606.03461</a></td></tr>
      </tbody>
    </table>
  </div>

  <h2 id="verified-tasks">如何大规模构建可验证的代码智能体任务？</h2>
  <p>任务只有能被环境证明才有训练价值：有缺陷的版本必须测试失败，参考修复必须测试通过。LegoFlow 的 Curator 模块发现已合并的 PR，把每个 PR 改写成无答案泄漏的任务，以 Harbor 任务格式组装隔离环境，并且只保留通过这一“先失败后通过”检查的任务。每个模块（Curator、Tracer、Trainer、Evaluator）都封装成插件 skill，可由 Claude Code、Codex 等代码智能体直接调用。</p>
  <p>LegoFlow-SWE 从 70 多万个仓库、1200 万个候选 PR 出发，最终保留 5000 个可验证任务，覆盖 8 种编程语言和 20 类任务标签，仅占原始池的 0.0417%。GLM-5.2 产生了 9767 条 rollout，其中 2780 条通过验证。在教师模型、脚手架和预算一致的条件下，LegoFlow-SWE 在 SWE-bench Verified、Pro、Multilingual 上分别比 SWE-rebench-v2 高 5.8、1.9、1.0 个点。</p>

  <h2 id="sft">只靠监督微调能训练出强的软件工程智能体吗？</h2>
  <p>对 8B 到 32B 的开源模型来说可以。SWE-Lego 结合真实与合成来源的 3.2 万个可执行任务和 1.8 万条验证轨迹，训练时掩码错误步骤，并按难度组织数据。消融实验中，数据集贡献 25.6 个点，改进的 SFT 贡献 3.8 个点，基于验证器的测试时扩展再贡献 6.2 个点，把 Qwen3-32B 在 SWE-bench Verified 上从 23.2% 提升到 58.8%。从 Git 历史中“偷看”答案的轨迹被过滤，结果在无泄漏镜像上报告。</p>

  <h2 id="harness-native-rl">为什么要在智能体的原生 harness 里做强化学习？</h2>
  <p>因为 harness 会改变模型学到的东西。同一个 Qwen3.5-35B-A3B 检查点在 OpenHands SDK、Claude Code、OpenCode 下的 SWE-bench Verified 分别是 64.0、62.4、57.2，仅 harness 就带来 6.8 个点的差距。Lego-RL 在每个 harness 内训练且不改动其控制流，保持 token-in/token-out 一致和历史对齐，并回放 rollout 时的 MoE 路由。训练与推理的采样 token 概率相关系数 r ≥ 0.998，异步训练比同步快 2.5 倍（按计算吞吐校正后约 1.9 倍）。</p>
  <p>三次训练都使用相同的 2699 个任务和 200k 上下文预算，共 126 步。在抽样的 OpenHands SDK 轨迹中，训练后“修改文件后重新读取确认”的比例从 73.6% 升至 98.1%。</p>

  <h2 id="teachers">更强的智能体是更好的教师吗？</h2>
  <p>不是。Terminal-Lego 研究中，Claude Opus 4.6 是 Terminal-Bench 2.0 上最强的解题者（69.4），但用它的轨迹训练的 Qwen3-8B 和 Qwen3-32B 学生只有 5.6 和 15.5；用 DeepSeek-V3.2（39.3）轨迹训练的学生达到 10.5 和 20.6。差异取决于“有相关先前观察支撑的动作”占比，而非教师得分。</p>
  <blockquote>“最好的解题者是最差的教师。”——<a href="https://www.legox.net/blog/terminal-lego/">LegoX，Terminal-Lego</a></blockquote>
  <p>Terminal-Lego 把 Stack Overflow 问题转化为 1.5 万多个经 Docker 验证的终端任务，覆盖 13 个类别下的 90 多个技术领域。</p>

  <h2 id="evaluation">代码智能体应该怎么评测？</h2>
  <p>固定题集上的静态通过率无法反映真实的软件开发过程。<a href="https://arxiv.org/abs/2505.23932">SwingArena</a>（ICLR 2026 Oral）让大模型轮流担任补丁提交者和编写测试的审阅者，在 CI 流水线中评测 400 多个真实 GitHub issue，覆盖 C++、Python、Rust、Go。<a href="https://arxiv.org/abs/2604.06861">REAgent</a>（ICSE 2027）把 issue 描述本身当作需要检查和完善的需求，在三个基准上优于五个基线。代码之外的强化学习奖励设计见 <a href="https://arxiv.org/abs/2601.18533">RLVRR</a>（ICLR 2026），它把单一可验证奖励转化为基于参考答案的奖励链。</p>

  <h2 id="resources">代码、数据与模型</h2>
  <ul>
    <li>LegoFlow：<a href="https://github.com/LegoX/LegoFlow">GitHub</a> · <a href="https://huggingface.co/collections/Lego-X/legoflow">Hugging Face</a> · <a href="https://www.legox.net/blog/legoflow/">介绍</a></li>
    <li>Lego-RL：<a href="https://github.com/LegoX/Lego-RL">GitHub</a> · <a href="https://huggingface.co/collections/Lego-X/lego-rl">Hugging Face</a> · <a href="https://www.legox.net/blog/lego-rl/">介绍</a></li>
    <li>Terminal-Lego：<a href="https://github.com/SWE-Lego/terminal-lego">GitHub</a> · <a href="https://huggingface.co/datasets/SWE-Lego/Terminal-Lego-15k">Terminal-Lego-15k</a> · <a href="https://www.legox.net/blog/terminal-lego/">介绍</a></li>
    <li>SWE-Lego：<a href="https://github.com/LegoX/SWE-Lego">GitHub</a> · <a href="https://arxiv.org/abs/2601.01426">论文</a> · <a href="https://www.legox.net/blog/swe-lego/">介绍</a></li>
  </ul>

  <h2 id="papers">相关论文</h2>
  {% include research/paper-list.liquid topic="coding-agents" lang="zh" %}

  {% include research/faq.liquid %}

  <p>相关页面：<a href="{{ '/zh/research/efficient-llm/' | relative_url }}">高效大模型训练与推理</a> · <a href="{{ '/zh/research/multimodal-reasoning/' | relative_url }}">多模态推理与智能体</a> · <a href="{{ '/llms.txt' | relative_url }}">llms.txt</a></p>
</div>
