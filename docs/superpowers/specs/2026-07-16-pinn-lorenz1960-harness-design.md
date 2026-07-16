# Design Spec — PINN Solver for the Lorenz-1960 System (FYDP-2)

**Date:** 2026-07-16
**Status:** Approved design — pending spec review, then implementation plan
**Branch:** `feat/pinn-lorenz1960-harness`
**Related:** `docs/adr/` (scope ADR, pending supervisor approval), `CONTEXT.md`, `CLAUDE.md`

---

## 1. Goal

Implement a Physics-Informed Neural Network (PINN) that solves the Lorenz-1960
ODE system **first** — to (a) verify a PINN can actually solve the system, and
(b) establish a baseline PINN architecture — before the later plain-ANN study.
The implementation must be config-driven so equations, initial conditions, and
architecture can be changed without editing code, and structured so the later
ANN model reuses the same harness.

**This experiment (v1):** a single training run with a fixed baseline
architecture (4 hidden layers × 40 nodes × tanh). A full architecture sweep is
future work, enabled by the central config.

## 2. Scope decision and guardrail reconciliation

- **Scope expansion:** The locked research scope (`CLAUDE.md`, `CONTEXT.md`) is
  "plain feedforward ANN only; PINNs are literature comparison, not implemented."
  Implementing a PINN expands that scope. This is recorded in a new ADR under
  `docs/adr/` and flagged **pending supervisor approval**. The research question
  in `CONTEXT.md` is **not** edited until that approval lands.
- **Folder placement:** Per user decision, all new code lives in a self-contained
  top-level **`fydp2/`** folder. This supersedes the `CLAUDE.md` guidance to place
  new code under `src/models/` and `src/experiments/` **for this FYDP-2 phase
  only**; the ADR records this. Rationale: keep FYDP-2 work isolated, importable,
  and independently testable, without tangling FYDP-1's `src/baseline`.
- **Baseline stays locked:** `src/baseline/lorenz1960_baseline.py` is imported as
  the ground-truth generator and validator. It is never modified.
- **Equation authority:** the Section-4.2 coefficients are imported from the
  baseline (`lorenz1960_coefficients`, `lorenz1960_rhs`) — never re-typed — so the
  equations stay single-sourced. With k=2, l=1: `dx/dt=-0.1yz`, `dy/dt=1.6xz`,
  `dz/dt=-0.75xy`; ICs `(0.5, 0.75, 1.0)`; `t ∈ [0,1]`.

## 3. Method (physics-informed, hard initial condition)

Approximate the solution with a network `N(t): ℝ¹ → ℝ³` and enforce the initial
condition **exactly** via a Lagaris/PinnDE trial-solution ansatz:

```
u_T(t) = u0 + g(t) · N(t),   g(t) = (t - t0) / (t_f - t0),   g(t0) = 0
```

so `u_T(t0) = u0` holds for any network weights. Component-wise, with
`u0 = (x0, y0, z0)`:

```
x_T(t) = x0 + g(t)·N_x(t),  y_T(t) = y0 + g(t)·N_y(t),  z_T(t) = z0 + g(t)·N_z(t)
```

**Residual** (from the imported Section-4.2 coefficients `c_x, c_y, c_z`):

```
r_x = x_T'(t) - c_x·y_T·z_T      (c_x = -0.1)
r_y = y_T'(t) - c_y·x_T·z_T      (c_y =  1.6)
r_z = z_T'(t) - c_z·x_T·y_T      (c_z = -0.75)
```

with `x_T'` etc. computed by `torch.autograd.grad`. **Loss = residual only:**

```
L(θ) = mean( r_x² + r_y² + r_z² )   over collocation points in [0, 1]
```

No IC penalty term, no data term. RK4/SciPy reference data is used **only** for
post-hoc validation, never in training. This is paper1's (PinnDE) default for
ODEs; paper1 states hard-constraining improves training and lowers error for
smooth solutions (Lorenz-1960 is smooth).

## 4. Reuse strategy (extract the method, not the library)

