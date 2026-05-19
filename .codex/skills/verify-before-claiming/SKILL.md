---
name: verify-before-claiming
description: Use when the agent is about to say something is fixed, complete, synced, or clean without a fresh command, test, or state check.
---

# Verify Before Claiming

## Overview

Do not claim completion without a fresh check. Conclusions come from current evidence, not memory.

## Use When

- You are about to say “fixed”, “committed”, “synced”, or “clean”
- Work resumes after interruption and state may have changed
- The conclusion depends on tests, commands, or external sync status

## Rules

- Check first, then conclude.
- For git claims, verify current `status` and latest `log`.
- For behavior changes, prefer test or command evidence.
- If verification is incomplete, say exactly what was not checked.

## Anti-Patterns

- Saying “already committed” from memory
- Assuming code is correct right after editing
- Claiming an external sync succeeded without rechecking

## Self-Check

`Is this claim coming from a fresh check, or from my impression?`
