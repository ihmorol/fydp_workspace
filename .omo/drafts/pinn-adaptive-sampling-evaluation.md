# Draft: PINN Adaptive Sampling Evaluation

## Requirements (confirmed)
- Explain `RAR`, `RAD`, and `RAR-D` from `paper1`.
- Explain how collocation points differ from training data points.
- Explain why adaptive sampling can improve PINN performance.
- Connect the explanation to `fydp-1-implementation` and prepare for evaluating whether the approach fits the FYDP work.
- Keep the evaluation literature-only.
- Stay in teaching mode.
- Provide concrete decisions: approaches to take, discuss, and avoid.

## Technical Decisions
- Use repository-local sources first: `fydp-1-implementation/paper1.txt`, `fydp_research_structure_plan.md`, and `lorenz_1960_equations_learning_guide.md`.
- Treat the request to “evaluate the approach” as planning/evaluation design, not implementation.

## Research Findings
- `paper1.txt` Section 2.4 defines adaptive point sampling as collocation-point sampling that depends on solution/domain features rather than purely random sampling.
- `paper1.txt` defines:
  - `RAR`: add new points where residual is largest.
  - `RAD`: resample the whole point set using a residual-weighted probability distribution.
  - `RAR-D`: add new points using the residual-weighted distribution.
- `paper1.txt` distinguishes collocation points used in physics loss from data points used in inverse/data-fitting loss.
- `fydp_research_structure_plan.md` frames Paper 1 / PinnDE as a PINN/DeepONet reference point, while the FYDP gap is closer to plain ANN comparison.
- `lorenz_1960_equations_learning_guide.md` says the numerical baseline must come first; ANN work is downstream and judged against a validated classical reference.

## Scope Boundaries
- INCLUDE: conceptual explanation, local-paper interpretation, and evaluation-planning questions for FYDP relevance.
- EXCLUDE: implementing PINN sampling, editing source code, running experiments, or writing evaluation files outside `.sisyphus/`.

## Open Questions
- No blocking questions right now.
- Current user preference: literature-only evaluation with recommendation-oriented explanation.
