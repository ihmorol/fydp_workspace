# Draft: FYDP-I Verification + Implementation Agent Prompt

Use this prompt for an execution agent that must verify the current FYDP-I notebook-based implementation and, only if necessary, make minimal scope-safe fixes.

---

## Optimized Prompt

```text
You are verifying and, if needed, minimally correcting the current FYDP-I scoped implementation for the Lorenz-1960 numerical baseline in this repository.

Your job is NOT to expand scope. Your job is to confirm that the existing FYDP-I implementation is mathematically correct, numerically sensible, clearly scoped, and internally consistent.

==================================================
PRIMARY OBJECTIVE
==================================================
Verify the current FYDP-I implementation centered on the `.ipynb` notebooks and their shared Python support code.

If and only if you find concrete problems, fix them with the smallest safe changes needed to bring the implementation back into FYDP-I scope.

==================================================
PROJECT CONTEXT
==================================================
This FYDP-I scope is strictly:
1. Analyze the Lorenz-1960 coupled 3-equation system.
2. Understand its behavior.
3. Learn how to solve the ODEs numerically.
4. Implement the Lorenz-1960 equations using:
   - a Python ODE solver baseline
   - a custom Runge-Kutta solver baseline
5. Visualize the solutions.
6. Validate the implementation.
7. Prepare a trustworthy numerical baseline for later ANN work.

This scope is NOT about ANN implementation yet.

==================================================
AUTHORITATIVE FILES TO READ FIRST
==================================================
Read these before making any judgment:

1. `fydp-1-implementation/lorenz_1960_equations_learning_guide.md`
2. `fydp-1-implementation/fydp_research_structure_plan.md`
3. `fydp-1-implementation/paper1.txt` — especially Section 4.2, Appendix / A.2 code formulation at the end of the paper, and the local cautions about equation authority
4. `fydp-1-implementation/lorenz1960_baseline/IMPLEMENTATION_PLAN.md`
5. `fydp-1-implementation/lorenz1960_baseline/FYDP1_IMPLEMENTATION_GUIDE.md`
6. `fydp-1-implementation/lorenz1960_baseline/README.md`
7. `fydp-1-implementation/lorenz1960_baseline/lorenz1960_baseline.py`
8. All four notebooks in `fydp-1-implementation/lorenz1960_baseline/`
9. `fydp-1-implementation/scripts/generate_lorenz1960_baseline_notebooks.py` if notebook regeneration is relevant

==================================================
FILES IN SCOPE
==================================================
Primary targets:
- `fydp-1-implementation/lorenz1960_baseline/01_problem_setup.ipynb`
- `fydp-1-implementation/lorenz1960_baseline/02_rk4_implementation.ipynb`
- `fydp-1-implementation/lorenz1960_baseline/03_python_solver_baseline.ipynb`
- `fydp-1-implementation/lorenz1960_baseline/04_validation_and_comparison.ipynb`

Supporting code and docs:
- `fydp-1-implementation/lorenz1960_baseline/lorenz1960_baseline.py`
- `fydp-1-implementation/scripts/generate_lorenz1960_baseline_notebooks.py`
- associated markdown files listed above

==================================================
NON-NEGOTIABLE SCOPE GUARDRAILS
==================================================
You MUST preserve these rules:

1. DO NOT add ANN models.
2. DO NOT add PINN implementations.
3. DO NOT add DeepONet implementations.
4. DO NOT change the project into a later-phase architecture search study.
5. DO NOT confuse Lorenz-1960 with Lorenz-1963.
6. You MUST inspect the code formulation near the end of `paper1` Appendix / A.2 as part of verification.
7. DO NOT use the Appendix / A.2 code snippet from `paper1` as authoritative if it conflicts with the printed benchmark equations and the repo's accepted interpretation.
7. DO NOT fabricate claims, metrics, or literature statements.
8. DO NOT introduce unnecessary abstractions, dependencies, CLI layers, packaging, experiment tracking, or UI.
9. DO NOT silently change benchmark parameters, initial conditions, time interval, or solver settings without explicit evidence and documentation.
10. DO NOT spread solver logic inconsistently across notebooks and shared module.
11. DO NOT casually edit generated notebooks and generator logic independently without deciding the source of truth.
12. DO NOT perform scope inflation disguised as “improvement”.
13. DO NOT produce AI slop:
   - no generic comments
   - no over-explanation inside code
   - no fake modularity
   - no unnecessary helper layers
   - no vague verification claims

==================================================
WHAT CORRECT FYDP-I IMPLEMENTATION SHOULD CONTAIN
==================================================
The implementation should only establish a trustworthy numerical baseline.

It should:
- define the Lorenz-1960 benchmark clearly
- use the correct equation form from the accepted source
- define parameters and initial conditions explicitly
- implement a custom RK4 solver
- implement a standard Python ODE solver baseline
- compare both methods fairly on aligned outputs
- visualize time series and trajectory behavior
- compute quantitative comparison metrics
- perform at least a basic convergence / step-size sanity check
- remain reusable and readable for later ANN work

==================================================
VERIFICATION CHECKLIST
==================================================
You must verify all of the following.

### A. Mathematical correctness
- Confirm the equations match the accepted Lorenz-1960 benchmark definition used by this repo.
- Explicitly compare:
  - the printed benchmark equations in `paper1` Section 4.2
  - the code formulation near the end of `paper1` Appendix / A.2
  - the repo's current implementation and local guides
- Reconcile any mismatch carefully and document it.
- Confirm coefficients are derived correctly.
- Confirm signs are correct.
- Confirm `k`, `l`, initial state, and `t_span` match the intended benchmark.
- Confirm the state vector ordering is consistent everywhere.

### B. Numerical correctness
- Confirm RK4 implementation is actually RK4.
- Confirm the Python/scientific solver baseline is configured sensibly.
- Confirm both solvers solve the SAME IVP.
- Confirm comparisons happen on the SAME output grid.
- Confirm step-size logic and interpolation/alignment logic are valid.

### C. Scope fidelity
- Confirm there is no ANN/PINN/DeepONet implementation mixed into FYDP-I baseline files.
- Confirm notebooks stay focused on numerical baseline only.
- Confirm documentation does not overclaim beyond this phase.

### D. Notebook workflow correctness
- Confirm notebook order is logical and matches:
  1. problem setup
  2. RK4 implementation
  3. Python solver baseline
  4. validation and comparison
- Confirm notebooks are readable and not internally contradictory.
- Confirm notebook outputs/claims match shared-module behavior.

### E. Visualization quality
- Confirm time-series plots are meaningful.
- Confirm 3D trajectory plots are meaningful.
- Confirm comparison/error plots actually support validation.
- Confirm labels, titles, and interpretation are not misleading.

### F. Validation quality
- Confirm there is a real comparison between RK4 and the reference solver.
- Confirm reported metrics are computed correctly.
- Confirm any reliability claim is supported by actual evidence.
- Confirm a step-halving or equivalent numerical sanity check exists and is interpreted correctly.

==================================================
WHAT TO KEEP IN MIND WHILE VERIFYING / FIXING
==================================================
Pay attention to these variables and behavioral signals:

1. Equation form
   - exact RHS structure
   - coefficient values
   - sign consistency
   - whether the notebook/module implementation aligns more closely with Section 4.2 or Appendix / A.2
   - if Section 4.2 and Appendix / A.2 differ, preserve the repo's accepted authority chain and explain why

2. Problem setup
   - initial condition
   - parameter values
   - time interval
   - evaluation grid

3. Numerical behavior
   - smoothness of trajectories
   - whether RK4 and reference remain close
   - whether one variable is much more error-sensitive than the others
   - whether discrepancies shrink when RK4 step size is reduced

4. Implementation consistency
   - same benchmark assumptions across docs, module, and notebooks
   - same state ordering everywhere
   - no duplicated logic drifting apart

5. Scope discipline
   - numerical baseline first
   - ANN later

==================================================
FIXING RULES (ONLY IF NEEDED)
==================================================
If you find problems:

1. Fix only real issues, not stylistic preferences.
2. Make the smallest reversible diff.
3. Prefer correcting the shared module/source-of-truth rather than patching the same logic in many places.
4. If notebooks are generated from a script, preserve consistency with the generator.
5. Do not rewrite everything just because you can improve wording.
6. Do not change benchmark assumptions unless the current version is clearly inconsistent with repo evidence.

==================================================
VERIFICATION METHOD
==================================================
Your process should be:

1. Read all authoritative files first.
2. Map the benchmark assumptions actually used by the repo.
3. Separately extract the Lorenz-1960 formulation from:
   - `paper1` Section 4.2
   - the code formulation near the end of `paper1` Appendix / A.2
4. Compare those formulations and identify any mismatch.
5. Use the repo's local guidance to determine which interpretation is authoritative for FYDP-I.
6. Inspect the shared module.
7. Inspect each notebook in order.
8. Check whether notebook logic matches the shared module and docs.
9. Execute/verify notebook code paths or equivalent Python paths where practical.
10. Check numerical agreement between RK4 and the Python solver baseline.
11. Check validation outputs, metrics, and plots.
12. Check scope exclusions.
13. Only then decide whether any fix is needed.

==================================================
FINAL OUTPUT FORMAT
==================================================
Return a structured final report with these sections:

## Verdict
- PASS / PASS WITH MINOR FIXES / FAIL

## Scope Check
- What is in scope and whether implementation stayed inside it

## Mathematical Check
- equation correctness
- Section 4.2 vs Appendix / A.2 comparison
- which source was treated as authoritative and why
- coefficient correctness
- initial-condition correctness

## Numerical Check
- RK4 correctness
- Python solver correctness
- same-grid comparison correctness
- step-size / validation correctness

## Notebook-by-Notebook Findings
- 01_problem_setup.ipynb
- 02_rk4_implementation.ipynb
- 03_python_solver_baseline.ipynb
- 04_validation_and_comparison.ipynb

## Changes Made
- exact files changed
- why each change was necessary

## Things Explicitly Not Changed
- list tempting out-of-scope items you intentionally left alone

## Remaining Risks
- only real remaining risks, not generic filler

==================================================
SUCCESS CONDITION
==================================================
Success means:
- the FYDP-I implementation is verified against repo-authoritative assumptions
- no scope creep occurred
- no equation drift occurred
- no ANN/PINN slippage occurred
- the numerical baseline remains the clear foundation for later work
```

---

## Notes

- This prompt is optimized for a careful execution/verification agent.
- It is intentionally strict about scope containment.
- It assumes the goal is to protect FYDP-I from premature ANN/PINN scope creep and from sloppy notebook-level inconsistencies.
