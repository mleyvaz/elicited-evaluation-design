"""Las tres reglas de diseno, medidas en el banco factual.

Replica del analisis del paper 11 en un dominio sin relacion con el neutrosofico.

NOTA DE DISENO. La primera version de este script tomaba como cantidad principal la
tasa de ALTA CONFIANZA (>= 0.9), por analogia con las tasas de sobreconfianza que
reporta la literatura de calibracion. Sobre los datos reales esa eleccion resulto ser
ella misma el artefacto que la regla 3 predice: cuatro de los cinco constructos quedan
clavados en 0.000 o 1.000, y el unico constructo con dispersion real entre modelos
(SD = 0.111 en la escala continua) colapsa a una tasa de 0.008. La binarizacion no
revela la senal, la corta.

Asi que la cantidad primaria aqui es la CONFIANZA CONTINUA, y la tasa binarizada se
conserva unicamente como demostracion de lo que el umbral le hace a la medida. Esa
inversion es el resultado que el banco factual aporta.

  1. muestreo de items : SD entre items dentro de cada constructo, y cuantos items
                         harian falta para un semiancho de 0.05
  2. instruccion       : full vs sin permiso vs sin encuadre
  3. umbral            : que le hace la binarizacion a la escala continua
  4. acuerdo           : dispersion entre modelos, por constructo

Uso:  python analyze_factual.py
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
    d = pd.DataFrame([json.loads(l) for l in
                      p.read_text(encoding="utf-8").splitlines() if l.strip()])
    raw = len(d)
    d = d[d["parsed"] & ~d["error"]].copy()
    d["confidence"] = pd.to_numeric(d["confidence"], errors="coerce")
    d = d.dropna(subset=["confidence"])
    d["high"] = (d["confidence"] >= HIGH).astype(int)
    return d, raw


def k_needed(sd, half=0.05):
    """Items necesarios para un semiancho IC95 de `half` dada la SD entre items."""
    return int(np.ceil((1.96 * sd / half) ** 2))


def boot_ci(vals, n=5000, seed=0):
    """IC95 por bootstrap agrupado por item (los items son la unidad de muestreo)."""
    rng = np.random.default_rng(seed)
    vals = np.asarray(vals, dtype=float)
    if len(vals) < 2:
        return (np.nan, np.nan)
    draws = rng.choice(vals, size=(n, len(vals)), replace=True).mean(axis=1)
    return tuple(np.percentile(draws, [2.5, 97.5]))


def main():
    r = load("full")
    if r is None:
        raise SystemExit("falta results/raw_factual_full.jsonl")
    full, full_raw = r
    core = full[~full["is_anchor"]]

    print("=" * 78)
    print("BANCO FACTUAL - replica de las tres reglas en un dominio sin relacion")
    print("=" * 78)
    print(f"condicion principal: {len(full)}/{full_raw} usables "
          f"({1 - len(full) / full_raw:.1%} fallo de parseo)")
    print(f"anclas aritmeticas: confianza media {full[full.is_anchor].groupby('truth')['confidence'].mean().to_dict()}")
    print()

    # ---------- 1. MUESTREO DE ITEMS, EN LA ESCALA CONTINUA ----------
    print("--- 1. MUESTREO DE ITEMS: SD entre items, escala continua ---")
    rows = []
    for c in CONSTRUCTS:
        per = core[core.construct == c].groupby("item_id")["confidence"].mean()
        lo, hi = boot_ci(per.values)
        rows.append({"construct": c, "mean": per.mean(), "sd_between": per.std(ddof=1),
                     "ci_lo": lo, "ci_hi": hi, "min": per.min(), "max": per.max(),
                     "k_for_0.05": k_needed(per.std(ddof=1)), "n_items": len(per)})
    t = pd.DataFrame(rows).set_index("construct")
    print(t.round(3).to_string())
    print()
    print(f"  k requerido va de {int(t['k_for_0.05'].min())} a {int(t['k_for_0.05'].max())} "
          f"items segun el constructo: un factor de "
          f"{t['k_for_0.05'].max() / max(t['k_for_0.05'].min(), 1):.0f}x dentro del mismo banco")
    print("  (en el banco neutrosofico el mismo calculo daba 69; el punto de la regla no es")
    print("   que la SD sea grande, sino que no se puede suponer sin medirla)")
    print()

    # ---------- 2. INSTRUCCION ----------
    print("--- 2. INSTRUCCION: tres condiciones anidadas (solo W1, pareado) ---")
    conds = []
    for name in ["full", "nolicense", "neutral"]:
        rr = load(name)
        if rr is None:
            print(f"  {name}: aun sin correr")
            continue
        d, raw = rr
        conds.append((name, d[d.wording == "W1"]))
    if len(conds) == 3:
        print(f"  {'condicion':<11} {'conf. media':>11} {'IC95':>18} "
              f"{'conf. unsettled':>16} {'tasa >=0.9':>11}")
        for name, d in conds:
            c = d[~d.is_anchor]
            per = c.groupby("item_id")["confidence"].mean()
            lo, hi = boot_ci(per.values)
            u = c[c.construct == "unsettled"]
            print(f"  {name:<11} {c['confidence'].mean():>11.3f} "
                  f"{f'[{lo:.3f}, {hi:.3f}]':>18} "
                  f"{u['confidence'].mean():>16.3f} {c['high'].mean():>11.3f}")
        print()
        print("  contraste pareado por item (misma pregunta W1, mismo modelo):")
        base = conds[0][1].set_index(["item_id", "model"])["confidence"]
        for name, d in conds[1:]:
            other = d.set_index(["item_id", "model"])["confidence"]
            j = pd.concat([base.rename("full"), other.rename(name)], axis=1).dropna()
            diff = j[name] - j["full"]
            lo, hi = boot_ci(diff.values)
            print(f"    {name:<11} delta = {diff.mean():+.3f}  IC95 [{lo:+.3f}, {hi:+.3f}]  "
                  f"n={len(j)}   {'cruza cero' if lo <= 0 <= hi else 'NO cruza cero'}")
        print()
        print("  el efecto donde deberia estar (constructo unsettled, pareado):")
        baseu = conds[0][1].query("construct=='unsettled'").set_index(["item_id", "model"])["confidence"]
        for name, d in conds[1:]:
            o = d.query("construct=='unsettled'").set_index(["item_id", "model"])["confidence"]
            j = pd.concat([baseu.rename("full"), o.rename(name)], axis=1).dropna()
            if len(j) < 2:
                continue
            diff = j[name] - j["full"]
            lo, hi = boot_ci(diff.values)
            print(f"    {name:<11} delta = {diff.mean():+.3f}  IC95 [{lo:+.3f}, {hi:+.3f}]  n={len(j)}")
    print()

    # ---------- 3. UMBRAL: lo que la binarizacion destruye ----------
    print("--- 3. UMBRAL: lo que la binarizacion le hace a la medida ---")
    v = full["confidence"].values
    print(f"  valores distintos: {len(np.unique(v))} en {len(v)} elicitaciones")
    print(f"  multiplos de 0.05: {100 * np.mean(np.abs(v * 20 - np.round(v * 20)) < 1e-9):.1f}%")
    print(f"  multiplos de 0.10: {100 * np.mean(np.abs(v * 10 - np.round(v * 10)) < 1e-9):.1f}%")
    vc = pd.Series(v).value_counts(normalize=True).head(6)
    print("  valores mas frecuentes: " + "  ".join(f"{k:.2f}({100 * x:.0f}%)" for k, x in vc.items()))
    print()
    print("  el mismo constructo, medido de las dos maneras:")
    print(f"  {'constructo':<17} {'conf. continua':>15} {'SD entre modelos':>17} "
          f"{'tasa >=0.9':>11} {'SD de la tasa':>14}")
    for c in CONSTRUCTS:
        s = core[core.construct == c]
        piv = s.pivot_table(index="item_id", columns="model", values="confidence", aggfunc="mean")
        pivh = s.pivot_table(index="item_id", columns="model", values="high", aggfunc="mean")
        print(f"  {c:<17} {s['confidence'].mean():>15.3f} {piv.std(axis=1).mean():>17.3f} "
              f"{s['high'].mean():>11.3f} {pivh.std(axis=1).mean():>14.3f}")
    print()
    print("  sensibilidad del corte (items de constructo):")
    for cut in [0.60, 0.70, 0.80, 0.85, 0.90, 0.95, 0.99]:
        print(f"    >= {cut:.2f}  ->  {(core['confidence'] >= cut).mean():.3f}   "
              f"unsettled {(core[core.construct == 'unsettled']['confidence'] >= cut).mean():.3f}")
    print()

    # ---------- 4. ACUERDO ----------
    print("--- 4. ACUERDO entre familias de modelos ---")
    print("  escala continua, SD entre modelos dentro de cada item:")
    for c in CONSTRUCTS:
        piv = core[core.construct == c].pivot_table(
            index=["item_id", "wording"], columns="model", values="confidence", aggfunc="mean")
        print(f"    {c:<17} {piv.std(axis=1).mean():.3f}")
    piv = core.pivot_table(index=["item_id", "wording"], columns="model",
                           values="confidence", aggfunc="mean").dropna()
    inter = [float(np.abs(piv[a] - piv[b]).mean()) for a, b in combinations(piv.columns, 2)]
    print(f"  desacuerdo medio par a par entre modelos: {np.mean(inter):.3f} (n={len(piv)})")
    intra = []
    for _, g in core.groupby(["item_id", "model"]):
        vals = list(g["confidence"])
        intra += [abs(a - b) for a, b in combinations(vals, 2)]
    print(f"  desacuerdo del mismo modelo entre redacciones: {np.mean(intra):.3f} (n={len(intra)})")
    print(f"  ratio intra/inter: {np.mean(intra) / max(np.mean(inter), 1e-9):.2f}")
    print()

    # ---------- calibracion ----------
    print("--- calibracion, donde hay verdad de referencia ---")
    kn = core[core.truth.notna()].copy()
    kn["p_correct"] = np.where(kn["truth"], kn["confidence"], 1 - kn["confidence"])
    print(kn.groupby("construct")[["confidence", "p_correct"]].mean().round(3).to_string())
    print(f"\n  Brier global (sin unsettled): "
          f"{np.mean((kn['confidence'] - kn['truth'].astype(float)) ** 2):.4f}")


if __name__ == "__main__":
    main()
