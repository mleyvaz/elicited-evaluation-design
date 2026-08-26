"""Generador de fig1_between_items, tomado del paper companion.

El fichero original produce dos figuras; aqui solo se invoca la primera, que es la
unica que este paper usa. La segunda se deja en el fichero sin llamar para no
divergir del script publicado con el companion.

ORIGINAL: Las dos figuras del paper. Salida PDF vectorial para LaTeX.

  fig1_between_items.pdf  la dispersion entre items dentro de cada fenomeno,
                          con el valor del piloto de un solo enunciado marcado
  fig2_manipulation.pdf   las tres condiciones del system message, con IC del 95%

Paleta validada (dataviz, modo claro): serie 1 azul #2a78d6, serie 2 naranja #eb6834.
Ambos pasan banda de luminosidad, suelo de croma, separacion CVD y contraste.

Uso:  python make_figures.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

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
    "axes.edgecolor": MUTED,
    "axes.linewidth": 0.6,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "pdf.fonttype": 42,
})

LABEL = {
    "ethical": "Ethical conflict",
    "paradox": "Logical paradox",
    "vagueness": "Vagueness",
    "ignorance": "Epistemic ignorance",
    "contingency": "Future contingency",
}


def per_item_strong():
    """Tasa de la escala FUERTE por item, calculada del crudo.

    El script del companion leia aqui un intermedio, fig1_per_item.json, que ningun
    script producia. Se sustituye por el calculo, verificado identico en los cinco
    constructos: items bare de los cinco fenomenos contestados, fraccion de las 18
    elicitaciones por item (6 modelos x 3 glosas) clasificadas en la escala fuerte.
    """
    import pandas as pd
    rows = [json.loads(l) for l
            in (BANK / "raw_quad_bank.jsonl").read_text(encoding="utf-8").splitlines()
            if l.strip()]
    d = pd.DataFrame(rows)
    d = d[d["parsed"] & ~d["error"]].copy()
    for c in "TINF":
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d = d.dropna(subset=list("TINF"))
    d = d[(d["form"] == "bare") & d["phenomenon"].isin(LABEL)]
    return {ph: sorted(g.assign(x=(g["rung"] == "strong").astype(int))
                       .groupby("item_id")["x"].mean().tolist())
            for ph, g in d.groupby("phenomenon")}


def fig1():
    """Dispersion entre items. Una serie, un color; el piloto va como anotacion."""
    per = per_item_strong()
    order = ["ethical", "paradox", "vagueness", "ignorance", "contingency"]

    fig, ax = plt.subplots(figsize=(3.35, 2.9))
    rng = np.random.default_rng(7)

    for i, ph in enumerate(order):
        v = np.array(per[ph])
        y = len(order) - 1 - i
        jit = rng.uniform(-0.13, 0.13, size=len(v))
        # media: barra vertical corta, recesiva
        ax.plot([v.mean(), v.mean()], [y - 0.28, y + 0.28],
                color=INK2, lw=1.4, solid_capstyle="butt", zorder=2)
        ax.scatter(v, y + jit, s=22, facecolor=BLUE, edgecolor=SURFACE,
                   linewidth=0.8, zorder=3, clip_on=False)

    # el enunciado unico del piloto: cae encima del item mas alto del banco
    ax.axvline(0.661, color=ORANGE, lw=1.4, ls=(0, (4, 2)), zorder=1)
    ax.annotate("the pilot's single sentence, 0.661,\n"
                "lands on the bank's highest item, 0.667",
                xy=(0.661, len(order) - 1 + 0.18), xytext=(0.16, len(order) - 0.16),
                color=ORANGE, fontsize=7, ha="left", va="top", linespacing=1.35,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.7,
                                shrinkA=2, shrinkB=3,
                                connectionstyle="angle,angleA=0,angleB=90,rad=0"))

    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([LABEL[p] for p in reversed(order)])
    ax.set_xlim(-0.02, 0.98)
    ax.set_ylim(-0.6, len(order) - 0.15)
    ax.set_xlabel("strong-rung rate, per item")
    ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8])
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color="#e8e7e3", lw=0.6, zorder=0)
    ax.set_axisbelow(True)

    fig.tight_layout(pad=0.3)
    fig.savefig(OUT / "fig1_between_items.pdf", bbox_inches="tight")
    plt.close(fig)
    print("fig1_between_items.pdf")


def wilson(k, n, z=1.96):
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(0.0, c - h), min(1.0, c + h)


def fig2():
    """Tres condiciones del system message. Dos series por el tipo de pregunta."""
    # (etiqueta, k, n) por panel, en orden de presentacion
    panels = [
        ("All contested items", [("licensed", 23, 298), ("no licence", 17, 285),
                                 ("no framing", 1, 276)]),
        ("Ethical conflict only", [("licensed", 12, 60), ("no licence", 9, 58),
                                   ("no framing", 0, 51)]),
    ]

    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.0), sharex=True)
    for ax, (title, rows) in zip(axes, panels):
        for j, (lab, k, n) in enumerate(rows):
            y = len(rows) - 1 - j
            p = k / n
            lo, hi = wilson(k, n)
            same_question = lab != "no framing"
            col = BLUE if same_question else ORANGE
            ax.plot([lo, hi], [y, y], color=col, lw=2, solid_capstyle="butt", zorder=2)
            ax.scatter([p], [y], s=42, facecolor=col, edgecolor=SURFACE,
                       linewidth=1.0, zorder=3)
            ax.text(hi + 0.012, y, f"{p:.3f}", color=INK, fontsize=7.5,
                    va="center", ha="left")
        ax.set_yticks(range(len(rows)))
        ax.set_yticklabels([r[0] for r in reversed(rows)])
        ax.set_ylim(-0.55, len(rows) - 0.45)
        ax.set_xlim(-0.01, 0.40)
        ax.set_title(title, fontsize=8, color=INK, pad=6, loc="left")
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.tick_params(axis="y", length=0)
        ax.grid(axis="x", color="#e8e7e3", lw=0.6, zorder=0)
        ax.set_axisbelow(True)
        ax.set_xlabel("strong-rung rate, 95% CI")

    # leyenda: la identidad no depende solo del color, y ademas va etiquetada en el eje
    h = [plt.Line2D([], [], color=BLUE, lw=2, marker="o", ms=5,
                    markeredgecolor=SURFACE, label="asks the neutrosophic question"),
         plt.Line2D([], [], color=ORANGE, lw=2, marker="o", ms=5,
                    markeredgecolor=SURFACE, label="does not")]
    axes[1].legend(handles=h, loc="lower right", frameon=False, fontsize=7,
                   handlelength=1.6, borderpad=0.2, labelspacing=0.3,
                   bbox_to_anchor=(1.0, -0.06))

    fig.tight_layout(pad=0.3)
    fig.savefig(OUT / "fig2_manipulation.pdf", bbox_inches="tight")
    plt.close(fig)
    print("fig2_manipulation.pdf")


if __name__ == "__main__":
    fig1()
