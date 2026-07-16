"""Generate brand-styled Lorenz-1960 figures for the defense deck/poster.

Imports the LOCKED baseline solver (does not modify it) and renders clean,
transparent-background figures in the deck's visual identity, in both a
dark variant (for the slides) and a light variant (for the poster).

Output: defense/web/assets/*.png
"""
from __future__ import annotations
import sys, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src", "baseline"))
import lorenz1960_baseline as lb  # noqa: E402

ASSETS = os.path.join(HERE, "assets")
os.makedirs(ASSETS, exist_ok=True)

# brand palette
CX, CY, CZ = "#5B8CFF", "#FF6A3D", "#1FC8AC"   # x indigo, y coral, z teal
THEMES = {
    "dark":  dict(text="#C7CEDB", grid="#FFFFFF", galpha=0.09, spine="#3A4straight"),
    "light": dict(text="#1B2440", grid="#1B2440", galpha=0.10, spine="#C2C9DA"),
}
# fix a typo-safe spine
THEMES["dark"]["spine"] = "#46506A"


def _style(ax, th):
    ax.set_facecolor("none")
    for s in ax.spines.values():
        s.set_color(th["spine"]); s.set_linewidth(1.0)
    ax.tick_params(colors=th["text"], labelsize=12, length=4)
    ax.grid(True, color=th["grid"], alpha=th["galpha"], linewidth=0.8)
    ax.xaxis.label.set_color(th["text"]); ax.yaxis.label.set_color(th["text"])


def _save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), dpi=400, transparent=True,
                bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)


# ---- data (locked baseline) -------------------------------------------------
cfg = lb.DEFAULT_CONFIG
ts, ys = lb.rk4_solve(lb.lorenz1960_rhs, cfg.t_span, cfg.initial_state, cfg.rk4_step)
t_ref, y_ref, _ = lb.solve_lorenz1960_scipy(config=cfg, t_eval=ts)
err = ys - y_ref
mse = float(np.mean(err**2))
print(f"solver-agreement MSE = {mse:.3e}")

cfg_long = lb.Lorenz1960Config(t_span=(0.0, 50.0), n_eval=6001)
tl, yl, _ = lb.solve_lorenz1960_scipy(config=cfg_long)

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 13,
                     "svg.fonttype": "none"})


def make(theme):
    th = THEMES[theme]
    sfx = theme

    # 1) solution x,y,z vs t on [0,1]
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    for col, c, lab in zip(ys.T, (CX, CY, CZ), ("x(t)", "y(t)", "z(t)")):
        ax.plot(ts, col, color=c, lw=3.2, label=lab, solid_capstyle="round")
    ax.set_xlabel("t"); ax.set_ylabel("state")
    leg = ax.legend(frameon=False, fontsize=12, labelcolor=th["text"], ncol=3,
                    loc="upper center", bbox_to_anchor=(0.5, 1.12), handlelength=1.4)
    _style(ax, th)
    _save(fig, f"fig_solution_{sfx}.png")

    # 2) validation: pointwise solver-agreement error vs t
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    for col, c, lab in zip(err.T, (CX, CY, CZ), (r"$\delta x$", r"$\delta y$", r"$\delta z$")):
        ax.plot(ts, col, color=c, lw=2.6, label=lab, solid_capstyle="round")
    ax.axhline(0, color=th["text"], lw=0.8, alpha=0.4)
    ax.set_xlabel("t"); ax.set_ylabel("RK4 − SciPy")
    ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    ax.yaxis.get_offset_text().set_color(th["text"])
    ax.legend(frameon=False, fontsize=12, labelcolor=th["text"], ncol=3,
              loc="upper center", bbox_to_anchor=(0.5, 1.12), handlelength=1.4)
    _style(ax, th)
    _save(fig, f"fig_validation_{sfx}.png")

    # 3) dynamics: long-term oscillation on [0,50]
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    for col, c, lab in zip(yl.T, (CX, CY, CZ), ("x", "y", "z")):
        ax.plot(tl, col, color=c, lw=2.0, label=lab, solid_capstyle="round")
    ax.set_xlabel("t"); ax.set_ylabel("state")
    ax.legend(frameon=False, fontsize=12, labelcolor=th["text"], ncol=3,
              loc="upper center", bbox_to_anchor=(0.5, 1.13), handlelength=1.4)
    _style(ax, th)
    _save(fig, f"fig_dynamics_{sfx}.png")

    # 4) hero phase portrait: a FAMILY of nested orbits (perturbed ICs),
    #    decorative line-art, no axes
    fig, ax = plt.subplots(figsize=(6.4, 6.4))
    base = np.array(cfg.initial_state, dtype=float)
    scales = np.linspace(0.55, 1.45, 9)
    grad = [CX, CY, CZ]
    for i, s in enumerate(scales):
        ic = base * s
        c = lb.Lorenz1960Config(initial_state=tuple(ic), t_span=(0.0, 50.0), n_eval=4000)
        try:
            _, yy, _ = lb.solve_lorenz1960_scipy(config=c)
        except Exception:
            continue
        col = grad[i % 3]
        ax.plot(yy[:, 1], yy[:, 2], color=col, lw=1.7,
                alpha=0.30 + 0.50 * (i / (len(scales) - 1)), solid_capstyle="round")
    ax.axis("off"); ax.set_aspect("equal", adjustable="datalim")
    _save(fig, f"hero_phase_{sfx}.png")


for t in ("dark", "light"):
    make(t)
print("done ->", ASSETS)
