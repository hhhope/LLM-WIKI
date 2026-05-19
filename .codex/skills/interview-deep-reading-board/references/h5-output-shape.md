# H5 Output Shape

Use this reference when an interview deep-reading board becomes an HTML/H5 or
shareable visual report.

## Source Model

Use ordered reading windows as the durable source model. Each window should
carry enough context for a reader to understand why it exists without reading
the full original transcript.

Recommended fields:

| Field | Purpose |
|---|---|
| `id` | Stable window id for links and UI state |
| `sequence` | Source-order position |
| `speakerContext` | Speaker or speaker-role context |
| `title` | Window-level claim or tension |
| `summary` | Paraphrase of the local passage |
| `keywords` | Terms that should resolve back to this window |
| `temperature` | Horizontal axis position or band |
| `evidence` | Short snippet, paraphrase, or source-position note |
| `beforeAfter` | Adjacent-window continuity |
| `question` | Deep-reading question or unresolved tension |

For long interviews, enough windows are required to preserve source-order
coverage. The number is proportional to source length; do not inflate short
interviews only to hit a numeric quota.

## Interaction Shape

- The timeline preserves interview sequence and lets the reader jump by source
  order.
- The temperature axis is a horizontal reading control. Dragging it should
  select or filter windows and evidence by conceptual temperature, such as
  system/efficiency/architecture toward people/organization/judgment/vision.
- The word cloud is an index. Selecting a keyword should reveal the windows and
  evidence where the keyword matters.
- The evidence panel should update with the selected window or keyword.
- The default focus should be a user-highlighted, previously missed, or
  highest-risk passage when repairing an output that drifted.

## Li Xiang Reference Shape

Validated reference:

- H5: `wiki/reports/lixiang-luoyonghao-ai-agent-reading-board.html`
- Data: `wiki/reports/lixiang-luoyonghao-ai-agent-reading-board-data.js`
- Source note:
  `wiki/sources/agentic-product-engineering-collaboration-lixiang-luoyonghao-ai-agent-reading-2026-05-18.md`

Counterexample:

- `wiki/reports/lixiang-luoyonghao-ai-agent-wordcloud.html`

The counterexample is useful because it shows the failure mode: a word cloud can
look like coverage while compressing timeline, speaker-turn logic, and named
passages.

The validated H5 repaired the shape by using many ordered windows and by
defaulting to the user-highlighted Coworker / Feishu / stable Agent / subagent /
MCP passage.

## Copyright Boundary

Do not store the full copyrighted interview transcript in a skill reference or
wiki example. Preserve reusable shape through:

- source URL and source note;
- source-order window ids;
- paraphrase;
- short evidence snippets;
- source-position hints;
- explicit notes about what was not formalized.

## Review Checklist

- Does every visible keyword resolve to concrete windows or evidence?
- Can a reader follow the interview sequence without guessing the original
  order?
- Does the temperature axis change what evidence is visible?
- Are user-highlighted passages explicit, not hidden under generic themes?
- Is the old word-cloud-only shape clearly treated as a counterexample?
- Are public-report review, publish, and Feishu sync boundaries still owned by
  `public-report-quality-gate`?
