---
layout: default
title: About
permalink: /
redirect_from:
  - /about/
  - /about.html
---

<!-- Page-scoped styles are rendered here because the gem's head does not load head/custom.html. -->
<style>
  .home-page {
    --home-muted: #59616b;
    --home-action-text: #ffffff;
    padding-bottom: 1rem;
    line-height: 1.65;
  }

  html[data-theme="dark"] .home-page {
    --home-muted: #b5bdc8;
    --home-action-text: #08191e;
  }

  .home-page *,
  .home-page *::before,
  .home-page *::after {
    box-sizing: border-box;
  }

  .home-page :is(section, h2, [id]) {
    scroll-margin-top: 5.5rem;
  }

  .home-page h1 {
    margin: 0;
    font-size: clamp(1.5rem, 7.4vw, 2.5rem);
    font-weight: 400;
    line-height: 1.2;
    letter-spacing: -0.025em;
  }

  .home-page h2 {
    margin: 0;
    font-size: 1.7rem;
    font-weight: 400;
    line-height: 1.3;
    letter-spacing: -0.02em;
  }

  .home-page h3 {
    margin: 0;
    font-size: 1.12rem;
    font-weight: 600;
    line-height: 1.45;
  }

  .home-page p {
    margin: 0 0 0.9rem;
  }

  .home-page a {
    color: var(--global-theme-color);
    text-underline-offset: 0.2em;
  }

  /* The theme sets strong/span colors explicitly, overriding ordinary link inheritance. */
  .home-page a :is(strong, span, i) {
    color: inherit;
  }

  .home-page a:focus-visible,
  .home-page summary:focus-visible {
    outline: 2px solid var(--global-theme-color);
    outline-offset: 4px;
    border-radius: 3px;
  }

  .home-section-links {
    display: flex;
    flex-wrap: wrap;
    gap: 1.25rem;
    margin-bottom: 1.5rem;
  }

  .home-section-links[hidden] {
    display: none;
  }

  .home-hero {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 220px;
    column-gap: 2.75rem;
    row-gap: 1.5rem;
    align-items: start;
  }

  .home-heading {
    grid-column: 1;
    grid-row: 1;
  }

  .home-intro {
    grid-column: 1;
    grid-row: 2;
    font-size: 1.04rem;
  }

  .home-photo {
    grid-column: 2;
    grid-row: 1 / span 2;
    padding-top: 0.25rem;
  }

  .home-photo figure {
    margin: 0;
  }

  .home-photo img {
    display: block;
    width: 100%;
    height: auto;
    border-radius: 0.65rem;
  }

  .home-actions,
  .home-resources {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.65rem 1rem;
  }

  .home-actions {
    margin-top: 1.25rem;
  }

  .home-page .home-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.55rem;
    min-height: 44px;
    padding: 0.55rem 1.15rem;
    border: 1px solid var(--global-divider-color);
    border-radius: 0.5rem;
    font-size: 0.94rem;
    font-weight: 500;
    line-height: 1.4;
    text-decoration: none;
  }

  .home-page .home-primary {
    background: var(--global-theme-color);
    border-color: var(--global-theme-color);
    color: var(--home-action-text);
  }

  .home-button:hover {
    text-decoration: underline;
  }

  .home-section {
    margin-top: 3.75rem;
  }

  .home-section-heading {
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    justify-content: space-between;
    gap: 0.5rem 1rem;
    margin-bottom: 1.2rem;
  }

  .home-section-heading > a {
    font-size: 0.88rem;
  }

  .home-section-description {
    max-width: 46rem;
    margin-bottom: 1.4rem !important;
  }

  .home-project-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
  }

  .home-project {
    display: flex;
    flex-direction: column;
    padding: 1.3rem 1.4rem;
    border: 1px solid var(--global-divider-color);
    border-radius: 0.7rem;
    background: var(--global-card-bg-color);
  }

  .home-page .home-project-kind {
    margin-bottom: 0.35rem;
    color: var(--home-muted);
    font-size: 0.78rem;
    letter-spacing: 0.015em;
  }

  .home-project h3 {
    margin-bottom: 0.5rem;
  }

  .home-project h3 a {
    text-decoration: underline;
    text-decoration-thickness: 1px;
  }

  .home-project > p:not(.home-project-kind) {
    font-size: 0.94rem;
    line-height: 1.6;
  }

  .home-project .home-resources {
    margin-top: auto;
    padding-top: 0.3rem;
    font-size: 0.82rem;
    font-weight: 500;
  }

  .home-paper-list {
    margin: 0;
    padding: 0;
    list-style: none;
  }

  .home-paper {
    padding: 1.25rem 0;
    border-bottom: 1px solid var(--global-divider-color);
  }

  .home-paper:first-child {
    padding-top: 0;
  }

  .home-paper h3 a {
    color: var(--global-text-color);
  }

  .home-paper h3 a:hover {
    color: var(--global-theme-color);
  }

  .home-page .home-paper-meta,
  .home-page .home-paper-authors {
    margin: 0.35rem 0;
    color: var(--home-muted);
    font-size: 0.87rem;
    line-height: 1.55;
  }

  .home-page .home-paper-authors strong {
    color: var(--global-text-color);
    font-weight: 600;
  }

  .home-paper-takeaway {
    margin: 0.6rem 0 !important;
    font-size: 0.94rem;
  }

  .home-paper .home-resources {
    font-size: 0.83rem;
    font-weight: 500;
  }

  .home-page .home-award {
    color: var(--global-theme-color);
    font-weight: 500;
  }

  .home-background {
    max-width: 49rem;
  }

  .home-publication-group {
    margin-top: 0.85rem;
    border: 1px solid var(--global-divider-color);
    border-radius: 0.6rem;
    padding: 0.9rem 1.15rem;
  }

  .home-publication-group > summary {
    cursor: pointer;
    font-weight: 500;
    line-height: 1.55;
  }

  .home-publication-group[open] > summary {
    margin-bottom: 1.3rem;
  }

  .home-page .home-count {
    margin-left: 0.35rem;
    color: var(--home-muted);
    font-size: 0.85rem;
    font-weight: 400;
  }

  .home-paper-details {
    margin-top: 0.7rem;
    font-size: 0.87rem;
  }

  .home-page .home-paper-details > summary {
    width: fit-content;
    color: var(--home-muted);
    cursor: pointer;
    font-size: 0.8rem;
  }

  .home-paper-details[open] > summary {
    margin-bottom: 0.65rem;
  }

  .home-contact {
    padding: 1.6rem 1.8rem;
    border: 1px solid var(--global-divider-color);
    border-radius: 0.8rem;
    background: var(--global-card-bg-color);
  }

  .home-contact h2 {
    margin-bottom: 1rem;
  }

  .home-contact .home-actions {
    margin: 1.1rem 0 1.5rem;
  }

  .home-page .home-intern-note {
    color: var(--home-muted);
    font-size: 0.87rem;
  }

  .home-socials {
    --link-box: clamp(2.75rem, 14vw, 3.75rem);
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    align-items: start;
    gap: 0.3rem;
    max-width: 27rem;
    margin: 1.5rem auto 0;
    padding-top: 1rem;
    border-top: 1px solid var(--global-divider-color);
  }

  .home-page .home-social-link {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 0;
    border-radius: 0.4rem;
    color: var(--global-text-color);
    text-align: center;
    text-decoration: none;
  }

  .home-social-link:hover {
    background: var(--global-code-bg-color);
  }

  .home-social-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: var(--link-box);
    height: var(--link-box);
    line-height: 1;
  }

  /* Preserve the existing optical sizing: each mark has ink height 0.6 × its box. */
  .home-social-icon i {
    display: block;
    font-size: calc(var(--link-box) * 0.8);
    line-height: 1;
  }

  .home-social-email .home-social-icon {
    color: #d93025;
  }

  .home-social-scholar .home-social-icon {
    color: #4285f4;
  }

  .home-social-github i {
    font-size: calc(var(--link-box) * 0.6352);
  }

  .home-social-icon img {
    display: block;
    object-fit: contain;
  }

  .home-social-hf img {
    width: calc(var(--link-box) * 0.7016);
    height: calc(var(--link-box) * 0.7016);
  }

  .home-social-legox img {
    width: var(--link-box);
    height: var(--link-box);
  }

  .home-social-label {
    padding: 0 0.1rem 0.4rem;
    font-size: 0.75rem;
    line-height: 1.35;
  }

  .home-services {
    font-size: 0.9rem;
  }

  .home-services h2 {
    margin-bottom: 0.8rem;
  }

  @media (max-width: 640px) {
    .home-hero {
      grid-template-columns: minmax(0, 1fr);
      row-gap: 1rem;
    }

    .home-heading {
      grid-column: 1;
      grid-row: 1;
    }

    .home-photo {
      grid-column: 1;
      grid-row: 2;
      width: 128px;
      padding: 0;
      justify-self: center;
    }

    .home-intro {
      grid-column: 1;
      grid-row: 3;
      font-size: 1rem;
    }

    .home-section {
      margin-top: 2.75rem;
    }

    .home-page h2 {
      font-size: 1.5rem;
    }

    .home-project-grid {
      grid-template-columns: minmax(0, 1fr);
    }

    .home-project {
      padding: 1.1rem 1.15rem;
    }

    .home-actions {
      gap: 0.6rem;
    }

    .home-page .home-button {
      padding-right: 0.9rem;
      padding-left: 0.9rem;
      font-size: 0.88rem;
    }

    .home-publication-group {
      padding: 0.85rem;
    }

    .home-contact {
      padding: 1.2rem 1rem;
    }

    .home-social-label {
      font-size: 0.7rem;
    }
  }

  @media (prefers-reduced-motion: no-preference) {
    .home-project {
      transition: border-color 0.15s ease;
    }

    .home-project:hover {
      border-color: var(--global-theme-color);
    }
  }
