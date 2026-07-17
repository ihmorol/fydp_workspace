# Design Spec — PINN Solver for the Lorenz-1960 System (FYDP-2)

**Date:** 2026-07-16
**Status:** Approved (lean revision) — ready for implementation plan
**Branch:** `feat/pinn-lorenz1960-harness`
**Related:** `docs/adr/` (scope ADR, pending supervisor approval), `CONTEXT.md`, `CLAUDE.md`

> Scope note: this is the **start of an undergraduate thesis implementation**.
> The design is deliberately small — one flat folder, a few readable files, and a
> notebook to run on Kaggle/Colab. No premature abstraction.

---

## 1. Goal

Implement a Physics-Informed Neural Network (PINN) that solves the Lorenz-1960
ODE system, to (a) verify a PINN can actually solve the system and (b) establish
a baseline PINN architecture — **before** the later plain-ANN study. v1 is a
**single experiment** with a fixed architecture (4 hidden layers × 40 nodes ×
tanh), driven by one small config so equations/IC/architecture can be changed
without editing code.

## 2. Scope decision and guardrails

- **Scope expansion:** the locked scope (`CLAUDE.md`, `CONTEXT.md`) is "plain ANN
  only; PINNs are literature comparison." Implementing a PINN expands that; it is
  recorded in a new ADR under `docs/adr/`, flagged **pending supervisor
  approval**. Do **not** edit the research question in `CONTEXT.md` until approved.
- **Folder placement:** all new code lives in one flat top-level **`fydp2/`**
  folder. This supersedes the `src/models`/`src/experiments` guidance in
  `CLAUDE.md` for this phase; the ADR records it.
- **Baseline locked:** `src/baseline/lorenz1960_baseline.py` is imported for the
  equations, ground truth, and error metrics — never modified.
- **Equation authority (imported, not re-typed):** with k=2, l=1,
  `dx/dt=-0.1yz`, `dy/dt=1.6xz`, `dz/dt=-0.75xy`; ICs `(0.5, 0.75, 1.0)`;
  `t ∈ [0,1]`. Validation target at `t=1`: `x≈0.4120105, y≈1.3588440, z≈0.6309875`.
- **Data discipline:** checkpoints → `data/fydp2/` (gitignored); figures/tables →
  `results/fydp2/` (tracked). No `.csv`/`.npz`/`.npy` committed.

## 3. Method (physics-informed, hard initial condition)

Network `N(t): ℝ¹ → ℝ³`. Enforce the IC **exactly** with a trial solution:

```
u_T(t) = u0 + g(t)·N(t),   g(t) = (t - t0)/(t_f - t0)   → here g(t) = t
```

so `u_T(0) = u0` for any weights. Residual (coefficients imported from baseline):

```
r_x = x_T'(t) - c_x·y_T·z_T     (c_x = -0.10)
r_y = y_T'(t) - c_y·x_T·z_T     (c_y =  1.60)
r_z = z_T'(t) - c_z·x_T·y_T     (c_z = -0.75)
```

`x_T'` etc. via `torch.autograd.grad`. **Residual-only loss** (no IC term, no data
term): `L = mean(r_x² + r_y² + r_z²)` over collocation points. RK4/SciPy reference
is **validation only** — never in the loss.

- **Optimizer:** Adam + `PolynomialDecay(1e-3 → 1e-4)` over epochs (PinnDE default).
- **Collocation:** uniform grid over `[0,1]` **plus adaptive RAR/RAD** refinement
  (add points where the residual is largest), per paper1 §2.4.

This is paper1's (PinnDE) default for ODEs; the paper states hard-constraining
improves training and lowers error for smooth solutions (Lorenz-1960 is smooth).

## 4. Reuse strategy (extract the method, reimplement in PyTorch)

