"""
generate_charts.py — NiCE-branded SVG charts for the demo page.

Run from the repo root:
    python3 generate_charts.py

Outputs:
    site/chart_recovery.svg            — stacked horizontal bar: recovery composition per dataset
    site/chart_progression.svg         — vertical bar: synthetic speech cumulative stage progression
    site/chart_progression_human.svg   — vertical bar: human speech cumulative stage progression
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Output directory ──────────────────────────────────────────────────────────
OUT_DIR = os.path.join(os.path.dirname(__file__), "site")

# ── NiCE brand colors ─────────────────────────────────────────────────────────
CHARCOAL   = "#21212b"
BLUE       = "#3694fc"
ELEC_BLUE  = "#025afb"
EMERALD    = "#00e2a0"
EMTINT     = "#9ceed2"
TEAL       = "#36ead0"
CORAL      = "#ff5b8a"
CORAL_TINT = "#f3b1c4"
GRAY_LIGHT = "#e0ddd8"   # remaining misses
WHITE      = "#ffffff"

# Segment colors: baseline / text repair / re-decode / remaining
SEG_COLORS = [CHARCOAL, EMERALD, CORAL, GRAY_LIGHT]
SEG_LABELS = ["v11 baseline", "Text repair", "Re-decode", "Remaining misses"]

matplotlib.rcParams.update({
    "font.family":     "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans"],
    "font.size":       11,
    "axes.spines.top":    False,
    "axes.spines.right":  False,
    "axes.spines.left":   False,
    "figure.facecolor":   WHITE,
    "axes.facecolor":     WHITE,
    "text.color":         CHARCOAL,
    "axes.labelcolor":    CHARCOAL,
    "xtick.color":        CHARCOAL,
    "ytick.color":        CHARCOAL,
})


# ── Chart 1: Recovery composition (stacked horizontal bars) ───────────────────
def chart_recovery():
    """
    Stacked horizontal bar chart showing how each fix type contributes to
    total recall, for both the synthetic and human speech datasets.

    Values (pp): baseline | text repair gain | re-decode gain | remaining
    All segments sum to 100%. The remaining misses segment is unlabelled to
    keep the focus on the achieved recall figure at the end of each bar.
    """
    datasets = [
        "Synthetic speech\n(HealthDial, TTS-generated, n=139)",
        "Human speech\n(ACCES DR1, real patients, n=65)",
    ]

    # [baseline, text_repair_gain, redecode_gain, remaining]
    data = [
        [69.1, 26.6,  2.9,  1.4],   # Synthetic speech
        [15.4, 53.8, 13.9, 16.9],   # Human speech
    ]

    fig, ax = plt.subplots(figsize=(10, 3.2))
    fig.subplots_adjust(left=0.26, right=0.98, top=0.82, bottom=0.22)

    y = np.arange(len(datasets))
    bar_h = 0.42

    lefts = np.zeros(len(datasets))
    for i, (color, label) in enumerate(zip(SEG_COLORS, SEG_LABELS)):
        vals = [row[i] for row in data]
        ax.barh(y, vals, bar_h, left=lefts, color=color, label=label, linewidth=0)

        # Label all segments except remaining misses (last segment, index 3)
        if i < 3:
            for j, (val, left) in enumerate(zip(vals, lefts)):
                if val >= 6:
                    txt_color = WHITE if color == CHARCOAL else CHARCOAL
                    ax.text(left + val / 2, y[j], f"{val:.1f}pp",
                            ha="center", va="center",
                            fontsize=9, fontweight="500", color=txt_color)
        lefts += vals

    # Final recall callout at end of bar
    final_recalls = [sum(row[:3]) for row in data]
    for j, (recall, ypos) in enumerate(zip(final_recalls, y)):
        ax.text(recall + 0.5, ypos, f"{recall:.1f}%",
                va="center", ha="left", fontsize=10,
                fontweight="600", color=ELEC_BLUE)

    ax.set_yticks(y)
    ax.set_yticklabels(datasets, fontsize=10)
    ax.set_xlim(0, 108)
    ax.set_xlabel("Drug name recall (%)", fontsize=10)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{int(v)}%"))
    ax.axvline(100, color=CHARCOAL, linewidth=0.6, linestyle="--", alpha=0.3)
    ax.spines["bottom"].set_color(GRAY_LIGHT)
    ax.tick_params(axis="x", length=0, pad=4)
    ax.tick_params(axis="y", length=0, pad=6)

    ax.set_title("Drug name recovery — how each fix contributes",
                 fontsize=12, fontweight="600", color=CHARCOAL,
                 loc="left", pad=10)

    ax.legend(handles=[
        mpatches.Patch(color=c, label=l)
        for c, l in zip(SEG_COLORS, SEG_LABELS)
    ], loc="lower center", bbox_to_anchor=(0.5, -0.55),
       ncol=4, frameon=False, fontsize=9)

    path = os.path.join(OUT_DIR, "chart_recovery.svg")
    fig.savefig(path, format="svg", bbox_inches="tight", transparent=False)
    plt.close(fig)
    print(f"  wrote {path}")


# ── Shared helper for progression bar charts ──────────────────────────────────
def _draw_progression(ax, stages, recalls, deltas, bar_colors):
    x = np.arange(len(stages))
    ax.bar(x, recalls, width=0.52, color=bar_colors, linewidth=0, zorder=3)

    for xi, val in zip(x, recalls):
        txt_color = WHITE if val < 40 else CHARCOAL
        ax.text(xi, val - 3.5, f"{val:.1f}%",
                ha="center", va="top", fontsize=10,
                fontweight="600", color=txt_color, zorder=4)

    for xi, (val, delta) in enumerate(zip(recalls, deltas)):
        if delta:
            ax.text(xi, val + 1.2, delta,
                    ha="center", va="bottom", fontsize=9,
                    fontweight="500", color=ELEC_BLUE, zorder=4)

    ax.set_xticks(x)
    ax.set_xticklabels(stages, fontsize=9.5)
    ax.set_ylim(0, 108)
    ax.set_ylabel("Drug name recall (%)", fontsize=10)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{int(v)}%"))
    ax.axhline(100, color=CHARCOAL, linewidth=0.6, linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color=GRAY_LIGHT, linewidth=0.8, zorder=0)
    ax.spines["bottom"].set_color(GRAY_LIGHT)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="x", length=0, pad=6)
    ax.tick_params(axis="y", length=0, pad=4)


# ── Chart 2: Synthetic speech stage progression ───────────────────────────────
def chart_progression_synthetic():
    stages = [
        "v11\nbaseline",
        "Text repair\n(original)",
        "+ 4-word\nwindow",
        "+ Confusion\nbypass",
        "+ Audio\nre-decode",
    ]
    recalls = [69.1, 89.9, 93.5, 95.7, 98.6]
    deltas  = [None, "+20.9pp", "+3.6pp", "+2.2pp", "+2.9pp"]
    colors  = [CHARCOAL, EMERALD, EMTINT, EMTINT, CORAL]

    fig, ax = plt.subplots(figsize=(9, 4.2))
    fig.subplots_adjust(left=0.08, right=0.98, top=0.82, bottom=0.20)
    _draw_progression(ax, stages, recalls, deltas, colors)
    ax.set_title("Synthetic speech — cumulative recall by engineering stage",
                 fontsize=12, fontweight="600", color=CHARCOAL, loc="left", pad=10)

    path = os.path.join(OUT_DIR, "chart_progression.svg")
    fig.savefig(path, format="svg", bbox_inches="tight", transparent=False)
    plt.close(fig)
    print(f"  wrote {path}")


# ── Chart 3: Human speech stage progression ───────────────────────────────────
def chart_progression_human():
    stages = [
        "v11\nbaseline",
        "Text repair\n(original)",
        "+ Confusion\nindex",
        "+ More\nconfusions",
        "+ Phrase-prefix\nre-decode",
    ]
    recalls = [15.4, 26.2, 61.5, 69.2, 83.1]
    deltas  = [None, "+10.8pp", "+35.3pp", "+7.7pp", "+13.9pp"]
    colors  = [CHARCOAL, EMERALD, EMTINT, EMTINT, CORAL]

    fig, ax = plt.subplots(figsize=(9, 4.2))
    fig.subplots_adjust(left=0.08, right=0.98, top=0.82, bottom=0.20)
    _draw_progression(ax, stages, recalls, deltas, colors)
    ax.set_title("Human speech — cumulative recall by engineering stage",
                 fontsize=12, fontweight="600", color=CHARCOAL, loc="left", pad=10)

    path = os.path.join(OUT_DIR, "chart_progression_human.svg")
    fig.savefig(path, format="svg", bbox_inches="tight", transparent=False)
    plt.close(fig)
    print(f"  wrote {path}")


def chart_domain_comparison():
    """
    Horizontal grouped bar chart comparing v11 baseline vs after-repair recall
    across all five benchmarked domains (medical + non-medical).
    Demonstrates chassis generality at a glance.
    """
    domains   = ['Synthetic speech\n(medical)', 'Human speech\n(medical)',
                 'Legal\n(Oyez SCOTUS)', 'Financial\n(SPGISpeech)',
                 'Contact center\n(Apptek AU)']
    baseline  = [69.1, 15.4, 85.2, 85.3, 92.6]
    repaired  = [98.6, 83.1, 95.8, 93.8, 96.3]
    gains     = [r - b for r, b in zip(repaired, baseline)]

    # Color: charcoal for baseline, gradient of blues/teals for repaired
    rep_colors = [EMERALD, EMERALD, BLUE, BLUE, TEAL]

    fig, ax = plt.subplots(figsize=(10, 4.2))
    fig.subplots_adjust(left=0.26, right=0.92, top=0.85, bottom=0.12)

    y      = np.arange(len(domains))
    height = 0.32

    ax.barh(y + height/2, baseline, height, color=CHARCOAL, label='v11 baseline', linewidth=0)
    for i, (val, color) in enumerate(zip(repaired, rep_colors)):
        ax.barh(y[i] - height/2, val, height, color=color, linewidth=0,
                label='After repair' if i == 0 else '')

    # Gain labels at end of repaired bar
    for i, (rep, gain) in enumerate(zip(repaired, gains)):
        ax.text(rep + 0.5, y[i] - height/2, f'+{gain:.1f}pp',
                va='center', ha='left', fontsize=9, fontweight='600',
                color=rep_colors[i])

    ax.set_yticks(y)
    ax.set_yticklabels(domains, fontsize=9.5)
    ax.set_xlim(0, 108)
    ax.set_xlabel('Term recall (%)', fontsize=10)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f'{int(v)}%'))
    ax.axvline(100, color=CHARCOAL, linewidth=0.6, linestyle='--', alpha=0.3)
    ax.spines['bottom'].set_color(GRAY_LIGHT)
    ax.set_axisbelow(True)
    ax.xaxis.grid(True, color=GRAY_LIGHT, linewidth=0.8, zorder=0)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='x', length=0, pad=4)
    ax.tick_params(axis='y', length=0, pad=6)

    ax.set_title('Recall before and after repair — across all domains',
                 fontsize=12, fontweight='600', color=CHARCOAL, loc='left', pad=10)

    # Legend placed top-right in the figure header area (above the axes)
    legend_handles = [
        mpatches.Patch(color=CHARCOAL, label='v11 baseline'),
        mpatches.Patch(color=EMERALD,  label='After repair'),
    ]
    fig.legend(handles=legend_handles, loc='upper right',
               bbox_to_anchor=(0.92, 0.97),
               ncol=1, frameon=False, fontsize=9)

    path = os.path.join(OUT_DIR, 'chart_domain_comparison.svg')
    fig.savefig(path, format='svg', bbox_inches='tight', transparent=False)
    plt.close(fig)
    print(f'  wrote {path}')


if __name__ == "__main__":
    print("Generating charts...")
    chart_recovery()
    chart_progression_synthetic()
    chart_progression_human()
    chart_domain_comparison()
    print("Done.")
