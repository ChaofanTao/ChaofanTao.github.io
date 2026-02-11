---  
permalink: /  
title: ""  
excerpt: "About me"  
author_profile: true  
redirect_from:  
  - /about/  
  - /about.html  
---  


## Chaofan Tao (陶超凡)
I am a researcher at Huawei Foundation Model Lab. I got my PhD from The University of Hong Kong (HKU), advised by [Prof. Ngai Wong](https://www.eee.hku.hk/~nwong/) and [Prof. Ping Luo](http://luoping.me/), as a member of the [MMLAB@HKU](https://mmlab.hk/) family.  I completed my Bachelor’s degree from Yingcai Honors College at University of Electronic Science and Technology of China. Previously, I interned at Sea AI Lab (Singapore), Amazon Web Services (Bellevue), Huawei (Shenzhen), and SenseTime (Shanghai).

## Research focus
- **Agentic coding & reasoning**: CI-driven evaluation, long-context GitHub issue solving, verifiable rewards/verifiers, test-time scaling, tool-using agents.
- **Efficient LLMs**: pruning/quantization/distillation, KV-cache efficiency, elastic tensor parallelism, long-context inference.
- **Multimodal reasoning**: post-training for reasoning VLMs, self-reflection RL, video-language compositionality.

## Links
- **Google Scholar**: [publications](https://scholar.google.com/citations?hl=en&view_op=list_works&user=gjmfLroAAAAJ)
- **Website**: `http://chaofantao.top/`
- **Email**: `tcftrees AT gmail DOT com`

## Hiring (interns / collaborators)
I’m looking for **research/engineering interns** and **collaborators** who are excited about AI.

- **Primary need**: agentic coding & reasoning / software engineering agents (verifiers, CI-based evaluation, long-context codebase navigation, retrieval/tooling).
- **Also welcome**: efficient LLM training/inference and multimodal learning.

If you’d like to join or collaborate, email me with **[Interest] + your profile + 1–2 representative links** (paper / GitHub / blog / demo).

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
  **TL;DR:** 提出 SWE-Lego：用高质量真实+合成数据与难度课程/错误mask的SFT, 且研究了软件工程场景下code agent做test-time scaling的表现规律，把开源8B/32B模型在 SWE-bench Verified 上推到SOTA。  

- **Title:** <span style="color: #92400e;">MMFormalizer: Multimodal Autoformalization in the Wild</span>  
  **Authors:** Jing Xiong, Qi Han, Yunta Hsieh, Hui Shen, Huajian Xin, Chaofan Tao, Chenyang Zhao, Hengyuan Zhang, Taiqiang Wu, Zhen Zhang, Haochen Wang, Zhongwei Wan, Lingpeng Kong, Ngai Wong  
  **Year:** 2026  
  **Venue:** <span style="color: #1e3a8a;">arXiv preprint arXiv:2601.03017</span>  
  **URL:** [arXiv:2601.03017](https://arxiv.org/abs/2601.03017)  
  **TL;DR (EN):** MMFormalizer extends autoformalization to multimodal math/physics by grounding visual entities and recursively composing axioms, enabling formal statements for real-world problems (including classical mechanics) on the PhyX-AF benchmark.  
  **TL;DR:** 提出 MMFormalizer，通过多模态grounding与递归公理组合把真实世界图文/物理场景自动形式化为可验证命题，并在 PhyX-AF 上展示从经典力学到量子/相对论等物理域的统一支持。  

- **Title:** <span style="color: #92400e;">SwingArena: Competitive Programming Arena for Long-context GitHub Issue Solving</span>  
  **Authors:** Wendong Xu, Jing Xiong, Chenyang Zhao, Qiujiang Chen, Haoran Wang, Hui Shen, Zhongwei Wan, Jianbo Dai, Taiqiang Wu, He Xiao, Chaofan Tao, Z Morley Mao, Ying Sheng, Zhijiang Guo, Hongxia Yang, Bei Yu, Lingpeng Kong, Quanquan Gu, Ngai Wong  
  **Year:** 2026  
  **Venue:** <span style="color: #1e3a8a;">International Conference on Learning Representations (oral)</span>  
  **URL:** [arXiv:2505.23932](https://arxiv.org/abs/2505.23932)  
  **TL;DR (EN):** SwingArena is a CI-driven competitive framework where LLMs act as submitters and reviewers, paired with retrieval-augmented code generation to handle long-context, multi-language GitHub issue solving.  
  **TL;DR:** 提出 SwingArena：让 LLM 以“提交者/审阅者”在 CI 回路中对抗迭代的真实软件开发式评测框架，并用检索增强代码生成模块解决长上下文与多编程语言问题。  

- **Title:** <span style="color: #92400e;">Mmsearch-plus: Benchmarking provenance-aware search for multimodal browsing agents</span>  
  **Authors:** Xijia Tao, Yihua Teng, Xinxing Su, Xinyu Fu, Jihao Wu, Chaofan Tao, Ziru Liu, Haoli Bai, Rui Liu, Lingpeng Kong  
  **Year:** 2026  
  **Venue:** <span style="color: #1e3a8a;">International Conference on Learning Representations</span>  
  **URL:** [arXiv:2508.21475](https://arxiv.org/abs/2508.21475)  
  **TL;DR (EN):** MMSearch-Plus is a 311-task benchmark and agent framework with set-of-mark tools that require provenance-aware, vision-in-the-loop search and cross-validation under retrieval noise.  
  **TL;DR:** 提出 MMSearch-Plus（311题）与 SoM 标注/裁剪工具链，强制在噪声检索下通过“视觉线索→检索→交叉验证”进行可追溯的多模态搜索推理，从而更严格评测浏览型多模态agent能力。  

- **Title:** <span style="color: #92400e;">OVD: On-policy Verbal Distillation</span>  
  **Authors:** Jing Xiong, Hui Shen, Shansan Gong, Yuxin Cheng, Jianghan Shen, Chaofan Tao, Haochen Tan, Haoli Bai, Lifeng Shang, Ngai Wong  
  **Year:** 2026  
  **Venue:** <span style="color: #1e3a8a;">arXiv preprint arXiv:2601.21968</span>  
  **URL:** [arXiv:2601.21968](https://arxiv.org/abs/2601.21968)  
  **TL;DR (EN):** On-policy Verbal Distillation replaces token-level matching with trajectory-level distillation using discrete teacher scores, reducing memory and improving student performance on web QA and math reasoning.  
  **TL;DR:** 提出 On-policy Verbal Distillation：用教师0–9离散评分做轨迹级对齐替代token级匹配，显著降低内存并提升学生模型在Web Search Agent场景与数学推理上的蒸馏效果。  


- **Title:** <span style="color: #92400e;">From Verifiable Dot to Reward Chain: Harnessing Verifiable Reference-based Rewards for Reinforcement Learning of Open-ended Generation</span>  
  **Authors:** Yuxin Jiang, Yufei Wang, Qiyuan Zhang, Xingshan Zeng, Liangyou Li, Jierun Chen, Chaofan Tao, Haoli Bai, Lifeng Shang  
  **Year:** 2026  
  **Venue:** <span style="color: #1e3a8a;">International Conference on Learning Representations</span>  
  **URL:** [arXiv:2601.18533](https://arxiv.org/abs/2601.18533)  
  **TL;DR (EN):** RLVRR turns single verifiable end rewards into ordered reference-derived reward chains (content + style) to make RL for open-ended generation more efficient and less prone to reward hacking.  
  **TL;DR:** 提出 RLVRR：从高质量参考中抽取按序“奖励链”，将奖励分解为可验证内容与可验证风格两维，使开放式生成也能进行更可靠的可验证强化学习并减少 reward hacking。  

- **Title:** <span style="color: #92400e;">PhyX: Does Your Model Have the "Wits" for Physical Reasoning?</span>  
  **Authors:** Hui Shen, Taiqiang Wu, Qi Han, Yunta Hsieh, Jizhou Wang, Yuyue Zhang, Yuxin Cheng, Zijian Hao, Yuansheng Ni, Xin Wang, Zhongwei Wan, Kai Zhang, Wendong Xu, Jing Xiong, Ping Luo, Wenhu Chen, Chaofan Tao, Zhuoqing Mao, Ngai Wong  
  **Year:** 2025  
  **Venue:** <span style="color: #1e3a8a;">arXiv preprint arXiv:2505.15929</span>  
  **URL:** [arXiv:2505.15929](https://arxiv.org/abs/2505.15929)  
  **TL;DR (EN):** PhyX introduces a 3K-question multimodal benchmark spanning six physics domains to test physics-grounded reasoning, revealing large gaps between top models and human experts.  
  **TL;DR:** 提出 PhyX：覆盖6大物理域/25子域的3K多模态物理推理的测评Benchmark，揭示 SOTA 模型在真实物理约束推理上与人类仍有显著差距。  


- **Title:** <span style="color: #92400e;">Scaling laws with vocabulary: Larger models deserve larger vocabularies</span>  
  **Authors:** Chaofan Tao, Qian Liu, Longxu Dou, Niklas Muennighoff, Zhongwei Wan, Ping Luo, Min Lin, Ngai Wong  
  **Year:** 2024  
  **Venue:** <span style="color: #1e3a8a;">Advances in Neural Information Processing Systems (NeurIPS-2024)</span>  
  **URL:** [arXiv:2407.13623](https://arxiv.org/abs/2407.13623)  
  **TL;DR (EN):** The paper derives compute-optimal vocabulary scaling laws and shows larger models benefit from larger vocabularies, improving downstream accuracy at fixed FLOPs.  
  **TL;DR:** 系统研究词表规模对LLM scaling law 的影响，提出多种方法预测计算最优词表并证明“更大模型/算力需要更大词表”，从而在同等FLOPs下提升下游表现。  

</details>

<details markdown="1">
<summary><strong>2) Efficient ML</strong></summary>

- **Title:** <span style="color: #92400e;">ATTS: Asynchronous Test-Time Scaling via Conformal Prediction</span>  
  **Authors:** Jing Xiong, Qiujiang Chen, Fanghua Ye, Zhongwei Wan, Chuanyang Zheng, Chenyang Zhao, Hui Shen, Alexander Hanbo Li, Chaofan Tao, Haochen Tan, Haoli Bai, Lifeng Shang, Lingpeng Kong, Ngai Wong  
  **Year:** 2026  
  **Venue:** <span style="color: #1e3a8a;">International Conference on Learning Representations</span>  
  **URL:** [arXiv:2509.15148](https://arxiv.org/abs/2509.15148)  
  **TL;DR (EN):** ATTS is an asynchronous, conformal-prediction-based test-time scaling method that cuts synchronization overhead and accelerates scaling with statistical guarantees and no accuracy loss.  
  **TL;DR:** 提出 ATTS：基于一致性(Conformal)假设检验的异步 test-time scaling 框架，用在线校准+三阶段拒绝采样同时扩展并行/串行维度，在不降精度下显著降延迟并提升吞吐。  

- **Title:** <span style="color: #92400e;">UNCOMP: Can Matrix Entropy Uncover Sparsity? - A Compressor Design from an Uncertainty-Aware Perspective</span>  
  **Authors:** Jing Xiong, Jianghan Shen, Fanghua Ye, Chaofan Tao, Zhongwei Wan, Jianqiao Lu, Xun Wu, Chuanyang Zheng, Zhijiang Guo, Min Yang, Lingpeng Kong, Ngai Wong  
  **Year:** 2025  
  **Venue:** <span style="color: #1e3a8a;">Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing</span>  
  **URL:** [DOI:10.48448/v1xq-f328](https://doi.org/10.48448/v1xq-f328)  
  **TL;DR (EN):** UNComp uses uncertainty (via truncated matrix entropy) to uncover KV-cache sparsity and perform adaptive compression for long-context inference, greatly shrinking cache while boosting throughput.  
  **TL;DR:** 提出 UNComp：用截断矩阵熵刻画不确定性以发现KV缓存的结构化稀疏并做自适应压缩，在长上下文推理中将KV降到极小比例同时提升预填速度与吞吐。  

- **Title:** <span style="color: #92400e;">Find your optimal teacher: Personalized data synthesis via router-guided multi-teacher distillation</span>  
  **Authors:** Hengyuan Zhang, Shiping Yang, Xiao Liang, Chenming Shang, Yuxuan Jiang, Chaofan Tao, Jing Xiong, Hayden Kwok-Hay So, Ruobing Xie, Angel X Chang, Ngai Wong  
  **Year:** 2025  
  **Venue:** <span style="color: #1e3a8a;">arXiv preprint arXiv:2510.10925</span>  
  **URL:** [arXiv:2510.10925](https://arxiv.org/abs/2510.10925)  
  **TL;DR (EN):** PerSyn “routes then generates” by assigning each prompt to its best teacher via a router that considers student learnability and teacher quality, improving synthetic-data distillation efficiency.  
  **TL;DR:** 提出 PerSyn（Route-then-Generate）：用查询级router为每个prompt选择最适合该学生的教师再合成数据，更高效且在指令微调与数学推理上优于常规蒸馏的做法。  

- **Title:** <span style="color: #92400e;">AnchorTP: Resilient LLM Inference with State-Preserving Elastic Tensor Parallelism</span>  
  **Authors:** Wendong Xu, Chujie Chen, He Xiao, Kuan Li, Jing Xiong, Chen Zhang, Wenyong Zhou, Chaofan Tao, Yang Bai, Bei Yu, Ngai Wong  
  **Year:** 2025  
  **Venue:** <span style="color: #1e3a8a;">arXiv preprint arXiv:2511.11617</span>  
  **URL:** [arXiv:2511.11617](https://arxiv.org/abs/2511.11617)  
  **TL;DR (EN):** AnchorTP provides state-preserving elastic tensor parallelism with a GPU-resident daemon and bandwidth-aware migration planning, enabling fast recovery from single-GPU failures.  
  **TL;DR:** 提出 AnchorTP：通过守护进程在GPU内存中保留参数与KV缓存并配合带宽感知迁移规划实现弹性张量并行，使多GPU推理在单卡故障后能快速恢复服务。  

- **Title:** <span style="color: #92400e;">Dynamic Discriminative Operations for Efficient Long-Context Inference of Large Language Models</span>  
  **Authors:** Zhongwei Wan, Xinjian Wu, Yu Zhang, Yi Xin, Chaofan Tao, Zhihong Zhu, Xin Wang, Siqi Luo, Jing Xiong, Longyue Wang, Mi Zhang  
  **Year:** 2024  
  **Venue:** <span style="color: #1e3a8a;">The Thirteenth International Conference on Learning Representations</span>  
  **URL:** [arXiv:2406.13035](https://arxiv.org/abs/2406.13035)  
  **TL;DR (EN):** D2O dynamically compresses KV cache at layer and token levels with allocation and recall/merge compensation, saving memory and improving long-context throughput without fine-tuning.  
  **TL;DR:** 提出 D2O：按层动态分配KV预算并按token相似度做“回召/合并”补偿的无微调缓存压缩方法，在大幅省内存的同时保持长上下文生成质量并提升吞吐。  

- **Title:** <span style="color: #92400e;">Crossget: Cross-guided ensemble of tokens for accelerating vision-language transformers</span>  
  **Authors:** Dachuan Shi, Chaofan Tao, Anyi Rao, Zhendong Yang, Chun Yuan, Jiaqi Wang  
  **Year:** 2024  
  **Venue:** <span style="color: #1e3a8a;">International Conference on Machine Learning</span>  
  **URL:** [arXiv:2305.17455](https://arxiv.org/abs/2305.17455)  
  **TL;DR (EN):** CrossGET accelerates vision-language Transformers by cross-modally matching and ensembling tokens with efficient soft matching, reducing compute with minimal accuracy loss.  
  **TL;DR:** 提出 CrossGET：利用跨模态引导的token软匹配与合并，在推理时动态集成核心的token以加速多种视觉-语言Transformer，同时保持多项下游任务性能。  

- **Title:** <span style="color: #92400e;">Rethinking kullback-leibler divergence in knowledge distillation for large language models</span>  
  **Authors:** Taiqiang Wu, Chaofan Tao, Jiahao Wang, Runming Yang, Zhe Zhao, Ngai Wong  
  **Year:** 2024  
  **Venue:** <span style="color: #1e3a8a;">Proceedings of the 31st International Conference on Computational Linguistics</span>  
  **URL:** [arXiv:2404.02657](https://arxiv.org/abs/2404.02657)  
  **TL;DR (EN):** It shows forward and reverse KL behave similarly in LLM distillation with enough training but emphasize head vs. tail early; Adaptive KL combines them to improve generation quality and diversity.  
  **TL;DR:** 重新审视蒸馏问题中的FKL/RKL，指出二者优化目标等价但早期关注分布头/尾不同，并提出自适应加权的AKL以提升蒸馏后LLM的生成质量与多样性。  

- **Title:** <span style="color: #92400e;">Structured pruning for efficient generative pre-trained language models</span>  
  **Authors:** Chaofan Tao, Lu Hou, Haoli Bai, Jiansheng Wei, Xin Jiang, Qun Liu, Ping Luo, Ngai Wong  
  **Year:** 2023  
  **Venue:** <span style="color: #1e3a8a;">Findings of the Association for Computational Linguistics: ACL 2023</span>  
  **URL:** [DOI:10.18653/v1/2023.findings-acl.692](https://doi.org/10.18653/v1/2023.findings-acl.692)  
  **TL;DR (EN):** It proposes structured pruning across multiple generative-PLM components using learnable masks and sparse training to extract size-flexible subnets with significant speedups.  
  **TL;DR:** 提出覆盖隐藏维、embedding、LN等结构的生成式语言模型的结构化剪枝：用可学习mask+稀疏训练找冗余并导出不同规模子网，在显著减参下带来GPU/CPU加速且可与量化叠加。  


- **Title:** <span style="color: #92400e;">Compression of Generative Pre-trained Language Models via Quantization</span>  
  **Authors:** Chaofan Tao, Lu Hou, Wei Zhang, Lifeng Shang, Xin Jiang, Qun Liu, Ping Luo, Ngai Wong  
  **Year:** 2022  
  **Venue:** <span style="color: #1e3a8a;">ACL 2022 (outstanding)</span>  
  **URL:** [arXiv:2203.10705](https://arxiv.org/abs/2203.10705)  
  **TL;DR (EN):** It adapts quantization to generative PLMs, addressing embedding homogenization with token-level contrastive distillation and module-wise dynamic scaling to achieve 13–14× compression at near full precision.  
  **TL;DR:** 提出面向生成式语言模型的量化方法：用token级对比蒸馏缓解词向量同质化问题，并用模块级动态缩放适配权重分布，实现GPT-2/BART在近似全精度下的10×+压缩。  

</details>

<details markdown="1">
<summary><strong>3) Large Vision-Language Models</strong></summary>

- **Title:** <span style="color: #92400e;">Autoregressive Models in Vision: A Survey</span>  
  **Authors:** Jing Xiong, Gongye Liu, Lun Huang, Chengyue Wu, Taiqiang Wu, Yao Mu, Yuan Yao, Hui Shen, Zhongwei Wan, Jinfa Huang, Chaofan Tao, Shen Yan, Huaxiu Yao, Lingpeng Kong, Hongxia Yang, Mi Zhang, Guillermo Sapiro, Jiebo Luo, Ping Luo, Ngai Wong  
  **Year:** 2025  
  **Venue:** <span style="color: #1e3a8a;">Transactions on Machine Learning Research (TMLR-2025)</span>  
  **URL:** [arXiv:2411.05902](https://arxiv.org/abs/2411.05902)  
  **TL;DR (EN):** A comprehensive survey of visual autoregressive modeling, covering representation strategies and applications across image, video, 3D, and multimodal generation, plus open challenges.  
  **TL;DR:** 系统综述视觉自回归建模的表示与框架（像素/token/多尺度），梳理其在图像/视频/3D与多模态生成中的进展、关联与挑战。  

- **Title:** <span style="color: #92400e;">Srpo: Enhancing multimodal llm reasoning via reflection-aware reinforcement learning</span>  
  **Authors:** Zhongwei Wan, Zhihao Dou, Che Liu, Yu Zhang, Dongfei Cui, Qinjian Zhao, Hui Shen, Jing Xiong, Yi Xin, Yifan Jiang, Chaofan Tao, Yangfan He, Mi Zhang, Shen Yan  
  **Year:** 2025  
  **Venue:** <span style="color: #1e3a8a;">arXiv preprint arXiv:2506.01713</span>  
  **URL:** [arXiv:2506.01713](https://arxiv.org/abs/2506.01713)  
  **TL;DR (EN):** SRPO is a reflection-aware RL framework that teaches MLLMs self-reflection and then optimizes concise, meaningful reflections with GRPO-style rewards to improve multimodal reasoning.  
  **TL;DR:** 提出 SRPO 两阶段反思强化学习：先构造反思数据让模型学会自我纠错，再在GRPO中用新奖励鼓励简洁有效反思，从而显著提升多模态推理准确率与反思质量。  

- **Title:** <span style="color: #92400e;">The synergy dilemma of long-cot sft and rl: Investigating post-training techniques for reasoning vlms</span>  
  **Authors:** Jierun Chen, Tiezheng Yu, Haoli Bai, Lewei Yao, Jiannan Wu, Kaican Li, Fei Mi, Chaofan Tao, Lei Zhu, Manyi Zhang, Xiaohui Li, Lu Hou, Lifeng Shang, Qun Liu  
  **Year:** 2025  
  **Venue:** <span style="color: #1e3a8a;">arXiv preprint arXiv:2507.07562</span>  
  **URL:** [arXiv:2507.07562](https://arxiv.org/abs/2507.07562)  
  **TL;DR (EN):** The study compares long-CoT SFT vs. RL for reasoning VLMs and finds their combination often fails to yield additive gains, instead trading off accuracy, verbosity, and style.  
  **TL;DR:** 系统研究长CoT SFT 与 RL 在多模态推理VLM中的作用差异与组合失败现象，指出两者常产生风格与难度上的权衡而非叠加收益，提出“协同困境”。  

- **Title:** <span style="color: #92400e;">NAVERO: Unlocking Fine-Grained Semantics for Video-Language Compositionality</span>  
  **Authors:** Chaofan Tao, Gukyeong Kwon, Varad Gunjal, Hao Yang, Zhaowei Cai, Yonatan Dukler, Ashwin Swaminathan, R Manmatha, Colin Jon Taylor, Stefano Soatto  
  **Year:** 2024  
  **Venue:** <span style="color: #1e3a8a;">arXiv preprint arXiv:2408.09511</span>  
  **URL:** [arXiv:2408.09511](https://arxiv.org/abs/2408.09511)  
  **TL;DR (EN):** NAVERO introduces the AARO benchmark and negative-text augmentation with a negative-augmented matching loss to improve video-language compositional understanding and retrieval.  
  **TL;DR:** 提出多模态组件的解耦式理解方案与负例增强训练/匹配损失，提升视频-语言模型对动作与关系等细粒度组合语义的辨别与检索性能。  

- **Title:** <span style="color: #92400e;">Upop: Unified and progressive pruning for compressing vision-language transformers</span>  
  **Authors:** Dachuan Shi, Chaofan Tao, Ying Jin, Zhendong Yang, Chun Yuan, Jiaqi Wang  
  **Year:** 2023  
  **Venue:** <span style="color: #1e3a8a;">International Conference on Machine Learning</span>  
  **URL:** [arXiv:2301.13741](https://arxiv.org/abs/2301.13741)  
  **TL;DR (EN):** UPop is a unified progressive pruning framework that searches multimodal subnets in a continuous space and progressively retrains to achieve high compression for vision-language Transformers.  
  **TL;DR:** 提出 UPop 统一且渐进的多模态Transformer剪枝框架，在连续空间搜索跨模态子网并逐步搜索-重训以获得更高压缩率，适用于多种视觉-语言任务与架构。  


</details>

## Services
**Reviewer Experience**  
- **Conferences**: ICML, ICLR,  NeurIPS, ACL, EMNLP, ICCV, CVPR，ECCV 
- **Journals**: T-NNLS  
