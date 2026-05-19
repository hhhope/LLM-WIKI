## MODIFIED Requirements

### Requirement: Learning capture SHALL own repo/README source learning

Learning capture SHALL route repo/README source learning through the
`learning-capture` skill and its repo/README module, not through a separate
active `readme-learning-capture` skill surface.

#### Scenario: Repo-shaped source is used for learning

- **WHEN** the user provides a GitHub/GitLab repository, README, repo-level
  docs, or project structure as learning, reference, or adaptation material
- **THEN** the agent SHALL route through `.codex/skills/learning-capture/SKILL.md`
- **AND** it SHALL use `references/repo-readme.md` for repo/README-specific
  admission, scoring, and adaptation boundaries
- **AND** it SHALL NOT load a separate active `readme-learning-capture` skill
  surface

#### Scenario: Historical README learning evidence mentions the old skill name

- **WHEN** archived notes, old OpenSpec changes, prior chat summaries, or
  historical wiki records mention `readme-learning-capture`
- **THEN** the mention SHALL be treated as historical evidence only
- **AND** it SHALL NOT become an active runtime route unless the repo-local
  skill file exists again through a new approved change
