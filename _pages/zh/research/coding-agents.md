---
layout: default
title: "代码智能体、智能体数据与智能体强化学习"
description: "陶超凡在 LegoX 的开源代码智能体研究：可验证任务数据、监督微调与强化学习方案、轨迹经验、评测方法与开源基础设施。"
permalink: /zh/research/coding-agents/
research_lang: zh
last_modified_at: 2026-11-04
og_image: /assets/img/og-image.png
about:
  - 代码智能体
  - 软件工程智能体
  - 智能体强化学习
  - 终端智能体
  - 智能体数据
faq:
  - q: "SWE-Lego 是什么？"
    a: "SWE-Lego 是一套开源的软件问题修复监督微调方案。它表明只要数据做对，轻量的纯 SFT 流程也能训练出很强的开源代码智能体：结合真实与合成任务、掩码错误步骤、按难度组织训练，并剔除从 Git 历史中“偷看”答案的轨迹。"
  - q: "Lego-RL 是什么？"
    a: "Lego-RL 是 LegoX 的强化学习框架，直接在模型实际运行的、未经修改的智能体 harness（如 OpenHands、Claude Code、OpenCode）里训练。它保留 rollout 时生成的原始 token，回放混合专家模型的路由，异步训练，并让每条轨迹都可检查。"
  - q: "LegoX 的数据、代码和模型开源吗？"
    a: "开源。代码在 GitHub 的 LegoX 与 SWE-Lego 组织下，数据集和模型在 Hugging Face 的 Lego-X 与 SWE-Lego 组织下。"
  - q: "更强的代码智能体就是更好的教师吗？"
    a: "不一定。Terminal-Lego 研究发现，显式地观察环境、基于观察行动、再验证结果的轨迹最能教会学生，即使它们来自更弱的智能体；而直接跳到答案的强模型，留给学生可模仿的行为很少。"
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

  <p class="research-lead"><strong>陶超凡在 <a href="https://www.legox.net/">LegoX</a> 研究如何端到端地训练开源大模型代码智能体。</strong>关注点是通常不公开的那部分技术栈：可验证的训练任务从哪里来、哪些智能体轨迹值得学习、微调和强化学习如何适配人们真正在用的智能体工具，以及智能体该如何评测。产出是可复用的方案、开放数据和基础设施，而不是一次性的模型。</p>

  <ul class="research-highlights">
    <li><strong>规模化的可验证数据</strong>把真实 PR 和社区问答转化为能由环境自动验证的可执行任务。</li>
    <li><strong>训练方案</strong>教会模型良好调试习惯的微调，以及在真实智能体 harness 内运行的强化学习。</li>
    <li><strong>实验经验</strong>什么样的轨迹值得模仿，以及为什么最强的智能体不一定是最好的教师。</li>
    <li><strong>开源基础设施</strong>可由智能体操作的流水线、沙箱环境和可视化看板，代码与数据全部开放。</li>
  </ul>

  <h2 id="why">为什么重要？</h2>
  <p>代码智能体如今以“能否修复真实软件”来衡量，但多数强系统的训练流程难以复现：数据、环境、训练和评测紧密耦合，且很少公开。这项工作把整条流程拆成可复用的模块，让其他人可以单独重建、审查和改进每一部分。</p>

  <h2 id="data">好的训练数据从哪里来？</h2>
  <p>来自真实的软件历史，并由执行结果把关。<a href="https://www.legox.net/blog/legoflow/">LegoFlow</a> 挖掘已合并的 PR，把每个 PR 改写成自带环境和测试的独立任务；只有环境能证明的任务才被保留：原始代码必须测试失败，参考修复必须测试通过。<a href="https://www.legox.net/blog/terminal-lego/">Terminal-Lego</a> 把同样的原则用于命令行任务，将社区问答转化为沙箱任务。</p>
  <p><strong>经验：</strong>原始候选中只有极少数能通过验证；按可验证性和轨迹中是否有真实推理来筛选，比单纯堆数据量更重要。</p>

  <h2 id="training">代码智能体该怎么训练？</h2>
  <p><strong>微调。</strong><a href="https://arxiv.org/abs/2601.01426">SWE-Lego</a> 表明，只要数据做对，轻量的纯 SFT 方案也能很强：结合真实与合成任务，掩码错误步骤避免模型模仿失误，按难度组织训练，并剔除从 Git 历史中“偷看”答案的轨迹。</p>
  <p><strong>强化学习。</strong><a href="https://www.legox.net/blog/lego-rl/">Lego-RL</a> 直接在智能体实际运行的、未经修改的 harness（如 OpenHands、Claude Code、OpenCode）里训练，因为 harness 决定了模型看到什么、做什么。关键工程点：保留 rollout 时生成的原始 token，回放混合专家模型的路由，异步训练，并让每条轨迹都可检查。</p>

  <h2 id="teachers">什么样的轨迹是好教材？</h2>
  <p>关键是“看得见的环境锚定”，而不是模型有多强。Terminal-Lego 研究发现，先观察环境、再基于观察行动、最后验证结果的轨迹最能迁移给学生；而直接跳到答案的强模型，留给学生可学的东西很少。</p>
  <blockquote>“最好的解题者是最差的教师。”——<a href="https://www.legox.net/blog/terminal-lego/">LegoX，Terminal-Lego</a></blockquote>
  <p>实践上的启示是：有意设计交互方式，让轨迹里包含值得模仿的行为，论文称之为 harness engineering。</p>

  <h2 id="evaluation">代码智能体该怎么评测？</h2>
  <p>要更贴近真实的软件开发。<a href="https://arxiv.org/abs/2505.23932">SwingArena</a>（ICLR Oral）把模型放进持续集成流程，让它们同时担任补丁提交者和编写测试的审阅者，覆盖多种编程语言。<a href="https://arxiv.org/abs/2604.06861">REAgent</a>（ICSE）把 issue 描述当作需要先检查和完善的需求。<a href="https://arxiv.org/abs/2601.18533">RLVRR</a>（ICLR）把可验证奖励从代码扩展到开放式生成。</p>

  <h2 id="resources">开源代码与数据</h2>
  <ul>
    <li>LegoFlow：<a href="https://github.com/LegoX/LegoFlow">代码</a> · <a href="https://huggingface.co/collections/Lego-X/legoflow">数据</a> · <a href="https://www.legox.net/blog/legoflow/">介绍</a></li>
    <li>Lego-RL：<a href="https://github.com/LegoX/Lego-RL">代码</a> · <a href="https://huggingface.co/collections/Lego-X/lego-rl">模型与数据</a> · <a href="https://www.legox.net/blog/lego-rl/">介绍</a></li>
    <li>Terminal-Lego：<a href="https://github.com/SWE-Lego/terminal-lego">代码</a> · <a href="https://huggingface.co/datasets/SWE-Lego/Terminal-Lego-15k">数据</a> · <a href="https://www.legox.net/blog/terminal-lego/">介绍</a></li>
    <li>SWE-Lego：<a href="https://github.com/LegoX/SWE-Lego">代码</a> · <a href="https://arxiv.org/abs/2601.01426">论文</a> · <a href="https://www.legox.net/blog/swe-lego/">介绍</a></li>
  </ul>

  {% include research/paper-list.liquid topic="coding-agents" lang="zh" %}

  {% include research/faq.liquid %}

  <p>相关页面：<a href="{{ '/zh/research/efficient-llm/' | relative_url }}">高效大模型训练与推理</a> · <a href="{{ '/zh/research/multimodal-reasoning/' | relative_url }}">多模态推理与智能体</a></p>
</div>
