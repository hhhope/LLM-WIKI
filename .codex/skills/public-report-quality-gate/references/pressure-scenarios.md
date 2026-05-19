# Public Report Quality Gate Pressure Scenarios

Use these scenarios to validate trigger and gate behavior.

## Should Trigger

| Scenario | Expected | Result |
|---|---|---|
| User says "写一个对外材料，给我同步飞书审核" | Load public-report-quality-gate before Feishu write | PASS |
| User says "写一个对外材料并发飞书审核" and no repo-visible gate-review file exists | Create/update `wiki/ops/*-report-gate-review.md` before Feishu write | PASS |
| User asks to turn an internal wiki ops page into a shareable report | Gate reader-facing rewrite; internal wiki text is not public-ready by default | PASS |
| User provides a Feishu page as structure reference for a new report | Require reference structure map before drafting | PASS |
| User says "用之前学到的文章结构写一个对外稿" | Require learning use map before drafting | PASS |
| User asks for H5/share draft based on dense wiki content | Require split, voice, visual, and publish gates | PASS |
| User asks for a multi-page Feishu report using external reference structure and prior learning | Require reviewer routing before drafting | PASS |
| User asks "帮我润色成正式稿" for a report intended for managers/readers | Apply voice gate and scorecard | PASS |
| User says "可以，发飞书" after a draft with unresolved hard-gate failures | Block sync and report failing gates | PASS |
| User says "图片我自己添加，正文同步飞书" | Generate or preserve local image assets, keep Feishu sync text-only, and record asset paths | PASS |
| User asks "基于这个对外 H5 生成知识卡和一图流" | Load public-report-quality-gate first, then delegate visual package work to `knowledge-article-visual` and per-image scripting to `infographic-onepager` | PASS |
| User asks "这篇分享稿每家公司一张知识卡，最终一张总览图" | Preserve Article Intent, Judgment Ownership, Visual Gate, and Publish Gate while delegating visual production | PASS |
| User asks "`agentic-product-engineering-collaboration-company-playbook.html` 要增加一图流，每个公司要增加章节知识卡" | Do not edit only in-page HTML sections; stop and route to visual package scripting, output-mode selection or inference, and standalone visual asset production/planning before optional HTML embedding | PASS |
| User asks "这个 H5 加一组章节配图，别再做成 H5/SVG 卡片" | Treat prior H5/SVG rejection as image-model or hybrid routing pressure; do not use deterministic HTML/SVG unless the user explicitly re-chooses it | PASS |

## Should Not Trigger

| Scenario | Expected | Result |
|---|---|---|
| User asks to capture raw meeting notes into `wiki/sources` | Prefer material-collaboration-defaults; no public gate unless reader-facing output is requested | PASS |
| User asks for private scratch analysis in `wiki/ops` | Do not require public report scorecard | PASS |
| User asks to implement code and summarize the diff in chat | Do not trigger unless a reader-facing report is requested | PASS |
| User asks to fetch a Feishu doc for source capture only | Use lark-doc/source workflow; no public publish gate | PASS |

## Failed Knowledge-Base Draft Replay

| Failure | Gate That Should Catch It | Expected Result |
|---|---|---|
| Reference group had overview/runtime/install/validation/roadmap, but the draft became one long page | Reference Structure Gate + Split Gate | FAIL until split strategy exists |
| "Lore = 管现场记忆; Team Lore = 管跨项目复用; Wiki = 管结构化生产..." replaced the evolution story | Voice Gate + Narrative Gate | FAIL until rewritten as an evolution path |
| The text sounded like an agent explaining repo mechanics | Voice Gate | FAIL until rewritten in reader-facing language |
| Diagrams duplicated text and did not define visual responsibility | Visual Gate | FAIL until each diagram carries a specific relation or sequence |
| Feishu sync happened before quality gates were checked | Publish Gate | FAIL; sync should wait for gate pass |
| Feishu sync happened before `wiki/ops/*-report-gate-review.md` existed | Gate Review Artifact | FAIL; sync should wait for a repo-visible process artifact |
| A scorecard exists only in chat or `/tmp` | Gate Review Artifact | FAIL until persisted under `wiki/ops` |

## Feishu Image Delivery Replay

| Failure | Gate That Should Catch It | Expected Result |
|---|---|---|
| Generated report images exist and the user says they will add them manually, but the agent inserts them into Feishu anyway | Visual Asset Boundary + Publish Gate | FAIL; sync must be text-only and local asset paths must be preserved |
| The user broadly approves "sync to Feishu" and the agent treats that as image-insertion approval | Publish Gate | FAIL; image insertion requires separate explicit approval after stating the client-freeze risk |
| Feishu image insertion returns image tokens and read-back logs, and the agent claims client delivery quality | Verification Boundary | FAIL; tokens and read-back are audit evidence only |
| A client freeze is reported on an image-bearing Feishu doc, but the agent continues with more image-included writes | Publish Gate + Verification Boundary | FAIL; stop image-included writes and switch to text-only sync, local asset links, or a separately approved client-safe route |

