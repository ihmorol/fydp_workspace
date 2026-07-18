"""From-scratch PyTorch PINN for the Lorenz-1960 ODE system."""
from __future__ import annotations

import torch
from torch import Tensor, nn

from .config import Config

_ACT = {"tanh": nn.Tanh, "relu": nn.ReLU, "sigmoid": nn.Sigmoid, "gelu": nn.GELU, "swish": nn.SiLU}


class PINN(nn.Module):
    def __init__(self, cfg: Config) -> None:
        super().__init__()
        act = _ACT[cfg.activation]
        layers: list[nn.Module] = [nn.Linear(1, cfg.width), act()]
        for _ in range(cfg.depth - 1):
            layers += [nn.Linear(cfg.width, cfg.width), act()]
        layers.append(nn.Linear(cfg.width, 3))
        self.net = nn.Sequential(*layers)

        for m in self.net:
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                nn.init.zeros_(m.bias)

        self.register_buffer("u0", torch.tensor([cfg.initial_state], dtype=torch.float32))
        self.register_buffer("coeffs", torch.as_tensor(cfg.coefficients, dtype=torch.float32).reshape(1, 3))
        self.t0, self.tf = float(cfg.t_span[0]), float(cfg.t_span[1])

    def forward(self, t: Tensor) -> Tensor:
        g = (t - self.t0) / (self.tf - self.t0)
        return self.u0 + g * self.net(t)


def ode_residual(u: Tensor, dudt: Tensor, coeffs) -> Tensor:
    c = torch.as_tensor(coeffs, dtype=u.dtype, device=u.device).reshape(3)
    x, y, z = u[:, 0], u[:, 1], u[:, 2]
    f = torch.stack([c[0] * y * z, c[1] * x * z, c[2] * x * y], dim=1)
    return dudt - f


def residual(model: PINN, t: Tensor, create_graph: bool = True) -> Tensor:
    u = model(t)
    cols = []
    for j in range(u.shape[1]):
        grad = torch.autograd.grad(u[:, j].sum(), t, create_graph=create_graph, retain_graph=True)[0]
        cols.append(grad[:, 0])
    dudt = torch.stack(cols, dim=1)
    return ode_residual(u, dudt, model.coeffs)


def residual_magnitude(model: PINN, t: Tensor) -> Tensor:
    # Adaptivity never backprops, so avoid retaining a higher-order graph.
    return residual(model, t, create_graph=False).detach().pow(2).sum(dim=1).sqrt()


def pinn_loss(model: PINN, t: Tensor) -> Tensor:
    return residual(model, t).pow(2).mean()
