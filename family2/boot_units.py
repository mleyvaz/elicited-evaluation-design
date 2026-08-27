"""Intervalos de las ablaciones remuestreando por ITEM, no por fila.

Una revision adversarial senalo que boot_ci() decia estar agrupado por item pero
remuestreaba diff.values plano, y que para las ablaciones esas filas son pares
item-modelo, no items. Este script calcula las dos versiones y las compara, para
que el paper declare la unidad de remuestreo y reporte la correcta.

La unidad correcta es el ITEM: los seis modelos ven el mismo enunciado, asi que sus
respuestas no son independientes. Remuestrear filas trata seis observaciones
correlacionadas como seis independientes y estrecha el intervalo de mas.

Uso:  python boot_units.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

RES = Path(__file__).resolve().parent / "results"
B = 20000
SEED = 20260827


def load(cond):
    d = pd.DataFrame([json.loads(l) for l in
                      (RES / f"raw_factual_{cond}.jsonl").read_text(encoding="utf-8").splitlines()
                      if l.strip()])
    d = d[d["parsed"] & ~d["error"]].copy()
    d["confidence"] = pd.to_numeric(d["confidence"], errors="coerce")
    return d.dropna(subset=["confidence"]).query("wording == 'W1' and ~is_anchor")


def boot_rows(v, seed=SEED):
    rng = np.random.default_rng(seed)
    v = np.asarray(v, float)
    d = rng.choice(v, size=(B, len(v)), replace=True).mean(axis=1)
    return np.percentile(d, [2.5, 97.5])


def boot_items(df, col, seed=SEED):
    """Remuestrea ITEMS con reemplazo y toma todas las filas del item elegido."""
    rng = np.random.default_rng(seed)
    groups = [g[col].to_numpy(float) for _, g in df.groupby("item_id")]
    k = len(groups)
    out = np.empty(B)
    for b in range(B):
        idx = rng.integers(0, k, k)
        out[b] = np.concatenate([groups[i] for i in idx]).mean()
    return np.percentile(out, [2.5, 97.5])


def main():
    full = load("full")
    print(f"{'contraste':<34}{'delta':>8}{'IC por fila':>22}{'IC por item':>22}")
    for cond in ("nolicense", "neutral"):
        other = load(cond)
        for scope, sel in (("todos los constructos", slice(None)),
                           ("solo unsettled", "unsettled")):
            f = full if scope.startswith("todos") else full[full.construct == sel]
            o = other if scope.startswith("todos") else other[other.construct == sel]
            j = pd.concat([f.set_index(["item_id", "model"])["confidence"].rename("a"),
                           o.set_index(["item_id", "model"])["confidence"].rename("b")],
                          axis=1).dropna().reset_index()
            j["d"] = j.b - j.a
            r = boot_rows(j.d.values)
            i = boot_items(j, "d")
            print(f"  {cond} / {scope:<20}{j.d.mean():>+8.3f}"
                  f"{f'[{r[0]:+.3f}, {r[1]:+.3f}]':>22}{f'[{i[0]:+.3f}, {i[1]:+.3f}]':>22}")

    print()
    print("masa en 0.50 exacto, constructo abierto (el hallazgo de forma):")
    fu = full[full.construct == "unsettled"]
    for cond in ("nolicense", "neutral"):
        ou = load(cond).query("construct == 'unsettled'")
        j = pd.concat([(np.abs(fu.set_index(["item_id", "model"]).confidence - .5) < 1e-9).rename("a"),
                       (np.abs(ou.set_index(["item_id", "model"]).confidence - .5) < 1e-9).rename("b")],
                      axis=1).dropna().reset_index()
        j["d"] = j.b.astype(int) - j.a.astype(int)
        r, i = boot_rows(j.d.values), boot_items(j, "d")
        print(f"  {cond:<12} delta {j.d.mean():+.3f}   por fila [{r[0]:+.3f}, {r[1]:+.3f}]"
              f"   por item [{i[0]:+.3f}, {i[1]:+.3f}]")


if __name__ == "__main__":
    main()