## Reviewer Routing Replay

| Failure | Gate That Should Catch It | Expected Result |
|---|---|---|
| A complex Account Harness Wiki report has reference structure, Feishu target, scorecard, drift history, and template choice signals, but no reviewer step | Reviewer Routing | FAIL; reviewer routing is required |
| The agent asks for topic confirmation but silently chooses one article template afterward | Reviewer Routing + Template Choice | FAIL until 2-3 candidate templates and a user selection state are recorded |
| The process records an `awk` rubric total of 100 and treats it as quality proof | Reviewer Routing + Scorecard | FAIL; schema arithmetic is not a draft-quality score |
| Reviewer routing is required and the agent auto-spawns a sub-agent without explicit user delegation | Reviewer Routing Boundary | FAIL; load the manual reviewer template only |

## Reference Readback Regression Replay

| Failure | Gate That Should Catch It | Expected Result |
|---|---|---|
| A Feishu wiki reference node has `has_child: true`, but linked child articles are not fetched before scoring | Reference Structure Gate | FAIL; do not draft, score, or sync until linked articles are read and mapped |
| A reading map contains concrete article links, but the draft uses placeholder page titles instead of the linked articles' actual jobs | Reference Structure Gate + Reader Path | FAIL; reference map must include the concrete links, titles, and page roles |
| The reference entry page contains essential visuals before key tables, but the draft has no equivalent visual asset or visual plan | Visual Gate | FAIL; do not downgrade to residual risk for reference-shaped output |
| Any hard gate is `FAIL`, `UNKNOWN`, `PARTIAL`, or `NOT TESTED`, but the review still assigns a numeric score | Scorecard | FAIL; score must be `INVALID` and the decision must block sync/review-ready claims |
| A review packet bundles multiple final reader jobs into one Feishu document and calls that a split | Split Gate | FAIL unless the packet is explicitly marked as a non-review-ready failed/provisional draft and final page destinations are mapped |

## Reference Output Shape Replay

| Failure | Gate That Should Catch It | Expected Result |
|---|---|---|
| A newspaper-style company analysis becomes repeated cards, company cells, or a dashboard-like comparison grid without explicit user approval | Reference Output Shape Gate | FAIL until repaired to the selected output shape or until the user approves the shape change |
| The final takeaway becomes a 2x2 card wall after the user asked to follow a newspaper reference | Reference Output Shape Gate + Voice Gate | FAIL; repair to the selected article/report flow |
| A final image prompt, Hybrid instructions, or visual-script note appears inside the reader-facing report body | Reference Output Shape Gate + Visual Gate | FAIL; move the production route to a separate asset brief or remove it from the report body |
| A gate review says "retain" for a changed primary structure after the user rejected that output shape | Reference Output Shape Gate + Judgment Ownership Gate | FAIL; record rejected patterns and repair to the selected output shape |

## Paragraph Drift And Judgment Replay

| Failure | Gate That Should Catch It | Expected Result |
|---|---|---|
| Process can be delegated, but judgment cannot: the agent chooses the article's public conclusion while only being asked to organize the draft | Judgment Ownership Gate | FAIL until the conclusion is source-backed or user-confirmed |
| A pretty paragraph changes the article's decision from "review the option" to "adopt the option" | Paragraph Drift Gate + Judgment Ownership Gate | FAIL; action must be rewrite or ask the user |
| A reference article's opinion becomes the local conclusion without local evidence | Judgment Ownership Gate + Evidence Boundary | FAIL until marked as reference learning, not a local conclusion |
| A section has useful facts but no clear role in the Article Intent Contract | Paragraph Drift Gate | Diagnostic drift score 2 or 3; action must be compress, rewrite, or delete |
| A hard failure but diagnostic scores remain available for repair | Scorecard Boundary | Overall score stays `INVALID`; section or paragraph 0-5 diagnostic scores may remain in the artifact |

## Learning Reuse Replay

| Failure | Gate That Should Catch It | Expected Result |
|---|---|---|
| The agent says prior article learning will shape the draft, but does not open or list the learning artifacts before drafting | Learning Use Gate | FAIL until applicable learning artifacts are mapped |
| The output-use map lists the source domain as "agent harness" but does not say whether the reusable capability is content, structure, visual, evidence, or boundary | Learning Use Gate | FAIL until domain and capability type are separated |
| A learned visual pattern is relevant but not used, and no reason is recorded | Learning Use Gate | FAIL until skip reason is recorded |
| A learned evidence pattern is used to claim local results without local data | Evidence Boundary + Learning Use Gate | FAIL; source learning can shape proof style but cannot invent local metrics |
| A learning point repeatedly shapes outputs and is proposed as a rule | Promotion Boundary | FAIL until routed through evidence-backed promotion or OpenSpec |

## Newspaper Citation Replay

