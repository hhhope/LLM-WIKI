---
name: project-management-weekly-skill
description: Use when the user asks about 项目管理, 周报, 里程碑, 风险, 甘特图, 项目推进, or provides weekly project-management materials that need structured weekly outputs
---

# Project Management Weekly Skill

## Overview

Turn project-management material into a fixed weekly output set instead of a free-form summary.

## When to Use

- The user asks about project management, weekly progress, milestones, risks, gantt views, or project tracking.
- The material is a weekly report, schedule, risk list, milestone update, gantt view, testing tracker, or issue tracker.
- The goal is a durable wiki workflow, not a one-off summary.

Do not use this skill for pure implementation work or ordinary meeting notes without project-tracking context.

## Rules

- Preserve a `source` page for the original weekly material.
- Add an `html/source companion` when the input includes editable weekly views such as `html`, `h5`, `preview`, gantt, or capability maps.
- If the user explicitly asks to update a visual source file, update the file itself instead of syncing wiki-only conclusions.
- Extract at least: milestone, current progress, drift, risks, next actions, owner, and whether the item is only a reminder or a true Codex handoff candidate.
- `reminder` is not the same as `Codex handoff`. Escalate only when the task is clearly an engineering implementation with minimal acceptance criteria.
- Follow repo patterns from [项目管理周推进循环](../../../wiki/ops/project-management-weekly-loop.md).

## Common Mistakes

- Leaving only conclusions and no source page
- Treating visual weekly views as ordinary text reports
- Updating wiki notes without updating the requested `html/h5/preview` source file
- Promoting a reminder directly into a Codex task
- Reporting percentage progress while omitting owner, drift, or risk
