# FYDP-I Research Structure
## Solving the Lorenz-1960 ODE System Using Optimal ANN Architectures
**Institution**: United International University (UIU) | **Department**: CSE | **Phase**: FYDP-I

---

## 1. Synthesized Research Idea

### Core Problem Statement
Classical numerical methods (Runge-Kutta, Euler, Adams-Bashforth) solve the Lorenz-1960 meteorological ODE system with high accuracy, but they are **computationally expensive**, **mesh-dependent**, and **cannot generalize** across different initial conditions without re-solving from scratch. This project investigates whether **Artificial Neural Networks (ANNs)** — without physics-based loss terms — can serve as a superior, generalizable solver for this ODE system, and identifies **which ANN architecture produces the best results**.

### Research Question
> *Which ANN architecture — in terms of depth, width, activation function, and training strategy — achieves the best accuracy when solving the Lorenz-1960 three-component ODE system as an initial value problem?*

### Target Equation: Lorenz-1960 System
The system (as used in Paper 1, Section 4.2):

```
dx/dt = kl(1/(k²+l²) - 1/k²) yz
dy/dt = kl(1/l² - 1/(k²+l²)) xz
dz/dt = kl²/2 (1/k² - 1/l²) xy
```
With parameters k=2, l=1 and initial conditions x(0)=0.5, y(0)=0.75, z(0)=1, t ∈ [0,1].

---

## 2. Paper-by-Paper Analysis

### Paper 1 — PinnDE (Reference Implementation)
**Citation**: Matthews, J. & Bihlo, A. (2025). *PinnDE: Physics-Informed Neural Networks for Solving Differential Equations*. arXiv:2408.10011v2.

| Element | Details |
|---|---|
| **Relevance** | Section 4.2 solves Lorenz-1960 using a **DeepONet** — directly related to your target equation |
| **Architecture used** | DeepONet: MLP branch+trunk nets, 4 hidden layers, 40 nodes/layer, tanh activation, Adam |
| **Method** | Operator learning — learns G(u₀)(t,x) mapping initial condition → solution |
| **Result** | Accurate solution over [0,1]; time-stepped to [0,6] with consistently low error |
| **Your gap** | PinnDE uses PINNs/DeepONets (physics-informed). You are exploring **plain ANNs** — *how does removing the physics constraint affect accuracy vs. efficiency?* |

**Key insight for your research**: Paper 1 gives you a **PINN-based baseline** for the Lorenz-1960 system. Your ANN approach without physics-informed loss is a direct comparison candidate.

---

### Paper 2 — ANN-based PDE Solver Survey
**Citation**: Pratama, D.A., Bakar, M.A., Ismail, N.B. & Mashuri, M. (2022). *ANN-based methods for solving partial differential equations: a survey*. Arab Journal of Basic and Applied Sciences, 29(1), 233–248. DOI: 10.1080/25765299.2022.2104224

| Element | Details |
|---|---|
| **Relevance** | Surveys three distinct ANN methodologies for solving differential equations |
| **Methods compared** | **PyDEns** (Deep Galerkin + ansatz), **NeuroDiffEq** (Trial Approximate Solution/TAS), **Nangs** (grid-point based training) |
| **Architecture** | All use: 3 hidden layers, 32 neurons each, tanh activation |
| **Key finding** | NeuroDiffEq and Nangs outperform PyDEns on high-dimensional PDEs; PyDEns only suitable for low-dimensional problems |
| **Your gap** | Focuses on PDEs, not ODEs specifically; does not study Lorenz-1960; does not do architecture optimization |

**Key insight for your research**:
- The **Trial Approximate Solution (TAS)** approach used by NeuroDiffEq is directly applicable to ODEs — it bakes initial conditions into the ansatz, removing the need for a boundary loss term
- This is a non-PINN, pure-ANN approach — **closely aligned with your methodology**
- The paper benchmarks **heat equation** only; you extend to a **nonlinear, coupled ODE system** (Lorenz-1960)

---

### Paper 3 — Neural ODEs (Paradigm-shifting)
**Citation**: Chen, R.T.Q., Rubanova, Y., Bettencourt, J. & Duvenaud, D. (2019). *Neural Ordinary Differential Equations*. NeurIPS 2018. arXiv:1806.07366v5.

| Element | Details |
|---|---|
| **Relevance** | Introduces a fundamentally different paradigm: using a neural network **as the ODE itself** |
| **Core idea** | `dh(t)/dt = f(h(t), t, θ)` — parameterize the derivative using a neural network; use a black-box ODE solver to compute outputs |
| **Training** | Adjoint sensitivity method — constant memory backpropagation through ODE solvers |
| **Applications** | Supervised classification (MNIST), continuous normalizing flows, time-series latent variable models |
| **Your gap** | Neural ODE uses the NN to *parameterize dynamics*, not to *approximate the solution function* — orthogonal to your approach |

