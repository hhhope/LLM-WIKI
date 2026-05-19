# Design: bootstrap self-running wiki governance

## Approach

Use `account-meeting-lore` as a prior-art shape reference, not a source to copy
line by line. `LLM-WIKI` should expose only seed-level operating rules:

- repository scope and source-of-truth boundaries;
- workflow-change and OpenSpec gates;
- intent routing through repo-local skills;
- wiki medical-loop authority;
- frontmatter taxonomy checks;
- output routing for sources, ops, examples, ADRs, and status;
- verification requirements before completion claims.

## AGENTS Boundary

The repo `AGENTS.md` remains compact. It should state the durable routing
contract and point to detailed assets instead of duplicating taxonomy values,
skill instructions, or long runtime models.

The seed must reject direct promotion of `account-meeting-lore` business rules
such as meeting-note output, Feishu-specific publication, Go service defaults,
or historical governance decisions that depend on that repository.

## OpenSpec Boundary

Large or semantic workflow changes require an active OpenSpec change with at
least:

- `proposal.md`;
- `design.md`;
- `tasks.md`.

This change introduces that lifecycle directory in the seed. Archive policy is
not implemented here; completion stops after verified implementation and a
commit.

## Medical Loop Boundary

The normal self-maintenance route is `wiki-medical-agent`; stage-specific
skills and scripts remain bounded evidence surfaces. The case file is the
authority for whether treatment, surgery, recovery, or archive review is
allowed.

## Frontmatter Boundary

The strict gate comes from `wiki/config/frontmatter-taxonomy.yaml`; `AGENTS.md`
must not restate taxonomy vocabulary. Generated review-decision records need
frontmatter because they live under `wiki/ops/**/*.md`, which the strict gate
covers.

## Behavior Evaluation

This is a semantic behavior-asset change. Evaluation records must include:

- the baseline failure from the old `AGENTS.md` absence of repo-local gates;
- the after-change route for the same scenario;
- verification commands for strict frontmatter, status, and medical-agent
  status reporting;
- residual risk that deeper runtime autonomy is still blocked by thin graph
  relations and the current medical case state.
