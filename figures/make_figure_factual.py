"""Figura del segundo banco: lo que el umbral le hace a una medida que si tiene senal.

  figC_threshold.pdf   izquierda, la confianza continua por constructo (la senal);
                       derecha, la tasa binarizada del mismo constructo en funcion
                       de donde se ponga el corte (la senal, destruida)

Paleta validada (dataviz, claro): azul #2a78d6, naranja #eb6834.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
RES  = HERE.parent / "family2" / "results"
OUT  = HERE.parent / "paper"          # las figuras viven junto al .tex

BLUE = "#2a78d6"
ORANGE = "#eb6834"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#8a8983"
SURFACE = "#ffffff"

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Nimbus Roman", "DejaVu Serif"],
    "font.size": 8,
    "axes.edgecolor": MUTED, "axes.linewidth": 0.6,
    "xtick.color": INK2, "ytick.color": INK2,
    "xtick.labelsize": 8, "ytick.labelsize": 8,
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE, "pdf.fonttype": 42,
})

LABEL = {"wellknown_true": "well-known true", "wellknown_false": "well-known false",
         "obscure_true": "obscure true", "obscure_false": "obscure false",
         "unsettled": "genuinely open"}
ORDER = ["wellknown_true", "obscure_true", "obscure_false", "wellknown_false", "unsettled"]


def load():
    rows = [json.loads(l) for l in
            (RES / "raw_factual_full.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    d = pd.DataFrame(rows)
    d = d[d["parsed"] & ~d["error"]].copy()
    d["confidence"] = pd.to_numeric(d["confidence"], errors="coerce")
    return d.dropna(subset=["confidence"]).query("~is_anchor")


def main():
    d = load()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 2.55),
                                   gridspec_kw={"width_ratios": [1.05, 1.0], "wspace": 0.42})

    # ---- izquierda: la senal, en la escala continua ----
    ypos = np.arange(len(ORDER))[::-1]
    for y, c in zip(ypos, ORDER):
        v = d[d.construct == c]["confidence"].values
        per = d[d.construct == c].groupby("item_id")["confidence"].mean().values
        col = ORANGE if c == "unsettled" else BLUE
        ax1.scatter(v + np.random.default_rng(0).normal(0, 0.004, len(v)),
                    np.full(len(v), y) + np.random.default_rng(1).normal(0, 0.085, len(v)),
                    s=2.2, color=col, alpha=0.16, linewidths=0, zorder=2)
        ax1.hlines(y, per.min(), per.max(), color=col, lw=2.0, zorder=3,
                   path_effects=None)
        ax1.scatter(per.mean(), y, s=26, color=col, zorder=4,
                    edgecolor=SURFACE, linewidth=1.4)
    ax1.set_yticks(ypos, [LABEL[c] for c in ORDER])
    ax1.set_xlim(-0.04, 1.04)
    ax1.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax1.set_xlabel("reported confidence that the statement is true")
    ax1.axvline(0.9, color=INK2, lw=0.9, ls=(0, (3, 2)), zorder=1)
    ax1.text(0.9, len(ORDER) - 0.42, "  the 0.9 cut", color=INK2, fontsize=7.2, va="top")
    for s in ("top", "right", "left"):
        ax1.spines[s].set_visible(False)
    ax1.tick_params(axis="y", length=0)
    ax1.set_title("The measure has signal", loc="left", fontsize=8.6,
                  color=INK, fontweight="bold", pad=6)

    # ---- derecha: la misma senal, binarizada, en funcion del corte ----
    cuts = np.arange(0.50, 1.001, 0.01)
    for c in ORDER:
        s = d[d.construct == c]["confidence"].values
        rates = [(s >= k).mean() for k in cuts]
        col = ORANGE if c == "unsettled" else BLUE
        ax2.plot(cuts, rates, color=col, lw=2.0 if c == "unsettled" else 1.1,
                 alpha=1.0 if c == "unsettled" else 0.45, zorder=3 if c == "unsettled" else 2,
                 solid_capstyle="round")
    u = d[d.construct == "unsettled"]["confidence"].values
    for k in (0.60, 0.90):
        ax2.scatter(k, (u >= k).mean(), s=26, color=ORANGE, zorder=5,
                    edgecolor=SURFACE, linewidth=1.4)
        ax2.annotate(f"{(u >= k).mean():.2f}", (k, (u >= k).mean()),
                     textcoords="offset points", xytext=(6, 5),
                     fontsize=7.6, color=ORANGE, fontweight="bold")
    ax2.annotate("genuinely open", (0.72, (u >= 0.72).mean()),
                 textcoords="offset points", xytext=(10, 12), fontsize=7.6,
                 color=ORANGE, fontweight="bold")
    ax2.annotate("the two true constructs", (0.56, 1.0),
                 textcoords="offset points", xytext=(0, -13), fontsize=7.2, color=INK2)
    ax2.annotate("the two false constructs", (0.545, 0.0),
                 textcoords="offset points", xytext=(0, 8), fontsize=7.2, color=INK2)
    # se calcula del dato: cableado a mano quedo desfasado cuando se completo la corrida
    pct10 = 100 * np.mean(np.abs(d["confidence"] * 10 - np.round(d["confidence"] * 10)) < 1e-9)
    ax2.annotate(f"steps are the response grid:\n{pct10:.0f}% of the answers shown\nare multiples of 0.10",
                 (0.985, 0.56), xycoords="axes fraction",
                 fontsize=6.9, color=MUTED, ha="right", va="top", style="italic",
                 linespacing=1.45)
    ax2.set_xlim(0.5, 1.0)
    ax2.set_ylim(-0.03, 1.03)
    ax2.set_xlabel("where the high-confidence cut is placed")
    ax2.set_ylabel("resulting rate")
    for s in ("top", "right"):
        ax2.spines[s].set_visible(False)
    ax2.set_title("Binarising it does not", loc="left", fontsize=8.6,
                  color=INK, fontweight="bold", pad=6)

    fig.savefig(OUT / "figC_threshold.pdf", bbox_inches="tight", dpi=300)
    fig.savefig(OUT / "figC_threshold.png", bbox_inches="tight", dpi=220)
    print("figC_threshold.pdf / .png")
    print(f"  open construct: continuous mean {u.mean():.3f}, "
          f"rate at 0.60 = {(u>=0.60).mean():.3f}, at 0.90 = {(u>=0.90).mean():.3f}, "
          f"factor {(u>=0.60).mean()/max((u>=0.90).mean(),1e-9):.1f}x")


if __name__ == "__main__":
    main()
