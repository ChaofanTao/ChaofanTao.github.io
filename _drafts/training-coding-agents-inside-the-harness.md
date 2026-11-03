---
layout: post
title: "Training coding agents inside the harness they run in"
description: "Engineering lessons from Lego-RL: token fidelity, MoE routing replay, and RL inside Claude Code, OpenHands and OpenCode."
tags: coding-agents reinforcement-learning lego-rl
---

<!--
DRAFT: needs first-hand engineering detail from Chaofan before publishing.
Move to _posts/YYYY-MM-DD-training-coding-agents-inside-the-harness.md when ready.
Verified facts (legox.net/blog/lego-rl, 2026-08-18):
- Qwen3.5-35B-A3B; one run per harness: OpenHands SDK 64.0 -> 70.4, Claude Code 62.4 -> 68.2, OpenCode 57.2 -> 66.6
- 2,699 tasks, 200k context, 3 epochs / 126 steps; train/inference prob correlation r >= 0.998
- async 2.5x vs sync (~1.9x after throughput correction)
- reread-edited-file share 73.6% -> 98.1% (OpenHands SDK samples)
-->

**TL;DR (first 60 words, answer-first):** TODO

## Why the harness matters (6.8-point spread from the harness alone)

## Keeping tokens faithful: what breaks when you re-tokenize

## MoE routing replay: why and how

## Failures we hit and how we made them observable

## What changed in agent behavior after RL

## Try it

Code: https://github.com/LegoX/Lego-RL · Models: https://huggingface.co/collections/Lego-X/lego-rl
