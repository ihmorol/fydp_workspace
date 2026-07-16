from __future__ import annotations

from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch


OUTPUT_DIR = Path(__file__).resolve().parents[2] / "paper"


def _style_axis(ax: plt.Axes) -> None:
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


def _entity_box(ax, xy, width, height, text, *, facecolor="#f0f0f0"):
    box = mpatches.FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=1.5,
        edgecolor="black",
        facecolor=facecolor,
    )
    ax.add_patch(box)
    ax.text(
        xy[0] + width / 2,
        xy[1] + height / 2,
        text,
        ha="center",
        va="center",
        fontsize=11,
        fontweight="bold",
    )


def _system_box(ax, xy, width, height, text):
    box = mpatches.FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.05,rounding_size=0.12",
        linewidth=2.0,
        edgecolor="black",
        facecolor="#ffffff",
    )
    ax.add_patch(box)
    ax.text(
        xy[0] + width / 2,
        xy[1] + height / 2,
        text,
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
    )


def _process_circle(ax, center, radius, number, label):
    circle = mpatches.Circle(
        center,
        radius,
        linewidth=1.5,
        edgecolor="black",
        facecolor="#ffffff",
    )
    ax.add_patch(circle)
    ax.text(
        center[0],
        center[1] + 0.04,
        f"P{number}",
        ha="center",
        va="center",
        fontsize=11,
        fontweight="bold",
    )
    ax.text(
        center[0],
        center[1] - 0.08,
        label,
        ha="center",
        va="center",
        fontsize=8.5,
        wrap=True,
    )


def _arrow(ax, start, end, label=None, *, curvature=0.0, label_offset=(0.0, 0.05)):
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle="->",
        mutation_scale=14,
        linewidth=1.2,
        color="black",
        connectionstyle=f"arc3,rad={curvature}",
    )
    ax.add_patch(arrow)
    if label:
        mid_x = (start[0] + end[0]) / 2 + label_offset[0]
        mid_y = (start[1] + end[1]) / 2 + label_offset[1]
        ax.text(
            mid_x,
            mid_y,
            label,
            ha="center",
            va="center",
            fontsize=8.5,
            style="italic",
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.0},
        )


def render_context_diagram(output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5)
    _style_axis(ax)

    _entity_box(ax, (0.3, 1.75), 2.2, 1.5, "Research\nTeam")
    _system_box(ax, (4.0, 1.4), 3.0, 2.2, "ANN Research\nPipeline")
    _entity_box(ax, (8.3, 1.75), 2.4, 1.5, "Academic /\nResearch\nCommunity")

    _arrow(
        ax,
        (2.5, 2.8),
        (4.0, 2.8),
        label="configurations,\nparameters",
        curvature=0.0,
        label_offset=(0.0, 0.25),
    )
    _arrow(
        ax,
        (4.0, 2.2),
        (2.5, 2.2),
        label="trained models,\nmetrics",
        curvature=0.0,
        label_offset=(0.0, -0.3),
    )
    _arrow(
        ax,
        (7.0, 2.5),
        (8.3, 2.5),
        label="findings,\nbest architecture,\nmethodology",
        curvature=0.0,
        label_offset=(0.0, 0.35),
    )

    ax.set_title(
        "Context Diagram: ANN Research Pipeline",
        fontsize=13,
        pad=14,
    )

    fig.tight_layout()
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def render_dfd_level1(output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(13, 7.5))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7.5)
    _style_axis(ax)

    _entity_box(ax, (0.3, 5.6), 2.2, 1.2, "Research\nTeam")
    _entity_box(ax, (10.5, 0.4), 2.2, 1.2, "Academic /\nResearch\nCommunity")

    process_specs = [
        (1, (2.0, 4.0), "Generate\nReference\nSolution"),
        (2, (4.8, 4.0), "Preprocess\nData"),
        (3, (7.6, 4.0), "Train ANN\nModels"),
        (4, (10.4, 4.0), "Evaluate\nModels"),
        (5, (7.6, 1.6), "Compare &\nSelect Best\nArchitecture"),
    ]
    radius = 0.85
    for number, center, label in process_specs:
        _process_circle(ax, center, radius, number, label)

    _arrow(
        ax,
        (1.4, 5.6),
        (1.9, 4.85),
        label="parameters,\nconfigs",
        label_offset=(-0.55, 0.0),
    )

    _arrow(
        ax,
        (2.85, 4.0),
        (3.95, 4.0),
        label="(t, x, y, z)\ntrajectory",
        label_offset=(0.0, 0.28),
    )
    _arrow(
        ax,
        (5.65, 4.0),
        (6.75, 4.0),
        label="train / val\nsets",
        label_offset=(0.0, 0.28),
    )
    _arrow(
        ax,
        (8.45, 4.0),
        (9.55, 4.0),
        label="trained\nmodels",
        label_offset=(0.0, 0.28),
    )
    _arrow(
        ax,
        (10.4, 3.15),
        (8.3, 2.05),
        label="metrics\nper model",
        label_offset=(0.55, 0.25),
    )
    _arrow(
        ax,
        (8.5, 1.95),
        (10.5, 1.2),
        label="findings,\nrecommendation",
        label_offset=(0.0, 0.30),
    )

    ax.set_title(
        "Data Flow Diagram (Level 1): ANN Research Pipeline",
        fontsize=13,
        pad=14,
    )

    fig.tight_layout()
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    context_path = OUTPUT_DIR / "context_diagram.png"
    dfd_path = OUTPUT_DIR / "dfd_level1.png"

    render_context_diagram(context_path)
    render_dfd_level1(dfd_path)

    print(f"Saved: {context_path}")
    print(f"Saved: {dfd_path}")


if __name__ == "__main__":
    main()
