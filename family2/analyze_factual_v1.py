"""PRIMERA VERSION del analisis del banco factual. Se conserva a proposito.

Este script tomaba como cantidad principal la TASA DE ALTA CONFIANZA (>= 0.9), por
analogia con las tasas de sobreconfianza que reporta la literatura de calibracion. Sobre
los datos reales esa eleccion resulto ser ella misma el artefacto que predice la regla
del umbral: cuatro de los cinco constructos quedan clavados en 0.000 o 1.000 con varianza
entre items nula, y el unico constructo con dispersion real entre modelos (SD = 0.110 en
la escala continua) colapsa a una tasa de 0.028.

Se publica sin corregir, junto a `analyze_factual.py`, que es la version que el paper
reporta y que toma la confianza continua como cantidad primaria. La secuencia entre los
dos ficheros es parte de la evidencia de la seccion de replica: la binarizacion no es un
resumen de la medida, es una segunda medida, y aqui es la que falla.

No usar para reproducir las cifras del paper. Usar `analyze_factual.py`.

Uso:  python analyze_factual_v1.py
"""
from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
HIGH = 0.9
CONSTRUCTS = ["wellknown_true", "wellknown_false", "obscure_true",
              "obscure_false", "unsettled"]


def load(cond):
    p = RES / f"raw_factual_{cond}.jsonl"
    if not p.exists():
        return None
    d = pd.DataFrame([json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()])
    raw = len(d)
    d = d[d["parsed"] & ~d["error"]].copy()
    d["confidence"] = pd.to_numeric(d["confidence"], errors="coerce")
    d = d.dropna(subset=["confidence"])
    d["high"] = (d["confidence"] >= HIGH).astype(int)
    return d, raw


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(0.0, c - h), min(1.0, c + h)


def main():
    full, full_raw = load("full")
    core = full[~full["is_anchor"]]

    print("=" * 74)
    print("BANCO FACTUAL - replica de las tres reglas en un dominio sin relacion")
    print("=" * 74)
    print(f"condicion principal: {len(full)}/{full_raw} usables "
          f"({1-len(full)/full_raw:.1%} fallo de parseo)")
    print()

    # ---------- 1. MUESTREO DE ITEMS ----------
    print("--- 1. MUESTREO DE ITEMS: SD entre items dentro de cada constructo ---")
    rows = []
    for c in CONSTRUCTS:
        per = core[core.construct == c].groupby("item_id")["high"].mean()
        rows.append({"construct": c, "mean": per.mean(), "sd_between": per.std(ddof=1),
                     "ratio": per.std(ddof=1) / max(per.mean(), 1e-9),
                     "min": per.min(), "max": per.max(), "k": len(per)})
    t = pd.DataFrame(rows).set_index("construct")
    print(t.round(3).to_string())
    print()
    sd_max = t["sd_between"].max()
    worst = t["sd_between"].idxmax()
    print(f"  mayor SD entre items: {sd_max:.3f} ({worst})")
    print(f"  con 1 item  -> semiancho IC95 = {1.96*sd_max:.3f}")
    print(f"  con 10 items-> semiancho IC95 = {1.96*sd_max/np.sqrt(10):.3f}")
    print(f"  para +/-0.05 hacen falta k = {int(np.ceil((1.96*sd_max/0.05)**2))} items")
    print(f"  constructos con SD >= media: {int((t['ratio']>=1).sum())} de {len(t)}")
    print()

    # ---------- 2. INSTRUCCION ----------
    print("--- 2. INSTRUCCION: tres condiciones anidadas (solo W1, pareado) ---")
    conds = []
    for name in ["full", "nolicense", "neutral"]:
        r = load(name)
        if r is None:
            print(f"  {name}: aun sin correr")
            continue
        d, raw = r
        d = d[d.wording == "W1"]
        conds.append((name, d, raw))
    if len(conds) == 3:
        for name, d, raw in conds:
            c = d[~d.is_anchor]
            k, n = int(c["high"].sum()), len(c)
            lo, hi = wilson(k, n)
            a = d[d.is_anchor]
            print(f"  {name:<10} alta confianza {k:3d}/{n:3d} = {k/n:.3f} "
                  f"IC95 [{lo:.3f}, {hi:.3f}]   anclas {a['high'].mean():.3f}")
        print()
        print("  alta confianza en 'unsettled' (donde deberia ser baja):")
        for name, d, _ in conds:
            u = d[d.construct == "unsettled"]
            print(f"    {name:<10} {u['high'].mean():.3f}   confianza media {u['confidence'].mean():.3f}")
    print()

    # ---------- 3. UMBRAL Y REJILLA ----------
    print("--- 3. UMBRAL: grano de la rejilla ---")
    v = full["confidence"].values
    print(f"  valores distintos: {len(np.unique(v))} en {len(v)} elicitaciones")
    print(f"  multiplos de 0.05: {100*np.mean(np.abs(v*20-np.round(v*20))<1e-9):.1f}%")
    print(f"  multiplos de 0.10: {100*np.mean(np.abs(v*10-np.round(v*10))<1e-9):.1f}%")
    vc = pd.Series(v).value_counts(normalize=True).head(6)
    print("  valores mas frecuentes: " + "  ".join(f"{k:.2f}({100*x:.0f}%)" for k, x in vc.items()))
    print(f"  confianza exactamente 0.90: {100*np.mean(np.abs(v-0.9)<1e-9):.1f}%")
    print(f"  el corte 0.90 cae sobre la moda? moda = {vc.index[0]:.2f}")
    print()
    print("  sensibilidad del corte, items de constructo:")
    for cut in [0.85, 0.90, 0.95, 0.99]:
        r = (core["confidence"] >= cut).mean()
        print(f"    >= {cut:.2f}  ->  {r:.3f}")
    print()

    # ---------- 4. ACUERDO ----------
    print("--- 4. ACUERDO entre familias de modelos ---")
    piv = core.pivot_table(index=["item_id", "wording"], columns="model",
                           values="high", aggfunc="first").dropna()
    inter = [float((piv[a] != piv[b]).mean()) for a, b in combinations(piv.columns, 2)]
    print(f"  desacuerdo par a par entre modelos: {np.mean(inter):.3f} (n={len(piv)} unidades)")
    intra = []
    for _, g in core.groupby(["item_id", "model"]):
        vals = list(g["high"])
        intra += [1 if a != b else 0 for a, b in combinations(vals, 2)]
    print(f"  desacuerdo del mismo modelo entre redacciones: {np.mean(intra):.3f} (n={len(intra)})")
    print(f"  ratio intra/inter: {np.mean(intra)/max(np.mean(inter),1e-9):.2f}")
    print()

    # ---------- calibracion, como bonus domestico ----------
    print("--- BONUS: calibracion (solo donde hay verdad de referencia) ---")
    kn = core[core.truth.notna()].copy()
    kn["correct_dir"] = np.where(kn["truth"], kn["confidence"], 1 - kn["confidence"])
    print(kn.groupby("construct")[["confidence", "correct_dir"]].mean().round(3).to_string())


if __name__ == "__main__":
    main()
