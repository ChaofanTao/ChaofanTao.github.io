---
layout: default
title: "Agentic Intelligence"
description: "Research across multimodal reasoning, robotics and coding agents, with open questions about learning, verification, multi-agent collaboration, AI for AI and recursive self-improvement."
permalink: /research/agentic-intelligence/
research_lang: en
last_modified_at: 2026-11-06
og_image: /assets/img/og-image.png
figure: /assets/img/research/agentic-loop.svg
about:
  - Agentic intelligence
  - Coding agents
  - Agentic reinforcement learning
  - Agentic data
  - Multimodal reasoning
  - Agent evaluation
  - Reward hacking
  - Long-horizon agents
  - Multi-agent systems
  - AI for AI
  - Recursive self-improvement
---

{% include research/styles.liquid %}
{% include research/jsonld.liquid group="agentic" %}

<div class="research-page">
  <nav class="research-breadcrumb" aria-label="Breadcrumb">
    <a href="{{ '/' | relative_url }}">Chaofan Tao</a><span aria-hidden="true">/</span>
    <a href="{{ '/research/' | relative_url }}">Research</a><span aria-hidden="true">/</span>
    <span>Agentic intelligence</span>
    <span aria-hidden="true">·</span><a href="{{ '/zh/research/agentic-intelligence/' | relative_url }}" lang="zh-Hans">中文版</a>
  </nav>

