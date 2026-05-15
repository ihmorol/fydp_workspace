# Research Context: Solving the Lorenz ODE System Using Optimal ANN Architectures

## Project Identity

**Title**: Solving the Lorenz ODE System Using Optimal ANN Architectures  
**Institution**: United International University (UIU), Department of CSE  
**Authors**: Ikramul Hasan Moral, Md. Abu Bakar, Samiur Rahman Omlan, Fariha Islam, Md. Touhidul Islam  
**Supervisor**: Dr. Muhammad Nomani Kabir  
**Paper format**: UIU FYDP LaTeX template, IEEE citation style (natbib unsrt)  
**Current state**: Chapters 1–2 complete; Chapters 3–6 in progress  

---

## Research Question

> Which feedforward ANN architecture (varying depth, width, and activation function) most accurately approximates the solution to the Lorenz-1960 ODE system, when trained purely on reference data from a validated RK4/SciPy numerical solver — without physics-informed loss terms?

---

## The Lorenz-1960 System (Equation Authority)

The target is the **Section 4.2 formulation** from Matthews & Bihlo (paper3.pdf / paper `[3]`):

```
dx/dt = kl (1/(k²+l²) - 1/k²) yz
dy/dt = kl (1/l² - 1/(k²+l²)) xz
dz/dt = kl²/2 (1/k² - 1/l²) xy
```

With **k=2, l=1** this reduces to:
```
dx/dt = -0.1 yz
dy/dt =  1.6 xz
dz/dt = -0.75 xy
```

**Initial conditions**: x(0)=0.5, y(0)=0.75, z(0)=1.0  
**Time interval**: t ∈ [0, 1]  
**Grid**: 1001 uniformly spaced points (h=0.001 for RK4)

⚠️ **CAUTION**: Appendix A.2 of paper3.pdf contains an inconsistent code snippet. Use only Section 4.2 equations. This is documented in `docs/research/lorenz_1960_equations_learning_guide.md`.

---

## Methodology

**Approach**: Waterfall (Literature Review → Concept Development → Algorithm Design → Implementation → Testing → Deployment)

**Data pipeline**:
1. Generate reference trajectory using RK4 (custom) and SciPy solve_ivp (DOP853)
2. Both solvers show agreement at RMSE ~2.33e-11 — this is the ground truth
3. Export canonical dataset (t, x, y, z) as `.npz` for ANN training
4. Train feedforward ANN architectures on (t → x, y, z) mapping
5. Evaluate using MSE, training convergence, and inference time

**ANN approach**: Plain feedforward (data-driven only). No physics-informed loss terms, no operator learning. Input: scalar t. Output: (x(t), y(t), z(t)).

**Architecture search axes**:
- Depth: 1–4 hidden layers
- Width: 20, 50, 100 neurons per layer
- Activation: tanh, ReLU, sigmoid, GELU, Swish
- Optimizer: Adam with default lr=1e-3
- Loss: MSE against RK4 reference trajectory

---

## Research Gaps Addressed (from Ch. 2 Gap Analysis)

1. **No architecture study for Lorenz-1960**: existing work uses fixed architectures
2. **No PINN vs. plain ANN comparison on Lorenz-1960**: our baseline will enable this
3. **No systematic activation function study**: tanh/ReLU/sigmoid/GELU/Swish on a coupled ODE
4. **No systematic depth × width study**: varying both dimensions together
5. **Limited generalization**: most papers train for a single initial condition only

---

## Baseline Solver Status

Verified and locked. Do not change:

| File | Role |
|---|---|
| `src/baseline/lorenz1960_baseline.py` | Source of truth — all equations, RK4, SciPy |
| `src/baseline/01_problem_setup.ipynb` | Problem definition notebook |
| `src/baseline/02_rk4_implementation.ipynb` | Custom RK4 solver |
| `src/baseline/03_python_solver_baseline.ipynb` | SciPy DOP853 baseline |
| `src/baseline/04_validation_and_comparison.ipynb` | Validation: RMSE 2.33e-11 |

**Verified numerical values (t=1)**:
- x(1) ≈ 0.4120105447758
- y(1) ≈ 1.3588439851225
- z(1) ≈ 0.6309874543508

---

## Cited Papers (Reference Authority)

| In-text | File | Description |
|---|---|---|
| [1] | references/paper1.pdf | ANN architecture reference (feedforward diagram) |
| [2] | references/paper2.pdf | PINN architecture reference (physics loss figure) |
| [3] | references/paper3.pdf | Matthews & Bihlo — PinnDE, Lorenz-1960 formulation |
| — | references/Solving_the_Lorenz_1960_ODE_System_Using_Optimal_ANN_Architectures-1.pdf | Our own working paper draft |

Full bibliography: `paper/fydp.bib`

---

## Domain Vocabulary

| Term | Definition |
|---|---|
| ODE | Ordinary Differential Equation — describes how a quantity changes over time |
| Lorenz-1960 | Three coupled nonlinear ODEs from Lorenz's 1960 meteorological model |
| RK4 | Fourth-order Runge-Kutta method — classical numerical ODE solver |
| SciPy solve_ivp | Python ODE solver using DOP853 (8th-order Dormand-Prince) |
| ANN | Artificial Neural Network — feedforward/MLP in this context |
| PINN | Physics-Informed Neural Network — embeds ODE residuals in the loss |
| MSE | Mean Squared Error — primary evaluation metric |
| Architecture search | Systematic variation of depth, width, and activation to find best ANN |
| Baseline | The validated RK4/SciPy solution used as training data and ground truth |

---

## Chapter Structure

| Chapter | Title | Status |
|---|---|---|
| 1 | Introduction | ✅ Complete |
| 2 | Background | ✅ Complete |
| 3 | Project Design | ❌ Stub |
| 4 | Implementation and Results | ❌ Stub |
| 5 | Standards and Design Constraints | ⚠️ Partial |
| 6 | Conclusion | ❌ Stub |

Chapter 3 must cover: experimental design, ANN architecture grid, training protocol, evaluation metrics, data split strategy, hyperparameter settings.

Chapter 4 must cover: training results per architecture, MSE tables, convergence plots, best architecture selection, comparison with PINN baselines from literature.

---

## ADR Log

Architecture decisions are documented in `docs/adr/`. When a significant design choice is made (choice of optimizer, data normalization strategy, train/val/test split rationale), record it there.
