---
layout: default
title: "Efficient LLM Training and Inference"
description: "Chaofan Tao's research on efficient LLMs: vocabulary scaling laws, quantization and pruning of generative models, KV cache compression, fast test-time scaling, and distillation."
permalink: /research/efficient-llm/
research_lang: en
last_modified_at: 2026-11-03
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
  - q: "What is the compute-optimal vocabulary size for an LLM?"
    a: "It grows with the compute budget, so larger models deserve larger vocabularies. Scaling Laws with Vocabulary (NeurIPS 2024) predicts that Llama2-70B should have used at least 216K tokens, 7 times its 32K vocabulary. At a fixed 2.3e21 FLOPs, increasing a 3B model's vocabulary from 32K to 43K raised ARC-Challenge accuracy from 29.1 to 32.0."
  - q: "Which paper by Chaofan Tao received the ACL 2022 Outstanding Paper Award?"
    a: "Compression of Generative Pre-trained Language Models via Quantization (ACL 2022). It shows that earlier quantization methods fail on generative models because of homogeneous word embeddings and varied weight distributions, and fixes this with token-level contrastive distillation and module-wise dynamic scaling, reaching 14.4x compression on GPT-2 and 13.4x on BART with performance comparable to full precision."
  - q: "How much can KV cache compression save in long-context inference?"
    a: "In UNComp (EMNLP 2025), uncertainty-guided compression reduces the KV cache to 4.74% of its original size with a 6.4x throughput gain. D2O, which allocates cache per layer and recalls discarded tokens by similarity, improves inference throughput by more than 3x without fine-tuning."
  - q: "Is there code or a demo for the vocabulary scaling law?"
    a: "Yes. Code is at github.com/sail-sg/scaling-with-vocab and an interactive demo that predicts the optimal vocabulary size is on Hugging Face Spaces at huggingface.co/spaces/sail/scaling-with-vocab-demo."
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

  <p class="research-lead"><strong>This line of work asks how to get more capability per FLOP and per byte of memory.</strong> It spans compute-optimal vocabulary scaling, quantization and structured pruning of generative language models, KV cache compression for long-context inference, faster test-time scaling, distillation, and fault-tolerant distributed inference. The quantization paper received the ACL 2022 Outstanding Paper Award.</p>

  <h2 id="key-results">Key results</h2>
  <div class="research-table-wrap">
    <table>
      <thead>
        <tr><th>Paper</th><th>Problem</th><th>Result</th></tr>
      </thead>
      <tbody>
        <tr><td><a href="https://arxiv.org/abs/2407.13623">Scaling Laws with Vocabulary</a> (NeurIPS 2024)</td><td>Compute-optimal vocabulary size</td><td>Llama2-70B should use ≥216K tokens (7× its 32K); 32K → 43K lifts ARC-Challenge 29.1 → 32.0 at 2.3e21 FLOPs</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2203.10705">Compression of Generative PLMs via Quantization</a> (ACL 2022, Outstanding Paper)</td><td>Low-bit generative models</td><td>14.4× (GPT-2) and 13.4× (BART) compression, comparable to full precision</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2410.03090">UNComp</a> (EMNLP 2025)</td><td>KV cache compression</td><td>Cache reduced to 4.74% of original, 6.4× throughput</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2406.13035">D2O</a></td><td>KV cache eviction without fine-tuning</td><td>More than 3× inference throughput</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2509.15148">ATTS</a> (ICLR 2026)</td><td>Test-time scaling latency</td><td>Up to 56.7× speedup in test-time scaling and 4.14× throughput, no accuracy loss</td></tr>
        <tr><td><a href="https://arxiv.org/abs/2606.10537">Prefilling-dLLM</a> (EMNLP 2026)</td><td>Long-context diffusion LLMs</td><td>9.1–28.0× speedup at 8K–32K context, training-free</td></tr>
      </tbody>
    </table>
  </div>

  <h2 id="vocabulary">What vocabulary size should an LLM use?</h2>
  <p>Larger than most models use today. By training models from 33M to 3B parameters on up to 500B characters, <a href="https://arxiv.org/abs/2407.13623">Scaling Laws with Vocabulary</a> derives the compute-optimal vocabulary size three ways (IsoFLOPs analysis, derivative estimation, and a parametric loss fit), and all three agree that the optimum grows with compute. Most open LLMs are under-provisioned: Llama2-70B should have used at least 216K tokens instead of 32K. Try the <a href="https://huggingface.co/spaces/sail/scaling-with-vocab-demo">interactive demo</a> or the <a href="https://github.com/sail-sg/scaling-with-vocab">code</a>.</p>

  <h2 id="quantization">How do you quantize generative language models without breaking generation?</h2>
  <p>Fix the word embeddings first. Earlier quantization methods that worked for BERT fail on GPT-2 and BART because low-bit word embeddings become homogeneous and weight distributions vary across modules. Token-level contrastive distillation keeps embeddings distinguishable, and module-wise dynamic scaling adapts each quantizer, giving 14.4× and 13.4× compression with near full-precision quality. Follow-up work applies learnable masks for <a href="https://doi.org/10.18653/v1/2023.findings-acl.692">structured pruning of generative PLMs</a> (Findings of ACL 2023).</p>

  <h2 id="long-context">How can long-context inference be made cheaper?</h2>
  <p>By deciding which parts of the KV cache matter. D2O allocates cache budgets per layer from attention density and recalls discarded tokens that are similar to kept ones. UNComp uses truncated matrix entropy as an uncertainty signal to find sparsity, which also exposes retrieval heads and layers. Prefilling-dLLM brings prefill/decode separation to diffusion language models by caching prefix chunks once and decoding over only the most relevant ones.</p>

  <h2 id="test-time">Can test-time scaling be fast?</h2>
  <p>Yes, if synchronization is removed. ATTS identifies synchronization, not compute, as the main bottleneck in speculative test-time scaling, and replaces it with asynchronous inference guided by conformal prediction. On MATH, AMC23, AIME24 and AIME25, it reaches up to 56.7× speedup while controlling the rejection rate.</p>

  <h2 id="distillation">What matters in LLM distillation?</h2>
  <p>With enough training, forward and reverse KL behave similarly, but early on they emphasize the head and tail of the distribution; <a href="https://arxiv.org/abs/2404.02657">Adaptive KL</a> (COLING 2024) combines them. <a href="https://arxiv.org/abs/2510.10925">PerSyn</a> (ACL 2026) routes each prompt to the teacher a given student can best learn from, and <a href="https://arxiv.org/abs/2601.21968">On-policy Verbal Distillation</a> replaces token-level matching with trajectory-level teacher scores.</p>

  <h2 id="systems">Efficient vision-language models and resilient serving</h2>
  <p><a href="https://arxiv.org/abs/2305.17455">CrossGET</a> (ICML 2024) and <a href="https://arxiv.org/abs/2301.13741">UPop</a> (ICML 2023) accelerate and compress vision-language Transformers through token ensembling and progressive pruning. <a href="https://arxiv.org/abs/2511.11617">AnchorTP</a> (DATE 2026) keeps LLM serving alive through single-GPU failures with state-preserving elastic tensor parallelism.</p>

  <h2 id="papers">Papers</h2>
  {% include research/paper-list.liquid topic="efficient-llm" lang="en" %}

  {% include research/faq.liquid %}

  <h2 id="cite">How to cite</h2>
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

  <p>Related: <a href="{{ '/research/coding-agents/' | relative_url }}">Coding agents and agentic RL</a> · <a href="{{ '/research/multimodal-reasoning/' | relative_url }}">Multimodal reasoning and agents</a> · <a href="{{ '/llms.txt' | relative_url }}">llms.txt</a></p>
</div>
