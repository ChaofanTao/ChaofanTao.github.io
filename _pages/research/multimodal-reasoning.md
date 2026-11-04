---
layout: default
title: "Multimodal Reasoning and Agents"
description: "Chaofan Tao's research on multimodal LLMs: how post-training shapes reasoning VLMs, teaching self-reflection, benchmarks that expose real gaps, and turning multimodal reasoning into robot behavior."
permalink: /research/multimodal-reasoning/
research_lang: en
last_modified_at: 2026-11-04
og_image: /assets/img/og-image.png
about:
  - Multimodal large language models
  - Vision-language models
  - Multimodal reasoning
  - Reinforcement learning for VLMs
  - Physical reasoning
  - Multimodal search agents
  - Embodied AI
faq:
  - q: "Should reasoning VLMs be trained with long chain-of-thought SFT or with RL?"
    a: "They help in different places. Long chain-of-thought SFT helps on hard problems but makes answers verbose and can hurt easy ones, while RL improves more broadly and keeps answers concise. Staged, interleaved and progressive training, data mixing and model merging all trade one benefit for another rather than adding them up, which the paper calls the synergy dilemma."
  - q: "What is PhyX?"
    a: "PhyX is a benchmark for physics-grounded reasoning in visual scenes across six physics domains. Its error analysis shows that current multimodal models rely on memorized knowledge, lean too heavily on mathematical formulas and match surface visual patterns instead of understanding the physical situation."
  - q: "What is MMSearch-Plus?"
    a: "MMSearch-Plus is a benchmark and agent framework for multimodal browsing in which answers depend on fine-grained visual cues that must be propagated through image and text search. It includes a set-of-mark module that lets agents mark, crop and zoom before searching."
  - q: "Does Chaofan Tao work on embodied AI?"
    a: "His main focus is coding agents and efficient LLMs. Embodied-related contributions include RoboCodeX (ICML), which turns instructions and visual input into robot behavior expressed as code, and PhyX, a benchmark for the physical reasoning such agents need."
---

{% include research/styles.liquid %}
{% include research/jsonld.liquid topic="multimodal" %}

