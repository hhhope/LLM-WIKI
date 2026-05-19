---
name: interview-deep-reading-board
description: Use when interview, podcast transcript, dialogue, or Q&A material is paired with deep reading, word cloud, timeline, temperature-axis, draggable-evidence, H5, or no-compression/full-coverage requests.
---

# Interview Deep Reading Board

## Overview

Route interview-like material into a source-order reading board when ordinary
summaries or word clouds would compress speaker-turn logic and evidence.

This skill is a delivery-sensitive module. It preserves
`public-report-quality-gate` for reader-facing H5/share/report outputs and
`material-collaboration-defaults` for source-first material processing.

## When To Use

Use this skill when the source is an interview, podcast transcript, dialogue,
or Q&A and the user asks for:

- deep reading, `精读`, or full-context reading;
- word cloud, timeline, temperature axis, draggable evidence, or H5 exploration;
- "do not compress the full text", "不要压缩全文", "太碎片", or "丢信息";
- repair after the user identifies a missing passage or collapsed keyword
  distinction.

Do not use it for ordinary non-dialogue article summaries, raw source fetching,
meeting minutes, or reader-facing publication gates by itself.

## Required Fork Question

Before building the output, ask:

> 这类访谈适合做“全文窗口式精读板”：按访谈顺序拆成足够多的阅读窗口，保留人物回合、时间线、温度轴、关键词和证据。要不要做这个类型？

If the user declines, continue with the requested narrower output while keeping
the compression risk visible.

## Hard Rules

- Keep source-order reading windows as the primary content unit.
- Treat word clouds as indexes into windows and evidence, never as the main
  reading structure.
- Connect temperature-axis movement to timeline position, window selection,
  keywords, and evidence.
- Preserve speaker-turn logic and adjacent-window continuity.
- User-highlighted or missing passages must become explicit windows or window
  groups; do not hide them under generic keywords.
- For copyrighted interviews, preserve coverage through source position,
  paraphrase, and short evidence snippets; do not store the full transcript
  verbatim in repo examples or skill references.
- For reader-facing H5/share/report output, route through
  `public-report-quality-gate` before review-ready, publish, or sync claims.

## Output Contract

An interview reading board should preserve:

- source position or sequence marker;
- speaker or speaker-role context;
- window title and short paraphrase;
- keywords tied to that window;
- temperature value or band;
- evidence snippets or source-position references;
- relation to adjacent windows;
- a deep-reading question or tension.

For H5 shape details, load `references/h5-output-shape.md`.

## Common Mistakes

- Producing a decorative word cloud and calling the interview "covered".
- Collapsing adjacent but different concepts such as `Agent` and `Agent to C`.
- Using ten broad theme cards for a long interview.
- Letting a polished H5 hide a missing source-order reading map.
- Treating this module as permission to bypass public output gates.