</style>

<div class="home-page">
  <nav class="home-section-links" aria-label="Page sections" data-homepage-navigation>
    <a href="#projects">Projects</a>
    <a href="#publications">Publications</a>
    <a href="#contact">Contact</a>
  </nav>

  <section class="home-hero" id="about" aria-labelledby="home-name">
    <header class="home-heading">
      <h1 id="home-name">{{ site.title }}</h1>
    </header>
    <div class="home-photo">
      {% include figure.liquid loading="eager" path="assets/img/prof_pic.png" class="img-fluid" sizes="(max-width: 640px) 128px, 220px" alt="Chaofan Tao at Sydney Harbour" cache_bust=true %}
    </div>
    <div class="home-intro" id="biography">
      <p>I am a researcher and developer at Huawei Foundation Model Lab, working on <strong>coding agents</strong>, <strong>agentic data and environments</strong>, and <strong>efficient training and inference infrastructure</strong>.</p>
      <p>My work on generative model quantization received an <a href="https://aclanthology.org/2022.acl-long.331/">ACL 2022 Outstanding Paper Award</a>.</p>
      <div class="home-actions">
        <a class="home-button home-primary" href="mailto:tcftrees@gmail.com"><i class="fa-solid fa-envelope" aria-hidden="true"></i>Email me</a>
        <a class="home-button" href="https://scholar.google.com/citations?user=gjmfLroAAAAJ">Google Scholar</a>
      </div>
    </div>
  </section>

  <section class="home-section" id="projects" aria-labelledby="projects-heading">
    <div class="home-section-heading">
      <h2 id="projects-heading">Recent projects</h2>
      <a href="https://www.legox.net/">Explore LegoX <span aria-hidden="true">↗</span></a>
    </div>
    <p class="home-section-description">I am actively involved in <a href="https://www.legox.net/"><strong>LegoX</strong></a>, an open-source effort connecting agentic data, training infrastructure, evaluation, and models.</p>
    <div class="home-project-grid">
      <article class="home-project">
        <p class="home-project-kind">Data &amp; environments</p>
        <h3><a href="https://www.legox.net/blog/legoflow/">LegoFlow</a></h3>
        <p>An agent-orchestrated framework for building verified coding tasks and training trajectories, from repository discovery to evaluation.</p>
        <div class="home-resources" aria-label="LegoFlow resources">
          <a href="https://www.legox.net/blog/legoflow/">Overview</a>
          <a href="https://github.com/LegoX/LegoFlow">Code</a>
          <a href="https://huggingface.co/collections/Lego-X/legoflow">Data</a>
        </div>
      </article>
      <article class="home-project">
        <p class="home-project-kind">Training infrastructure</p>
        <h3><a href="https://www.legox.net/blog/lego-rl/">Lego-RL</a></h3>
        <p>Reinforcement learning inside unmodified coding-agent harnesses, preserving generation-time tokens and MoE routing for faithful training.</p>
        <div class="home-resources" aria-label="Lego-RL resources">
          <a href="https://www.legox.net/blog/lego-rl/">Overview</a>
          <a href="https://github.com/LegoX/Lego-RL">Code</a>
          <a href="https://huggingface.co/collections/Lego-X/lego-rl">Models &amp; data</a>
        </div>
      </article>
      <article class="home-project">
        <p class="home-project-kind">Terminal agents</p>
        <h3><a href="https://www.legox.net/blog/terminal-lego/">Terminal-Lego</a></h3>
        <p>Executable tasks and grounded interaction trajectories for terminal-agent training, using 30× fewer examples in the reported comparison.</p>
        <div class="home-resources" aria-label="Terminal-Lego resources">
          <a href="https://www.legox.net/blog/terminal-lego/">Overview</a>
          <a href="https://github.com/SWE-Lego/terminal-lego">Code</a>
          <a href="https://huggingface.co/datasets/SWE-Lego/Terminal-Lego-15k">Data</a>
        </div>
      </article>
      <article class="home-project">
        <p class="home-project-kind">Coding agents</p>
        <h3><a href="https://www.legox.net/blog/swe-lego/">SWE-Lego</a></h3>
        <p>A supervised fine-tuning recipe for software issue resolution, combining verified data, error masking, and curriculum learning.</p>
        <div class="home-resources" aria-label="SWE-Lego resources">
          <a href="https://www.legox.net/blog/swe-lego/">Overview</a>
          <a href="https://github.com/SWE-Lego/SWE-Lego">Code</a>
          <a href="https://arxiv.org/abs/2601.01426">Paper</a>
        </div>
      </article>
    </div>
  </section>

  <section class="home-section" id="publications" aria-labelledby="selected-heading">
    <div class="home-section-heading" id="publications-2022">
      <h2 id="selected-heading">Selected publications</h2>
      <a href="#all-publications">All {{ site.data.homepage.publications.size }} publications <span aria-hidden="true">↓</span></a>
    </div>
    {% assign selected_papers = site.data.homepage.publications | where_exp: "paper", "paper.selected_order" | sort: "selected_order" %}
    <ol class="home-paper-list">
      {% for paper in selected_papers %}
        <li class="home-paper">
          <h3><a href="{{ paper.url | escape }}">{{ paper.title | escape }}</a></h3>
          <p class="home-paper-meta">{{ paper.venue | escape }} · {{ paper.year }}{% if paper.award %} · <a class="home-award" href="{{ paper.award_url }}">Outstanding Paper Award</a>{% endif %}</p>
          <p class="home-paper-authors">{{ paper.short_authors | escape | replace: 'Chaofan Tao', '<strong>Chaofan Tao</strong>' }}</p>
          <p class="home-paper-takeaway">{{ paper.takeaway | escape }}</p>
          <div class="home-resources" aria-label="Resources for {{ paper.title | escape }}">
            <a href="{{ paper.url | escape }}">Paper</a>
            {% if paper.code %}<a href="{{ paper.code | escape }}">Code</a>{% endif %}
            {% if paper.data %}<a href="{{ paper.data | escape }}">Data</a>{% endif %}
            {% if paper.demo %}<a href="{{ paper.demo | escape }}">Demo</a>{% endif %}
          </div>
        </li>
      {% endfor %}
    </ol>
  </section>

  <section class="home-section home-background" id="background" aria-labelledby="background-heading">
    <div class="home-section-heading"><h2 id="background-heading">Background</h2></div>
    <p>I received my PhD from <a href="https://www.hku.hk/">The University of Hong Kong</a>, advised by <a href="https://www.eee.hku.hk/~nwong/">Prof. Ngai Wong</a> and <a href="http://luoping.me/">Prof. Ping Luo</a>, as a member of the <a href="https://mmlab.hk/">MMLAB@HKU</a> family. I completed my bachelor's degree at the Yingcai Honors College of the University of Electronic Science and Technology of China.</p>
    <p>Previously, I interned at Sea AI Lab, Amazon Web Services, Huawei, and SenseTime. My work has appeared at ICLR, ICML, NeurIPS, ACL, EMNLP, COLM, and ECCV, as well as related journals.</p>
  </section>

  <section class="home-section" id="all-publications" aria-labelledby="all-publications-heading">
    <div class="home-section-heading"><h2 id="all-publications-heading">All publications <span class="home-count">2022–2026</span></h2></div>
    <p class="home-section-description">Browse by topic. Each paper includes its full author list and a Chinese summary under “Authors &amp; 中文摘要”.</p>
    {% for group in site.data.homepage.groups %}
      {% assign papers = site.data.homepage.publications | where: "group", group.id %}
      <details class="home-publication-group">
        <summary>{{ group.title | escape }} <span class="home-count">{{ papers.size }} papers</span></summary>
        <ol class="home-paper-list">
          {% for paper in papers %}
            <li class="home-paper">
              <h3><a href="{{ paper.url | escape }}">{{ paper.title | escape }}</a></h3>
              <p class="home-paper-meta">{{ paper.venue | escape }} · {{ paper.year }}{% if paper.award %} · <a class="home-award" href="{{ paper.award_url }}">Outstanding Paper Award</a>{% endif %}</p>
              <p class="home-paper-authors">{{ paper.short_authors | escape | replace: 'Chaofan Tao', '<strong>Chaofan Tao</strong>' }}</p>
              <p class="home-paper-takeaway">{{ paper.abstract_en | escape }}</p>
              <div class="home-resources" aria-label="Resources for {{ paper.title | escape }}">
                <a href="{{ paper.url | escape }}">Paper</a>
                {% if paper.code %}<a href="{{ paper.code | escape }}">Code</a>{% endif %}
                {% if paper.data %}<a href="{{ paper.data | escape }}">Data</a>{% endif %}
                {% if paper.demo %}<a href="{{ paper.demo | escape }}">Demo</a>{% endif %}
              </div>
              <details class="home-paper-details">
                <summary>Authors &amp; <span lang="zh">中文摘要</span></summary>
                <p>{{ paper.authors | escape | replace: 'Chaofan Tao', '<strong>Chaofan Tao</strong>' }}</p>
                <p lang="zh">{{ paper.abstract_zh | escape }}</p>
              </details>
            </li>
          {% endfor %}
        </ol>
      </details>
    {% endfor %}
  </section>

  <section class="home-section home-contact" id="contact" aria-labelledby="hiring-and-collaboration">
    <h2 id="hiring-and-collaboration">Let's connect</h2>
    <p>I welcome <strong>research/engineering interns</strong> and <strong>collaborators</strong> interested in coding agents, agentic data, and efficient training and inference.</p>
    <p>Whether you have a concrete project or an early idea, I'd love to hear from you. A short introduction and a link to something you've worked on are plenty.</p>
    <div class="home-actions">
      <a class="home-button home-primary" href="mailto:tcftrees@gmail.com"><i class="fa-solid fa-envelope" aria-hidden="true"></i>Email me</a>
      <a href="mailto:tcftrees@gmail.com">tcftrees@gmail.com</a>
    </div>
    <p class="home-intern-note">For internship inquiries, please use “[Interest]” in the subject and include your profile and 1–2 representative links: a paper, GitHub repository, blog, or demo.</p>
    <div class="home-socials" id="links" aria-label="Contact and profile links">
      <a class="home-social-link home-social-email" href="mailto:tcftrees@gmail.com" aria-label="Email Chaofan Tao">
        <span class="home-social-icon"><i class="fa-solid fa-envelope" aria-hidden="true"></i></span>
        <span class="home-social-label">Email</span>
      </a>
      <a class="home-social-link home-social-github" href="https://github.com/ChaofanTao" aria-label="Chaofan Tao on GitHub">
        <span class="home-social-icon"><i class="fa-brands fa-github" aria-hidden="true"></i></span>
        <span class="home-social-label">GitHub</span>
      </a>
      <a class="home-social-link home-social-scholar" href="https://scholar.google.com/citations?user=gjmfLroAAAAJ" aria-label="Chaofan Tao on Google Scholar">
        <span class="home-social-icon"><i class="ai ai-google-scholar" aria-hidden="true"></i></span>
        <span class="home-social-label">Scholar</span>
      </a>
      <a class="home-social-link home-social-hf" href="https://huggingface.co/tcftrees" aria-label="Chaofan Tao on Hugging Face">
        <span class="home-social-icon"><img src="https://huggingface.co/front/assets/huggingface_logo-noborder.svg" alt="" aria-hidden="true" loading="lazy"></span>
        <span class="home-social-label">Hugging Face</span>
      </a>
      <a class="home-social-link home-social-legox" href="https://www.legox.net/" aria-label="LegoX">
        <span class="home-social-icon"><img src="https://www.legox.net/logo/legox-parallel-pipeline.svg" alt="" aria-hidden="true" loading="lazy"></span>
        <span class="home-social-label">LegoX</span>
      </a>
    </div>
  </section>

  <section class="home-section home-services" id="services" aria-labelledby="services-heading">
    <h2 id="services-heading">Service</h2>
    <p>Conference reviewer: ICLR, ICML, NeurIPS, ACL, EMNLP, COLM, ICCV, CVPR, ECCV.<br>Journal reviewer: T-NNLS.</p>
  </section>
</div>

<script src="{{ '/assets/js/homepage.js' | relative_url }}" defer></script>
