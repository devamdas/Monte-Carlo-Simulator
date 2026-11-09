import matplotlib
matplotlib.use("Agg")  # draw straight to image files, no window
import matplotlib.pyplot as plt

plt.rcParams["text.parse_math"] = False  # treat $ as a dollar sign, not the start of a math formula

from src.metrics import percentile_path, ruin_curve, median_result

# One fixed color per strategy so it looks the same in every chart
COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
SURFACE = "#fcfcfb"
TEXT = "#0b0b0b"
MUTED = "#52514e"
GRID = "#e4e3df"


def _style(ax):
    ax.set_facecolor(SURFACE)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=9)


def _new_figure(width=9, height=5.5, rows=1):
    fig, axes = plt.subplots(rows, 1, figsize=(width, height), facecolor=SURFACE, sharex=True)
    for ax in (axes if rows > 1 else [axes]):
        _style(ax)
    return fig, axes


def _label_line_ends(ax, curves: dict):
    "Writes each strategy's name just past the right end of its line, nudged apart so labels don't overlap"
    last_x = max(len(curve) for curve in curves.values()) - 1
    ax.set_xlim(0, last_x * 1.18)  # leave room on the right for the labels
    low, high = ax.get_ylim()
    gap = (high - low) * 0.045
    # Lines that end at the same value share one label
    groups = {}
    for name, curve in curves.items():
        groups.setdefault(round(curve[-1], 6), []).append(name)
    previous = None
    for value in sorted(groups):
        y = value if previous is None else max(value, previous + gap)
        previous = y
        ax.text(last_x * 1.015, y, "\n".join(groups[value]), va="center", fontsize=9, color=TEXT)


def _moving_average(values: list, window: int) -> list:
    "Centered average over `window` points, shrinking at the edges"
    half = window // 2
    smoothed = []
    for i in range(len(values)):
        chunk = values[max(0, i - half):i + half + 1]
        smoothed.append(sum(chunk) / len(chunk))
    return smoothed


def plot_median_paths(results: dict, start_bankroll: float, title: str, path: str):
    "Median bankroll over time for each strategy"
    fig, ax = _new_figure()
    curves = {}
    for color, (name, paths) in zip(COLORS, results.items()):
        # The raw median zigzags because bankrolls land on a grid of possible values; smoothing shows the trend
        curves[name] = _moving_average(percentile_path(paths, 50), 15)
        ax.plot(curves[name], color=color, linewidth=2, label=name)
    ax.axhline(start_bankroll, color=MUTED, linewidth=1, linestyle="--")
    ax.set_title(title, loc="left", color=TEXT, fontsize=12)
    ax.set_xlabel("Bet number", color=MUTED)
    ax.set_ylabel("Median bankroll ($, 15-bet average)", color=MUTED)
    ax.legend(frameon=False, fontsize=9, loc="best", labelcolor=TEXT)
    _label_line_ends(ax, curves)
    fig.tight_layout()
    fig.savefig(path, dpi=150, facecolor=SURFACE)
    plt.close(fig)


def plot_ruin_curves(results: dict, min_bet: float, title: str, path: str):
    "Share of simulations that have gone broke by each bet number"
    fig, ax = _new_figure()
    curves = {}
    for color, (name, paths) in zip(COLORS, results.items()):
        curves[name] = [100 * share for share in ruin_curve(paths, min_bet)]
        ax.plot(curves[name], color=color, linewidth=2, label=name)
    ax.set_ylim(0, 100)
    ax.set_title(title, loc="left", color=TEXT, fontsize=12)
    ax.set_xlabel("Bet number", color=MUTED)
    ax.set_ylabel("Simulations ruined (%)", color=MUTED)
    ax.legend(frameon=False, fontsize=9, loc="best", labelcolor=TEXT)
    _label_line_ends(ax, curves)
    fig.tight_layout()
    fig.savefig(path, dpi=150, facecolor=SURFACE)
    plt.close(fig)


def plot_final_distributions(results: dict, start_bankroll: float, title: str, path: str):
    "One histogram of final bankrolls per strategy, stacked vertically on a shared x axis"
    fig, axes = _new_figure(height=1.6 * len(results) + 1, rows=len(results))
    finals = {name: [p[-1] for p in paths] for name, paths in results.items()}
    upper = max(sorted(values)[int(len(values) * 0.98)] for values in finals.values())
    bins = [upper * i / 40 for i in range(41)]
    for ax, color, (name, values) in zip(axes, COLORS, finals.items()):
        clipped = [min(v, upper) for v in values]
        ax.hist(clipped, bins=bins, color=color, edgecolor=SURFACE, linewidth=1)
        ax.axvline(start_bankroll, color=MUTED, linewidth=1, linestyle="--")
        median = median_result(values)
        ax.axvline(median, color=TEXT, linewidth=1.5)
        ax.text(0.99, 0.85, f"{name}   median ${median:,.0f}", transform=ax.transAxes,
                ha="right", va="top", fontsize=9, color=TEXT)
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
    axes[0].set_title(title, loc="left", color=TEXT, fontsize=12)
    axes[-1].set_xlabel("Final bankroll ($)   ·   dashed = starting bankroll, solid = median, top 2% grouped at right edge", color=MUTED, fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=150, facecolor=SURFACE)
    plt.close(fig)
