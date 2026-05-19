# Wiki Explore Behavior Gate

Use these gates to evaluate whether a `wiki-explore` answer is deep enough.

## Required Output

| Section | Required |
|---|---|
| Current Object | Exact wiki-backed topic, thread, report, source set, or governance object being explored |
| Opened Evidence | Concrete files, source groups, specs, skills, or command contracts actually opened |
| Evidence Surface | Whether source map, broad scan, public timeline, podcast/video pool, evidence matrix, gate review, output draft, and residual risks exist |
| Enoughness Judgment | Enough / not enough / enough for X but not Y, with reasons |
| Next Boundary | Continue exploration / harden sources / propose OpenSpec / repair output / stop |

## Re-anchor Gate

Fail if the answer does not identify the current object.

Fail if it answers a nearby topic without stating that the target changed. For
example, if the user asks about yesterday's agent collaboration exploration, do
not answer with inbox cleanup or completion-bridge drift.

## Evidence Surface Gate

Fail if the answer summarizes from chat memory only.

The answer must open repo-visible evidence from the relevant layers:

- `wiki/ops`
- `wiki/sources`
- `wiki/reports`
- `openspec/specs`
- `openspec/changes/archive`
- `.codex/skills`
The answer does not need to open every layer for every topic, but it must say
which layers exist and which are missing.

## Public Source Depth Gate

When public material is involved, fail if the answer does not distinguish:

- primary sources;
- secondary/media sources;
- candidate leads;
- transcript or upstream-capture gaps;
- internal synthesis, gate review, or report draft evidence.

Fail if the answer treats a source pool, broad scan, or timeline as
publication-ready proof by itself.

## Enoughness Judgment Gate

Fail if the answer says "done", "ready", or "looks good" without saying what it
is enough for and what remains weak.

Preferred shape:

```text
Enough for: internal discussion / direction setting / next-source selection.
Not enough for: public citation / Feishu review-ready / final publication.
Missing: transcript capture / primary source / role integration / visual QA.
```

## Next Boundary Gate

Fail if the answer continues implementation, source hardening, report repair,
or OpenSpec changes without making the boundary explicit.

Valid next boundaries:

- continue exploring;
- harden public sources;
- propose an OpenSpec change;
- repair a report/H5;
- stop because the object is already sufficient for the stated use.

## Replay: RED

Input:

```text
wiki:explore 看下昨天 agent 团队协作这个事情，我一直说不够
```

Bad answer:

```text
We have no active OpenSpec changes. Next we can process inbox/nirvana.
```

Why it fails:

- wrong current object;
- no opened evidence;
- no evidence surface;
- no enoughness judgment.

## Replay: GREEN

Input:

```text
wiki:explore 看下昨天 agent 团队协作这个事情，我一直说不够
```

Good answer:

1. Current object:
   `agentic-product-engineering-collaboration`.
2. Opened evidence:
   source map, public timeline, podcast/video discussion pool, article
   evidence matrix, report gate review, and relevant H5/report drafts.
3. Evidence surface:
   source map, broad scan, timeline, podcast/video pool, evidence matrix, gate
   review, output drafts, and residual risks exist.
4. Enoughness judgment:
   enough for internal discussion, not enough for public publication or hard
   quotation.
5. Next boundary:
   source hardening, role-change integration, or report repair, depending on
   user goal.

This is the behavioral depth standard, not a requirement that every topic have
the same artifact count.
