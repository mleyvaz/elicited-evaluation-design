"""Descompone el desacuerdo del piloto en ruido del mismo modelo y desacuerdo entre modelos.

Produce las dos cifras que el paper reporta en la seccion de acuerdo y que hasta ahora
no salian de ningun script publicado. Una revision adversarial lo senalo, con razon:
un paper que exige que cada tasa se pueda recomputar desde los datos no puede tener
dos numeros propios que solo existan en la prosa.

  INTRA  mismo modelo, mismo enunciado, misma glosa, pares entre las diez repeticiones
  INTER  mismo enunciado, misma glosa, misma repeticion, pares entre los seis modelos

Ambas sobre los CINCO enunciados contestados. Los tres controles tautologicos se
excluyen porque su etiqueta casi nunca esta en disputa; incluirlos baja las dos tasas
a la mitad sin cambiar su cociente, y el script lo imprime para que se vea.

Intervalos por bootstrap agrupado por enunciado, que es la unidad de muestreo.

Uso:  python analyze_pilot_agreement.py
"""
from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

RAW = Path(__file__).resolve().parent / "results" / "raw_quadruple_pilot.jsonl"
B = 10000
SEED = 20260827


def load():
    d = pd.DataFrame([json.loads(l) for l in
                      RAW.read_text(encoding="utf-8").splitlines() if l.strip()])
    return d[d["parsed"] & ~d["error"]].copy()


def pairs(df, keys):
    """Devuelve, por enunciado, la lista de comparaciones 1/0 dentro de cada grupo."""
    out = {}
    for k, g in df.groupby(keys):
        stmt = k[keys.index("statement")]
        v = list(g["regime"])
        out.setdefault(stmt, []).extend(int(a != b) for a, b in combinations(v, 2))
    return out


def rate_ci(by_stmt, seed=SEED):
    flat = [x for v in by_stmt.values() for x in v]
    stmts = list(by_stmt)
    rng = np.random.default_rng(seed)
    draws = np.empty(B)
    for b in range(B):
        idx = rng.integers(0, len(stmts), len(stmts))
        pool = [x for i in idx for x in by_stmt[stmts[i]]]
        draws[b] = np.mean(pool)
    return float(np.mean(flat)), len(flat), tuple(np.percentile(draws, [2.5, 97.5]))


def main():
    d = load()
    contested = d[~d["phenomenon"].str.startswith("Tautology")]

    print("=" * 72)
    print("DESCOMPOSICION DEL DESACUERDO EN EL PILOTO")
    print("=" * 72)
    print(f"registros usables: {len(d)}   de ellos contestados: {len(contested)}")
    print(f"enunciados contestados: {contested['statement'].nunique()}   "
          f"controles: {d['phenomenon'].str.startswith('Tautology').sum()} evaluaciones")
    print()

    for label, sub in (("CONTESTADOS (lo que reporta el paper)", contested),
                       ("todos, incluidos los controles", d)):
        intra = pairs(sub, ["model", "statement", "gloss"])
        inter = pairs(sub, ["statement", "gloss", "rep"])
        ra, na, ca = rate_ci(intra)
        rb, nb, cb = rate_ci(inter)
        print(f"--- {label} ---")
        print(f"  intra-modelo entre repeticiones  {ra:.3f}  "
              f"IC95 [{ca[0]:.3f}, {ca[1]:.3f}]   n = {na:,} pares")
        print(f"  inter-modelo                     {rb:.3f}  "
              f"IC95 [{cb[0]:.3f}, {cb[1]:.3f}]   n = {nb:,} pares")
        print(f"  fraccion del desacuerdo que es un solo modelo variando: {ra / rb:.3f}")
        print()

    print("--- para el paper ---")
    intra = pairs(contested, ["model", "statement", "gloss"])
    inter = pairs(contested, ["statement", "gloss", "rep"])
    ra, na, ca = rate_ci(intra)
    rb, nb, cb = rate_ci(inter)
    print(f"Two repetitions of the same item by the same model under the same wording land on")
    print(f"different labels {ra*100:.1f}% of the time (n = {na:,} pairs, 95% CI "
          f"[{ca[0]*100:.1f}, {ca[1]*100:.1f}]); two different models answering the same item,")
    print(f"wording and repetition disagree {rb*100:.1f}% of the time (n = {nb:,} pairs, 95% CI "
          f"[{cb[0]*100:.1f}, {cb[1]*100:.1f}]).")


if __name__ == "__main__":
    main()
