import numpy as np
import torch

from fydp2.config import Config, reference_trajectory
from fydp2.pinn import PINN, ode_residual


def test_hard_ic_exact():
    model = PINN(Config())
    out = model(torch.zeros(1, 1))
    expected = torch.tensor([Config().initial_state])
    assert torch.allclose(out, expected, atol=1e-6)


def test_residual_zero_on_truth():
    t, ys = reference_trajectory(Config(), n=1001)
    dudt = np.gradient(ys, t, axis=0)
    r = ode_residual(
        torch.tensor(ys, dtype=torch.float64),
        torch.tensor(dudt, dtype=torch.float64),
        Config().coefficients,
    )
    assert r[1:-1].abs().max().item() < 1e-2


def test_training_reduces_loss():
    from fydp2.train import train

    cfg = Config(epochs=100, n_collocation=101, lbfgs_iters=50, seed=0)
    _, history = train(cfg)
    assert history[-1] < 0.1 * history[0]


def test_soft_ic_trains():
    from fydp2.train import train

    cfg = Config(ic="soft", epochs=200, n_collocation=101, lbfgs_iters=50, seed=0)
    _, history = train(cfg)
    assert history[-1] < 0.1 * history[0]
