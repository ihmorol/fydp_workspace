"""Train the Lorenz-1960 PINN, evaluate against the locked baseline, save results."""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
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
    t0, tf = cfg.t_span
    return torch.linspace(t0, tf, cfg.n_collocation, device=device).reshape(-1, 1)


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

    plt.figure()
    plt.semilogy(history)
    plt.xlabel("iteration")
    plt.ylabel("residual loss")
    plt.title("PINN convergence (Adam + L-BFGS)")
    plt.tight_layout()
    plt.savefig(results / "convergence.png", dpi=150)
    plt.close()

    fig, axes = plt.subplots(3, 1, figsize=(8, 8), sharex=True)
    for j, ax in enumerate(axes):
        ax.plot(t, ys[:, j], "k--", label="RK4/SciPy")
        ax.plot(t, pred[:, j], label="PINN")
        ax.set_ylabel(STATE[j])
        ax.legend(loc="best")
    axes[-1].set_xlabel("t")
    fig.suptitle("PINN vs baseline")
    fig.tight_layout()
    fig.savefig(results / "solution.png", dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(3, 1, figsize=(8, 8), sharex=True)
    for j, ax in enumerate(axes):
        ax.plot(t, np.abs(pred[:, j] - ys[:, j]))
        ax.set_ylabel(f"|d{STATE[j]}|")
    axes[-1].set_xlabel("t")
    fig.suptitle("Absolute error vs t")
    fig.tight_layout()
    fig.savefig(results / "error.png", dpi=150)
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
