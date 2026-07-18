# Design Spec — PINN Solver for the Lorenz-1960 System (FYDP-2)

**Date:** 2026-07-16 (rev. after paper1 alignment review)
**Status:** Implemented on `feat/pinn-lorenz1960-harness`
**Related:** `docs/adr/0001-implement-pinn-first.md`, `CONTEXT.md`, `CLAUDE.md`

> Start of an undergraduate thesis implementation: one flat folder, a few
> readable files, a notebook for Kaggle/Colab. No premature abstraction.

---

## 1. Goal

A forward PINN that solves the Lorenz-1960 ODE system, to (a) verify a PINN can
solve it and (b) establish a baseline architecture before the plain-ANN study.
v1 is a single experiment with a fixed architecture (4 hidden layers x 40 nodes x
tanh), driven by one small config so equations/IC/architecture can change without
editing code.

## 2. Scope decision and guardrails

- **Scope expansion** (implementing a PINN) recorded in `docs/adr/0001`, pending
  supervisor approval; `CONTEXT.md`'s research question is unchanged until then.
- All new code lives in one flat top-level **`fydp2/`** folder (supersedes the
  `src/models` guidance in `CLAUDE.md` for this phase; recorded in the ADR).
- **Baseline locked:** `src/baseline/lorenz1960_baseline.py` is imported for the
  equations, ground truth, and error metrics — never modified.
- **Equation authority (imported, not re-typed):** k=2, l=1 gives
  `dx/dt=-0.1yz`, `dy/dt=1.6xz`, `dz/dt=-0.75xy`; ICs `(0.5,0.75,1.0)`; `t∈[0,1]`.
  Validation target at `t=1`: `x≈0.4120105, y≈1.3588440, z≈0.6309875`.
- **Data discipline:** checkpoints → `data/fydp2/` (gitignored); figures/tables →
  `results/fydp2/` (tracked).

## 3. Method (physics-informed, hard initial condition)

Network `N(t): R^1 -> R^3`. Enforce the IC exactly with a trial solution:

```
u_T(t) = u0 + g(t)·N(t),   g(t) = (t - t0)/(t_f - t0)   -> here g(t) = t
```

Residual (coefficients imported from the baseline):

```
r_x = x_T'(t) - c_x·y_T·z_T     (c_x = -0.10)
r_y = y_T'(t) - c_y·x_T·z_T     (c_y =  1.60)
r_z = z_T'(t) - c_z·x_T·y_T     (c_z = -0.75)
```

Derivatives via `torch.autograd.grad`. **Residual-only loss** `mean(r_x²+r_y²+r_z²)`.

- **Collocation:** a uniform grid over `[0,1]`. (No adaptive sampling — the
  Lorenz solution is smooth; paper1 uses adaptivity only for the shock-bearing
  Burgers case, not for its ODE examples.)
- **Optimizer:** Adam + polynomial LR decay (1e-3 -> 1e-4) then **L-BFGS**
  fine-tuning, matching paper1's forward-PINN two-step protocol (Section 4.1).
- **Soft-IC mode** (`ic="soft"`): raw network output with a Raissi-style penalty
  `gamma·||N(t0) - u0||²` added to the loss — available for hard-vs-soft ablation
  and to reproduce paper1's soft-constrained setup. Hard is the default.

RK4/SciPy reference is validation-only, never in the loss.

## 4. Reuse strategy (extract the method, reimplement in PyTorch)

| Source | Method taken | Reuse |
|---|---|---|
| **paper1 / PinnDE** | Hard-IC ODE ansatz; residual loss; Adam+decay; two-step Adam->L-BFGS (Sec 4.1) | `pinn.py` / `train.py` |
| **Raissi PINNs** | `net_u`/`net_f` autodiff split; L-BFGS fine-tuning; soft `MSE_u+MSE_f` | autograd residual; soft-IC mode |
| **paper2** (survey) | Confirms hard-IC (TAS) | Supports design |
| **Lagaris 1998** | Trial-solution ansatz | Root of the hard constraint |
| **ANN-net/** (local) | PyTorch conventions | Match style |
| **src/baseline/** (locked) | coefficients, RHS, solver, error metrics | Imported |

## 5. File layout — one flat folder

```
fydp2/
  README.md            # what it is, how to run, dependencies
  requirements.txt
  config.py            # ONE Config dataclass (equations/IC/arch/training)
  pinn.py              # MLP + hard/soft IC + autograd residual + loss
  train.py             # Adam -> L-BFGS; evaluate vs baseline; save metrics + plots
  test_pinn.py         # sanity + training tests
  lorenz_pinn.ipynb    # Kaggle/Colab notebook
```

## 6. Configuration (`config.py`)

One frozen dataclass; the notebook builds one instance and overrides fields.

```
Config:
  k, l, initial_state, t_span                          # system (coeffs via baseline)
  depth=4, width=40, activation in {tanh,relu,sigmoid,gelu,swish}
  ic in {"hard","soft"}, gamma=1.0                     # IC enforcement
  epochs=20000, lbfgs_iters=2000, lr_start=1e-3, lr_end=1e-4, seed=0
  n_collocation=1001
  results_dir, ckpt_dir
```

## 7. Data flow

```
Config -> coefficients + IC + t-span (baseline)
       -> uniform collocation grid in [0,1]
       -> PINN (hard trial solution or soft raw net)
       -> Adam (poly decay) on residual loss -> L-BFGS fine-tune
       -> evaluate vs RK4 baseline -> metrics table + plots (results/fydp2/)
```

## 8. Testing (`test_pinn.py`)

1. Hard IC exact: `u_T(t0) == u0` for random weights.
2. Residual ~0 on the RK4 reference trajectory (residual-formula sanity).
3. Training reduces loss (hard, exercises autograd + Adam + L-BFGS).
4. Soft-IC training reduces loss (exercises the soft path).

## 9. Evaluation and acceptance

- Hard IC exact at `t=0`.
- Trained PINN reproduces the baseline to well below rel-err `1e-2` at `t=1`
  (Adam+L-BFGS reaches ~1e-6 rel-err / ~1e-10 MSE).
- Full-trajectory MSE reported; convergence / solution / error plots saved.

## 10. Out of scope (v1) / future

- Architecture sweep + best-architecture selection with multiple seeds (the
  actual FYDP contribution — next phase).
- A paper1-faithful reference config (soft IC, 4x60, Adam->L-BFGS) as a
  literature anchor.
- DeepONet / operator learning, Neural ODEs.
- The plain-ANN study (later phase; reuses `pinn.py`'s MLP and `train.py`).
- Editing `CONTEXT.md`'s research question (awaits supervisor approval).
