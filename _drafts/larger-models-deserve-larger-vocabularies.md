---
layout: post
title: "Larger models deserve larger vocabularies: a practitioner's guide"
description: "How to pick a compute-optimal vocabulary size for your LLM, with the three estimation methods and an interactive calculator."
tags: scaling-laws tokenizer efficient-llm
---

<!--
DRAFT: written for newcomers; needs Chaofan's own framing and practical advice before publishing.
Verified facts (arXiv:2407.13623, NeurIPS 2024):
- models 33M-3B params, up to 500B characters
- three methods: IsoFLOPs, derivative estimation, parametric loss fit
- Llama2-70B optimal vocab >= 216K (7x its 32K)
- 3B model, 2.3e21 FLOPs: 32K -> 43K vocab, ARC-Challenge 29.1 -> 32.0
Demo: https://huggingface.co/spaces/sail/scaling-with-vocab-demo
-->

**TL;DR (first 60 words, answer-first):** TODO

## Why vocabulary size is a scaling dimension

## Three ways to estimate the optimum

## How to use the calculator for your model

## Common mistakes

## Further reading
