"""Central configuration and locked-baseline access for the FYDP-2 PINN."""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

_REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO_ROOT / "src" / "baseline"))

from lorenz1960_baseline import (  # noqa: E402
    Lorenz1960Config,
    compute_error_metrics,
    lorenz1960_coefficients,
    solve_lorenz1960_scipy,
)

ACTIVATIONS = ("tanh", "relu", "sigmoid", "gelu", "swish")
IC_MODES = ("hard", "soft")


@dataclass(frozen=True)
class Config:
    k: float = 2.0
    l: float = 1.0
    initial_state: tuple[float, float, float] = (0.5, 0.75, 1.0)
    t_span: tuple[float, float] = (0.0, 1.0)

    depth: int = 4
    width: int = 40
    activation: str = "tanh"

    ic: str = "hard"          # "hard" trial solution, or "soft" IC penalty (Raissi-style)
    gamma: float = 1.0        # soft-IC penalty weight (unused when ic="hard")

    epochs: int = 20000       # Adam epochs
    lbfgs_iters: int = 2000   # L-BFGS fine-tuning iterations (0 disables)
    lr_start: float = 1e-3
    lr_end: float = 1e-4
    seed: int = 0

    n_collocation: int = 1001

    results_dir: str = "results/fydp2"
    ckpt_dir: str = "data/fydp2"

    def __post_init__(self) -> None:
        if self.activation not in ACTIVATIONS:
            raise ValueError(f"activation must be one of {ACTIVATIONS}")
        if self.ic not in IC_MODES:
            raise ValueError(f"ic must be one of {IC_MODES}")

    @property
    def coefficients(self) -> np.ndarray:
        return lorenz1960_coefficients(self.k, self.l)


def reference_trajectory(cfg: Config, n: int = 1001) -> tuple[np.ndarray, np.ndarray]:
    """Ground-truth (t, [x,y,z]) from the locked SciPy baseline solver."""
    baseline = Lorenz1960Config(
        k=cfg.k, l=cfg.l, initial_state=cfg.initial_state, t_span=cfg.t_span, n_eval=n
    )
    t, ys, _ = solve_lorenz1960_scipy(config=baseline)
    return t, ys


__all__ = ["Config", "reference_trajectory", "compute_error_metrics", "ACTIVATIONS", "IC_MODES"]