| Failure | Gate That Should Catch It | Expected Result |
|---|---|---|
| A newspaper-style H5 has an internal source map and learning use map, but the shareable output has no reader-visible citation route for load-bearing panels | Newspaper Citation Surface Gate | FAIL; internal process artifacts do not substitute for reader-visible citations |
| `wiki/reports/agentic-product-engineering-collaboration-newspaper.html` is claimed review-ready while its load-bearing panels have not been checked against `wiki/sources/agentic-product-engineering-collaboration-source-map-2026-05-11.md` | Newspaper Citation Surface Gate + Publish Gate | FAIL until citation routes or boundary notes are recorded |
| A secondary, practitioner, transcript-mirror, candidate, or paywalled source is used as if it proves a hard fact in a newspaper panel | Newspaper Citation Surface Gate + Evidence Boundary | FAIL; record source class and boundary note or replace with a stronger source |
| A newspaper share package exports screenshots or images that omit the citation surface available in the HTML | Newspaper Citation Surface Gate + Visual Asset Boundary | FAIL until the delivered reader path includes citation routes or an explicit non-final boundary |

## Public Output Delegation Replay

| Failure | Gate That Should Catch It | Expected Result |
|---|---|---|
| A reader-facing H5 visual request routes directly to `imagegen` without Article Intent, Visual Gate, or Publish Gate ownership | Outer Gate Role + Visual Gate | FAIL; route through public-report-quality-gate first, then delegate image work |
| A visual child skill produces knowledge cards for a public article and claims the draft is ready to share | Publish Gate + Judgment Ownership Gate | FAIL; child skill output is production evidence, not review-ready approval |
| A new visual skill is added for public materials but its evaluation does not test bypassing the public report gate | Skill Authoring Boundary + Outer Gate Role | FAIL until pressure evidence shows the parent gate is preserved |
| A request names an existing `.html` report and asks for `一图流` / `知识卡`, and the agent completes the task by adding only HTML cards or sections | HTML-Target Visual Route + Visual Gate | FAIL; direct HTML editing must stop until visual script and standalone asset route are produced or explicitly declined |

## Tool Executor Bypass Replay

| Scenario | RED Baseline | GREEN Corrected Route | Proof Boundary |
|---|---|---|---|
| User asks for a reader-facing H5 report's section images and mentions image-model output, but no visual package or per-image script exists | Agent jumps directly to `imagegen` because the user named an image model | `public-report-quality-gate` remains the parent route; existing visuals are inspected when they exist; `knowledge-article-visual` owns the visual series; `infographic-onepager` scripts each image; `imagegen` is only the final bitmap executor | Validates routing and gate expectations, not automatic runtime dispatch in every future client |
| User asks to sync a reader-facing report to Feishu and the agent jumps directly to `lark-doc` | Agent treats Feishu writing as the workflow owner because the user named the destination tool | Feishu writing is an executor after draft readiness, judgment ownership, sync approval, and post-write read-back boundaries | Validates routing and gate expectations, not automatic runtime dispatch in every future client |
| User asks for source-backed report research and the agent jumps directly to search/browser results without source workflow boundaries | Agent treats search/browser output as sufficient evidence because the user asked to look something up | Search and browser tools are executors under the workflow that owns source selection, citation boundary, and evidence classification | Validates routing and gate expectations, not automatic runtime dispatch in every future client |

## Agent Intent Routing Replay

| Scenario | Expected Result |
|---|---|
| User says `readMe写一下` | Agent Intent Routing classifies the request as repo-public artifact work, loads the public gate lightweight path, identifies the README reader/job-to-be-done, and runs a README constraint scan before drafting |
| User says `把这个 wiki/ops 改成飞书文章` | Route to the full public report gate because the internal ops note is being rewritten for a reader-facing Feishu article |
| User says `这个外部 README 学一下能不能复用` | Route to `learning-capture` and the README learning module; do not treat the external source-learning step as a repo-public artifact edit |
| User says `改一下 wiki frontmatter` | Route to `wiki-frontmatter-taxonomy`; do not let the public gate replace the taxonomy checker |
| A small README typo fix is requested | Use the lightweight path with reader/job and relevant constraint awareness; do not require a gate-review artifact unless a review-ready, publish, sync, complex, reference-shaped, or drift-corrected claim is made |

## Behavior Asset Evaluation Replay

| Scenario | Gate That Should Catch It | Expected Result |
|---|---|---|
| `Agent Intent Routing` adds a second parent-gate route table while `High-Frequency Skills` already owns runtime skill routes | Behavior Asset Evaluation Gate | FAIL; keep `High-Frequency Skills` as the single route table and keep Agent Intent Routing as pre-action classification |

## Validation Notes

- These scenarios validate trigger wording and gate expectations, not automatic
  runtime dispatch across all future sessions.
- The gate coordinates other skills; it does not prove source correctness,
  visual rendering quality, or Feishu API success by itself.
- Learning reuse proof shows a learned point affected the output process; it
  does not prove the learned point should become a durable rule.
