"""Adaptive collocation sampling (RAR, RAD) from PinnDE paper, section 2.4."""
from __future__ import annotations

import torch
from torch import Tensor

from .config import Config
from .pinn import residual_magnitude


def make_grid(cfg: Config, device) -> Tensor:
    t0, tf = cfg.t_span
    return torch.linspace(t0, tf, cfg.n_collocation, device=device).reshape(-1, 1)


def _uniform_pool(cfg: Config, device, n: int) -> Tensor:
    t0, tf = cfg.t_span
    return (t0 + (tf - t0) * torch.rand(n, 1, device=device)).requires_grad_(True)


def resample(model, cfg: Config, device, current: Tensor) -> Tensor:
    if cfg.adapt == "grid":
        return current

    if cfg.adapt == "rar":
        pool = _uniform_pool(cfg, device, 10 * cfg.n_collocation)
        eps = residual_magnitude(model, pool)
        idx = torch.topk(eps, cfg.n_add).indices
        picked = pool[idx].detach()
        return torch.cat([current, picked], dim=0)

    # rad
    pool = _uniform_pool(cfg, device, 10 * cfg.n_collocation)
    eps = residual_magnitude(model, pool)
    p = eps / eps.mean() + 1.0
    idx = torch.multinomial(p, cfg.n_collocation, replacement=True)
    return pool[idx].detach()
