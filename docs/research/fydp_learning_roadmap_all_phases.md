# FYDP Learning Roadmap
## From Beginner → Researcher: Solving Lorenz-1960 ODEs with ANNs
**For a team of beginners | UIU CSE FYDP-I**

---

> [!IMPORTANT]
> This roadmap is split into 3 phases. **Do NOT skip Phase 0.** The research will fail without the mathematical and coding foundations. Treat Phase 0 as seriously as the research itself.

---

## Phase Overview

```
Phase 0 (Pre-Phase)          Phase 1 (FYDP-I Active)       Phase 2 (FYDP-II Ongoing)
Weeks 1–6                    Weeks 7–16                     Weeks 17–24+
──────────────────           ───────────────────            ─────────────────────
Build foundations  →   Implement & experiment   →   Optimize & write paper
(Math + Code + ML)       (ANN models on Lorenz)        (Results + analysis)
```

---

## Phase 0: Pre-Phase — Build Your Foundation
**Duration**: Weeks 1–6 (can be done in parallel, 2 hrs/day per topic)

### 0.1 Mathematics Prerequisites

#### Topic A: Ordinary Differential Equations (ODEs) ⭐ *Most Critical*
You **must** understand what ODEs are before you can solve them with ANNs.

**What to learn:**
- What is a differential equation? (dy/dx, dy/dt notation)
- Initial Value Problem (IVP) — what it means, why initial conditions matter
- First-order ODE systems (exactly what Lorenz-1960 is)
- Classical solvers: Euler method and Runge-Kutta 4 (RK4) — understand the algorithm, not just the code
- What "solution accuracy" means (local vs. global error)

