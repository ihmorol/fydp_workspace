# Lorenz-1960 Numerical Baseline

This folder contains the initial research-grade numerical baseline for the FYDP Lorenz-1960 project.

## Files
- `01_problem_setup.ipynb`: benchmark definition, assumptions, and numerical configuration.
- `02_rk4_implementation.ipynb`: custom fixed-step RK4 implementation and simulation.
- `03_python_solver_baseline.ipynb`: SciPy `solve_ivp` baseline on the same initial value problem.
- `04_validation_and_comparison.ipynb`: visual and quantitative comparison of both solvers.
- `lorenz1960_baseline.py`: shared equations, constants, solvers, metrics, and plotting helpers.
- `IMPLEMENTATION_PLAN.md`: concise plan used to structure the implementation.

## Intended Use
- Open the notebooks in order.
- Run each notebook from top to bottom.
- The notebooks are written to be compatible with Google Colab using standard scientific Python packages.

## Verified Local Context Used
- `lorenz_1960_equations_learning_guide.md`
- `fydp_research_structure_plan.md`
- `paper1.txt` Section 4.2

## Scope
- This baseline covers only numerical solution and validation.
- No ANN models are implemented in this folder.