**Key insight for your research**:
- Neural ODEs are a **related but distinct** paradigm — worth mentioning in your literature review as a contrasting approach
- Your project uses ANN to **approximate the solution** u(t); Neural ODEs use ANN to **approximate the derivative** f(t)
- The adjoint method from Paper 3 is important background knowledge for understanding gradient flow in ODE-based learning
- Helps define your **gap**: you are not parameterizing the dynamics, you are finding the best **solution approximator** architecture

---

## 3. Supervisor Video Summary
**Video**: *Physics Informed Neural Networks (PINNs) [Physics Informed Machine Learning]*
**Creator**: Steve Brunton (University of Washington) | **Date**: May 29, 2024 | **Duration**: 34:31 | **Views**: 174K

### Key Takeaways Relevant to Your FYDP
| Topic | Summary |
|---|---|
| **What PINNs are** | Standard MLP + PDE residual added to loss function; uses automatic differentiation to compute partial derivatives |
| **Advantage** | Works with small/sparse datasets; leverages virtual points for physics validation |
| **Limitation** | Physics is "suggested" not enforced; stiff optimization; can fail for chaotic/discontinuous systems |
| **Failure modes** | Convection-reaction-diffusion PDEs fail in certain parameter regimes; hard to balance data vs. physics loss |
| **Why this matters for you** | Your approach uses ANN **without** physics in the loss — you are exploring the other extreme: pure data-driven ODE solving |
| **Steve's point** | The hyperparameter balancing data loss vs. physics loss is critical — your research sidesteps this by removing physics loss entirely |

> **Important signal**: Your supervisor gave you this video as background. This tells you PINNs are the reference point your supervisor wants you to **understand and then differentiate from**.

---

## 4. Research Positioning & Gap Analysis

### Taxonomy of Approaches

```
ANN-based ODE/PDE Solvers
│
├── Physics-Informed (PINN family)
│   ├── PINNs (Raissi et al., 2019) — adds PDE residual to loss
│   ├── PinnDE (Matthews & Bihlo, 2025) — Paper 1 — library
│   └── DeepONet — learns solution operator, not just one solution
│
├── Pure ANN (no physics constraint)
│   ├── Deep Galerkin Method → PyDEns — Paper 2
│   ├── Trial Approximate Solution → NeuroDiffEq — Paper 2
│   ├── Grid-based training → Nangs — Paper 2
│   └── ← YOUR RESEARCH SITS HERE →
│       (Finding optimal ANN architecture for Lorenz-1960 ODE)
│
└── Neural ODEs
    └── Chen et al. NeurIPS 2018 — Paper 3
        (NN parameterizes f(t) in dh/dt = f(h,t,θ))
```

### Identified Research Gaps
1. **No architecture study for Lorenz-1960 specifically**: Paper 1 uses it but doesn't optimize architecture; Paper 2 studies other equations; no paper compares ANN architectures on Lorenz-1960
2. **PINNs vs. pure ANNs for Lorenz-1960**: No direct comparison between physics-informed and data-driven approaches on this specific coupled ODE system
3. **Activation function impact on ODE solving**: Paper 2 uses tanh throughout without ablation; Paper 1 uses tanh without questioning it
4. **Effect of network depth and width**: No systematic study on how layer count and neuron count affect ODE solution quality for Lorenz-type systems
5. **Generalization across initial conditions**: Most papers train for one initial condition; your system could study how well trained models generalize

---

## 5. Proposed Research Title & Objectives

### Proposed Title
> **"Optimal ANN Architecture for Solving the Lorenz-1960 ODE System: A Comparative Study of Depth, Width, and Activation Functions"**

*(Revise with your supervisor — this is a working title)*

### Objectives
1. Implement and reproduce the Lorenz-1960 ODE solution from Paper 1 as a baseline
2. Design and train multiple ANN architectures (varying layers: 2–6, neurons: 20–100, activation: tanh/ReLU/sigmoid/GELU) to solve the Lorenz-1960 system
3. Evaluate and compare architectures using MSE against a high-accuracy RK4 numerical reference solution
4. Identify the architecture that achieves the lowest approximation error
5. Compare results with the PINN-based result from Paper 1 (PinnDE) and the survey-based results from Paper 2

---

## 6. Chapter-by-Chapter Plan (FYDP-I Template)

### Chapter 1: Introduction *(FYDP-I Required)*
| Section | What to Write |
|---|---|
| **1.1 Project Overview** | Background on ODEs in physics; why Lorenz-1960 matters; problem statement — classical solvers vs. ANNs |
| **1.2 Motivation** | Real-world weather/atmospheric modeling context; limitations of Runge-Kutta for parametric studies; potential of ANNs for fast inference |
| **1.3 Objectives** | List the 5 objectives above |
| **1.4 Methodology** | Brief: implement multiple ANN architectures, train on Lorenz-1960 IVP, compare via MSE vs. RK4 |
| **1.5 Project Outcome** | Expected: identification of optimal ANN architecture; comparison table with baselines from Paper 1 & 2 |
| **1.6 Organization of Report** | Chapter-by-chapter narrative |

