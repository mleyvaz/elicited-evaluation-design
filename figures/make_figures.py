"""Figuras del paper de metodo. Salida PDF vectorial.

  figA_precision.pdf   semiancho del IC95 de una tasa a nivel de constructo
                       en funcion del numero de items, con la SD entre items
                       medida en cinco fenomenos
  figB_grid.pdf        el grano al que responden los modelos: histograma de
                       T+F con la moda sobre el umbral

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
BANK = HERE.parent / "family1" / "results"
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


def load():
    rows = [json.loads(l) for l in (BANK / "raw_quad_bank.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    d = pd.DataFrame(rows)
    d = d[d["parsed"] & ~d["error"]].copy()
    for c in "TINF":
        d[c] = pd.to_numeric(d[c], errors="coerce")
    return d.dropna(subset=list("TINF"))


def figA():
    """Cuantos items hacen falta. Una serie: la curva. Las SD medidas van como marcas."""
    sd_ref = 0.211
    k = np.arange(1, 201)
    hw = 1.96 * sd_ref / np.sqrt(k)

    fig, ax = plt.subplots(figsize=(3.35, 2.5))
    ax.plot(k, hw, color=BLUE, lw=2, zorder=3)

    for kk, lab in [(1, "1 item"), (10, "10"), (69, "69")]:
        h = 1.96 * sd_ref / np.sqrt(kk)
        ax.scatter([kk], [h], s=30, facecolor=BLUE, edgecolor=SURFACE, lw=1, zorder=4)
        ax.annotate(f"{lab}\n±{h:.2f}", xy=(kk, h), xytext=(kk * 1.35, h + 0.035),
                    color=INK, fontsize=7, ha="left", va="bottom", linespacing=1.25)

    ax.axhline(0.05, color=ORANGE, lw=1.2, ls=(0, (4, 2)), zorder=2)
    ax.text(1.05, 0.058, "±0.05 target", color=ORANGE, fontsize=7, ha="left", va="bottom")

    ax.set_xscale("log")
    ax.set_xlim(0.9, 220)
    ax.set_ylim(0, 0.46)
    ax.set_xticks([1, 3, 10, 30, 100, 200])
    ax.set_xticklabels(["1", "3", "10", "30", "100", "200"])
    ax.set_xlabel("items per construct")
    ax.set_ylabel("95% CI half-width")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(color="#e8e7e3", lw=0.6, zorder=0)
    ax.set_axisbelow(True)
    fig.tight_layout(pad=0.3)
    fig.savefig(OUT / "figA_precision.pdf", bbox_inches="tight")
    plt.close(fig)
    print("figA_precision.pdf")


def figB():
    """El grano de la respuesta. Una serie; el umbral va como anotacion."""
    d = load()
    tf = (d["T"] + d["F"]).values

    fig, ax = plt.subplots(figsize=(3.35, 2.3))
    vals, counts = np.unique(np.round(tf, 4), return_counts=True)
    share = counts / counts.sum()
    ax.bar(vals, share, width=0.035, color=BLUE, edgecolor=SURFACE, lw=0.4, zorder=3)

    ax.axvline(1.0, color=ORANGE, lw=1.2, ls=(0, (4, 2)), zorder=4)
    ax.annotate("the threshold sits on\nthe modal value:\nT+F = 1.00 in 37.9%",
                xy=(1.0, 0.30), xytext=(1.18, 0.34),
                color=ORANGE, fontsize=7, ha="left", va="top", linespacing=1.3,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.7, shrinkA=2, shrinkB=2))

    ax.set_xlim(-0.05, 2.05)
    ax.set_ylim(0, 0.42)
    ax.set_xlabel("T + F, as reported")
    ax.set_ylabel("share of evaluations")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color="#e8e7e3", lw=0.6, zorder=0)
    ax.set_axisbelow(True)
    fig.tight_layout(pad=0.3)
    fig.savefig(OUT / "figB_grid.pdf", bbox_inches="tight")
    plt.close(fig)
    print("figB_grid.pdf")


if __name__ == "__main__":
    figA()
    figB()
