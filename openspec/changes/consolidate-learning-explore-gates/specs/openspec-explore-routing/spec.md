## ADDED Requirements

### Requirement: Explicit explore trigger SHALL stay read-only until exited

When the user explicitly triggers `$openspec-explore`, the repository SHALL
enter a read-only exploration stance before any implementation or behavior-asset
write.

#### Scenario: User explicitly triggers explore

- **WHEN** the user names `$openspec-explore`
- **THEN** the agent SHALL enter a read-only exploration stance
- **AND** it SHALL NOT edit `AGENTS.md`, `.codex/skills/*`, `wiki/*`,
  `scripts/*`, or implementation files during explore
- **AND** it SHALL require the user to exit explore or enter an OpenSpec
  proposal/apply gate before ordinary repository edits

#### Scenario: Explore produces a likely direction

- **WHEN** explore mode produces a likely rule, route, skill, or wiki change
- **THEN** the result SHALL remain a candidate conclusion
- **AND** it SHALL NOT be treated as write approval or completion evidence

### Requirement: Missing local skill routes SHALL stop

The repository SHALL stop rather than continue when a selected repo-local skill
route names a missing local skill file.

#### Scenario: Route table points to a missing local skill

- **WHEN** the selected route depends on a repo-local skill path that does not
  exist
- **THEN** the agent SHALL stop and report the missing local skill
- **AND** it SHALL NOT continue as if the skill loaded
- **AND** it SHALL NOT substitute a historical skill name, global skill, or
  prior chat memory as the active repo-local route