| Source | Extracted method | How reused |
|---|---|---|
| **paper1 / PinnDE** (primary) | Hard-IC ODE ansatz; residual-only loss `L_Δ`; Adam + `PolynomialDecay(1e-3→1e-4)`; residual-adaptive sampling (RAR/RAD) | Reimplemented in PyTorch autograd; Adam schedule; `collocation.py` implements RAR/RAD |
| **Raissi PINNs** (secondary) | `net_u`/`net_f` split; derivatives by autodiff; two-stage Adam→L-BFGS | `net_f` via `torch.autograd.grad`; L-BFGS offered as an optional optimizer |
| **paper2** (survey) | Confirms hard-IC ansatz (NeuroDiffEq TAS); `3×32 tanh` literature point | Supports design; available as a future config point |
| **paper3** (Neural ODEs) | Contrast paradigm | Literature-review contrast only — not implemented |
| **Lagaris 1998** | Original trial-solution ansatz | Theoretical root of the hard constraint; cited |
| **Raissi 2019** | Soft-PINN `MSE_u+MSE_f` | Documented alternative; not built in v1 |
| **ANN-net/** (local) | PyTorch conventions: `nn.Module`, Xavier init, autograd-derivative pattern, config dicts | Match conventions; nanofluid domain code **not** reused |
| **src/baseline/** (local, locked) | `lorenz1960_coefficients`, `lorenz1960_rhs`, `solve_lorenz1960_scipy`, `compute_error_metrics` | Imported for equations, ground truth, and error metrics |

Default optimizer confirmed from PinnDE source: `train(self, epochs, opt="adam", ...)`,
`lr = PolynomialDecay(1e-3, epochs, 1e-4)`. L-BFGS exists as `opt="lbfgs"` but is
not the default.

## 5. Architecture and module layout

Self-contained package. Each module has one responsibility and a documented
interface, so units are understandable and testable in isolation.

```
fydp2/
  __init__.py
  README.md                 # what it is, how to run, dependencies
  requirements.txt          # torch, numpy, scipy, matplotlib, pandas (+ tqdm)
  config.py                 # dataclasses (see §6) — the single source of run settings

  models/
    __init__.py
    base.py                 # SolverModel protocol: forward(t: Tensor[N,1]) -> Tensor[N,3]
    mlp.py                  # MLP(depth, width, activation) with Xavier init; activation registry
    pinn.py                 # PINNSolver: trial-solution hard-IC wrapper around an MLP;
                            #   residual(t) using autograd + imported coefficients

  training/
    __init__.py
    collocation.py          # initial grid over [0,1] + RAR / RAD residual-adaptive refinement
    trainer.py              # Adam + PolynomialDecay loop; residual loss; history; checkpoint;
                            #   optional L-BFGS refinement stage

  evaluation/
    __init__.py
    evaluate.py             # compare trained trajectory vs RK4 baseline (imports
                            #   compute_error_metrics); final-state table; MSE; plots

  run.py                    # single-experiment entrypoint: build config -> train -> evaluate
                            #   -> save; device-agnostic (cuda if available)
  notebooks/
    run_kaggle.ipynb        # thin wrapper calling run.py logic, for Kaggle GPU

  tests/
    __init__.py
    test_config.py          # config defaults / validation
    test_mlp.py             # shapes, activation registry, determinism under seed
    test_pinn.py            # hard-IC exact at t0; residual≈0 on RK4 truth; grad plumbing
    test_evaluate.py        # error metrics wiring vs baseline
    test_integration.py     # short train run reaches rel-err < 1e-2 at t=1 (marked slow)
```

**Interfaces (isolation):**
- `SolverModel` (Protocol) — `forward(t) -> (N,3)`. `PINNSolver` implements it now;
  a future `ANNSolver` implements the same, so `trainer`/`evaluate` are model-agnostic.
- `PINNSolver.residual(t) -> (N,3)` — the only physics-aware method; depends on
  `config` + baseline coefficients, nothing else.
- `trainer.train(model, collocation, config) -> History` — depends on a
  `SolverModel` and configs; knows nothing about Lorenz specifics.
- `evaluate.evaluate(model, system_config) -> Report` — imports baseline for truth.

## 6. Configuration schema (`fydp2/config.py`)

Frozen dataclasses; `run.py` composes one `ExperimentConfig`. Changing equation,
IC, architecture, or training is a config edit — never a code edit.

```
SystemConfig:      k=2.0, l=1.0, initial_state=(0.5,0.75,1.0), t_span=(0.0,1.0)
                   # coefficients derived via imported lorenz1960_coefficients(k,l)
ArchConfig:        depth=4, width=40, activation="tanh"          # v1 baseline
                   # activation ∈ {tanh, relu, sigmoid, gelu, swish}
CollocationConfig: n_initial=1001, strategy="rar", refine_every=2000 (epochs),
                   n_add=100, rad_k=1.0, rad_c=1.0              # RAR/RAD params
TrainConfig:       optimizer="adam", lr_start=1e-3, lr_end=1e-4, epochs=20000,
                   seed=0, lbfgs_refine=False                   # defaults; tunable in plan
ExperimentConfig:  system, arch, collocation, train, output_dir
```

## 7. Data flow

```
ExperimentConfig
  -> SystemConfig gives u0, t_span, coefficients (imported from baseline)
  -> CollocationConfig builds initial t-grid in [0,1]
  -> PINNSolver = trial-solution( MLP(ArchConfig) )
  -> loop: residual(t) via autograd -> loss -> Adam(PolynomialDecay) step
           -> RAR/RAD refine collocation on high-residual regions
  -> (optional) L-BFGS polish
  -> trained model
  -> evaluate vs RK4 baseline -> metrics table + convergence/solution/error plots
  -> save checkpoint (data/fydp2/, gitignored) + figures & tables (results/fydp2/, tracked)
```

## 8. Clean-code and reusability principles (enforced in review)

- **Single responsibility per module/function**; small, focused files.
- **Config over constants:** no magic numbers or equation constants inline;
  equations come from the baseline, run settings from dataclasses.
- **Model-agnostic core:** `trainer` and `evaluate` depend on the `SolverModel`
  protocol, not on `PINNSolver`, so the ANN phase reuses them unchanged.
- **Pure functions where practical** (residual, collocation, metrics) → easy tests.
- **Type hints + concise docstrings** (what it does, inputs, dependencies).
- **No duplication** of baseline logic; import it.
- **Determinism:** seeded runs reproduce; seed lives in config.
- **Match ANN-net conventions** (PyTorch `nn.Module`, Xavier init) for familiarity.

## 9. Evaluation and acceptance criteria

- Hard IC satisfied **exactly**: `u_T(t0) == u0` (numerically, to float tolerance).
- Residual on the RK4 reference trajectory is near zero (sanity of the residual).
- Trained PINN reproduces the locked baseline at `t=1` within **relative error
  < 1e-2** (first target): `x(1)≈0.4120105, y(1)≈1.3588440, z(1)≈0.6309875`.
- Full-trajectory MSE vs RK4 reported; convergence, solution-vs-reference, and
  error-vs-t plots saved to `results/fydp2/`.

## 10. Testing (TDD)

Tests written before implementation, per module (see §5 tree). The integration
test (short training run hitting the `<1e-2` target) is marked slow and runnable
locally on CPU with reduced epochs; full training runs on Kaggle GPU.

## 11. Kaggle GPU workflow

`run.py` selects `cuda` when available and is import-clean so a thin
`notebooks/run_kaggle.ipynb` can `from fydp2.run import main; main(config)`.
Checkpoints and metrics are written to the output dirs; figures/tables are
committed back to `results/fydp2/` after a run.

## 12. Outputs and data discipline

- `data/fydp2/` — checkpoints, generated collocation caches (**gitignored**).
- `results/fydp2/` — metrics tables (CSV), figures (**tracked**).
- No `.csv`/`.npz`/`.npy` training data committed.

## 13. Out of scope (v1)

- Architecture sweep and best-architecture selection (config-enabled, future).
- Soft-IC (Raissi) loss mode — documented, not built.
- DeepONet / operator learning, Neural ODEs, PINN adaptive meta-learning.
- The plain-ANN study (later phase; reuses this harness via `SolverModel`).
- Editing `CONTEXT.md`'s research question (awaits supervisor approval).

## 14. Future work (enabled by this design)

- `fydp2/experiments/sweep.py` iterating `ArchConfig` over depth×width×activation.
- `ANNSolver` implementing `SolverModel` for the data-driven ANN comparison.
- Optional soft-IC mode and multi-seed stability runs.
