# Draft: FYDP-I Learning Path

## Requirements (confirmed)
- FYDP-I scope is to analyze the Lorenz-1960 coupled 3-equation system.
- Understand the system's behavior.
- Understand how to solve the ODEs.
- Learn how to design models to solve them later.
- Before model work, learn to implement Lorenz equations using:
  - a Python ODE solver
  - a Runge-Kutta solver
- Learn how to visualize the implementations.
- Learn how to validate the implementations.
- Learn what information, variables, and behavioral signals to watch during implementation.
- Teaching should be step-by-step before any implementation planning begins.

## Technical Decisions
- Start with conceptual teaching first, not implementation.
- Follow the repo's existing logic: numerical baseline first, ANN/model design later.
- Use Lorenz-1960 as a benchmark dynamical system, not as an ANN-first task.

## Research Findings
- `lorenz_1960_equations_learning_guide.md` says the numerical baseline comes first and ANN is judged against a validated classical solver.
- `lorenz1960_baseline/` already reflects the intended numerical-learning workflow: setup -> RK4 -> SciPy baseline -> validation.
- `fydp_research_structure_plan.md` frames Paper 1 as a physics-informed / DeepONet reference, not the immediate first implementation target.

## Scope Boundaries
- INCLUDE: mathematics intuition, behavior interpretation, solver intuition, implementation checklist, visualization logic, validation logic.
- EXCLUDE: coding implementation for now.

## Open Questions
- Preferred teaching granularity: broad roadmap first, then one section at a time?
- Should explanations stay mostly intuitive, or include derivations where useful?
