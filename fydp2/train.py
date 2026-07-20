"""Train the Lorenz-1960 PINN, evaluate against the locked baseline, save results."""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from scipy.stats import qmc
from torch import Tensor

from .config import Config, compute_error_metrics, reference_trajectory
from .pinn import PINN, pinn_loss

STATE = ("x", "y", "z")


def get_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def set_seed(seed: int) -> None:
    torch.manual_seed(seed)
    np.random.seed(seed)


def make_grid(cfg: Config, device: torch.device) -> Tensor:
    # Latin hypercube sampling over [t0, tf], following paper1.
    t0, tf = cfg.t_span
    sample = qmc.LatinHypercube(d=1, seed=cfg.seed).random(cfg.n_collocation)
    t = t0 + (tf - t0) * sample
    return torch.as_tensor(t, dtype=torch.float32, device=device).reshape(-1, 1)


def train(cfg: Config) -> tuple[PINN, list[float]]:
    set_seed(cfg.seed)
    device = get_device()
    model = PINN(cfg).to(device)
    grid = make_grid(cfg, device)
    history: list[float] = []

    def loss_fn() -> Tensor:
        return pinn_loss(model, grid.clone().requires_grad_(True))

    adam = torch.optim.Adam(model.parameters(), lr=cfg.lr_start)
    decay = cfg.lr_end / cfg.lr_start
    sched = torch.optim.lr_scheduler.LambdaLR(
        adam, lambda e: 1.0 + (decay - 1.0) * min(e, cfg.epochs) / cfg.epochs
    )
    for _ in range(cfg.epochs):
        adam.zero_grad()
        loss = loss_fn()
        loss.backward()
        adam.step()
        sched.step()
        history.append(loss.item())

    if cfg.lbfgs_iters > 0:
        lbfgs = torch.optim.LBFGS(
            model.parameters(), max_iter=cfg.lbfgs_iters, history_size=50,
            tolerance_grad=1e-12, tolerance_change=1e-14, line_search_fn="strong_wolfe",
        )

        def closure() -> Tensor:
            lbfgs.zero_grad()
            loss = loss_fn()
            loss.backward()
            history.append(loss.item())
            return loss

        lbfgs.step(closure)

    return model, history


def predict(model: PINN, t: np.ndarray) -> np.ndarray:
    device = next(model.parameters()).device
    tt = torch.as_tensor(t, dtype=torch.float32, device=device).reshape(-1, 1)
    with torch.no_grad():
        return model(tt).cpu().numpy().astype(np.float64)


def evaluate(model: PINN, cfg: Config) -> pd.DataFrame:
    t, ys = reference_trajectory(cfg, n=1001)
    return compute_error_metrics(ys, predict(model, t))


def save_results(model: PINN, history: list[float], cfg: Config) -> pd.DataFrame:
    results = Path(cfg.results_dir)
    results.mkdir(parents=True, exist_ok=True)
    ckpt = Path(cfg.ckpt_dir)
    ckpt.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), ckpt / "pinn.pt")

    t, ys = reference_trajectory(cfg, n=1001)
    pred = predict(model, t)
    metrics = compute_error_metrics(ys, pred)
    metrics.to_csv(results / "metrics.csv", index=False)
    mse = float(np.mean((pred - ys) ** 2))

    # Single paper1-style figure: solution vs reference | error (+MSE) | loss (+L-BFGS start).
    fig, ax = plt.subplots(1, 3, figsize=(15, 4))
    colors = ("tab:blue", "tab:orange", "tab:green")
    for j, c in enumerate(colors):
        ax[0].plot(t, pred[:, j], color=c, label=STATE[j])
        ax[0].plot(t, ys[:, j], "--", color=c, label=f"{STATE[j]} (ref)")
    ax[0].set_xlabel("t")
    ax[0].set_ylabel(", ".join(STATE))
    ax[0].set_title("Neural network solution vs reference")
    ax[0].legend(loc="best", ncol=2)
    ax[0].grid(alpha=0.3)

    for j, c in enumerate(colors):
        ax[1].plot(t, pred[:, j] - ys[:, j], color=c, label=f"{STATE[j]} - {STATE[j]}(ref)")
    ax[1].set_xlabel("t")
    ax[1].set_ylabel("error")
    ax[1].set_title(f"MSE: {mse:.2e}")
    ax[1].legend(loc="best")
    ax[1].grid(alpha=0.3)

    ax[2].semilogy(history)
    if cfg.lbfgs_iters > 0:
        ax[2].axvline(cfg.epochs, color="red", linestyle="--", label="L-BFGS start")
        ax[2].legend(loc="best")
    ax[2].set_xlabel("iteration")
    ax[2].set_ylabel("loss")
    ax[2].set_title("Epoch loss")
    ax[2].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(results / "results.png", dpi=150)
    plt.close(fig)

    return metrics


def main(cfg: Config | None = None) -> tuple[PINN, list[float], pd.DataFrame]:
    cfg = cfg or Config()
    model, history = train(cfg)
    metrics = save_results(model, history, cfg)
    print(metrics.to_string(index=False))
    return model, history, metrics


if __name__ == "__main__":
    main()