| Source | Method taken | Reuse |
|---|---|---|
| **paper1 / PinnDE** (primary) | Hard-IC ODE ansatz; residual-only loss; Adam+PolynomialDecay; RAR/RAD | Reimplement in `pinn.py` / `collocation.py` |
| **Raissi PINNs** (secondary) | `net_u`/`net_f` autodiff split | `torch.autograd.grad` for the residual |
| **paper2** (survey) | Confirms hard-IC (TAS) | Supports design |
| **paper3** (Neural ODEs) | Contrast paradigm | Lit-review only — not implemented |
| **Lagaris 1998** | Original trial-solution ansatz | Root of the hard constraint; cited |
| **Raissi 2019** | Soft-PINN `MSE_u+MSE_f` | Documented alternative; not built |
| **ANN-net/** (local) | PyTorch conventions (`nn.Module`, Xavier init, autograd pattern) | Match style; nanofluid code not reused |
| **src/baseline/** (local, locked) | `lorenz1960_coefficients`, `lorenz1960_rhs`, `solve_lorenz1960_scipy`, `compute_error_metrics` | Imported |

Optimizer confirmed from PinnDE source: `train(self, epochs, opt="adam", ...)`,
`lr = PolynomialDecay(1e-3, epochs, 1e-4)`.

## 5. File layout — one flat folder

```
fydp2/
  README.md            # what it is, how to run (local + Kaggle/Colab), dependencies
  requirements.txt     # torch, numpy, scipy, matplotlib, pandas
  config.py            # ONE dataclass: equations/IC/t-span + arch (4,40,tanh) + training + collocation
  pinn.py              # MLP(depth,width,activation) + trial-solution hard-IC wrapper + residual + loss
  collocation.py       # uniform grid + RAR/RAD residual-adaptive refinement
  train.py             # Adam+PolynomialDecay loop; evaluate vs baseline; save metrics + plots
  test_pinn.py         # 2 sanity checks (see §8)
  lorenz_pinn.ipynb    # runnable notebook for Kaggle/Colab: imports the modules, runs, shows results
```

No subpackages, no protocol/interface layer, no separate entrypoint script — the
notebook is the entrypoint and imports the plain functions/classes from the
modules. Keep each file short and single-purpose.

## 6. Configuration (`config.py`)

One frozen dataclass holds everything; the notebook builds one instance and can
override any field. Changing equation/IC/architecture is a field edit, not a code
change.

```
Config:
  k=2.0, l=1.0, initial_state=(0.5,0.75,1.0), t_span=(0.0,1.0)   # coeffs via imported fn
  depth=4, width=40, activation="tanh"        # activation ∈ {tanh,relu,sigmoid,gelu,swish}
  epochs=20000, lr_start=1e-3, lr_end=1e-4, seed=0
  n_collocation=1001, adapt="rar", refine_every=2000, n_add=100  # RAR/RAD (defaults, tunable)
```

## 7. Data flow

```
Config → coefficients + IC + t-span (from baseline)
      → collocation grid in [0,1]
      → PINN = trial-solution( MLP(config) )
      → loop: residual via autograd → loss → Adam(PolynomialDecay) step
              → RAR/RAD add points at high residual
      → trained model → evaluate vs RK4 baseline → metrics table + plots (results/fydp2/)
```

## 8. Testing (`test_pinn.py`, two checks)

1. **Hard IC is exact:** `u_T(0) == u0` to float tolerance, for random weights.
2. **Residual is ~0 on truth:** feeding the RK4 reference trajectory into the
   residual gives ≈ 0 (sanity of the residual definition).

## 9. Evaluation and acceptance

- Hard IC exact at `t=0`.
- Trained PINN reproduces the locked baseline at `t=1` within **relative error
  `<1e-2`** (first target).
- Full-trajectory MSE reported; convergence, solution-vs-reference, and
  error-vs-t plots saved to `results/fydp2/`.

## 10. Clean-code principles

Single-purpose files; config over magic numbers; equations imported from the
baseline; type hints + short docstrings; seeded determinism; match ANN-net's
PyTorch style. No duplication of baseline logic.

## 11. Out of scope (v1) / future

- Architecture sweep + best-architecture selection (config-enabled later).
- Soft-IC (Raissi) loss mode; L-BFGS refinement.
- DeepONet, operator learning, Neural ODEs.
- The plain-ANN study (later phase — will reuse `pinn.py`'s MLP and `train.py`).
- Editing `CONTEXT.md`'s research question (awaits supervisor approval).
