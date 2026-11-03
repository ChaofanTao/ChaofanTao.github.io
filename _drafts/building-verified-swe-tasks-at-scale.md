---
layout: post
title: "What we learned building verified SWE tasks at scale"
description: "From 12M pull requests to 5,000 verified tasks: filtering rules, verification failures and cost lessons from LegoFlow-SWE."
tags: coding-agents data legoflow swe-bench
---

<!--
DRAFT: needs first-hand detail (failure modes, cost, surprises) from Chaofan before publishing.
Verified facts (legox.net/blog/legoflow, 2026-09-18):
- 700K+ repos, 12M candidate PRs -> 600K after diff/patch/test/issue filters -> 5,000 verified (0.0417%)
- 8 languages, 20 task tags; GLM-5.2 9,767 rollouts, 2,780 pass
- Qwen3.5-35B-A3B-Base on ~1K trajectories: Verified 70.2 / Pro 48.8 / Multilingual 57.0;
  vs SWE-rebench-v2 same setup +5.8 / +1.9 / +1.0
- Self-improvement: 7.6 -> 56.1 (iter 1) -> 64.4 (iter 2, 512 trajectories after reasoning-depth filter)
-->

**TL;DR (first 60 words, answer-first):** TODO

## Why only 0.04% of pull requests survive

## The fail-then-pass check and where it fails

## Shallow reasoning traces: the filter that moved 56.1% to 64.4%

## Costs and throughput

## Data and code

Code: https://github.com/LegoX/LegoFlow · Data: https://huggingface.co/collections/Lego-X/legoflow