<div class="research-page">
  <nav class="research-breadcrumb" aria-label="Breadcrumb">
    <a href="{{ '/' | relative_url }}">Chaofan Tao</a><span aria-hidden="true">/</span>
    <a href="{{ '/research/' | relative_url }}">Research</a><span aria-hidden="true">/</span>
    <span>Multimodal reasoning</span>
    <span aria-hidden="true">·</span><a href="{{ '/zh/research/multimodal-reasoning/' | relative_url }}" lang="zh-Hans">中文版</a>
  </nav>

  <h1>Multimodal Reasoning and Agents</h1>
  <p class="research-meta">By <a href="{{ '/' | relative_url }}">Chaofan Tao (陶超凡)</a> · Last updated <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%B %-d, %Y" }}</time></p>

  <p class="research-lead"><strong>Vision-language models can describe images and solve visual math problems, but it is still unclear when they truly reason over what they see.</strong> This line of work studies how post-training shapes their reasoning, teaches them to check their own answers, and builds benchmarks that reveal where they fail, from physics in images to search that depends on visual evidence. It then takes a step toward agents that act in the physical world.</p>

  <p class="research-toc">On this page: <a href="#post-training">Post-training</a> · <a href="#reflection">Self-reflection</a> · <a href="#gaps">Where models fail</a> · <a href="#embodied">Toward embodied agents</a></p>

  <h2 id="post-training">Should reasoning VLMs be trained with long chain-of-thought SFT or with RL?</h2>
  <p>They help in different places, and combining them is harder than it looks. The <a href="https://arxiv.org/abs/2507.07562">synergy dilemma</a> study (TMLR) compares the two across multimodal reasoning benchmarks. Long chain-of-thought SFT teaches structured, in-depth reasoning that helps on hard questions, but it makes answers verbose and hurts easy ones. RL improves generalization and keeps answers short, with consistent gains across difficulty levels but smaller gains on the hardest problems. In language-only models the two usually stack. For vision-language models, every combination tested (two-stage, interleaved and progressive training, data mixing and model merging) traded accuracy, reasoning style and response length against each other instead of adding up.</p>
  <p class="research-knowhow-label">Know-how</p>
  <ul class="research-knowhow">
    <li>Choose by target: long chain-of-thought SFT for hard, multi-step problems; RL for broad robustness and concise answers.</li>
    <li>Do not assume that recipes from text-only reasoning models transfer to VLMs; combining the two adaptively remains an open problem.</li>
  </ul>
  <p class="research-readmore">Read more: <a href="https://arxiv.org/abs/2507.07562">paper</a> · <a href="https://github.com/JierunChen/SFT-RL-SynergyDilemma">code</a></p>

  <h2 id="reflection">How can multimodal models learn to reflect?</h2>
  <p>Self-reflection, noticing and correcting one's own mistakes, is weaker in multimodal models than in text-only ones, and prompting alone cannot add knowledge the model does not have. <a href="https://arxiv.org/abs/2506.01713">SRPO</a> (NeurIPS) works in two stages. First, a stronger multimodal model critiques the policy's initial answers to build a reflection-focused dataset, so the model learns how to reflect, not just what to answer. Second, during GRPO-style reinforcement learning, a reward favors reflections that are concise and actually improve the reasoning, and discourages redundant self-talk.</p>
  <p class="research-knowhow-label">Know-how</p>
  <ul class="research-knowhow">
    <li>Teach the form of good reflection with data before rewarding it with RL.</li>
    <li>Reward the usefulness of a reflection, not its length.</li>
  </ul>
  <p class="research-readmore">Read more: <a href="https://arxiv.org/abs/2506.01713">paper</a> · <a href="https://github.com/SUSTechBruce/SRPO_MLLMs">code</a></p>

  <h2 id="gaps">Where do multimodal models still fall short?</h2>
  <p>A benchmark is only useful if it cannot be solved by shortcuts, and three evaluations target specific blind spots. <a href="https://arxiv.org/abs/2505.15929">PhyX</a> tests physics-grounded reasoning in visual scenes across six physics domains; its error analysis shows models relying on memorized textbook knowledge, leaning too heavily on mathematical formulas, and matching surface visual patterns rather than understanding the physical situation. <a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a> (ICLR) addresses browsing benchmarks that can be solved with text alone: its questions require extracting fine-grained visual cues, such as spatial details and temporal traces, and carrying them through repeated image and text searches to facts outside the image, such as events or venues. Its agent framework adds a set-of-mark module to mark, crop and zoom before searching. <a href="https://arxiv.org/abs/2408.09511">NAVERO</a> targets video, where relations between objects and actions change over time, with a benchmark built from negative descriptions and a training method that learns from them.</p>
  <p class="research-knowhow-label">Know-how</p>
  <ul class="research-knowhow">
    <li>Design questions that fail if the model ignores the image.</li>
    <li>Most search-agent failures come from finding the right page and telling apart visually similar events, not from the final reasoning step.</li>
  </ul>
  <p class="research-readmore">Read more: <a href="https://github.com/killthefullmoon/PhyX">PhyX</a> · <a href="https://github.com/mmsearch-plus/MMSearch-Plus">MMSearch-Plus</a></p>

  <h2 id="embodied">How can multimodal reasoning become robot behavior?</h2>
  <p>By using code as the bridge between perception and control. <a href="https://arxiv.org/abs/2402.16117">RoboCodeX</a> (ICML) decomposes a high-level instruction, in a tree structure, into object-centric manipulation units, each annotated with physical preferences such as affordances and safety constraints, and then writes them as code, which lets one model generalize across robot platforms. A multimodal reasoning dataset is used for pre-training and an iterative self-updating procedure for fine-tuning. The <a href="https://arxiv.org/abs/2411.05902">survey of autoregressive models in vision</a> (TMLR) organizes visual generation into pixel-, token- and scale-based approaches and covers applications including embodied AI; its <a href="https://github.com/ChaofanTao/Autoregressive-Models-in-Vision-Survey">GitHub paper list</a> is widely used.</p>
  <p class="research-knowhow-label">Know-how</p>
  <ul class="research-knowhow">
    <li>Code is a useful interface between perception and control: it is inspectable, composable and portable across robots.</li>
  </ul>
  <p>For making vision-language Transformers cheaper to run, see token merging and joint pruning on the <a href="{{ '/research/efficient-llm/#vision-language' | relative_url }}">efficient LLM page</a>.</p>

  {% include research/paper-list.liquid topic="multimodal" lang="en" %}

  {% include research/faq.liquid %}

  <p>Related: <a href="{{ '/research/coding-agents/' | relative_url }}">Coding agents and agentic RL</a> · <a href="{{ '/research/efficient-llm/' | relative_url }}">Efficient LLM training and inference</a></p>
</div>
