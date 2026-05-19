# Public Report Quality Scorecard

Use this before creating/updating Feishu documents, H5/share drafts, or other
reader-facing reports.

## Hard Gates

Any hard-fail blocks publishing, Feishu sync, or a "ready for review" claim.

| Gate | Hard-fail signal |
|---|---|
| Learning Use Gate | The output claims to use prior learning or reference examples, but no output-use map identifies applicable learning artifacts, domain/topic, reusable capability type, used output element, and skip reasons for relevant unused points. |
| Reference Structure Gate | A reference artifact exists, but the draft does not map its actual overall structure, page split, reader path, visual logic, writing standard, concrete links, and linked-page roles before drafting. If the reference is a Feishu wiki node with `has_child: true` or a reading map with article links, those linked pages must be fetched and mapped before this gate can pass. |
| Reference Output Shape Gate | A reference-shaped draft preserves the topic but silently replaces the selected output shape with a different primary structure, or leaves production instructions, image prompts, tool notes, or Hybrid routing text inside reader-facing content. |
| Split Gate | One draft carries multiple reader jobs such as overview, runtime, migration, validation, and roadmap without an explicit split decision and final destination map. A review packet does not count as a split unless it is explicitly labeled non-final and not claimed review-ready. |
| Voice Gate | Chat residue, slogan simplification, loose narrator, weak section openings, internal ops leakage, or tone mismatch remains in reader-facing text. |
| Narrative Gate | The core story changes, such as turning an evolution path into a static responsibility split. |
| Paragraph Drift Gate | A section or important paragraph does not serve the Article Intent Contract, changes the main line, or lacks a repair action after drift is found. |
| Judgment Ownership Gate | The agent silently turns source material, reference examples, or polished prose into the user's conclusion, priority, proof-strength claim, or public stance without source support or user confirmation. |
| Visual Gate | Diagrams are decorative, duplicated text, or fail to say what relationship or decision they carry. If the reference uses essential visuals, a reference-shaped draft without corresponding visual assets or a concrete visual plan fails this gate; missing visuals cannot be downgraded to residual risk for review-ready output. |
| Publish Gate | Review status, source boundary, residual risks, or non-goals are missing before sync/publish. |

## Voice Gate Detail

| Check | Fail Condition |
|---|---|
| Chat residue | Phrases such as "这页是", "我们现在", "下一步去哪", or "一句话记忆" remain as chat/worklog framing instead of report prose. |
| Slogan simplification | A slogan replaces a definition, causal chain, maturity path, or argument. |
| Loose narrator | The draft sounds like an agent explaining what it did rather than a report serving a reader. |
| Weak section opening | A section starts by announcing its topic instead of giving a judgment, reader benefit, or necessary context. |
| Internal ops leakage | Repo paths, OpenSpec mechanics, gates, traces, or agent workflow appear without translation into reader-facing context. |
| Tone mismatch | The requested output is public/executive/shareable, but the tone remains scratch note, chat recap, or wiki draft. |

## Reference Output Shape Gate Detail

When the user or a reference artifact establishes an output shape, the draft
must preserve that shape unless the user explicitly approves a change. Record
the selected output shape before drafting: article/report flow, Feishu review
document, visual one-pager, card/grid page, dashboard, image brief, or another
named form.

Observable failures include:

- replacing a linear article or report structure with a modular grid or
  repeated block system as the primary body
- replacing a reference-led narrative with a comparison table as the primary
  body
- changing from an image brief, H5/share page, Feishu review document, or other
  named form to another form without explicit user approval
- leaving production instructions, image prompts, tool notes, or Hybrid routing
  text inside reader-facing content

This gate does not ban cards, grids, tables, dashboards, visual panels, or
image prompts when the user asks for them or the reference itself uses them. It
blocks silent replacement of the selected output shape.

## Article Intent Contract

Before paragraph drift can be judged, record the anchor:

| Field | Meaning |
|---|---|
| Reader | Who the article serves. |
| Reader decision or action | What the reader should understand, decide, or do after reading. |
| Main line | The article's controlling story or argument. |
| Non-goals | Topics, claims, or detail levels the article should not carry. |
| User-owned judgments | Conclusions, priorities, tradeoffs, proof-strength claims, or public stance that require user confirmation. |
| Agent-allowed work | Organization, summarization, rewriting, evidence mapping, or alternatives the agent may perform. |

## Section And Paragraph Drift Review

For complex, scored, reference-shaped, or drift-corrected drafts, record
diagnostic scores against the Article Intent Contract.

| Field | Meaning |
|---|---|
| Section objective | What this section is supposed to do for the reader. |
| Paragraph claim | What the paragraph actually asserts. |
| Mainline role | Setup, explanation, evidence, contrast, transition, conclusion, or off-track. |
| Target fit score | 0-5 diagnostic score for serving the reader decision or action. |
| Narrative drift score | 0-5 diagnostic score for deviation from the main line. |
| Evidence fit score | 0-5 diagnostic score for whether evidence supports the paragraph. |
| Judgment source | User, source material, agent inference, or unknown. |
| Action | Retain, compress, rewrite, delete, or ask the user. |

Drift scale:

| Score | Meaning |
|---:|---|
| 0 | Fully serves the main line. |
| 1 | Weak but acceptable support. |
| 2 | Related but should be compressed. |
| 3 | Drifting and should be rewritten. |
| 4 | Changes article judgment and needs user review. |
| 5 | Violates the target or replaces user judgment. |

## Judgment Ownership Gate Detail

Process can be delegated, but judgment cannot. The agent may organize,
summarize, rewrite, and propose alternatives. It must not silently own the
article's main line, strategic conclusion, priority, proof strength, or public
stance.

## Scorecard

Only score after all hard gates pass.

If any hard gate is `FAIL`, `PARTIAL`, `UNKNOWN`, or `NOT TESTED`, do not assign
a numeric score. Mark the scorecard `INVALID`, record the failing gate, and block
Feishu sync, publication, and review-ready claims.

If a hard gate fails, the overall score remains `INVALID`, but diagnostic scores
for section or paragraph drift may remain available to guide repair. Do not
convert those diagnostic scores into a publish or review-ready score.

| Dimension | Points | Full-credit standard |
|---|---:|---|
| Reference fidelity | 15 | Reuses the reference's organization, reader journey, visual logic, and writing standard while changing content appropriately. |
| Learning reuse | 10 | Shows which learned points shaped the output and where they appear, or records skip reasons for relevant unused points. |
| Core narrative | 20 | The main story remains stable from title through diagrams and section conclusions. |
| Progressive split | 15 | Long material is split into overview and follow-up pages, or the single-page choice is justified. |
| Reader path | 15 | The reader knows who the material is for, what decision it supports, what to read first, and where to go next. |
| Visual information design | 15 | Each diagram carries structure, sequence, contrast, or decision logic that prose alone cannot scan quickly. |
| Report voice | 5 | Language is formal, concise, reader-facing, and free of chat residue. |
| Evidence boundary | 5 | Source/reference/local truth boundaries are explicit without overwhelming the reader. |

## Thresholds

| Score | Meaning | Action |
|---:|---|---|
| 90-100 | Strong | May proceed to review/sync after final verification. |
| 80-89 | Acceptable | May proceed, but record residual risks. |
| 70-79 | Draft only | Do not sync/publish; revise first. |
| Below 70 | Failed | Re-plan structure before rewriting. |

Hard-gate failure overrides the numeric score.
