# Literature Review Workspace

This folder tracks the FYDP literature review for the Lorenz-1960 ANN research topic.

## Goal
Build a disciplined, cumulative literature review system that:
- stores one new relevant paper every two days
- logs why it matters
- captures gaps, methods, and reusable insights
- makes Chapter 2 writing faster and cleaner

## Structure
- `master-table.md` — master tracking table for all reviewed papers
- `daily/` — one markdown log per reading cycle
- `papers/` — one folder per paper with detailed notes
- `templates/` — reusable templates
- `notes/` — synthesis notes, gap analysis, topic maps, reading questions

## Workflow
1. Find one new highly relevant paper from the web.
2. Skip the three seed/background papers already known in the workspace.
3. Add an entry to `master-table.md`.
4. Create a dedicated paper folder under `papers/`.
5. Fill `summary.md` using the paper template.
6. Add a short dated log in `daily/`.
7. Update synthesis notes when a new pattern or gap appears.
8. Commit the literature changes locally.
9. Push only when explicitly requested.

## Current research focus
**Topic:** Solving the Lorenz-1960 ODE System Using ANN and Identifying the Optimal Architecture

## Selection rule
Paper choice should optimize for the FYDP research direction and final goal, not generic AI interest.

Priority order:
1. Lorenz-1960 directly
2. Lorenz-family / chaotic ODE papers
3. Plain ANN for ODE solving
4. Architecture-comparison papers for differential equations
5. PINN / DeepONet baseline papers if they sharpen comparison

## Important rule
Relevance beats volume. One strong paper with disciplined notes is better than five weak papers with no synthesis.
