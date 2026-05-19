# Design: consolidate learning and explore gates

## Approach

Adopt the already-proven shape from `account-meeting-lore` selectively:
`learning-capture` owns external-source learning, while repo/README-specific
behavior is a module under its references. Do not copy source-repository
business rules, trace conventions, or report-portfolio defaults.

This change treats behavior assets as runtime contracts:

- `AGENTS.md` owns repo-local routing and stop gates.
- `.codex/skills/learning-capture/` owns source-learning routing.
- `.codex/skills/openspec-explore/` owns exploration stance.
- OpenSpec evaluation owns proof boundary and behavior replay.

## Runtime Shape

Repo/README learning:

```text
user source + learning intent
        |
        v
learning-capture
        |
        v
references/repo-readme.md
        |
        v
admission -> score -> deep/brief/skip -> reuse/adapt/reject boundary
```

`readme-learning-capture` is removed from the active skill surface. Historical
mentions remain historical evidence only.

Explore mode:

```text
explicit $openspec-explore
        |
        v
read-only exploration stance
        |
        +--> may read and compare
        +--> may draft OpenSpec artifacts only when explicitly requested
        +--> must not edit AGENTS, skills, wiki, scripts, or implementation
             until the user exits explore or enters a proposal/apply gate
```

Missing skill gate:

```text
route table names local skill path
        |
        v
file exists? -- no --> stop and report missing route
        |
       yes
        |
        v
load skill and continue through parent gates
```

## Behavior Evaluation

Add static replay tests because this repository does not yet have a full
behavior-asset checker script:

- active README learning surface is retired;
- repo/README module is self-contained under `learning-capture`;
- AGENTS active route table does not mention `readme-learning-capture`;
- AGENTS missing-local-skill stop gate exists;
- `openspec-explore` defines read-only, non-implementation, and exit
  boundaries.

## Boundaries

- `weixin-reader` remains a source reader, not a learning parent gate.
- `learning-capture` remains the parent gate for external learning.
- `openspec-explore` does not grant implementation permission.
- Missing historical skill names do not become active route surfaces.