<h1>Agentic Intelligence</h1>
  <p class="research-dek">What does a model need beyond the ability to produce an answer, if it is to explore, check its work and improve? My work in multimodal reasoning, robotics and coding agents approaches this question from different directions. Further ahead lie questions about teams of agents and AI that helps improve AI.</p>
  <p class="research-meta">By <a href="{{ '/' | relative_url }}">Chaofan Tao (陶超凡)</a> · Last updated <time datetime="{{ page.last_modified_at | date: '%Y-%m-%d' }}">{{ page.last_modified_at | date: "%B %-d, %Y" }}</time></p>

  <p>A detail in an image can determine what to search for. A failed test can overturn a diagnosis. A plausible action can depend on conditions that do not exist in the environment. An agent has to work through these gaps: inspect what is there, choose a next step, and revise its understanding when the result arrives.</p>
  <p>Code offers a useful place to study this process because actions, changes and test results leave records. It shares questions with my earlier work on vision, multimodal reasoning and robotics: where the evidence for an action comes from, how errors are discovered, and whether experience helps on the next task. Recent LegoX projects make parts of this process executable and inspectable. I also draw on work from other teams to consider how these lessons might extend to agentic intelligence more broadly.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/agentic-loop.svg' | relative_url }}" alt="Environment, experience, training signals and evaluation interact in agent learning, with related projects shown at each stage." width="760" height="480" loading="eager"></div>
    <figcaption>An attempt leaves experience. Training extracts capabilities from it, and evaluation checks whether they carry over to new tasks.</figcaption>
  </figure>

  <p class="research-toc">On this page: <a href="#environment">Evidence for action</a> · <a href="#physical">Vision and robotics</a> · <a href="#experience">Useful experience</a> · <a href="#signal">Training and feedback</a> · <a href="#evaluation">Independent checks</a> · <a href="#long-horizon">Multiple agents</a> · <a href="#insights">AI for AI and RSI</a> · <a href="#open-questions">Open questions</a></p>

  <h2 id="environment">What the model can do depends on what it gets to see</h2>
  <p>A coding agent reaches its environment through a harness. The harness determines how files are read, how tool results appear, when history is compacted, and how execution continues after a failed command. If an important error message is truncated, the model has to make its next decision without it. That can change the outcome.</p>
  <p>In one <a href="https://www.legox.net/blog/lego-rl/">Lego-RL</a> evaluation, the same starting model's scores differed by 6.8 percentage points across three harnesses. This motivated training in the harness used for execution, followed by <a href="https://www.legox.net/blog/lego-rl-cross-harness/">training one model across several harnesses</a>. On the three evaluated interfaces, the shared model approached the average performance of three separately trained models. That supports sharing capabilities across familiar interfaces. Which capabilities survive an unfamiliar tool or environment remains a further question.</p>

  <h3 id="physical">Images and robots make the question tangible</h3>
  <p><a href="https://arxiv.org/abs/2508.21475">MMSearch-Plus</a> asks agents to follow fine visual cues through several rounds of image-text retrieval and cross-checking. Being able to crop a detail and search from it changes what the agent can reason about next. <a href="https://arxiv.org/abs/2505.15929">PhyX</a> asks models to connect visible phenomena with physical constraints, while <a href="https://arxiv.org/abs/2408.09511">NAVERO</a> tests distinctions between similar actions and relations in video. An incorrect answer may begin with perception, retrieval or reasoning; identifying the point of failure gives a more specific starting point for improvement.</p>
  <p><a href="https://arxiv.org/abs/2402.16117">RoboCodeX</a> breaks high-level instructions into operations on particular objects and generates control code, making perception, constraints and actions more explicitly connected. Physical environments also change the cost of feedback: a command can be rerun, but a physical action may be irreversible. Could more autonomous agents learn when to observe and when to act according to the environment? Connecting visual generation and understanding to action raises that question too. Our <a href="https://arxiv.org/abs/2411.05902">survey of autoregressive models in vision</a> provides background on those visual models.</p>

  <h2 id="experience">A useful example leaves the reasoning available to learn</h2>
  <p><a href="https://www.legox.net/blog/legoflow/">LegoFlow</a> turns real code changes into executable tasks, checking that the original version fails relevant tests and the reference patch passes. <a href="https://arxiv.org/abs/2601.01426">SWE-Lego</a> combines real issues with tasks constructed by injecting bugs, balancing complexity and scale. Once the tasks exist, a harder selection problem begins: which records of attempts are worth teaching from?</p>
  <p><a href="https://arxiv.org/abs/2606.03461">Terminal-Lego</a> offers a useful example. Across the teacher and student combinations studied, a stronger solver did not necessarily produce a stronger student. Traces that exposed inspection, action and verification transferred better. For a student, the gap between a sequence of correct commands and a usable method is the evidence that explains each decision.</p>
  <p>Length is an imperfect substitute for that evidence. In <a href="https://www.legox.net/blog/legoflow-experiments/">LegoFlow's experiments</a>, students trained on groups ordered by average reasoning length performed much worse on the shortest group, but gains across the remaining groups quickly flattened. Filtering examples with inadequate analysis helped; adding more text did not promise the same return. The more useful questions are whether a consequential decision has support and whether the agent changes course when new information arrives.</p>
  <p>Release details matter here. The <a href="https://huggingface.co/datasets/Lego-X/LegoFlow-SWE">LegoFlow-SWE data card</a> explains that a zero reward in the raw release includes both test failures and unscored runs. A reward of one records verifier success, rather than a completed audit for answer leakage. How should a system preserve these distinctions if it collects its own data and updates itself? Treating an environment failure as a reasoning error, or retrieving an existing patch as solving the problem, could teach the next round the wrong lesson.</p>

  <h2 id="signal">How does experience become a lasting capability?</h2>
  <p>Supervised fine-tuning (SFT) learns from demonstrations that may themselves contain mistakes. SWE-Lego retains failed steps as context while excluding them from the imitation loss. The student can still see why an attempt failed and how it recovered. A failure supplies information; whether its actions should be imitated is a separate choice.</p>
  <p>Reinforcement learning (RL) updates behavior from outcomes and requires the training record to correspond to the attempt that produced them. <a href="https://arxiv.org/abs/2608.17393">Lego-RL</a> captures tokens, probabilities and mixture-of-experts routing during generation, then checks correspondence on the training side. History rewrites still complicate reconstruction. Such problems can hide behind normal training curves: the program runs, while its update may no longer represent the decision that actually occurred.</p>
  <p>Tasks without a unique answer need more detailed feedback. <a href="https://arxiv.org/abs/2601.18533">RLVRR</a> derives content and style requirements from reference answers; <a href="https://arxiv.org/abs/2601.21968">OVD</a> uses a teacher's verbal scores to retain better student-generated portions and replace weaker continuations. In multimodal reasoning, our <a href="https://arxiv.org/abs/2507.07562">long-CoT SFT and RL study</a> found that their gains did not simply add in the tested combinations, while <a href="https://arxiv.org/abs/2506.01713">SRPO</a> specifically trains concise, useful reflection. These studies make the objective concrete: which behavior should change, and what feedback would reveal that change?</p>

  <h2 id="evaluation">A check should add evidence</h2>
  <p>A patch can fix the example and miss an edge case. An experiment report can read convincingly without ruling out another explanation. <a href="https://arxiv.org/abs/2607.06065">SWE-Review</a> has a reviewer inspect the repository and investigate the issue before judging a candidate patch. We measure both decision accuracy and whether the feedback helps a subsequent repair. The useful contribution is what the review checks that generation left unresolved.</p>
  <p>Agreement between two agents does not automatically supply two independent pieces of evidence. With the same material and assumptions, they may miss the same error. Could collaboration be organized around reproducible experiments, counterexamples and traceable sources? Tests and continuous integration in <a href="https://arxiv.org/abs/2505.23932">SwingArena</a>, and the explicit requirements in <a href="https://arxiv.org/abs/2604.06861">REAgent</a>, provide concrete objects to check.</p>
  <p>The evaluation environment needs scrutiny too. <a href="https://arxiv.org/abs/2610.24206">SWE-Bench Pro V2</a> repairs tasks and regrades patches applied to clean containers, echoing the leakage encountered in LegoFlow. More capable exploration can reach defects in grading that earlier systems never exposed. Self-improvement takes this a step further: if the agent can change the evaluation procedure itself, what should establish that it has improved?</p>

  <h2 id="long-horizon">Multiple agents: what can a division of work achieve?</h2>
  <p>A complex goal can involve finding evidence, proposing hypotheses, designing experiments, implementing methods and checking results. Those activities may need different tools, context and working rhythms. Multiple agents can pursue them concurrently and examine each other's work. How they divide the task, what they share and when they combine results all matter.</p>
  <p><a href="https://arxiv.org/abs/2512.08296">Towards a Science of Scaling Agent Systems</a> finds that coordination benefits depend on task structure in comparisons with controlled tools and compute. Decomposable tasks can benefit, while strictly sequential tasks can suffer from coordination overhead. <a href="https://arxiv.org/abs/2503.13657">Studies of multi-agent failures</a> also identify unclear specifications, misalignment between agents, and problems with verification and stopping. This sharpens the research question: can a team learn how to organize itself, deciding when to explore in parallel and when to converge on a decision?</p>
  <p><a href="https://arxiv.org/abs/2610.24454">MELD, from October 2026</a>, moves this question into learning by updating both a team coordinator and individual research agents while keeping the executor fixed. Assignments determine the experience each member receives; what members learn changes the division of work worth trying next. How can an experiment distinguish gains from better individuals, better organization and additional computation?</p>
  <p>Shared memory presents a related problem. If one member reports that a method works, others need to know on which data, code version and settings. Should that conclusion be checked again when those conditions change? Can a team share the necessary evidence while preserving different lines of inquiry? These questions connect perception, tools, memory and verification well beyond programming tasks.</p>

  <h2 id="insights">AI for AI: can an improvement help produce the next one?</h2>
  <p>AI for AI studies the use of AI to develop data, training methods, evaluation and computing systems. <a href="https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/">AlphaEvolve</a> combines program generation, automated evaluation and evolutionary search for algorithm discovery, including improvements to computing infrastructure. <a href="https://sakana.ai/dgm/">The Darwin Gödel Machine</a> modifies the agent's own code and retains different versions for further exploration. They improve different objects, but both make proposing, testing and retaining changes into an ongoing process.</p>
  <p>Recursive self-improvement (RSI) asks a further question: can the improvement from this round make the next round of discovery more effective? <a href="https://arxiv.org/abs/2609.26457">AIDE², reported in September 2026</a>, modifies its own research code and uses accepted versions in subsequent rounds, reporting successive improvements and transfer to held-out tasks. These experiments make the question testable. They also leave room to examine whether gains come from better search, better memory, or increasing familiarity with a particular task collection.</p>
  <p>If agents generate evaluators as well, the source of feedback becomes part of the research. <a href="https://arxiv.org/abs/2610.04184">EvalResearchBench</a> studies whether agents can construct cheaper evaluations, finding that the best evaluator on development targets need not remain best on sealed targets. One avenue to investigate is separating the information used to propose changes, select candidates and perform final replication, while adding tasks that never participated in the search. How can this remain reliable without verification consuming the entire gain? That question connects RSI directly to <a href="{{ '/research/efficient-ml-ai-infrastructure/#long-horizon' | relative_url }}">efficiency research</a>.</p>

  <figure class="research-figure">
    <div class="research-figure-scroll"><img src="{{ '/assets/img/research/self-improvement-questions.svg' | relative_url }}" alt="Research questions in self-improvement: agents propose and execute candidates, independent checks select improvements to inherit, and those improvements feed the next round of exploration." width="960" height="320" loading="lazy"></div>
    <figcaption>A possible self-improvement loop. Its arrows are empirical questions: producing a new version still leaves usefulness, transfer and better subsequent exploration to establish.</figcaption>
  </figure>

  <h2 id="open-questions">Questions these connections leave open</h2>
  <ul>
    <li>At the same total budget, how can multiple agents obtain evidence and explore possibilities that a single agent would miss? Can they learn to adjust their division of work to the task?</li>
    <li>To turn a successful attempt into a lasting capability, should experience enter model weights, external skills or shared memory? Where does each form transfer?</li>
    <li>After several rounds of improvement, how can we establish that subsequent discovery became more effective, beyond having screened more candidates? How should fresh evaluations and replication be budgeted?</li>
  </ul>

  <h2 id="resources">Project resources and papers</h2>
  <p>These releases accompany the recent projects discussed above. Related papers from different stages of my research, with full author lists, follow below. Further work is available through <a href="https://scholar.google.com/citations?user=gjmfLroAAAAJ">Google Scholar</a>, <a href="https://github.com/ChaofanTao">GitHub</a> and <a href="https://huggingface.co/tcftrees">Hugging Face</a>.</p>
  <ul>
    <li>LegoFlow: <a href="https://github.com/LegoX/LegoFlow">code</a> · <a href="https://huggingface.co/collections/Lego-X/legoflow">data</a></li>
    <li>SWE-Lego: <a href="https://github.com/LegoX/SWE-Lego">code</a> · <a href="https://huggingface.co/collections/Lego-X/swe-lego">data and models</a></li>
    <li>Terminal-Lego: <a href="https://github.com/LegoX/Terminal-Lego">code</a> · <a href="https://huggingface.co/datasets/Lego-X/Terminal-Lego-15k">data</a></li>
    <li>Lego-RL: <a href="https://github.com/LegoX/Lego-RL">code</a> · <a href="https://huggingface.co/collections/Lego-X/lego-rl">models and data</a></li>
    <li>SWE-Review: <a href="https://github.com/LegoX/SWE-Review">code</a> · <a href="https://huggingface.co/collections/Lego-X/swe-review">models and data</a></li>
  </ul>

{% include research/paper-list.liquid group="agentic" lang="en" %}

  <p>Related: <a href="{{ '/research/efficient-ml-ai-infrastructure/' | relative_url }}">Efficient ML and AI infrastructure</a></p>
</div>
