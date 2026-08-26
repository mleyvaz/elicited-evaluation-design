"""Tres condiciones del system message sobre los mismos 60 items x 6 modelos x G1.

  LICENCIADA  rol de experto + dimensiones + "NOT constrained to sum to 1.0" +
              "can be simultaneously partially true, partially false"
  SIN LICENCIA  identica menos esas dos frases   <- aisla el factor
  NEUTRA        sin rol, sin dimensiones, sin licencia

Si la tasa fuerte cae en SIN LICENCIA tanto como en NEUTRA, la causa es la licencia.
Si solo cae en NEUTRA, la causa es el encuadre.

Uso:  python analyze_system_conditions.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
CONT = ["ethical", "ignorance", "vagueness", "contingency", "paradox"]


def load(path):
    rows = [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]
    d = pd.DataFrame(rows)
    raw_n = len(d)
    d = d[d["parsed"] & ~d["error"]].copy()
    for c in "TINF":
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d = d.dropna(subset=list("TINF"))
    d["TF"] = d["T"] + d["F"]
    d["sum4"] = d[["T", "I", "N", "F"]].sum(axis=1)
    return d, raw_n


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, c - h), min(1.0, c + h))


def main():
    lic, lic_raw = load(RES / "raw_quad_bank.jsonl")
    lic = lic[(lic["gloss"] == "G1") & (lic["form"].isin(["bare", "anchor"]))]
    nol, nol_raw = load(RES / "raw_nolicense_system.jsonl")
    neu, neu_raw = load(RES / "raw_neutral_system.jsonl")

    conds = [("LICENCIADA", lic, 360), ("SIN LICENCIA", nol, nol_raw), ("NEUTRA", neu, neu_raw)]

    print("=" * 78)
    print("TRES CONDICIONES DEL SYSTEM MESSAGE  —  mismos items, modelos y glosa")
    print("=" * 78)
    for name, d, raw in conds:
        print(f"  {name:<13} usables {len(d):3d}/{raw}   fallos de parseo {1-len(d)/raw:.1%}")
    print()

    print("--- 1. PELDANO FUERTE (T+F>1), items contestados ---")
    for name, d, _ in conds:
        c = d[d.phenomenon.isin(CONT)]
        k = int((c["rung"] == "strong").sum())
        lo, hi = wilson(k, len(c))
        print(f"  {name:<13} {k:3d}/{len(c):3d} = {k/len(c):.3f}   IC95 [{lo:.3f}, {hi:.3f}]")
    print()

    print("--- 2. FUERTE EN ITEMS ETICOS (el titular del paper) ---")
    for name, d, _ in conds:
        e = d[(d.phenomenon == "ethical") & (d.form == "bare")]
        k = int((e["rung"] == "strong").sum())
        lo, hi = wilson(k, len(e))
        print(f"  {name:<13} {k:2d}/{len(e):2d} = {k/len(e):.3f}   IC95 [{lo:.3f}, {hi:.3f}]")
    print()

    print("--- 3. DESVIACION DEBIL (suma de los cuatro > 1), contestados ---")
    for name, d, _ in conds:
        c = d[d.phenomenon.isin(CONT)]
        print(f"  {name:<13} {(c['sum4'] > 1).mean():.3f}")
    print()

    print("--- 4. NORMALIZACION ESPONTANEA (suma exactamente 1,00) ---")
    for name, d, _ in conds:
        c = d[d.phenomenon.isin(CONT)]
        print(f"  {name:<13} {(np.abs(c['sum4'] - 1) < 1e-9).mean():.3f}")
    print()

    print("--- 5. DISTRIBUCION DE PELDANOS, contestados ---")
    rows = {}
    for name, d, _ in conds:
        c = d[d.phenomenon.isin(CONT)]
        rows[name] = c["rung"].value_counts(normalize=True)
    t = pd.DataFrame(rows).reindex(["strong", "weak", "very_weak", "classical"]).fillna(0)
    print(t.round(3).to_string())
    print()

    print("--- 6. MEDIAS DE COMPONENTES, contestados ---")
    for name, d, _ in conds:
        c = d[d.phenomenon.isin(CONT)]
        print(f"  {name:<13} " + "  ".join(f"{k}={c[k].mean():.3f}" for k in "TINF")
              + f"   T+F={c['TF'].mean():.3f}   suma4={c['sum4'].mean():.3f}")
    print()

    print("--- 7. ANCLAS (control) ---")
    for name, d, _ in conds:
        a = d[~d.phenomenon.isin(CONT)]
        print(f"  {name:<13} fuerte {(a['rung']=='strong').mean():.3f}   "
              f"suma4>1 {(a['sum4']>1).mean():.3f}   n={len(a)}")
    print()

    print("--- 8. FUERTE POR MODELO, contestados ---")
    t2 = pd.DataFrame({
        name: d[d.phenomenon.isin(CONT)].groupby("model").apply(
            lambda g: (g["rung"] == "strong").mean(), include_groups=False)
        for name, d, _ in conds})
    print(t2.round(3).to_string())
    print()

    print("--- 9. FALLOS DE PARSEO POR MODELO ---")
    for name, path in [("SIN LICENCIA", "raw_nolicense_system.jsonl"),
                       ("NEUTRA", "raw_neutral_system.jsonl")]:
        d = pd.DataFrame([json.loads(l) for l in (RES / path).read_text(encoding="utf-8").splitlines() if l.strip()])
        bad = (~(d["parsed"] & ~d["error"])).groupby(d["model"]).sum()
        print(f"  {name:<13} " + "  ".join(f"{k}={v}" for k, v in bad.items() if v))
    print()

    print("=" * 78)
    print("LECTURA")
    lic_c = lic[lic.phenomenon.isin(CONT)]
    nol_c = nol[nol.phenomenon.isin(CONT)]
    neu_c = neu[neu.phenomenon.isin(CONT)]
    a, b, c = [(x["rung"] == "strong").mean() for x in (lic_c, nol_c, neu_c)]
    print(f"  fuerte: licenciada {a:.3f} -> sin licencia {b:.3f} -> neutra {c:.3f}")
    if a > 0:
        print(f"  la supresion de la licencia explica el {100*(a-b)/a:.0f}% de la caida total")
        print(f"  el encuadre explica el {100*(b-c)/a:.0f}% adicional")
    print("=" * 78)


if __name__ == "__main__":
    main()
