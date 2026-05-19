# Article Learning SOP

## 1. Source Intake

Record:

- original URL
- title
- author or publisher, if available
- publication date, if available
- access date
- source type: article / blog / paper / WeChat / article collection
- retrieval method: browser, `weixin-reader`, pasted text, screenshot, local PDF
- source class: primary source / secondary interpretation / structure
  reference / low-relevance/general-interest
- source artifact type: extracted markdown / source map / bounded excerpts /
  retrieval failure note

For `mp.weixin.qq.com` links, try `weixin-reader` when body text is needed. If it
fails, ask for pasted text or screenshots.

Preserve source grounding before scoring or deep reading:

- Use an extracted markdown snapshot when the source is available and copyright
  boundaries allow local storage.
- Use a source map with section headings and bounded excerpts when the full
  source cannot be stored.
- Use a retrieval-failure note when the original cannot be accessed; ask for
  pasted text or screenshots before interpreting the article.
- Do not treat another model's summary as the source artifact.

## 2. Admission and Score

Apply `article-scorecard.md` before deep reading.

- 75 or higher: deep-read and write durable wiki learning notes.
- 60-74: brief-read and keep a candidate note.
- Below 60: record source and skip reason.

Do not deep-read low-scoring material by default. If a score is created after
deep reading or after conclusions were drafted, mark it `retrospective`; it is
useful for audit but does not count as score-first admission evidence.

## 3. Reading Draft

The reading draft is for understanding the article, not extracting rules.

Capture:

- problem the article is solving
- method, architecture, or process
- evidence type: experiment, benchmark, case study, product experience, logs,
  research result, opinion
- assumptions and context
- what the article does not prove
- structured translation notes or paraphrased reading notes

Copyright boundary:

- short excerpts only when needed
- prefer paraphrase
- no full verbatim article text
- no full verbatim translation
- no full verbatim translation draft as the durable wiki output

## 4. Transferable Learning

Only extract points that might affect this repo, agent workflow, output methods,
or behavior-asset candidates.

For each point, record:

- source
- claim
- evidence
- local usefulness
- adoption boundary
- status: accepted / candidate / rejected

These are metadata for transfer candidates. They are not the article summary.

When an article learning point is expected to shape a report, H5, Feishu draft,
skill, or OpenSpec proposal, record the reusable capability type:

- `content`
- `structure`
- `visual`
- `evidence`
- `boundary`

Also record the intended output use or skip reason when it is already known.
This is process evidence for the downstream output gate, not a public citation
requirement.

If the article describes a GitHub/GitLab project and the user asks whether the
project structure or README can be reused, read the repo/README and then route
that second step through `repo-readme.md`.

## 5. Promotion Boundary

Default routing:

- `wiki/ops`: workflow, governance, operating behavior, agent practice
- `wiki/examples`: output-shape, writing style, visual grammar, reusable format
- `wiki/team-lore-candidates.md`: only after a project-local record exists and
  the learning appears cross-project reusable
- OpenSpec change: when the learning becomes a scoped repository behavior or
  asset change

Keep `intake` as a directory and topic entry. Put deep notes in a
`reading-notes` page or equivalent section.

Before promoting any takeaway into `AGENTS.md`, `rules/`, `skills/`, specs, or
archive-ready claims, require one accepted evidence shape:

- external-document excerpt with URL and exact section or line reference
- local RED/GREEN demo or fixture with command/manual replay
- git-like project comparison with repository, commit or path, and observable
  structure or behavior difference

Unsupported learning remains a candidate observation.

## 6. Output Language

Durable internal wiki learning notes default to Chinese. Use English only when
the user asks for English, the target artifact is English-first, or the audience
requires English.
