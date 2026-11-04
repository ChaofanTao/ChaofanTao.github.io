---
layout: default
title: "Efficient LLM Training and Inference"
description: "Chaofan Tao's research on efficient LLMs: choosing vocabulary size, compressing generative models, cheaper long-context inference, faster test-time scaling, and distillation."
permalink: /research/efficient-llm/
research_lang: en
last_modified_at: 2026-11-04
og_image: /assets/img/og-image.png
about:
  - Efficient large language models
  - Scaling laws
  - Tokenizer vocabulary size
  - Model quantization
  - Structured pruning
  - KV cache compression
  - Knowledge distillation
  - Test-time scaling
faq:
  - q: "How large should an LLM's vocabulary be?"
    a: "Larger than most models use today. Scaling Laws with Vocabulary (NeurIPS) estimates the compute-optimal vocabulary size in three independent ways, and all of them show that the optimum grows with the compute budget, so larger models deserve larger vocabularies. An interactive calculator is available on Hugging Face Spaces."
  - q: "Which paper by Chaofan Tao received the ACL 2022 Outstanding Paper Award?"
    a: "Compression of Generative Pre-trained Language Models via Quantization. It explains why quantization methods designed for BERT-style encoders fail on GPT-style generative models and fixes the problem with token-level contrastive distillation and module-wise dynamic scaling."
  - q: "How can long-context LLM inference use less memory?"
    a: "By keeping only the parts of the KV cache that matter. D2O allocates cache budgets per layer and recalls useful discarded tokens, UNComp uses an uncertainty signal to decide what can be compressed, and Prefilling-dLLM brings prefill and decode separation to diffusion language models."
  - q: "Is there code for these methods?"
    a: "Yes. Most papers on this page link to public code, including the vocabulary scaling law (sail-sg/scaling-with-vocab), D2O, UNComp, ATTS and Prefilling-dLLM. See the paper list for links."
---

{% include research/styles.liquid %}
{% include research/jsonld.liquid topic="efficient-llm" %}

