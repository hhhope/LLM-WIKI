# Gate Review Artifact

Create or update a repo-visible gate-review artifact before Feishu sync or a
review-ready claim.

## Location

Use `wiki/ops/<canonical-object>-report-gate-review.md`.

If the report belongs to an existing canonical object, reuse that object in the
filename. Do not keep the gate review only in chat, `/tmp`, or the Feishu
document.

## Required Sections

| Section | Required Content |
|---|---|
| Review Target | Target title, destination, scope, and non-scope |
| Reviewer Routing | Required/not required/not applicable/blocked, checked escalation signals, reviewer result when required, and user-selected template status |
| Article Intent Contract | Reader, reader decision or action, main line, non-goals, user-owned judgments, and agent-allowed work |
| Reference Structure Map | Source, reader job, page group, reading path, visual logic, writing standard, reuse boundary, and linked-page readback when the reference has child pages or concrete reading-map links |
| Reference Output Shape | Selected output shape, retained patterns, rejected patterns, user-approved shape changes, Reference Output Shape Gate result, and replay notes when shape drift was repaired |
| Learning Use Map | Applicable learning artifacts, domain/topic, reusable capability type, learning point, intended output use, and skip reason when relevant |
| Newspaper Citation Surface | Required for newspaper-style H5/share packages and public newspaper drafts: output path, source map path, load-bearing claim or visual panel, reader-visible citation target, source class, and boundary note when source strength is limited |
| Section And Paragraph Drift Review | Section objective, Paragraph claim, mainline role, target fit score, narrative drift score, evidence fit score, Judgment source, and action |
| Judgment Ledger | User-owned judgments, source-backed judgments, agent inferences, unknown judgments, and required user confirmations |
| Hard Gate Results | Learning use, reference, split, voice, narrative, paragraph drift, judgment ownership, visual, and publish gate results |
| Scorecard | Point breakdown and total score only after all hard gates pass; otherwise `INVALID` with the failing gate. Diagnostic paragraph scores may remain available for repair. |
| Decision | Whether the draft may update Feishu or be claimed review-ready |
| Residual Risks | Proof boundary and known gaps |
| Feishu Update Verification | Update command result, title, update log id, read-back result, read-back log id, and opening text |
| Visual Asset Boundary | Local asset paths, whether Feishu sync is text-only, whether image insertion was explicitly approved, and any client-usability limitation |

## Stable Workflow

```text
reader-facing request
  -> create/update wiki/ops/*-report-gate-review.md
  -> decide reviewer routing before drafting
  -> run reviewer flow or record why reviewer is not required
  -> record Article Intent Contract
  -> complete reference structure map and linked-page readback
  -> record selected output shape, retained patterns, rejected patterns,
     user-approved shape changes, and Reference Output Shape Gate result
  -> complete learning use map when learned references are applicable
  -> complete Newspaper Citation Surface when the output is a newspaper-style
     H5/share package or public newspaper draft
  -> choose split strategy and destination map
  -> draft reader-facing content
  -> complete Section And Paragraph Drift Review and Judgment Ledger
  -> pass hard gates and score >= 80
  -> update Feishu or publish target
     (text-only by default when local images exist)
  -> read back target
  -> append update/read-back evidence to gate-review artifact
  -> commit gate-review artifact
```

If the gate-review artifact is missing or incomplete, do not sync to Feishu and
do not claim the draft is ready for review.

If reviewer routing is required but not run, record the score as `INVALID` and
stop before drafting, Feishu sync, or review-ready claims unless the user
explicitly selects the template and scopes the reviewer step out for this run.

If the reference map is incomplete, or any hard gate is failed, partial,
unknown, or not tested, record the score as `INVALID` and stop before Feishu
sync or review-ready claims.

If a reference output shape is mapped but the draft silently changes to a
different primary structure, record the Reference Output Shape Gate as failed.
Keep the draft internal until repaired to the selected output shape or until
the user explicitly approves a different output shape. If production
instructions, image prompts, tool notes, or Hybrid routing text appear in
reader-facing content, move them to a separate asset brief or remove them.

If the Article Intent Contract, Section And Paragraph Drift Review, or Judgment
Ledger is missing for complex, scored, reference-shaped, or drift-corrected
drafts, record the score as `INVALID`. Keep diagnostic 0-5 paragraph scores if
they help repair, but do not treat them as a publish or review-ready score.

If a paragraph's judgment source is agent inference or unknown for the article's
main line, conclusion, priority, proof-strength claim, or public stance, ask the
user before claiming review-ready status.

If the output claims to use learned references but the learning use map is
missing, incomplete, or only says "used the reference" without a concrete output
use or skip reason, stop before drafting, Feishu sync, or review-ready claims.

If the output is a newspaper-style H5/share package or public newspaper draft,
and load-bearing claims, figures, company examples, or visual panels lack a
reader-visible citation route, record the Newspaper Citation Surface Gate as
failed. Internal source maps, learning use maps, or gate-review artifacts are
not substitutes for reader-visible citations in the shareable output path.

If local visual assets exist, Feishu sync remains text-only unless the user
explicitly asks the agent to insert images. When image insertion is requested,
record the known client-freeze risk, the explicit approval, image tokens, and
read-back logs. Treat those logs as audit evidence only; they do not prove
Feishu client usability.
