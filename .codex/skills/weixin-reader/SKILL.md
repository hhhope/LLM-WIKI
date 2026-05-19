---
name: weixin-reader
description: Use when the user provides an mp.weixin.qq.com article link and wants to read, analyze, summarize, or extract the article content
---

# Weixin Reader

## Overview

Fetch a Weixin article body and return it as Markdown for downstream analysis.

## When to Use

- The user provides an `mp.weixin.qq.com` link.
- The user wants to analyze, summarize, or extract the actual article body.
- The workflow needs Markdown content before further processing.

Do not use this skill for generic web scraping or when metadata alone is enough.

## Command

```bash
python3 .codex/skills/weixin-reader/scripts/fetch_weixin.py "<微信文章URL>"
```

## Output

The script returns Markdown with `title`, `author`, `date`, `url`, and `content`.

## Rules

- Treat environment verification or anti-bot blocks as fetch failure, not partial success.
- If `#js_content` is missing, report the fetch as failed.
- After fetch succeeds, continue with the user's requested analysis rather than stopping at raw Markdown.