<div class="research-page">
  <nav class="research-breadcrumb" aria-label="Breadcrumb">
    <a href="{{ '/' | relative_url }}">Chaofan Tao</a><span aria-hidden="true">/</span>
    <a href="{{ '/research/' | relative_url }}">Research</a><span aria-hidden="true">/</span>
    <span>Efficient LLMs</span>
    <span aria-hidden="true">·</span><a href="{{ '/zh/research/efficient-llm/' | relative_url }}" lang="zh-Hans">中文版</a>
  </nav>

  <h1>Efficient LLM Training and Inference</h1>
  <p class="research-meta">By <a href="{{ '/' | relative_url }}">Chaofan Tao (陶超凡)</a> · Last updated <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%B %-d, %Y" }}</time></p>

  <p class="research-lead"><strong>This work asks how to get more capability from every unit of compute and memory,</strong> from design choices made before training to the way models are compressed and served. Each project starts from a concrete bottleneck, explains why existing methods fail on it, and turns that explanation into a practical fix with released code. The quantization work received an ACL 2022 Outstanding Paper Award.</p>

  <ul class="research-highlights">
    <li><strong>Design before training</strong>Vocabulary size treated as a scaling dimension, with a principled way to choose it.</li>
    <li><strong>Compression that keeps generation</strong>Why quantizing GPT-style models breaks, and how to fix it.</li>
    <li><strong>Cheaper long context</strong>Deciding which parts of the KV cache really matter.</li>
    <li><strong>Faster reasoning and serving</strong>Removing synchronization from test-time scaling, and surviving GPU failures.</li>
  </ul>

  <h2 id="vocabulary">How large should an LLM's vocabulary be?</h2>
  <p>Larger than most models use today. Scaling studies usually vary parameters and data but treat the tokenizer as fixed. <a href="https://arxiv.org/abs/2407.13623">Scaling Laws with Vocabulary</a> (NeurIPS) estimates the compute-optimal vocabulary size in three independent ways, and all three agree that it grows with compute: larger models deserve larger vocabularies, and many popular models are under-provisioned. An <a href="https://huggingface.co/spaces/sail/scaling-with-vocab-demo">interactive calculator</a> turns the result into a practical choice.</p>

  <h2 id="quantization">Why does quantization break generative models, and how do you fix it?</h2>
  <p>Methods that worked for BERT-style encoders fail on GPT-style generators for two reasons: low-bit word embeddings collapse toward each other, and weight ranges differ widely across modules. <a href="https://arxiv.org/abs/2203.10705">Token-level contrastive distillation</a> keeps embeddings distinguishable, and module-wise dynamic scaling fits each quantizer to its module (ACL 2022 Outstanding Paper). Follow-up work learns which components to remove through <a href="https://doi.org/10.18653/v1/2023.findings-acl.692">structured pruning</a>.</p>

  <h2 id="long-context">How can long-context inference use less memory?</h2>
  <p>By keeping only the parts of the KV cache that matter. <a href="https://arxiv.org/abs/2406.13035">D2O</a> gives each layer a cache budget based on how its attention is spread and can recall discarded tokens that resemble kept ones. <a href="https://arxiv.org/abs/2410.03090">UNComp</a> uses an uncertainty signal to find what can be compressed, which also reveals the heads and layers responsible for retrieval. <a href="https://arxiv.org/abs/2606.10537">Prefilling-dLLM</a> brings prefill and decode separation to diffusion language models without retraining.</p>

  <h2 id="test-time">How can reasoning-time compute run faster?</h2>
  <p>Remove the waiting. <a href="https://arxiv.org/abs/2509.15148">ATTS</a> shows that synchronization, not raw compute, is the main bottleneck when a small model drafts and a large model checks, and replaces it with asynchronous inference backed by statistical guarantees. On the serving side, <a href="https://arxiv.org/abs/2511.11617">AnchorTP</a> keeps an LLM service running through single-GPU failures by preserving state across elastic tensor parallelism.</p>

  <h2 id="distillation">What matters in distillation?</h2>
  <p>Matching the student to the right signal. With enough training, forward and reverse KL behave similarly, but early on they focus on different parts of the teacher's distribution; <a href="https://arxiv.org/abs/2404.02657">Adaptive KL</a> combines their strengths. <a href="https://arxiv.org/abs/2510.10925">PerSyn</a> sends each prompt to the teacher a given student can learn from best, and <a href="https://arxiv.org/abs/2601.21968">On-policy Verbal Distillation</a> learns from whole-trajectory teacher feedback instead of token-by-token matching.</p>

  {% include research/paper-list.liquid topic="efficient-llm" lang="en" %}

  {% include research/faq.liquid %}

  <details class="research-more">
    <summary>How to cite</summary>
<pre><code>@inproceedings{tao2024scaling,
  title     = {Scaling Laws with Vocabulary: Larger Models Deserve Larger Vocabularies},
  author    = {Tao, Chaofan and Liu, Qian and Dou, Longxu and Muennighoff, Niklas and Wan, Zhongwei and Luo, Ping and Lin, Min and Wong, Ngai},
  booktitle = {Advances in Neural Information Processing Systems},
  year      = {2024}
}

@inproceedings{tao2022compression,
  title     = {Compression of Generative Pre-trained Language Models via Quantization},
  author    = {Tao, Chaofan and Hou, Lu and Zhang, Wei and Shang, Lifeng and Jiang, Xin and Liu, Qun and Luo, Ping and Wong, Ngai},
  booktitle = {Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics},
  year      = {2022}
}</code></pre>
  </details>

  <p>Related: <a href="{{ '/research/coding-agents/' | relative_url }}">Coding agents and agentic RL</a> · <a href="{{ '/research/multimodal-reasoning/' | relative_url }}">Multimodal reasoning and agents</a></p>
</div>
