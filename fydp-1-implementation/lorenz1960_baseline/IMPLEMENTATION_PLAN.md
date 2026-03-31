# Lorenz-1960 Numerical Baseline Implementation Plan

## Problem Setup
- Use the Lorenz-1960 system exactly as defined in the local project guide and `paper1` Section 4.2.
- Verified benchmark setup from local sources:
  - `k = 2`
  - `l = 1`
  - `x(0) = 0.5`, `y(0) = 0.75`, `z(0) = 1.0`
  - `t in [0, 1]`
- Use the simplified coefficient form after substitution:
  - `dx/dt = -0.1 yz`
  - `dy/dt = 1.6 xz`
  - `dz/dt = -0.75 xy`

## Solver Design
- Implement a fixed-step RK4 solver from scratch for transparency and reproducibility.
- Implement a SciPy `solve_ivp` baseline using the same right-hand side and initial value problem.
- Use a shared helper module so both solvers use identical equations, constants, and plotting utilities.

## Validation Method
- Evaluate both solvers on the same output grid for a fair comparison.
- Primary RK4 setting: `h = 1e-3`, which matches a 1001-point grid on `[0, 1]`.
- Primary SciPy setting: `solve_ivp` with `method="DOP853"`, `rtol=1e-10`, `atol=1e-12`.
- Compare:
  - time-series overlays for `x(t)`, `y(t)`, `z(t)`
  - 3D trajectories
  - absolute error curves
  - quantitative metrics: MAE, RMSE, max absolute error
- Add an RK4 step-halving check to confirm that reducing `h` decreases the discrepancy against the SciPy reference.

## File Structure
- `lorenz1960_baseline/README.md`
- `lorenz1960_baseline/IMPLEMENTATION_PLAN.md`
- `lorenz1960_baseline/lorenz1960_baseline.py`
- `lorenz1960_baseline/01_problem_setup.ipynb`
- `lorenz1960_baseline/02_rk4_implementation.ipynb`
- `lorenz1960_baseline/03_python_solver_baseline.ipynb`
- `lorenz1960_baseline/04_validation_and_comparison.ipynb`
- `scripts/generate_lorenz1960_baseline_notebooks.py`

## Notebook Sequence
1. `01_problem_setup.ipynb`: define the benchmark and justify numerical choices.
2. `02_rk4_implementation.ipynb`: implement and run the custom RK4 solver.
3. `03_python_solver_baseline.ipynb`: run the SciPy solver on the same problem.
4. `04_validation_and_comparison.ipynb`: compare both methods and assess baseline reliability.

## Risks And Assumptions
- Assumption: the printed equations in `paper1` Section 4.2 are authoritative, because the local guide explicitly warns that the appendix code snippet is inconsistent.
- Assumption: the problem is non-stiff on `[0, 1]`, so explicit RK methods are appropriate for the first baseline.
- Risk: a coarse fixed RK4 step could understate numerical accuracy.
  - Mitigation: include step-halving validation in the comparison notebook.
- Risk: a library solver can look better only because of tighter internal tolerances.
  - Mitigation: compare both methods on the same output grid and document the solver settings explicitly.
