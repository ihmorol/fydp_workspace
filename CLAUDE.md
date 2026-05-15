# Claude Agent Instructions — FYDP Research Repository

## Project Summary

This is a final-year design project (FYDP) research repository at UIU. The work investigates which plain feedforward ANN architecture best approximates the Lorenz-1960 ODE system, trained on RK4/SciPy reference data. See `CONTEXT.md` for the full research context, domain vocabulary, and chapter status.

---

## Research Guardrails

These rules govern all AI-assisted work on this project. They are drawn from the ARS (Academic Research Skills) framework installed in this repo.

### Equation Authority

- The **only** authoritative source for the Lorenz-1960 equations is `paper3.pdf` **Section 4.2** (not Appendix A.2, which is inconsistent).
- The reduced form with k=2, l=1 is: `dx/dt = -0.1yz`, `dy/dt = 1.6xz`, `dz/dt = -0.75xy`.
- Any change to the equations, initial conditions, or time interval **must** be documented in `docs/adr/` before implementation.

### Baseline is Locked

- `src/baseline/lorenz1960_baseline.py` is the source of truth for all numerical computation.
- Do not modify the RK4 or SciPy solver parameters without creating an ADR first.
- Do not add ANN code to the baseline module — that belongs in `src/models/`.

### Citation Rules (IRON RULE from ARS)

- Every claim in the paper must have a citation or be supported by the project's own experimental data.
- Never fabricate or invent references. Every citation must be verifiable via DOI or the files in `references/`.
- The bibliography lives in `paper/fydp.bib`. Citation numbers must match in-text `\cite{}` calls and the bib file.
- Run `/ars-citation-check` before finalizing any chapter.

### Writing Quality Rules (from ARS anti-patterns)

- Do not use AI-typical overused phrases: "delve into", "crucial", "it is important to note", "in the realm of".
- Do not use more than 2 em dashes per page.
- Do not open paragraphs with throat-clearing: "In this section, we will discuss..."
- Vary paragraph lengths naturally (2–8 sentences). Uniform 4-sentence paragraphs signal AI.
- Every criticism must be substantiated; do not add unrequested content during revision.

### Scope Discipline

- This study uses **plain feedforward ANNs only** — no PINNs, no operator learning, no DeepONet.
- We compare results against PINNs from the literature (Matthews & Bihlo [3]); we do not implement PINNs.
- Architecture search is strictly: depth (1–4 hidden layers) × width (20/50/100 neurons) × activation (tanh/ReLU/sigmoid/GELU/Swish).
- Do not introduce new research questions without supervisor approval.

### Data Discipline

- Generated datasets (`.csv`, `.npz`) go in `data/` — this directory is gitignored.
- Results (figures, plots, metrics tables) go in `results/` — this directory IS tracked.
- Use `src/baseline/lorenz1960_baseline.py` to regenerate data; do not commit raw data files.

### ARS Skills Available

Use these slash commands for paper writing assistance:

| Command | Use when |
|---|---|
| `/ars-plan` | Planning a new chapter (Socratic dialogue) |
| `/ars-outline` | Generating a detailed chapter outline |
| `/ars-lit-review` | Expanding or auditing the literature review |
| `/ars-citation-check` | Verifying citation completeness and format |
| `/ars-abstract` | Writing or revising the abstract |
| `/ars-revision` | Applying reviewer feedback to a draft |
| `/ars-revision-coach` | Parsing unstructured supervisor feedback into a revision roadmap |
| `/ars-full` | Full paper writing pipeline (use for new chapters) |
| `/ars-disclosure` | Generating AI-usage disclosure statement for submission |
| `/ars-format-convert` | Converting to/from LaTeX, DOCX, or citation formats |

---

## Codebase Structure

```
/
├── paper/              LaTeX source (fydp.tex + chapter .tex files + fydp.bib)
├── src/
│   ├── baseline/       Lorenz-1960 RK4 + SciPy solver (LOCKED — do not modify)
│   ├── models/         ANN model definitions (next phase)
│   ├── experiments/    Training + evaluation scripts
│   ├── analysis/       Result analysis and visualization
│   └── data_gen/       Dataset export scripts
├── data/               Generated datasets (gitignored, regenerable)
├── results/            Figures, plots, metrics (git-tracked)
├── references/         Cited paper PDFs
├── literature/         Literature review notes
├── presentations/      Presentation decks
├── docs/
│   ├── agents/         Agent skill setup (issue tracker, triage, domain)
│   ├── research/       Research guides, equation authority, roadmaps
│   └── adr/            Architecture Decision Records
├── CONTEXT.md          Research context and domain vocabulary
└── CLAUDE.md           This file
```

---

## Agent skills

### Issue tracker

Issues are tracked in GitHub Issues at `github.com/ihmorol/fydp_workspace`. See `docs/agents/issue-tracker.md`.

### Triage labels

Default triage label vocabulary applies. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout: one `CONTEXT.md` at the repo root + `docs/adr/` for architecture decisions. See `docs/agents/domain.md`.

---

## Branch Naming

Follow the global rules in `~/.claude/CLAUDE.md`:
- `feat/` for new experiment capabilities
- `fix/` for bug fixes in solvers or training scripts
- `docs/` for paper chapter work
- `chore/` for restructuring or tool changes
- `refactor/` for code restructuring without behavior change

---

## What NOT to do

- Do not commit generated data files (`.csv`, `.npz`, `.npy`) — they belong in `data/` which is gitignored
- Do not commit LaTeX build artifacts (`.aux`, `.log`, `.toc`, etc.) — covered by `.gitignore`
- Do not modify `src/baseline/lorenz1960_baseline.py` without an ADR
- Do not invent citations — every reference must exist in `references/` or be verifiable by DOI
- Do not push to `main` directly — work on feature branches
