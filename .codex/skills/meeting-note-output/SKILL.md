---
name: meeting-note-output
description: Use when the user asks to organize meeting notes, produce a meeting-minutes document, sync Feishu meeting notes, or provides notes, transcripts, or speech-to-text material that requires a fixed minutes format rather than a loose summary.
---

# Meeting Note Output

## Overview

Turn meeting material into a review-ready minutes document. The main note is the primary output; transcripts are supporting evidence.

## When to Use

- The user asks to “整理会议纪要”, “输出会议纪要文档”, or sync a Feishu note.
- The input is a meeting note, transcript, or speech-to-text source.
- The output must be a fixed minutes document, not a loose summary.

Do not use this skill for ordinary project weekly reports or generic document archiving without a meeting context.

## Rules

- Default to a review version first.
- Review versions must include `待确认` and `需你澄清`.
- Do not publish or sync a final Feishu note while unresolved confirmation items remain open.
- Use the repo's fixed meeting-note structure; keep the main note and Feishu review copy aligned.
- Keep transcripts as supporting evidence. Do not dump raw transcript text into the main minutes body.
- If the meeting contains option conflicts, make the final option, rejected option, and rejection reason explicit.
- For format details, use [meeting-note-format-example.md](references/meeting-note-format-example.md) and the repo boundary in [AGENTS.md](../../../AGENTS.md).

## Common Mistakes

- Writing only a short summary instead of minutes prose
- Treating wiki helper blocks such as `Source Metadata` as Feishu body content
- Omitting rejected options when the discussion clearly had alternatives
- Leaving action items unstructured
- Updating the repo note but skipping the required Feishu review copy
- Sending a final note without `待确认` or `需你澄清`
