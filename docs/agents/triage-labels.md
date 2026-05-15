---
name: triage-labels
description: Label vocabulary for the five canonical triage states
type: reference
---

# Triage Labels

## Canonical Label Mapping

| Role | Label string | Meaning |
|---|---|---|
| needs-triage | `needs-triage` | Maintainer needs to evaluate this issue |
| needs-info | `needs-info` | Waiting on reporter (e.g., supervisor clarification) |
| ready-for-agent | `ready-for-agent` | Fully specified; an AFK agent can pick it up |
| ready-for-human | `ready-for-human` | Needs manual implementation |
| wontfix | `wontfix` | Will not be actioned |

All labels use their default names. No custom overrides.

## Creating Labels on GitHub

If the labels don't exist yet on the repo, create them with:

```bash
gh label create "needs-triage"     --color "e4e669" --description "Needs evaluation"
gh label create "needs-info"       --color "d93f0b" --description "Waiting on reporter"
gh label create "ready-for-agent"  --color "0075ca" --description "Agent-ready: fully specified"
gh label create "ready-for-human"  --color "008672" --description "Needs human implementation"
gh label create "wontfix"          --color "ffffff" --description "Will not be actioned"
```

## State Transitions

```
[new issue] -> needs-triage
    needs-triage -> needs-info         (supervisor clarification required)
    needs-triage -> ready-for-agent    (fully specified, unambiguous)
    needs-triage -> ready-for-human    (needs manual work)
    needs-triage -> wontfix            (out of scope)
    needs-info   -> ready-for-agent    (clarification received, now fully specified)
    needs-info   -> ready-for-human    (clarification received, needs human)
    needs-info   -> wontfix            (resolved as out of scope)
```
