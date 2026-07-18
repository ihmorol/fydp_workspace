# fydp2 — PINN solver for the Lorenz-1960 ODE system

A Physics-Informed Neural Network (PINN) that solves the Lorenz-1960 system
(FYDP-2). Hard initial condition via a trial solution, residual-only loss, Adam
with polynomial learning-rate decay, and adaptive RAR/RAD collocation. Validated
against the locked RK4/SciPy baseline in `src/baseline/`.

## Files

| File | Purpose |
|---|---|
| `config.py` | One `Config` dataclass: equations, IC, architecture, training, collocation |
| `pinn.py` | MLP + hard-IC trial solution + autograd residual + loss |
| `collocation.py` | Uniform grid + RAR/RAD adaptive refinement |
| `train.py` | Adam training loop, evaluation vs baseline, plots |
| `test_pinn.py` | Two sanity checks |
| `lorenz_pinn.ipynb` | Runnable notebook (Kaggle / Colab) |

## Method

`u_T(t) = u0 + g(t)·N(t)`, `g(t) = (t − t0)/(t_f − t0)` — the initial condition is
satisfied exactly. Loss is residual-only: `mean(r²)`, `r_j = d u_j/dt − f_j(u)`,
with `f` from the Section-4.2 coefficients imported from the baseline. The
RK4/SciPy reference is used only to validate, never in the loss.

## Run locally

```
pip install -r fydp2/requirements.txt
python -m pytest fydp2/test_pinn.py -q
python -c "from fydp2.train import main; main()"   # trains, evaluates, writes results/fydp2/
```

## Run on Kaggle / Colab

Open `lorenz_pinn.ipynb`. On Colab, clone the repo in the first cell so
`import fydp2` works; a GPU runtime is used automatically when available.

## Outputs

- `results/fydp2/` — `metrics.csv`, `convergence.png`, `solution.png`, `error.png` (tracked)
- `data/fydp2/pinn.pt` — checkpoint (gitignored)

## Config knobs

Change equation, IC, or architecture without editing code, e.g.
`Config(depth=3, width=50, activation="gelu", adapt="rad", epochs=5000)`.

## Scope

PINN-first: verify feasibility and a baseline architecture before the plain-ANN
study. The baseline solver is imported, never modified. See
`docs/adr/0001-implement-pinn-first.md` (pending supervisor approval).
