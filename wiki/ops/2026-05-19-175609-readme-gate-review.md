---
layer: ops
domain: wiki
ops_area: report-quality
canonical_object: llm-wiki-readme-quality-gate
artifact_type: gate-review
status: generated
---

# README Gate Review

## Reader Intent Contract

- Reader: first-time repository visitor and future Agent operator.
- Reader job: understand what LLM-WIKI is, how AI co-builds the wiki, which
  skills matter, and where learning / medical / governance loops live.
- Main line: LLM-WIKI is a Karpathy-style context engineering system for
  human-AI wiki co-building.
- Non-goals: script inventory as the primary story; Python-led positioning;
  generic Markdown wiki positioning; installer-style README.
- User-owned judgment: governance belongs after architecture; then gates; then
  specialized skills; then concrete cases.
- User-owned correction: the example must use the real Li Xiang / Luo Yonghao
  reading-board evidence chain, not a generic WeChat-to-H5 flow.
- User-owned correction: featured skills must be presented as operating loops,
  not as a flat tool list.
- User-owned correction: governance gates should be table-shaped, and README
  must state the environment requirements an AI needs before operating.
- User-owned correction: README must separately explain frontmatter and MOC
  maintenance as part of the Medical Agent's value, not only mention medical
  stages.

## Reference / Drift Correction

- The earlier README drifted into command lists and health status.
- The corrected shape centers:
  - architecture first;
  - governance design and gates second;
  - environment requirements after governance gates;
  - specialized skill loops third;
  - Medical Agent frontmatter / graph / MOC maintenance as its own value
    section;
  - Li Xiang / Luo Yonghao interview-to-H5 example as evidence-backed routing;
  - boundaries and entry points.

## Gate Checks

- Public artifact: yes, `README.md` and `README.en.md`.
- Bilingual requirement: yes.
- Reference-shaped output: yes, but adapted to this repo's own architecture.
- Learning use map: `learning-capture`, repo/README module,
  `weixin-reader`, `public-report-quality-gate`,
  `interview-deep-reading-board`.
- Judgment ownership: user corrected the framing; README now follows that
  correction.
- Python boundary: scripts are described as tool-layer batch processors, not
  the primary operating model.
- Medical-agent boundary: AI interprets case files; humans confirm key
  decisions; tools execute approved actions and leave recovery evidence.
- Frontmatter / MOC boundary: low-risk page frontmatter repair requires
  confirmed treatment; taxonomy, relation, MOC, and structural changes route to
  surgery or OpenSpec and are not written by status or preview output.
- Example boundary: the Li Xiang / Luo Yonghao case is a captured
  output-shape example with H5, `data.js`, source note, process record, and
  process snapshots; it is not a generic claim that every article becomes H5.
- Featured skills boundary: Skills are operating protocols for intake,
  retrieval, medical maintenance, reader-facing output, and governance
  promotion; they are not command wrappers.
- Environment boundary: Python and OpenSpec are named as runtime requirements
  for verification and governance; Python remains a tool layer, not the
  decision layer.
- Verification to run: read back both README files, check referenced paths,
  run frontmatter checker, run existing tests, inspect git status.

## Proof Boundary

This review verifies README intent and structure. It does not claim the example
is a publish-ready report; it verifies that the repository contains the cited
H5, data, source, process, and snapshot evidence.
