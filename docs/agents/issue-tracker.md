---
name: issue-tracker
description: Where issues and tasks are tracked for this research repository
type: reference
---

# Issue Tracker: GitHub Issues

Issues for this project live in **GitHub Issues** at:

```
https://github.com/ihmorol/fydp_workspace/issues
```

## CLI Tool

Use the `gh` CLI (GitHub CLI) for all issue operations:

```bash
# List open issues
gh issue list

# Create a new issue
gh issue create --title "..." --body "..." --label "..."

# View an issue
gh issue view <number>

# Close an issue
gh issue close <number>
```

## Issue Types for This Research Project

When creating issues, use these title prefixes to make triage easy:

| Prefix | Use for |
|---|---|
| `[paper]` | Chapter writing, revisions, citation work |
| `[code]` | Implementation bugs, notebook failures, solver issues |
| `[exp]` | New experiments to run, architecture variants to test |
| `[data]` | Dataset generation, export, or validation |
| `[docs]` | Documentation updates, ADRs, research guides |

## Workflow

1. `needs-triage` — newly created issue, not yet evaluated
2. `needs-info` — waiting for clarification (supervisor feedback, unclear requirements)
3. `ready-for-agent` — fully specified, an AI agent can pick it up without human context
4. `ready-for-human` — needs manual implementation (e.g., running experiments, LaTeX editing)
5. `wontfix` — out of scope or deliberately not addressed

## Notes

- Use GitHub Milestones to group issues by chapter or phase (e.g., "Chapter 3", "ANN Phase")
- Link issues to pull requests via `Closes #N` in the PR description
- Tag supervisor questions as `needs-info` until resolved
