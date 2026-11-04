---
layout: default
title: "Efficient LLM Training and Inference"
description: "Chaofan Tao's research on efficient LLMs: choosing vocabulary size, quantizing generative models, cheaper long-context inference, faster test-time scaling, resilient serving, and distillation."
permalink: /research/efficient-llm/
research_lang: en
last_modified_at: 2026-11-04
og_image: /assets/img/og-image.png
about:
  - Efficient large language models
  - Scaling laws
  - Tokenizer vocabulary size
  - Model quantization
  - KV cache compression
  - Test-time scaling
  - Knowledge distillation
faq:
  - q: "How large should an LLM's vocabulary be?"
    a: "Larger than most models use, but growing more slowly than the rest of the model. Scaling Laws with Vocabulary (NeurIPS) estimates the compute-optimal vocabulary size in three independent ways, and all three agree that it grows with the compute budget. With scarce data a smaller vocabulary is better, and with far more data than compute-optimal a larger one helps, while a bigger vocabulary also costs inference compute."
  - q: "Which paper by Chaofan Tao received the ACL 2022 Outstanding Paper Award?"
    a: "Compression of Generative Pre-trained Language Models via Quantization. It shows that quantization fails on GPT-style models because low-precision word embeddings become nearly identical and weight distributions vary across modules, and fixes this with token-level contrastive distillation and module-wise dynamic scaling."
  - q: "How can long-context LLM inference use less memory?"
    a: "By keeping only the parts of the KV cache that matter. D2O gives each layer its own cache budget and lets discarded tokens be recalled or merged, UNComp uses matrix entropy to find low-information regions, and Prefilling-dLLM caches the prefix of diffusion language models once in chunks and decodes over only the relevant ones."
  - q: "Is there code for these methods?"
    a: "Yes. Most papers on this page link to public code, including the vocabulary scaling law with an interactive calculator, D2O, UNComp, ATTS, Prefilling-dLLM and Adaptive KL. See the paper list for links."
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

  <p class="research-lead"><strong>Large language models are expensive at every stage:</strong> deciding how to build them, training and compressing them, and serving them to users. This line of work looks for the places where compute and memory are spent without paying off. The common method is diagnosis first: understand why an existing approach fails on a specific bottleneck, then turn that explanation into a simple, practical fix with released code. The quantization work received an ACL 2022 Outstanding Paper Award.</p>

  <p class="research-toc">On this page: <a href="#vocabulary">Vocabulary</a> · <a href="#quantization">Quantization and pruning</a> · <a href="#long-context">Long context</a> · <a href="#test-time">Test-time scaling and serving</a> · <a href="#distillation">Distillation</a> · <a href="#vision-language">Vision-language efficiency</a></p>

  <h2 id="vocabulary">How large should an LLM's vocabulary be?</h2>
  <p>Larger than most models use, but growing more slowly than the rest of the model. Classic scaling laws vary parameters and data but leave the tokenizer out, which is why models of similar size ship with very different vocabularies. <a href="https://arxiv.org/abs/2407.13623">Scaling Laws with Vocabulary</a> (NeurIPS) separates vocabulary parameters from the rest of the network, measures data in characters rather than tokens, and uses a loss that does not depend on vocabulary size, so different tokenizers can be compared fairly. Three independent estimates, from IsoFLOPs analysis, a derivative-based method and a parametric loss fit, reach the same conclusion.</p>
  <p class="research-knowhow-label">Know-how</p>
  <ul class="research-knowhow">
    <li>An optimum exists because of a trade-off: a larger vocabulary splits text into fewer tokens, but embeddings for rare tokens are hard to learn when compute is limited.</li>
    <li>Vocabulary parameters should grow with model size, but more slowly than the rest of the model; many popular models are still under-provisioned.</li>
    <li>Adjust for data: with scarce data use a smaller vocabulary, and with far more data than compute-optimal a larger one, remembering that a bigger vocabulary also costs inference compute.</li>
  </ul>
  <p class="research-readmore">Read more: <a href="https://arxiv.org/abs/2407.13623">paper</a> · <a href="https://huggingface.co/spaces/sail/scaling-with-vocab-demo">interactive calculator</a> · <a href="https://github.com/sail-sg/scaling-with-vocab">code</a></p>

  <h2 id="quantization">Why does quantization break generative models, and how do you fix it?</h2>
  <p>Quantization stores weights in fewer bits. Methods that worked for BERT-style encoders failed on GPT-style generators, and it was unclear why. The diagnosis behind this ACL 2022 Outstanding Paper has two parts. At low precision, word embeddings become nearly identical, so the model can no longer tell tokens apart when it generates. And weight distributions differ widely between modules, so a single quantizer setting fits none of them well. Token-level contrastive distillation pulls each token's representation toward the full-precision teacher's and away from other tokens, and module-wise dynamic scaling learns a separate range for each module. Follow-up work learns which components to remove through structured pruning with learnable masks.</p>
  <p class="research-knowhow-label">Know-how</p>
  <ul class="research-knowhow">
    <li>For generative models, check embedding diversity first; it is the first thing to collapse.</li>
    <li>Treat modules separately; a single global scale hides the problem.</li>
  </ul>
  <p class="research-readmore">Read more: <a href="https://arxiv.org/abs/2203.10705">quantization paper</a> · <a href="https://doi.org/10.18653/v1/2023.findings-acl.692">structured pruning paper</a></p>

  <h2 id="long-context">How can long-context inference use less memory?</h2>
  <p>The KV cache, which stores keys and values for every previous token, grows with context length and soon dominates memory. The question is which parts can be dropped without losing information. <a href="https://arxiv.org/abs/2406.13035">D2O</a> gives each layer its own cache budget based on how concentrated its attention is, and keeps a way to recall or merge discarded tokens that resemble kept ones, without any fine-tuning. <a href="https://arxiv.org/abs/2410.03090">UNComp</a> uses matrix entropy as an uncertainty signal to find low-information regions, which also reveals the heads and layers responsible for retrieval. Diffusion language models re-encode the whole prefix at every denoising step; <a href="https://arxiv.org/abs/2606.10537">Prefilling-dLLM</a> caches the prefix once in chunks and decodes over only the most relevant ones.</p>
  <p class="research-knowhow-label">Know-how</p>
  <ul class="research-knowhow">
    <li>Layers differ: shallow and deep layers need different cache budgets.</li>
    <li>Eviction is safer with a way back: let discarded tokens be recalled or merged.</li>
    <li>In chunked caches, a beginning-of-sequence token at the start of each chunk acts as an attention anchor, and sparse prefilling can even outperform dense attention.</li>
  </ul>
  <p class="research-readmore">Read more: <a href="https://github.com/AIoT-MLSys-Lab/D2O">D2O code</a> · <a href="https://github.com/menik1126/UNComp">UNComp code</a> · <a href="https://github.com/menik1126/Prefilling-dLLM">Prefilling-dLLM code</a></p>

  <h2 id="test-time">How can reasoning-time compute and LLM serving be faster and more reliable?</h2>
  <p>Test-time scaling improves answers by spending more compute while generating, often with a small model drafting and a large model checking. <a href="https://arxiv.org/abs/2509.15148">ATTS</a> analyzes where the time goes and finds that synchronization, not arithmetic, is the main bottleneck. It replaces synchronous checks with asynchronous inference calibrated online by conformal prediction, scaling along both sequential and parallel dimensions while keeping statistical control over how often drafts are rejected. On the serving side, a single GPU failure can take down a multi-GPU service. <a href="https://arxiv.org/abs/2511.11617">AnchorTP</a> keeps model weights and KV caches alive in a daemon outside the inference process, repartitions the model across the remaining GPUs, and plans the minimum data movement needed to restore service.</p>
  <p class="research-knowhow-label">Know-how</p>
  <ul class="research-knowhow">
    <li>Measure arithmetic intensity before optimizing; latency problems are often coordination problems.</li>
    <li>Keep state (weights and caches) separate from the process that can crash.</li>
  </ul>
  <p class="research-readmore">Read more: <a href="https://github.com/menik1126/Asynchronous-Test-Time-Scaling">ATTS code</a> · <a href="https://arxiv.org/abs/2511.11617">AnchorTP paper</a></p>

  <h2 id="distillation">What matters in distillation?</h2>
  <p>Distillation trains a smaller student from a stronger teacher, and a recurring lesson is that the obvious teacher signal is not always the best one. For LLMs, forward and reverse KL divergence turn out to share the same optimum, and neither shows the mode-seeking or mean-seeking behavior usually attributed to it. The practical difference is that early in training forward KL focuses on the head of the distribution and reverse KL on the tail, which <a href="https://arxiv.org/abs/2404.02657">Adaptive KL</a> combines. <a href="https://arxiv.org/abs/2510.10925">PerSyn</a> starts from the observation that stronger models are not always better teachers and routes each prompt to the teacher a given student can learn from best before generating data. <a href="https://arxiv.org/abs/2601.21968">On-policy Verbal Distillation</a> works with black-box teachers that only return text: their scores rank the student's own partial attempts, keeping good prefixes and replacing weak continuations.</p>
  <p class="research-knowhow-label">Know-how</p>
  <ul class="research-knowhow">
    <li>Match the teacher to what the student can learn, not just to benchmark strength. The same lesson appears in <a href="{{ '/research/coding-agents/#trajectories' | relative_url }}">coding-agent trajectories</a>.</li>
    <li>Keeping the student's own good prefixes preserves exploration and helps avoid collapse.</li>
  </ul>

  <h2 id="vision-language">What about vision-language models?</h2>
  <p>The same diagnose-then-fix approach applies. <a href="https://arxiv.org/abs/2305.17455">CrossGET</a> (ICML) merges redundant tokens at inference time, using information from one modality to guide matching in the other, and works for both separate-encoder models and multimodal LLMs. <a href="https://arxiv.org/abs/2301.13741">UPop</a> (ICML) searches for a smaller sub-network across vision and language jointly, so the pruning ratio of each modality is learned rather than fixed, and alternates search with retraining to reach higher compression.</p>

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