**Resources (Free):**
| Resource | Why | Link |
|---|---|---|
| 3Blue1Brown — Differential Equations series | Visual, intuitive intro, WATCH FIRST | [youtube.com/3b1b](https://www.youtube.com/playlist?list=PLZHQObOWTQDNPOjrT6KVlfJuKtYTftqH6) |
| MIT OCW 18.03 (Gilbert Strang) | Full ODE course, free | [ocw.mit.edu/18-03](https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/) |
| Khan Academy — Differential Equations | Beginner-friendly exercises | [khanacademy.org/de](https://www.khanacademy.org/math/differential-equations) |
| Lorenz 1960 paper summary | Read the section 4.2 of Paper 1 | Paper 1 on your disk |

**Milestone checkpoint:** You can manually trace through one Euler step of the Lorenz-1960 system by hand.

---

#### Topic B: Linear Algebra ⭐ *Required*
ANNs are fundamentally a series of matrix operations.

**What to learn:**
- Vectors and matrices (addition, multiplication)
- Dot product and matrix-vector product
- Transpose, inverse (conceptual)
- What a gradient is (direction of steepest ascent)

**Resources:**
| Resource | Why | Link |
|---|---|---|
| 3Blue1Brown — Essence of Linear Algebra | Best visual introduction ever made | [youtube.com/3b1b-linalg](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab) |
| MIT OCW 18.06 | Deep linear algebra (optional depth) | [ocw.mit.edu/18-06](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/) |

**Milestone checkpoint:** You understand that an ANN layer computes `h = activation(Wx + b)`.

---

#### Topic C: Calculus — Derivatives & Chain Rule ⭐ *Required*
Backpropagation is just the chain rule, applied repeatedly.

**What to learn:**
- Derivatives (dy/dx) — rate of change
- Partial derivatives (∂f/∂x, ∂f/∂y)
- Chain rule (this IS backpropagation)
- Gradient descent concept: move in the direction of -∇Loss

**Resources:**
| Resource | Why | Link |
|---|---|---|
| 3Blue1Brown — Essence of Calculus | Visual, watch before anything else | [youtube.com/3b1b-calc](https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr) |
| Khan Academy — Multivariable Calculus | Partial derivatives exercises | [khanacademy.org/mv-calc](https://www.khanacademy.org/math/multivariable-calculus) |

---

### 0.2 Machine Learning Prerequisites

#### Topic D: How ANNs Work ⭐ *Most Critical*
**What to learn (in this order):**
1. What is a neuron? What is a layer?
2. Forward pass: input → hidden layers → output
3. Activation functions: sigmoid, tanh, ReLU — what they do, why tanh is preferred for ODEs
4. Loss function: what it measures, why MSE is used
5. Backpropagation: how gradients flow backwards
6. Gradient descent and optimizers: SGD, Adam
7. What overfitting is and how to detect it

**Resources:**
| Resource | Why | Link |
|---|---|---|
| 3Blue1Brown — Neural Networks series | *The* best visual introduction | [youtube.com/3b1b-nn](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi) |
| Andrej Karpathy — Neural Networks: Zero to Hero | Coding from scratch, very practical | [youtube.com/karpathy](https://www.youtube.com/@AndrejKarpathy) |
| fast.ai Practical Deep Learning | Hands-on first, theory later | [course.fast.ai](https://course.fast.ai) |
| Deep Learning book (Goodfellow) Chs 1–6 | Free online, reference level | [deeplearningbook.org](https://www.deeplearningbook.org) |

**Milestone checkpoint:** You can implement a 2-layer ANN in Python from scratch (no library) that learns to approximate `y = sin(x)`.

---

#### Topic E: Automatic Differentiation (AutoDiff)
This is how PyTorch/TensorFlow compute gradients — critical to understand.

**What to learn:**
- What `grad()` does in PyTorch
- Computational graph concept
- Why AutoDiff is more accurate than numerical differentiation

**Resources:**
| Resource | Why |
|---|---|
| PyTorch Autograd tutorial | Official, practical | [pytorch.org/tutorials/autograd](https://pytorch.org/tutorials/beginner/blitz/autograd_tutorial.html) |
| Baydin et al. (2018) — Automatic Differentiation survey | The paper cited in all 3 of your papers | arXiv:1502.05767 |

---

### 0.3 Python & Coding Prerequisites

#### Topic F: Python for Scientific Computing ⭐ *Required*

**What to learn (tools):**
| Tool | Purpose | Resource |
|---|---|---|
| **Python basics** | Variables, functions, loops, classes | [python.org/tutorial](https://docs.python.org/3/tutorial/) |
| **NumPy** | Array operations, math | [numpy.org/learn](https://numpy.org/learn/) |
| **SciPy** | Numerical ODE solving (`solve_ivp`) | [scipy.org](https://docs.scipy.org/doc/scipy/tutorial/integrate.html) |
| **Matplotlib** | Plotting results | [matplotlib.org/tutorials](https://matplotlib.org/stable/tutorials/index.html) |
| **PyTorch** | Building and training ANNs | [pytorch.org/tutorials](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html) |
| **Jupyter Notebook** | Interactive coding environment | [jupyter.org](https://jupyter.org/try) |

**Milestone checkpoint:** Run the Lorenz-1960 system using `scipy.integrate.solve_ivp` and plot x(t), y(t), z(t) using Matplotlib.

```python
# Target code you should be able to write and understand after Phase 0
from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt

k, l = 2, 1
def lorenz1960(t, state):
    x, y, z = state
    dxdt = k*l * (1/(k**2 + l**2) - 1/k**2) * y * z
    dydt = k*l * (1/l**2 - 1/(k**2 + l**2)) * x * z
    dzdt = k*l**2/2 * (1/k**2 - 1/l**2) * x * y
    return [dxdt, dydt, dzdt]

sol = solve_ivp(lorenz1960, [0, 1], [0.5, 0.75, 1.0], 
                method='RK45', dense_output=True, rtol=1e-10)
t = np.linspace(0, 1, 500)
y = sol.sol(t)
plt.plot(t, y[0], label='x(t)')
plt.plot(t, y[1], label='y(t)')
plt.plot(t, y[2], label='z(t)')
plt.legend()
plt.show()
```

---

### 0.4 Supplementary Background

#### Topic G: Read the Papers Strategically
Don't try to understand every equation immediately. Use this reading order:

**First pass (Week 1–2):** Read only Abstract + Introduction + Conclusion of all 3 papers
**Second pass (Week 3–4):** Read Paper 2 Section 2 (ANN overview) + Paper 1 Section 2 (background)
**Third pass (Week 5–6):** Read Paper 1 Section 4.2 (Lorenz solution) + Paper 2 Section 3 (methods) in detail
**Paper 3:** Read the Introduction and Figure 1 only — enough to describe it in your literature review

**How to annotate a paper:**
- Highlight: anything you don't understand
- Write in margin: what each section is about in plain English
- Mark with ⭐: results that are directly comparable to what you'll compute

---

## Phase 1: Active Research — FYDP-I (Weeks 7–16)

### 1.1 Week-by-Week Implementation Plan

| Week | Task | Deliverable |
|---|---|---|
| 7 | Generate Lorenz-1960 reference data using RK45 | Python script + plots |
| 8 | Implement baseline ANN (3 layers, 32 nodes, tanh) — replicate Paper 2 setup | Working ANN, initial MSE |
| 9 | Train and evaluate baseline; compare with RK45 | First result table |
| 10 | Vary number of layers (2–6), record MSE | Layer depth analysis |
| 11 | Vary neurons per layer (20–100), record MSE | Width analysis |
| 12 | Vary activation functions (tanh, ReLU, sigmoid, GELU) | Activation comparison |
| 13 | Vary optimizer (Adam vs L-BFGS vs Adam→L-BFGS) | Optimizer analysis |
| 14 | Identify best architecture; run 5 training seeds for stability | Best model + error bars |
| 15 | Write Chapter 1 & 2 of FYDP-I report | Draft chapters |
| 16 | Finalize FYDP-I report + prepare presentation | Final submission |

---

### 1.2 Your ANN Model Structure (What to Actually Build)

```
Input:  t ∈ [0, 1]  (scalar time)
         ↓
[Hidden Layer 1: N neurons, activation]
         ↓
[Hidden Layer 2: N neurons, activation]
         ↓
    ... (L total hidden layers)
         ↓
Output: [x(t), y(t), z(t)]  (3 outputs)

Loss = MSE(ANN_output, RK45_reference)
     = (1/n) Σ[(x_pred - x_ref)² + (y_pred - y_ref)² + (z_pred - z_ref)²]
```

**Important design decision:** Feed initial conditions as extra inputs OR enforce them as a hard constraint (see [instruction.md](file:///e:/University/FYDP/resources/instruction.md) note about initial conditions — confirm with supervisor).

---

### 1.3 How to Report Your Results

Every experiment must record:

| Column | Description |
|---|---|
| Architecture | e.g., `L=4, N=60, tanh` |
| Parameters | Total trainable parameters |
| Epochs | Training steps |
| Train MSE | Final training loss |
| Test MSE | Loss on held-out validation points |
| Training time | Seconds/minutes |
| Notes | Any instability, divergence |

Create a results table like this and grow it with every experiment.

---

### 1.4 Experiment Tracking (Critical for Research)

> [!TIP]
> Use **Weights & Biases (wandb)** or simple **CSV logging** to track every experiment. Never trust your memory. If you don't log it, it didn't happen.

**Free option — simple CSV logger:**
```python
import csv, datetime

def log_experiment(arch, params, epochs, train_mse, test_mse, time_s):
    with open('experiments.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now(), arch, params, 
                         epochs, train_mse, test_mse, time_s])
```

**Professional option:**
- [Weights & Biases](https://wandb.ai) — free for students, beautiful dashboards
- [MLflow](https://mlflow.org) — open source

---

### 1.5 Research Contribution Guidelines

To make a **valuable contribution**, your work must do at least ONE of:

| Contribution Type | What it looks like for your project |
|---|---|
| **Empirical benchmark** | Systematic table: 20+ architectures tested on Lorenz-1960, MSE recorded |
| **Novel comparison** | First paper to compare plain-ANN vs. PINN approaches on Lorenz-1960 specifically |
| **Best architecture claim** | "Architecture X (L layers, N nodes, tanh) achieves state-of-the-art on Lorenz-1960" with statistical evidence (multiple seeds) |
| **Transferability study** | Does the best architecture for Lorenz-1960 also work well for other 3-ODE systems? |

> [!WARNING]
> **What is NOT a contribution**: Running one architecture, getting low MSE, and saying "it works". You must compare at minimum 3–5 architectures and analyze WHY one outperforms others.

---

## Phase 2: Ongoing Advanced Learning (FYDP-II, Weeks 17–24)

### 2.1 Advanced Topics to Pick Up As Needed

| Topic | When you need it | Resource |
|---|---|---|
| **Hyperparameter tuning** | Week 13+ | Optuna library docs; Andrew Ng's ML course |
| **Batch training vs. full-batch** | Week 8 onwards | PyTorch DataLoader tutorial |
| **Learning rate scheduling** | When training is unstable | PyTorch `lr_scheduler` docs |
| **Physics-informed loss addition** | If supervisor suggests | Paper 1 Section 2.1 + Brunton video |
| **Neural ODEs (Paper 3 approach)** | If you want to extend research | `torchdiffeq` library — same authors |
| **Statistical analysis** | Chapter 4, results section | Scipy stats; pandas for data |

---

### 2.2 Writing the Research Paper / Chapter 2

**Literature review writing rules:**
1. Never copy-paste from papers. Always summarize in your own words.
2. Every claim must have a citation: `(Matthews & Bihlo, 2025)`
3. Use the structure: *What* → *How* → *Result* → *Gap*
4. End every paper summary with: "However, [this paper] does not address [your gap]"

**Gap analysis writing template:**
```
"While [Paper X] demonstrated [method] for [problem], their work 
was limited to [limitation]. In contrast, our work focuses specifically 
on [your specific angle], which has not been explored in the literature."
```

---

## Team Roles & Specializations

Divide learning and responsibilities across team members:

| Role | Primary Learning | Responsibility |
|---|---|---|
| **Math Lead** | Topics A, B, C (ODEs, Linear Algebra, Calculus) | Verify equations, check math in report |
| **ML Engineer** | Topics D, E, F (ANN, AutoDiff, PyTorch) | Write training code, run experiments |
| **Data & Results Lead** | SciPy, Matplotlib, results tracking | Generate reference data, plot all results |
| **Technical Writer** | Paper reading strategy, LaTeX | Write and structure report chapters |

> Each team member should still do ALL of Phase 0 to some degree — the roles just indicate primary depth.

---

## Recommended Daily Learning Schedule (Phase 0)

```
Mon/Wed/Fri (2 hrs each):
  30min — Watch/read resource
  60min — Code practice (implement what you just learned)
  30min — Write a 5-sentence summary of what you learned

Tue/Thu (1 hr each):
  Read one section of one of the 3 papers
  Write one sentence describing what each section does

Weekend (3 hrs):
  Work through the weekly coding milestone
  Team sync: share what each person learned
```

---

## Quick Reference: What "Good Research" Looks Like

| Criterion | Poor | Good |
|---|---|---|
| Number of experiments | 1–2 architectures | 15–30+ systematic experiments |
| Comparison | No baseline | Compared to RK45, Paper1, Paper2 results |
| Reproducibility | "We ran it and it worked" | Code on GitHub, seeds fixed, results in table |
| Analysis | "MSE was low" | "tanh outperformed ReLU by 43% because..." |
| Visualization | Raw numbers | Loss curves, error plots, solution vs. reference plots |

---

## Checklist: Are You Ready to Start Research?

**Phase 0 Exit Criteria — verify before proceeding to Phase 1:**

- [ ] Can solve a simple ODE on paper using Euler method
- [ ] Can explain what `dz/dt = f(z,t)` means in plain English
- [ ] Can write a working ANN in PyTorch that trains on toy data
- [ ] Can run the Lorenz-1960 system in Python using `scipy.solve_ivp`
- [ ] Have read the Abstracts of all 3 papers
- [ ] Understand what MSE means and how to compute it
- [ ] Have Python, PyTorch, and Jupyter Notebook installed and running
- [ ] Have a shared GitHub repository set up for the team
