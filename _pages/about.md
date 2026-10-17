---
layout: about
title: about
permalink: /

profile:
  align: right
  image: prof_pic.png
  image_circular: false
  more_info: >
    <p>Email: <a href="mailto:tcftrees@gmail.com">tcftrees@gmail.com</a></p>

selected_papers: false
social: false
redirect_from:
  - /about/
  - /about.html
announcements:
  enabled: false
latest_posts:
  enabled: false
---

<style>
  /* The page title renders at a fixed 40px, at which "Chaofan Tao (陶超凡)" measures
     378.6px -- wider than the 345px of content on a 375px phone and the 290px on a
     320px one, so it wrapped to two lines on every small screen. Scaling with the
     viewport keeps it on one line: 30px measures 284.0px, which fits 320px with room,
     while the 2.5rem cap preserves the original size on desktop. */
  .post-header .post-title {
    font-size: clamp(1.5rem, 7.4vw, 2.5rem);
    line-height: 1.2;
  }

  /* Section rhythm. The theme zeroes every block's top margin and leaves paragraph
     bottom margins at 16px, so a paragraph was separated from the following heading by
     only 16px -- the same as the gap between two paragraphs. Restoring a larger top
     margin on headings gives each section a visible break, and the space scales down on
     narrow screens rather than being fixed. */
  .post article > .clearfix > h2 {
    margin-top: 2.75rem;
    margin-bottom: 1rem;
  }

  .post article > .clearfix > h3 {
    margin-top: 2.25rem;
    margin-bottom: 0.75rem;
  }

  /* A heading directly after another heading does not need the full gap. */
  .post article > .clearfix > h2 + h3 {
    margin-top: 1rem;
  }

  .post article > .clearfix > p {
    margin-bottom: 1.1rem;
  }

  .post article > .clearfix > p + p {
    margin-top: 1.35rem; /* a bit more air between paragraphs than inside one */
  }

  .post article > .clearfix > ul {
    margin-top: 0.25rem;
    margin-bottom: 1.25rem;
  }

  .post article > .clearfix > ul li {
    margin-bottom: 0.55rem;
  }

  .post article > .clearfix > ul li:last-child {
    margin-bottom: 0;
  }

  /* The profile sidebar's contact line: make the address stand out as a link rather
     than reading as another line of body text. */
  .profile .more-info a,
  .profile .more-info a:visited {
    color: var(--global-theme-color, #b509ac);
    text-decoration: none;
  }

  .profile .more-info a:hover,
  .profile .more-info a:focus-visible {
    color: var(--global-hover-color, #b509ac);
    text-decoration: underline;
  }

  /* LegoX project links in the biography: use theme color so they read as links
     rather than plain text. */
  .post article ul li a[href*="legox.net/blog"],
  .post article ul li a[href*="legox.net/blog"]:visited {
    color: var(--global-theme-color, #b509ac);
    text-decoration: none;
    font-weight: 600;
  }

  .post article ul li a[href*="legox.net/blog"]:hover,
  .post article ul li a[href*="legox.net/blog"]:focus-visible {
    color: var(--global-hover-color, #b509ac);
    text-decoration: underline;
  }

  @media (max-width: 576px) {
    .post article > .clearfix > h2 {
      margin-top: 2rem;
      margin-bottom: 0.85rem;
    }

    .post article > .clearfix > h3 {
      margin-top: 1.75rem;
      margin-bottom: 0.6rem;
    }

    .post article > .clearfix > p + p {
      margin-top: 1.1rem;
    }
  }
</style>

## Biography

I am a researcher and developer at Huawei Foundation Model Lab, working on **agentic intelligence** and **AI infrastructure**. My paper [**Compression of Generative Pre-trained Language Models via Quantization**](https://arxiv.org/abs/2203.10705) received the **ACL 2022 Outstanding Paper Award**, and I have publications at **ICLR, ICML, NeurIPS, ACL, EMNLP, COLM, and ECCV**, as well as related journals.

I received my PhD from [The University of Hong Kong](https://www.hku.hk/), advised by [Prof. Ngai Wong](https://www.eee.hku.hk/~nwong/) and [Prof. Ping Luo](http://luoping.me/), as a member of the [MMLAB@HKU](https://mmlab.hk/) family. I completed my bachelor's degree at the Yingcai Honors College of the University of Electronic Science and Technology of China. Previously, I interned at Sea AI Lab, Amazon Web Services, Huawei, and SenseTime.

I am actively involved in [**LegoX**](https://www.legox.net/), an open-source collection advancing frontier agentic intelligence across agentic data pipelines, training frameworks, evaluation benchmarks, and foundation models. Recent work includes:

- [**LegoFlow**](https://www.legox.net/blog/legoflow/): an agent-orchestrated code data engineering framework modularizing the full pipeline as composable blocks, driving recursive self-improvement from 7.6% to 64.4% on SWE-bench Verified across two iterations.
- [**Lego-RL**](https://www.legox.net/blog/lego-rl/): reinforcement learning training directly inside unmodified coding harnesses (OpenHands, Claude Code, OpenCode) via in-process proxying and MoE routing replay, reaching 66.6–70.4% on SWE-bench Verified in single training runs.
- [**Terminal-Lego**](https://www.legox.net/blog/terminal-lego/): 15k+ executable terminal tasks demonstrating that environment-grounded trajectories with explicit observe-act-verify cycles outperform imitation of stronger but less grounded teachers, achieving comparable performance with 30× fewer examples.
- [**SWE-Lego**](https://www.legox.net/blog/swe-lego/): supervised fine-tuning with error masking and curriculum learning on 32k task instances, achieving 52.6% Pass@1 and 58.8% with test-time scaling on SWE-bench Verified.

Explore the work at [legox.net](https://www.legox.net/) or the [LegoX GitHub organization](https://github.com/LegoX).

### Hiring and collaboration

I am looking for **research/engineering interns** and **collaborators** who are excited about AI. Please email me with **[Interest] + your profile + 1–2 representative links** (paper, GitHub, blog, or demo).

### Links

<!--
  Icon sizing note.

  al-folio v1 renders _includes/head.liquid from the al_folio_core gem, which never
  included _includes/head/custom.html. The style block lives on this page instead,
  which is reliably rendered; a _includes/ override would also work but would shadow a
  gem-owned file and drift on every upgrade.

  These five icons come from three different sources whose artwork fills its box by a
  different fraction, so one shared font-size/box CANNOT make them look the same size.
  Ink (visible artwork) as a fraction of the icon's own em box / SVG canvas:

    Email         fa-envelope          ink  512.0 x 384.0 / 512 upm   -> h 0.7500
    GitHub        fa-github            ink  496.0 x 483.6 / 512 upm   -> h 0.9446
    Scholar       ai-google-scholar    ink  344.0 x 384.0 / 512 upm   -> h 0.7500
    Hugging Face  remote svg 95x88     ink   88.0 x  81.3 / 88        -> h 0.9236
    LegoX         remote svg 100x100   ink   64.0 x  60.0 / 100       -> h 0.6000

  What matters visually is the ink HEIGHT (a logo and a letterform are not comparable by
  area), so every icon is driven from one --link-ink variable and each factor below
  converts that target ink height into the value its own source needs:

    font icons   font-size = ink / (ink fraction of em)     -> 1.3333, 1.0585 of ink
    <img> icons  box size  = ink / (ink fraction of canvas) -> 1.0827, 1.6667 of ink

  The --link-box variable is the square each icon is centred in, and every factor is
  expressed as a fraction of it so the whole row keeps its proportions at any width:

    --link-box: clamp(3rem, 14vw, 3.75rem)   48px floor, 60px cap
    font icons: 0.8    x box   (glyph ink 0.7500 of em  -> 0.6 x box)
    GitHub:     0.6352 x box   (glyph ink 0.9446 of em  -> 0.6 x box)
    HF img:     0.7016 x box   (canvas ink 81.28 / 95   -> 0.6 x box)
    LegoX img:  1.0    x box   (canvas ink 60 / 100     -> 0.6 x box)

  So all five land on 0.6 x --link-box: 36px ink at the 60px cap, 28.8px at the 48px
  floor. A 5-column grid keeps them on ONE row down to 320px, which a flex row with a
  fixed gap could not (the old boxes were unequal, so their optical centres were uneven).
-->
<style>
  .about-links-card {
    box-sizing: border-box;
    width: 100%; /* match the content column rather than sitting narrower than its siblings */
    margin: 1.25rem 0 1.5rem;
    padding: 1.4rem 1.5rem 1.3rem;
    border: 1px solid var(--global-divider-color, rgba(0, 0, 0, 0.1));
    border-radius: 0.75rem;
    background: var(--global-card-bg-color, transparent);
  }

  .about-links {
    --link-box: clamp(3rem, 14vw, 3.75rem);
    display: grid;
    /* Five equal columns, so the icons stay evenly spaced and on one row at 320px.
       Capped and centred so a wide card does not spread five icons thinly. */
    grid-template-columns: repeat(5, minmax(0, 1fr));
    justify-items: center;
    align-items: center;
    gap: 0.4rem;
    max-width: 27rem;
    margin: 0 auto;
  }

  .about-link {
    box-sizing: border-box;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    /* One uniform square per icon, so their optical centres are evenly spaced by the
       grid. The artwork is sized INSIDE this box, never the box itself. */
    width: var(--link-box);
    height: var(--link-box);
    border-radius: 0.4rem;
    line-height: 1;
    text-decoration: none;
    transition:
      transform 0.15s ease,
      background-color 0.15s ease,
      opacity 0.15s ease;
  }

  .about-link:hover,
  .about-link:focus-visible {
    transform: translateY(-2px);
    background-color: var(--global-code-bg-color, rgba(0, 0, 0, 0.05));
  }

  /* Font icons: font-size decides ink height. 0.8 x box makes the glyph ink land on
     0.6 x box, the same target the two images are sized to. */
  .about-link i {
    display: block;
    font-size: calc(var(--link-box) * 0.8);
    line-height: 1;
    text-align: center;
  }

  /* Brand colours, kept in both themes: they are recognisable marks and each already
     reads on either background. */
  .about-link-email {
    color: #d93025;
  }

  /* FA7 sets width: var(--fa-width, 1.25em) on the .fa* base rule, so the element is
     wider than the glyph; the flex box centres it. The GitHub mark is monochrome and
     must follow the theme, or it disappears against the dark background
     (html[data-theme=dark] sets #e8e8e8 text on #1c1c1d). */
  .about-link-github {
    color: var(--global-text-color, #24292f);
  }

  /* fa-github ink is 0.9446 of em, so a smaller font-size than the other glyphs is
     needed for the SAME ink height: 0.8 / 0.9446 x 0.75 = 0.6352. */
  .about-link-github i {
    font-size: calc(var(--link-box) * 0.6352);
  }

  /* Academicons ink is 0.6719 of em wide on a 0.75em advance, so the glyph reads
     smaller than its font-size suggests; its ink height is 0.7500 of em like the
     envelope, so it shares the 0.8 factor. */
  .about-link-scholar {
    color: #4285f4;
  }

  /* The two SVG icons are <img>, so object-fit: contain fits the WHOLE canvas into the
     element and each file's own padding shrinks the visible artwork. Their sizes are
     therefore per file rather than equal, so the ink still lands on 0.6 x box. */
  .about-link-image img {
    display: block;
    object-fit: contain;
  }

  /* HuggingFace canvas 95x88 holds ink 88.0 x 81.3: 0.7016 x box yields 0.6 x box ink. */
  .about-link-hf img {
    width: calc(var(--link-box) * 0.7016);
    height: calc(var(--link-box) * 0.7016);
  }

  /* LegoX canvas 100x100 holds ink 64 x 60 (artwork centred in a padded viewBox),
     so a full-box square yields 0.6 x box ink. */
  .about-link-legox img {
    width: var(--link-box);
    height: var(--link-box);
  }

  .about-links-note {
    margin: 0.85rem 0 0;
    line-height: 1.55;
  }

  .about-links-cta {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    min-height: 2.75rem; /* 44px: the iOS minimum comfortable tap target */
    margin-top: 0.85rem;
    padding: 0 1.1rem;
    border-radius: 2rem;
    background: var(--global-theme-color, #b509ac);
    color: #ffffff;
    font-weight: 500;
    text-decoration: none;
    transition:
      opacity 0.15s ease,
      transform 0.15s ease;
  }

  .about-links-cta:hover,
  .about-links-cta:focus-visible {
    opacity: 0.88;
    transform: translateY(-1px);
    color: #ffffff;
  }

  .about-links-cta i {
    font-size: 1em;
  }

  @media (max-width: 576px) {
    .profile.float-right {
      float: none !important;
      width: min(100%, 220px);
      max-width: 220px;
      margin: 0 auto 1.25rem;
    }

    .profile.float-right .more-info {
      text-align: center;
    }

    .about-links-card {
      padding: 1rem 0.75rem 0.9rem;
    }

    .about-links {
      --link-box: clamp(3rem, 16vw, 3.75rem);
      gap: 0.25rem;
    }

    .about-links-cta {
      display: flex;
      justify-content: center;
      width: 100%;
      box-sizing: border-box;
    }
  }
</style>

<div class="about-links-card" aria-label="Contact and profile links">
  <div class="about-links">
    <a class="about-link about-link-email" href="mailto:tcftrees@gmail.com" title="Email" aria-label="Email"><i class="fa-solid fa-envelope" aria-hidden="true"></i></a>
    <a class="about-link about-link-github" href="https://github.com/ChaofanTao" title="GitHub" aria-label="GitHub" rel="external nofollow noopener" target="_blank"><i class="fa-brands fa-github" aria-hidden="true"></i></a>
    <a class="about-link about-link-scholar" href="https://scholar.google.com/citations?user=gjmfLroAAAAJ" title="Google Scholar" aria-label="Google Scholar" rel="external nofollow noopener" target="_blank"><i class="ai ai-google-scholar" aria-hidden="true"></i></a>
    <a class="about-link about-link-image about-link-hf" href="https://huggingface.co/tcftrees" title="Hugging Face" aria-label="Hugging Face" rel="external nofollow noopener" target="_blank"><img src="https://huggingface.co/front/assets/huggingface_logo-noborder.svg" alt="" aria-hidden="true"></a>
    <a class="about-link about-link-image about-link-legox" href="https://www.legox.net/" title="LegoX" aria-label="LegoX" rel="external nofollow noopener" target="_blank"><img src="https://www.legox.net/logo/legox-parallel-pipeline.svg" alt="" aria-hidden="true"></a>
  </div>

  <p class="about-links-note">
    If any of this resonates, I'd love to hear from you — an email with a line about what you're working on and one or two links (a paper, GitHub, blog, or demo) is plenty. Research, engineering, collaboration, and LegoX inquiries all welcome.
  </p>

  <a class="about-links-cta" href="mailto:tcftrees@gmail.com"><i class="fa-solid fa-envelope" aria-hidden="true"></i>Email me</a>
</div>

## Publications (2022+)

Below are my recent papers organized by topic. Each entry includes URL + bilingual TL;DR for quick scanning.



<details open markdown="1">
<summary><strong>1) Agentic Coding, Reasonings and Evaluation</strong></summary>

- **Title:** <span style="color: #92400e;">Swe-lego: Pushing the limits of supervised fine-tuning for software issue resolving</span>  
  **Authors:** Chaofan Tao, Jierun Chen, Yuxin Jiang, Kaiqi Kou, Shaowei Wang, Ruoyu Wang, Xiaohui Li, Sidi Yang, Yiming Du, Jianbo Dai, Zhiming Mao, Xinyu Wang, Lifeng Shang, Haoli Bai  
  **Year:** 2026  
  **Venue:** <span style="color: #1e3a8a;">arXiv preprint arXiv:2601.01426</span>  
  **URL:** [arXiv:2601.01426](https://arxiv.org/abs/2601.01426)  
  **TL;DR (EN):** SWE-Lego presents a strong SFT-only recipe (new dataset + curriculum/error masking) and studies verifier-based test-time scaling, pushing open 8B/32B models to SOTA on SWE-bench Verified.  
  **TL;DR:** SWE-Lego提出仅用监督微调的软工代码智能体配方（真实+合成数据集+课程学习/错误掩码），并研究了软工场景的测试时扩展，将开源8B/32B模型在SWE-bench Verified上推至SOTA。  

- **Title:** <span style="color: #92400e;">MMFormalizer: Multimodal Autoformalization in the Wild</span>  
  **Authors:** Jing Xiong, Qi Han, Yunta Hsieh, Hui Shen, Huajian Xin, Chaofan Tao, Chenyang Zhao, Hengyuan Zhang, Taiqiang Wu, Zhen Zhang, Haochen Wang, Zhongwei Wan, Lingpeng Kong, Ngai Wong  
  **Year:** 2026  
  **Venue:** <span style="color: #1e3a8a;">arXiv preprint arXiv:2601.03017</span>  
  **URL:** [arXiv:2601.03017](https://arxiv.org/abs/2601.03017)  
  **TL;DR (EN):** MMFormalizer extends autoformalization to multimodal math/physics by grounding visual entities and recursively composing axioms, enabling formal statements for real-world problems (including classical mechanics) on the PhyX-AF benchmark.  
  **TL;DR:** MMFormalizer将自动形式化扩展到多模态数学/物理领域，在PhyX-AF基准上实现真实世界问题（包括经典力学）的形式化表述。  

- **Title:** <span style="color: #92400e;">SwingArena: Competitive Programming Arena for Long-context GitHub Issue Solving</span>  
  **Authors:** Wendong Xu, Jing Xiong, Chenyang Zhao, Qiujiang Chen, Haoran Wang, Hui Shen, Zhongwei Wan, Jianbo Dai, Taiqiang Wu, He Xiao, Chaofan Tao, Z Morley Mao, Ying Sheng, Zhijiang Guo, Hongxia Yang, Bei Yu, Lingpeng Kong, Quanquan Gu, Ngai Wong  
  **Year:** 2026  
  **Venue:** <span style="color: #1e3a8a;">International Conference on Learning Representations (oral)</span>  
  **URL:** [arXiv:2505.23932](https://arxiv.org/abs/2505.23932)  
  **TL;DR (EN):** SwingArena is a CI-driven competitive benchmark where LLMs act as submitters and reviewers, paired with retrieval-augmented code generation to handle long-context, multi-language GitHub issue solving.  
  **TL;DR:** SwingArena是一个CI驱动的测评框架，让大语言模型扮演代码的提交者和审阅者角色，配合检索增强的代码生成来处理长上下文、多编程语言的GitHub问题解决。  

- **Title:** <span style="color: #92400e;">Mmsearch-plus: Benchmarking provenance-aware search for multimodal browsing agents</span>  
  **Authors:** Xijia Tao, Yihua Teng, Xinxing Su, Xinyu Fu, Jihao Wu, Chaofan Tao, Ziru Liu, Haoli Bai, Rui Liu, Lingpeng Kong  
  **Year:** 2026  
  **Venue:** <span style="color: #1e3a8a;">International Conference on Learning Representations</span>  
  **URL:** [arXiv:2508.21475](https://arxiv.org/abs/2508.21475)  
  **TL;DR (EN):** MMSearch-Plus is a 311-task benchmark and agent framework with set-of-mark tools that require provenance-aware, vision-in-the-loop search and cross-validation under retrieval noise.  
  **TL;DR:** MMSearch-Plus是一个包含311个任务的benchmark和多模态智能体搜索问答框架，配备set-of-mark工具，要求在检索噪声下进行可追溯、引入视觉搜索和交叉验证。  

- **Title:** <span style="color: #92400e;">OVD: On-policy Verbal Distillation</span>  
  **Authors:** Jing Xiong, Hui Shen, Shansan Gong, Yuxin Cheng, Jianghan Shen, Chaofan Tao, Haochen Tan, Haoli Bai, Lifeng Shang, Ngai Wong  
  **Year:** 2026  
  **Venue:** <span style="color: #1e3a8a;">arXiv preprint arXiv:2601.21968</span>  
  **URL:** [arXiv:2601.21968](https://arxiv.org/abs/2601.21968)  
  **TL;DR (EN):** On-policy Verbal Distillation replaces token-level matching with trajectory-level distillation using discrete teacher scores, reducing memory and improving student performance on web QA and math reasoning.  
  **TL;DR:** On-policy Verbal Distillation用轨迹级蒸馏替代token级匹配蒸馏，使用离散的教师评分，降低内存占用并在网络搜索问答和数学推理上提升学生模型性能。  


- **Title:** <span style="color: #92400e;">From Verifiable Dot to Reward Chain: Harnessing Verifiable Reference-based Rewards for Reinforcement Learning of Open-ended Generation</span>  
  **Authors:** Yuxin Jiang, Yufei Wang, Qiyuan Zhang, Xingshan Zeng, Liangyou Li, Jierun Chen, Chaofan Tao, Haoli Bai, Lifeng Shang  
  **Year:** 2026  
  **Venue:** <span style="color: #1e3a8a;">International Conference on Learning Representations</span>  
  **URL:** [arXiv:2601.18533](https://arxiv.org/abs/2601.18533)  
  **TL;DR (EN):** RLVRR turns single verifiable end rewards into ordered reference-derived reward chains (content + style) to make RL for open-ended generation more efficient and less prone to reward hacking.  
  **TL;DR:** RLVRR将传统RL里单一的可验证终端奖励转化为有序的参考衍生奖励链（内容+风格），使开放式生成的强化学习更高效且更不易出现奖励破解。  

- **Title:** <span style="color: #92400e;">PhyX: Does Your Model Have the "Wits" for Physical Reasoning?</span>  
  **Authors:** Hui Shen, Taiqiang Wu, Qi Han, Yunta Hsieh, Jizhou Wang, Yuyue Zhang, Yuxin Cheng, Zijian Hao, Yuansheng Ni, Xin Wang, Zhongwei Wan, Kai Zhang, Wendong Xu, Jing Xiong, Ping Luo, Wenhu Chen, Chaofan Tao, Zhuoqing Mao, Ngai Wong  
  **Year:** 2025  
  **Venue:** <span style="color: #1e3a8a;">arXiv preprint arXiv:2505.15929</span>  
  **URL:** [arXiv:2505.15929](https://arxiv.org/abs/2505.15929)  
  **TL;DR (EN):** PhyX introduces a 3K-question multimodal benchmark spanning six physics domains to test physics-grounded reasoning, revealing large gaps between top models and human experts.  
  **TL;DR:** PhyX引入一个包含3000个问题的多模态基准，覆盖六个物理领域，用于测试基于物理的推理，观察道顶级模型与人类专家之间的较大差距。  


- **Title:** <span style="color: #92400e;">Scaling laws with vocabulary: Larger models deserve larger vocabularies</span>  
  **Authors:** Chaofan Tao, Qian Liu, Longxu Dou, Niklas Muennighoff, Zhongwei Wan, Ping Luo, Min Lin, Ngai Wong  
  **Year:** 2024  
  **Venue:** <span style="color: #1e3a8a;">Advances in Neural Information Processing Systems (NeurIPS-2024)</span>  
  **URL:** [arXiv:2407.13623](https://arxiv.org/abs/2407.13623)  
  **TL;DR (EN):** The paper derives compute-optimal vocabulary scaling laws and shows larger models benefit from larger vocabularies, improving downstream accuracy at fixed FLOPs.  
  **TL;DR:** 推导了计算最优的词表规模扩展规律，证明更大模型需要更大词表，在相同计算量下提升下游任务准确率。  

- **Title:** <span style="color: #92400e;">Autoregressive Models in Vision: A Survey</span>  
  **Authors:** Jing Xiong, Gongye Liu, Lun Huang, Chengyue Wu, Taiqiang Wu, Yao Mu, Yuan Yao, Hui Shen, Zhongwei Wan, Jinfa Huang, Chaofan Tao, Shen Yan, Huaxiu Yao, Lingpeng Kong, Hongxia Yang, Mi Zhang, Guillermo Sapiro, Jiebo Luo, Ping Luo, Ngai Wong  
  **Year:** 2025  
  **Venue:** <span style="color: #1e3a8a;">Transactions on Machine Learning Research (TMLR-2025)</span>  
  **URL:** [arXiv:2411.05902](https://arxiv.org/abs/2411.05902)  
  **TL;DR (EN):** A comprehensive survey of visual autoregressive modeling, covering representation strategies and applications across image, video, 3D, and multimodal generation, plus open challenges.  
  **TL;DR:** 全面综述视觉自回归模型的建模方法，涵盖表示策略及其在图像、视频、3D和多模态生成中的应用，并讨论开放挑战。  

- **Title:** <span style="color: #92400e;">Srpo: Enhancing multimodal llm reasoning via reflection-aware reinforcement learning</span>  
  **Authors:** Zhongwei Wan, Zhihao Dou, Che Liu, Yu Zhang, Dongfei Cui, Qinjian Zhao, Hui Shen, Jing Xiong, Yi Xin, Yifan Jiang, Chaofan Tao, Yangfan He, Mi Zhang, Shen Yan  
  **Year:** 2025  
  **Venue:** <span style="color: #1e3a8a;">arXiv preprint arXiv:2506.01713</span>  
  **URL:** [arXiv:2506.01713](https://arxiv.org/abs/2506.01713)  
  **TL;DR (EN):** SRPO is a reflection-aware RL framework that teaches MLLMs self-reflection and then optimizes concise, meaningful reflections with GRPO-style rewards to improve multimodal reasoning.  
  **TL;DR:** SRPO是一个反思感知的多模态RL框架，先训练多模态大模型学会自我反思，再用GRPO式奖励优化简洁有效的反思，从而提升多模态推理能力。  

- **Title:** <span style="color: #92400e;">The synergy dilemma of long-cot sft and rl: Investigating post-training techniques for reasoning vlms</span>  
  **Authors:** Jierun Chen, Tiezheng Yu, Haoli Bai, Lewei Yao, Jiannan Wu, Kaican Li, Fei Mi, Chaofan Tao, Lei Zhu, Manyi Zhang, Xiaohui Li, Lu Hou, Lifeng Shang, Qun Liu  
  **Year:** 2025  
  **Venue:** <span style="color: #1e3a8a;">arXiv preprint arXiv:2507.07562</span>  
  **URL:** [arXiv:2507.07562](https://arxiv.org/abs/2507.07562)  
  **TL;DR (EN):** The study compares long-CoT SFT vs. RL for reasoning VLMs and finds their combination often fails to yield additive gains, instead trading off accuracy, verbosity, and style.  
  **TL;DR:** 比较长链思维监督微调（SFT）与强化学习（RL）在视觉语言模型推理中的作用，发现两者组合往往无法带来叠加收益，而是在准确率、冗长程度和风格之间权衡。  

- **Title:** <span style="color: #92400e;">NAVERO: Unlocking Fine-Grained Semantics for Video-Language Compositionality</span>  
  **Authors:** Chaofan Tao, Gukyeong Kwon, Varad Gunjal, Hao Yang, Zhaowei Cai, Yonatan Dukler, Ashwin Swaminathan, R Manmatha, Colin Jon Taylor, Stefano Soatto  
  **Year:** 2024  
  **Venue:** <span style="color: #1e3a8a;">arXiv preprint arXiv:2408.09511</span>  
  **URL:** [arXiv:2408.09511](https://arxiv.org/abs/2408.09511)  
  **TL;DR (EN):** NAVERO introduces the AARO benchmark and negative-text augmentation with a negative-augmented matching loss to improve video-language compositional understanding and retrieval.  
  **TL;DR:** NAVERO提出AARO基准，并通过负文本增强和负增强匹配损失，提升视频-语言模型对组合语义的理解和检索能力。  

</details>

<details open markdown="1">
<summary><strong>2) Efficient ML</strong></summary>

- **Title:** <span style="color: #92400e;">ATTS: Asynchronous Test-Time Scaling via Conformal Prediction</span>  
  **Authors:** Jing Xiong, Qiujiang Chen, Fanghua Ye, Zhongwei Wan, Chuanyang Zheng, Chenyang Zhao, Hui Shen, Alexander Hanbo Li, Chaofan Tao, Haochen Tan, Haoli Bai, Lifeng Shang, Lingpeng Kong, Ngai Wong  
  **Year:** 2026  
  **Venue:** <span style="color: #1e3a8a;">International Conference on Learning Representations</span>  
  **URL:** [arXiv:2509.15148](https://arxiv.org/abs/2509.15148)  
  **TL;DR (EN):** ATTS is an asynchronous, conformal-prediction-based test-time scaling method that cuts synchronization overhead and accelerates scaling with statistical guarantees and no accuracy loss.  
  **TL;DR:** ATTS是一种基于一致性预测的异步测试时扩展方法，减少同步开销，在尽可能最小化准确率损失的情况下加速扩展。  

- **Title:** <span style="color: #92400e;">UNCOMP: Can Matrix Entropy Uncover Sparsity? - A Compressor Design from an Uncertainty-Aware Perspective</span>  
  **Authors:** Jing Xiong, Jianghan Shen, Fanghua Ye, Chaofan Tao, Zhongwei Wan, Jianqiao Lu, Xun Wu, Chuanyang Zheng, Zhijiang Guo, Min Yang, Lingpeng Kong, Ngai Wong  
  **Year:** 2025  
  **Venue:** <span style="color: #1e3a8a;">Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing</span>  
  **URL:** [DOI:10.48448/v1xq-f328](https://doi.org/10.48448/v1xq-f328)  
  **TL;DR (EN):** UNComp uses uncertainty (via truncated matrix entropy) to uncover KV-cache sparsity and perform adaptive compression for long-context inference, greatly shrinking cache while boosting throughput.  
  **TL;DR:** UNComp使用不确定性（通过截断矩阵熵）来发现KV缓存的稀疏性，并对长上下文推理进行自适应压缩，大幅缩小缓存同时提升吞吐量。  

- **Title:** <span style="color: #92400e;">Find your optimal teacher: Personalized data synthesis via router-guided multi-teacher distillation</span>  
  **Authors:** Hengyuan Zhang, Shiping Yang, Xiao Liang, Chenming Shang, Yuxuan Jiang, Chaofan Tao, Jing Xiong, Hayden Kwok-Hay So, Ruobing Xie, Angel X Chang, Ngai Wong  
  **Year:** 2025  
  **Venue:** <span style="color: #1e3a8a;">arXiv preprint arXiv:2510.10925</span>  
  **URL:** [arXiv:2510.10925](https://arxiv.org/abs/2510.10925)  
  **TL;DR (EN):** PerSyn "routes then generates" by assigning each prompt to its best teacher via a router that considers student learnability and teacher quality, improving synthetic-data distillation efficiency.  
  **TL;DR:** PerSyn采用"先路由后生成"策略，通过考虑学生学习能力和教师质量的路由器为每个提示分配最佳教师，提高合成数据蒸馏效率。  

- **Title:** <span style="color: #92400e;">AnchorTP: Resilient LLM Inference with State-Preserving Elastic Tensor Parallelism</span>  
  **Authors:** Wendong Xu, Chujie Chen, He Xiao, Kuan Li, Jing Xiong, Chen Zhang, Wenyong Zhou, Chaofan Tao, Yang Bai, Bei Yu, Ngai Wong  
  **Year:** 2026  
  **Venue:** <span style="color: #1e3a8a;">DATE</span>  
  **URL:** [arXiv:2511.11617](https://arxiv.org/abs/2511.11617)  
  **TL;DR (EN):** AnchorTP provides state-preserving elastic tensor parallelism with a GPU-resident daemon and bandwidth-aware migration planning, enabling fast recovery from single-GPU failures.  
  **TL;DR:** AnchorTP提供状态保持的弹性张量并行，通过GPU常驻守护进程和带宽感知的迁移规划，实现单GPU故障场景的快速恢复。  

- **Title:** <span style="color: #92400e;">Dynamic Discriminative Operations for Efficient Long-Context Inference of Large Language Models</span>  
  **Authors:** Zhongwei Wan, Xinjian Wu, Yu Zhang, Yi Xin, Chaofan Tao, Zhihong Zhu, Xin Wang, Siqi Luo, Jing Xiong, Longyue Wang, Mi Zhang  
  **Year:** 2024  
  **Venue:** <span style="color: #1e3a8a;">The Thirteenth International Conference on Learning Representations</span>  
  **URL:** [arXiv:2406.13035](https://arxiv.org/abs/2406.13035)  
  **TL;DR (EN):** D2O dynamically compresses KV cache at layer and token levels with allocation and recall/merge compensation, saving memory and improving long-context throughput without fine-tuning.  
  **TL;DR:** D2O在层和token级别动态压缩KV缓存，通过分配和召回/合并补偿，无需微调即可节省内存并提升长上下文吞吐量。  

- **Title:** <span style="color: #92400e;">Crossget: Cross-guided ensemble of tokens for accelerating vision-language transformers</span>  
  **Authors:** Dachuan Shi, Chaofan Tao, Anyi Rao, Zhendong Yang, Chun Yuan, Jiaqi Wang  
  **Year:** 2024  
  **Venue:** <span style="color: #1e3a8a;">International Conference on Machine Learning</span>  
  **URL:** [arXiv:2305.17455](https://arxiv.org/abs/2305.17455)  
  **TL;DR (EN):** CrossGET accelerates vision-language Transformers by cross-modally matching and ensembling tokens with efficient soft matching, reducing compute with minimal accuracy loss.  
  **TL;DR:** CrossGET通过跨模态匹配和集成token，使用相似token匹配和合并加速视觉-语言Transformer，在最小准确率损失下减少计算量。  

- **Title:** <span style="color: #92400e;">Rethinking kullback-leibler divergence in knowledge distillation for large language models</span>  
  **Authors:** Taiqiang Wu, Chaofan Tao, Jiahao Wang, Runming Yang, Zhe Zhao, Ngai Wong  
  **Year:** 2024  
  **Venue:** <span style="color: #1e3a8a;">Proceedings of the 31st International Conference on Computational Linguistics</span>  
  **URL:** [arXiv:2404.02657](https://arxiv.org/abs/2404.02657)  
  **TL;DR (EN):** It shows forward and reverse KL behave similarly in LLM distillation with enough training but emphasize head vs. tail early; Adaptive KL combines them to improve generation quality and diversity.  
  **TL;DR:** 研究表明在充分训练下，前向和反向KL在大语言模型蒸馏中表现相似，但早期分别关注分布头部和尾部；自适应KL结合两种蒸馏方式的优势，以提升模型的生成质量和多样性。  

- **Title:** <span style="color: #92400e;">Structured pruning for efficient generative pre-trained language models</span>  
  **Authors:** Chaofan Tao, Lu Hou, Haoli Bai, Jiansheng Wei, Xin Jiang, Qun Liu, Ping Luo, Ngai Wong  
  **Year:** 2023  
  **Venue:** <span style="color: #1e3a8a;">Findings of the Association for Computational Linguistics: ACL 2023</span>  
  **URL:** [DOI:10.18653/v1/2023.findings-acl.692](https://doi.org/10.18653/v1/2023.findings-acl.692)  
  **TL;DR (EN):** It proposes structured pruning across multiple generative-PLM components using learnable masks and sparse training to extract size-flexible subnets with significant speedups.  
  **TL;DR:** 提出对生成式预训练语言模型多个组件的结构化剪枝，使用可学习掩码和稀疏训练提取尺寸灵活的子网络，实现显著加速。  


- **Title:** <span style="color: #92400e;">Compression of Generative Pre-trained Language Models via Quantization</span>  
  **Authors:** Chaofan Tao, Lu Hou, Wei Zhang, Lifeng Shang, Xin Jiang, Qun Liu, Ping Luo, Ngai Wong  
  **Year:** 2022  
  **Venue:** <span style="color: #1e3a8a;">ACL 2022 (outstanding)</span>  
  **URL:** [arXiv:2203.10705](https://arxiv.org/abs/2203.10705)  
  **TL;DR (EN):** It adapts quantization to generative PLMs （e.g. GPT-2, BART）, addressing embedding homogenization with token-level contrastive distillation and module-wise dynamic scaling to achieve 13–14× compression at near full precision.  
  **TL;DR:** 将量化方法适配到生成式预训练语言模型（e.g. GPT-2, BART），通过token级对比蒸馏解决嵌入同质化问题，并用模块级动态缩放实现接近全精度的13-14倍压缩。  

- **Title:** <span style="color: #92400e;">Upop: Unified and progressive pruning for compressing vision-language transformers</span>  
  **Authors:** Dachuan Shi, Chaofan Tao, Ying Jin, Zhendong Yang, Chun Yuan, Jiaqi Wang  
  **Year:** 2023  
  **Venue:** <span style="color: #1e3a8a;">International Conference on Machine Learning</span>  
  **URL:** [arXiv:2301.13741](https://arxiv.org/abs/2301.13741)  
  **TL;DR (EN):** UPop is a unified progressive pruning framework that searches multimodal subnets in a continuous space and progressively retrains to achieve high compression for vision-language Transformers.  
  **TL;DR:** UPop是一个统一的渐进式剪枝框架，在连续空间中搜索多模态子网络并逐步重训练，实现视觉-语言Transformer的高压缩率。  

</details>


## Services

**Reviewer experience**

- **Conferences:** ICLR, ICML, NeurIPS, ACL, EMNLP, COLM, ICCV, CVPR, ECCV
- **Journals:** T-NNLS
