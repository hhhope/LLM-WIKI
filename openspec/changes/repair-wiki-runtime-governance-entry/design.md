# Design: repair wiki runtime governance entry

## Approach

Treat `AGENTS.md` as the startup index for the full `LLM-WIKI` runtime, not as
a short repository note. The entry should stay compact enough to load early,
but it must expose the behavior rails that future agents need before they open
lower-level files.

The source reference contributes structure only. `LLM-WIKI` owns its own
runtime objects, skill names, scripts, and boundaries.

## Runtime Entry Shape

`AGENTS.md` will contain these durable sections:

- scope and authority;
- workflow change gate;
- workflow routing;
- hard stops;
- behavior replay gate;
- behavior asset prior-art gate;
- high-frequency skills;
- agent intent routing;
- wiki runtime stack;
- wiki medical loop;
- frontmatter taxonomy gate;
- skill authoring contract;
- output routing;
- verification.

## Ownership Rules

`High-Frequency Skills` is the single route table. `Agent Intent Routing`
classifies before acting and points back to that table; it must not create a
second route table.

Runtime scripts are executors and evidence surfaces. They do not replace agent
judgment, route selection, hard stops, or case-file authority.

## Behavior Evaluation

This is a semantic behavior-asset change because it changes future-agent
triggers, required routes, forbidden actions, authority framing, and completion
evidence.

Evaluation must include:

- pressure scenarios with positive and negative routes;
- RED baseline against the current thin `AGENTS.md`;
- GREEN result against the repaired entry;
- prior-art / common-rule dedupe covering repo `AGENTS.md`, `PROJECT.md`,
  `.codex/skills`, `wiki/ops`, `wiki/config`, global rules, and the source
  reference;
- parent-gate preservation for skill routing, frontmatter, medical loop,
  OpenSpec, and public/material outputs.

## Non-Promotion Boundary

Source-reference material stays rejected unless it maps to an existing
`LLM-WIKI` runtime or generic behavior gate. Business-specific Go, Feishu,
meeting-lore, and report-portfolio details remain out of this repo entry.
