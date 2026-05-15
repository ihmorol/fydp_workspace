---
name: domain
description: Domain documentation layout and consumer rules for agent skills
type: reference
---

# Domain Documentation

## Layout

**Single-context** — this repository has one research domain context.

| File / Dir | Role |
|---|---|
| `CONTEXT.md` | Primary domain context. Read this first for domain vocabulary, research questions, methodology, and chapter status. |
| `docs/adr/` | Architecture Decision Records. Read these to understand past design choices (solver settings, data splits, ANN training configuration). |
| `docs/research/` | Supporting research guides, roadmaps, and equation authority documents. |
| `paper/fydp.bib` | Authoritative bibliography. All in-text citations must correspond to entries here. |
| `references/` | PDF copies of cited papers. Truth-check citations against these files. |

## Consumer Rules

### For `improve-codebase-architecture`, `diagnose`, `tdd` skills

1. Read `CONTEXT.md` before making any code suggestions
2. Check `docs/adr/` for existing decisions before proposing alternatives
3. The Lorenz-1960 equations in `CONTEXT.md` are the equation authority — do not derive or modify them without supervisor sign-off

### For `academic-paper`, `ars-*` skills

1. Read `CONTEXT.md` for the research question, methodology, and chapter status
2. Verify every citation against `paper/fydp.bib` and the files in `references/`
3. Use the UIU FYDP LaTeX template in `paper/` — do not reformat the document structure
4. The 5 research gaps in `CONTEXT.md § Research Gaps Addressed` define the paper's contribution — do not stray from them
5. **Chapter 3 decisions are fully locked** — read `CONTEXT.md § Chapter 3 Design Decisions` before writing any part of Chapter 3. Do not invent or change any experimental parameter, requirement, or design choice not recorded there.
6. Chapter 3 section 3.1.4 (UI Design) is explicitly omitted — this project has no user interface.
7. ANN input = scalar t only. ANN output = (x(t), y(t), z(t)). x, y, z are state variable predictions, not inputs. Do not confuse.
8. Total experiments = 69 (60 Phase 1 + 9 Phase 2). Do not cite 60 as the total.
9. Normalization: z-score on output targets during training; all reported metrics are in original physical units.

### For `triage`, `to-issues`, `to-prd` skills

1. Issues live at `github.com/ihmorol/fydp_workspace/issues` — see `docs/agents/issue-tracker.md`
2. Use triage labels from `docs/agents/triage-labels.md`

## ADR Naming Convention

Place ADRs in `docs/adr/` with the naming pattern:

```
docs/adr/YYYY-MM-DD-short-description.md
```

Example: `docs/adr/2026-05-15-rk4-step-size-rationale.md`

Each ADR covers: **Context** → **Decision** → **Consequences**.
