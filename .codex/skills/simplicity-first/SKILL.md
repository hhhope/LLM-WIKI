---
name: simplicity-first
description: Use when a solution is growing speculative abstractions, extra configuration, or future-proofing that the current task does not require.
---

# Simplicity First

## Overview

Build the smallest verifiable solution first. Do not prepay complexity for imaginary future needs.

## Use When

- The solution is growing around hypothetical future reuse
- A one-off need is turning into multiple abstraction layers
- A small change is drifting toward framework building

## Rules

- Implement only the capability required by the current task.
- Do not generalize a one-time path before repetition exists.
- No repeated need, no shared abstraction yet.
- If 200 lines can become 50, first suspect unnecessary complexity.

## Anti-Patterns

- Adding strategy, manager, or config layers for a single function
- Treating “flexibility” as a default virtue
- Justifying present complexity with future guesses

## Self-Check

`Is this solving today's task, or fantasizing about tomorrow's?`
