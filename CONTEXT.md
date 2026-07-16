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

**FYDP Segments**:
- FYDP-I: Literature Review + Concept Development + Design (Ch1, Ch2, Ch3, baseline solver)
- FYDP-II: Implementation + Testing (69 ANN experiments, evaluation, Ch4)
- FYDP-III: Deployment (Ch5 results analysis, Ch6 conclusion, final report submission)

**Data pipeline**:
1. Generate reference trajectory using RK4 (custom) and SciPy solve_ivp (DOP853)
2. Both solvers show agreement at RMSE ~2.33e-11 — this is the ground truth
3. Split data 80/20 random train/validation, seed=42
4. Z-score normalize each output variable (x, y, z) during training; unnormalize before reporting
5. Train feedforward ANN architectures on (t → x, y, z) mapping
6. Evaluate using MSE, MAE, max absolute error, training time, inference time

**ANN approach**: Plain feedforward (data-driven only). No physics-informed loss terms, no operator learning. Input: scalar t (scalar). Output: (x(t), y(t), z(t)) — the three state variables of the Lorenz-1960 system.

**Loss function**: Pure MSE on (x, y, z) targets. No IC penalty, no physics residual.

**Architecture search axes (Phase 1 — 60 runs)**:
- Depth: 1, 2, 3, 4 hidden layers
- Width: 20, 50, 100 neurons per layer (uniform across all hidden layers)
- Activation: tanh, ReLU, sigmoid, GELU, Swish
- Optimizer: Adam, lr=1e-3 (fixed for Phase 1)
- Total: 4 × 3 × 5 = 60 experiments

**Optimizer comparison (Phase 2 — 9 runs)**:
- Take top-3 architectures by combined MSE from Phase 1
- Compare: Adam (lr=1e-3) vs L-BFGS vs SGD with momentum
- Total: 3 architectures × 3 optimizers = 9 experiments

**Total experiments: 69**

**Training protocol**:
- Max epochs: 10,000
- Early stopping: patience=500 epochs on validation loss; restore best weights
- Batch size: full batch (800 training points per step)
- Random seed: torch.manual_seed(42) set before each model initialization
- Data split seed: 42 (fixed, applied once before all experiments)

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
| 3 | Project Design | ⚠️ Decisions locked — ready to write |
| 4 | Implementation and Results | ❌ Stub |
| 5 | Standards and Design Constraints | ⚠️ Partial |
| 6 | Conclusion | ❌ Stub |

Chapter 3 decisions are fully locked (see Chapter 3 Design Decisions section below). Write using those decisions directly.

Chapter 4 must cover: training results per architecture, MSE/MAE/Max error tables, convergence plots, best architecture selection, Phase 2 optimizer comparison, comparison with PINN baselines from literature.

---

## Chapter 3 Design Decisions (Locked — 2026-05-15)

All decisions below are final for Chapter 3 (Project Design). Do not override without supervisor approval.

### 3.1 Requirements

**Functional Requirements**

| ID | Requirement |
|---|---|
| FR1 | Generate high-accuracy numerical reference solution for Lorenz-1960 using RK4 and SciPy DOP853 over t∈[0,1] at 1001 uniformly spaced points |
| FR2 | Partition reference dataset into training and validation subsets using 80/20 random split, seed=42 |
| FR3 | Construct feedforward ANN models with systematically varied depth (1–4), width (20/50/100), and activation (tanh/ReLU/sigmoid/GELU/Swish) |
| FR4 | Train all Phase 1 models under identical conditions using Adam optimizer; record convergence behaviour |
| FR5 | Conduct Phase 2 optimizer comparison (Adam vs L-BFGS vs SGD) on top-3 architectures from Phase 1 |
| FR6 | Evaluate each model: MSE, MAE, maximum absolute error, training time, inference time against RK4 reference |
| FR7 | Produce comparison tables, solution trajectory plots, and error curves for all evaluated models |

**Non-Functional Requirements**

| ID | Requirement |
|---|---|
| NFR1 | All experiments fully reproducible via fixed seed=42 for weight initialization and data splitting |
| NFR2 | Numerical reference solution maintains solver agreement within RMSE < 1e-10 between RK4 and SciPy DOP853 |
| NFR5 | All results, model configurations, and metrics logged systematically to allow independent verification |

### 3.1.2 Context Diagram

**External entities (2 only):**
1. **Research Team** — configures pipeline, triggers experiments, receives outputs
2. **Academic / Research Community** — consumes findings, reuses methodology, builds on results

No other entities. System boundary contains all 5 pipeline processes.

### 3.1.3 Data Flow Diagram Level 1

**5 processes:**
1. Generate Reference Solution (RK4 + SciPy DOP853)
2. Preprocess Data (80/20 split, z-score normalize targets)
3. Train ANN Models (Phase 1: 60 runs; Phase 2: 9 runs)
4. Evaluate Models (MSE, MAE, Max error, training time, inference time)
5. Compare & Select Best Architecture → report to Academic/Research Community

### 3.2 Experimental Design Summary

| Decision | Value |
|---|---|
| Framework | PyTorch |
| Input | Scalar t |
| Output | (x(t), y(t), z(t)) — 3 state variables |
| Data points | 1001 uniformly spaced, t∈[0,1] |
| Train/val split | 80/20 random, seed=42 |
| Target normalization | Z-score per variable; unnormalize before reporting |
| Loss function | Pure MSE — no IC penalty, no physics term |
| Phase 1 grid | Depth 1–4 × Width 20/50/100 × 5 activations = 60 runs |
| Phase 2 | Top-3 architectures × Adam/L-BFGS/SGD = 9 runs |
| Total experiments | 69 |
| Optimizer (Phase 1) | Adam, lr=1e-3 |
| Max epochs | 10,000 |
| Early stopping | Patience=500, restore best weights |
| Batch size | Full batch (800 points) |
| Seed | torch.manual_seed(42) per model |
| Eval metrics | MSE + MAE + Max absolute error + Training time + Inference time |
| Reproducibility | Single run per config, fixed seed=42 |

### 3.3 Project Plan

Three-segment FYDP narrative (no Gantt, no timeline):
- **FYDP-I**: Literature Review, Concept Development, Design — Ch1, Ch2, Ch3, baseline solver
- **FYDP-II**: Implementation, Testing — 69 ANN experiments, evaluation, Ch4
- **FYDP-III**: Deployment — Ch5, Ch6, final report

### 3.4 Task Allocation

| Member | ID | Role | Responsibilities |
|---|---|---|---|
| Ikramul Hasan Moral | 0112230489 | Implementation Lead | Baseline solver, data preprocessing, ANN model implementation (PyTorch), training loop, experiment runner |
| Md. Abu Bakar | 0112230200 | Analysis | Evaluation pipeline, metrics computation, architecture comparison |
| Samiur Rahman Omlan | 0112230195 | Analysis | Results interpretation, visualization, plots, figures |
| Fariha Islam | 0112230431 | Writing & Research | Paper writing, literature review, citation management |
| Md. Touhidul Islam | 0112230435 | Writing & Research | Paper writing, chapter drafting, report compilation |

---

## ADR Log

Architecture decisions are documented in `docs/adr/`. When a significant design choice is made (choice of optimizer, data normalization strategy, train/val/test split rationale), record it there.