**Images to include** (per instruction.md):
- Real-life physics examples where Lorenz-type equations arise (weather, fluid dynamics, planetary motion)
- Diagram comparing classical numerical solver vs. ANN solver workflow

---

### Chapter 2: Background *(FYDP-I Required)*
| Section | What to Write |
|---|---|
| **2.1 Preliminaries** | ANN basics (MLP, backpropagation, activation functions); ODE definition; Lorenz-1960 equations; classical solvers (Euler, RK4) |
| **2.2.1 Similar Applications** | Other ODE/PDE systems solved with ANNs (heat equation from Paper 2; rigid body from Paper 1) |
| **2.2.2 Related Research** | Paper 1 (PinnDE), Paper 2 (PyDEns/NeuroDiffEq/Nangs), Paper 3 (Neural ODEs); Steve Brunton PINNs overview |
| **2.3 Gap Analysis** | Table of what each paper does NOT cover, leading to your specific gap |
| **2.4 Summary** | 1-paragraph synthesis leading into Chapter 3 |

**Literature table to build** (for gap analysis):

| Paper | Method | ODE/PDE | Architecture Study | Lorenz-1960 | Plain ANN |
|---|---|---|---|---|---|
| PinnDE (Paper 1) | PINN+DeepONet | Both | No | ✓ (Section 4.2) | No |
| ANN Survey (Paper 2) | PyDEns/NeuroDiffEq/Nangs | PDE only | No | No | ✓ |
| Neural ODEs (Paper 3) | Neural ODE | ODE | No | No | Partial |
| **Your work** | **Plain ANN** | **ODE** | **✓ (main contribution)** | **✓** | **✓** |

---

### Chapter 3: Project Design *(FYDP-I Required)*
| Section | What to Write |
|---|---|
| **3.1 Requirements** | Functional: train/evaluate ANN models; Non-functional: accuracy < 1e-4 MSE vs. RK4; tools: Python, PyTorch/TensorFlow |
| **3.2 Methodology** | Step-by-step: define Lorenz-1960 IVP → generate training data (RK4 reference) → design architectures → train → evaluate |
| **3.3 Project Plan** | 24-week Gantt chart (FYDP-I + FYDP-II) |
| **3.4 Task Allocation** | Per team member |

---

## 7. Methodology Detail (What to Actually Implement)

### Data Generation
- Use `scipy.integrate.solve_ivp` (RK45 with tight tolerances: rtol=1e-10, atol=1e-12) to generate a high-accuracy numerical solution as **ground truth**
- Sample `N=1000–5000` time points in [0, 1]
- Split: 80% training, 20% validation

### Architecture Search Space
| Hyperparameter | Values to Test |
|---|---|
| Hidden layers | 2, 3, 4, 5, 6 |
| Neurons per layer | 20, 40, 60, 80, 100 |
| Activation function | tanh, ReLU, sigmoid, GELU, Swish |
| Optimizer | Adam, L-BFGS, Adam→L-BFGS |
| Loss function | MSE vs. RK4 reference; optionally + IC residual |

### Evaluation Metrics
- MSE between ANN output and RK4 reference
- Training loss convergence rate
- Inference time (after training)
- Number of parameters

### Baseline Comparisons
- Runge-Kutta 4 (classical numerical) — gold standard
- PinnDE/DeepONet result from Paper 1 Section 4.2
- NeuroDiffEq architecture (3 layers, 32 nodes, tanh) from Paper 2

---

## 8. Standards & Tools

| Category | Selection |
|---|---|
| **Language** | Python 3.10+ |
| **Frameworks** | PyTorch or TensorFlow (decide based on supervisor preference) |
| **Numerical reference** | SciPy `solve_ivp` (RK45) |
| **Visualization** | Matplotlib, Seaborn |
| **Standards** | IEEE Std 829 (Software Test Documentation); reproducible research (code on GitHub) |
| **Reporting** | LaTeX (UIU FYDP template) |

---

## 9. Open Questions to Clarify with Supervisor

1. Should the ANN take only `t` as input and output `(x, y, z)`, or should it incorporate initial conditions too (operator learning style)?
2. Are you allowed to include the initial condition in the loss function (soft constraint), or must it be a hard constraint in the network architecture (like NeuroDiffEq TAS)?
3. How many architectures are expected to be tested — is this a grid search or a literature-guided selection?
4. Will FYDP-I require any preliminary results, or only the proposal + methodology?
5. Is there a specific metric threshold (e.g., MSE < 1e-3) that defines "optimal"?
