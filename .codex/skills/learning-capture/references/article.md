# Article Module

Use this module for articles, blogs, papers, WeChat posts, newsletters, and
article collections after `learning-capture` has classified the request as
learning material.

## Runtime Boundary

`learning-capture` is the only runtime entry. This module does not delegate to
an `article-learning-capture` skill and must not recreate a second trigger
surface.

## Required Gates

- Preserve original URL, title, publisher or author when available, publication
  date when available, and access date.
- Classify source before scoring: primary source, secondary interpretation,
  structure reference, or low-relevance/general-interest.
- Preserve source grounding before analysis: extracted markdown when permitted,
  source map with bounded excerpts, or retrieval-failure note.
- Score before deep reading.
- Use the article scorecard threshold: 75+ deep-read, 60-74 brief candidate,
  below 60 skip reason.
- Mark retrospective scoring explicitly; it is not score-first admission
  evidence.
- Respect copyright boundaries: no full verbatim copyrighted article text and no
  full verbatim translation.
- Separate article comprehension from local transfer extraction.
- Distinguish source domain/topic from reusable output capability type when
  recording transferable learning.
- Write durable internal wiki learning output in Chinese by default, unless the
  user or target artifact requires English.

## References

- SOP: `article-sop.md`
- Scorecard: `article-scorecard.md`
- Wiki template: `article-wiki-template.md`
- Pressure scenarios: `article-pressure-scenarios.md`
