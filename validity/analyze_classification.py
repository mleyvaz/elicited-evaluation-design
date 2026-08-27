"""Acuerdo entre clasificadores y contra la asignacion original del banco.

Produce los tres numeros que el paper necesita para responder a la objecion de validez
de constructo:

  1. Cohen kappa entre los dos clasificadores        -> es reproducible la asignacion?
  2. Acuerdo de cada uno con la clave original       -> es la asignacion del autor la que
                                                        harian otros?
  3. Matriz de confusion por constructo              -> donde se rompe, si se rompe

Uso:  python analyze_classification.py
      (requiere classification/rater_A.csv y rater_B.csv con la columna category llena)
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
CL = HERE / "classification"

CODE = {"EC": "ethical conflict", "EI": "epistemic ignorance", "VG": "vagueness",
        "FC": "future contingency", "LP": "logical paradox", "ST": "settled truth"}
ORDER = ["EC", "EI", "VG", "FC", "LP", "ST"]
INV = {v: k for k, v in CODE.items()}


def read(rater):
    p = CL / f"rater_{rater}.csv"
    if not p.exists():
        return None
    out = {}
    with p.open(encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            c = (row.get("category") or "").strip().upper()
            if c:
                out[row["item"]] = c
    return out


def kappa(a, b, cats):
    """Cohen kappa sobre las etiquetas emparejadas."""
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum((ca[c] / n) * (cb[c] / n) for c in cats)
    return (po - pe) / (1 - pe) if pe < 1 else float("nan")


def main():
    key = json.loads((CL / "key.json").read_text(encoding="utf-8"))
    gold = {k: INV[v["gold"]] for k, v in key.items()}

    A, B = read("A"), read("B")
    if not A or not B:
        missing = [r for r, d in (("A", A), ("B", B)) if not d]
        print(f"faltan hojas rellenas: rater_{', rater_'.join(missing)}")
        print("El instrumento esta listo; esto se corre cuando vuelvan.")
        return

    common = [k for k in key if k in A and k in B]
    bad = {r: [c for c in d.values() if c not in CODE] for r, d in (("A", A), ("B", B))}
    for r, b in bad.items():
        if b:
            print(f"  AVISO rater {r}: codigos no validos {sorted(set(b))}")

    print("=" * 66)
    print(f"VALIDEZ DE CONSTRUCTO — {len(common)}/{len(key)} items clasificados por ambos")
    print("=" * 66)

    la = [A[k] for k in common]
    lb = [B[k] for k in common]
    lg = [gold[k] for k in common]

    print(f"\n1. ACUERDO ENTRE CLASIFICADORES")
    print(f"   acuerdo simple      {np.mean([x == y for x, y in zip(la, lb)]):.3f}")
    print(f"   Cohen kappa         {kappa(la, lb, ORDER):.3f}")

    print(f"\n2. ACUERDO CON LA ASIGNACION DEL BANCO")
    for lab, l in (("clasificador A", la), ("clasificador B", lb)):
        print(f"   {lab}: acuerdo {np.mean([x == y for x, y in zip(l, lg)]):.3f}   "
              f"kappa {kappa(l, lg, ORDER):.3f}")
    both = [k for k in common if A[k] == B[k]]
    if both:
        agree_gold = np.mean([A[k] == gold[k] for k in both])
        print(f"   donde A y B coinciden ({len(both)} items): "
              f"acuerdo con el banco {agree_gold:.3f}")

    print(f"\n3. POR CONSTRUCTO (recuperacion de la asignacion del banco)")
    print(f"   {'constructo':<22}{'n':>4}{'A':>8}{'B':>8}{'A=B':>8}")
    for c in ORDER:
        ks = [k for k in common if gold[k] == c]
        if not ks:
            continue
        print(f"   {CODE[c]:<22}{len(ks):>4}"
              f"{np.mean([A[k] == c for k in ks]):>8.2f}"
              f"{np.mean([B[k] == c for k in ks]):>8.2f}"
              f"{np.mean([A[k] == B[k] for k in ks]):>8.2f}")

    print(f"\n4. CONFUSIONES MAS FRECUENTES (banco -> clasificador)")
    conf = Counter()
    for k in common:
        for l in (A[k], B[k]):
            if l != gold[k]:
                conf[(gold[k], l)] += 1
    for (g, l), n in conf.most_common(6):
        print(f"   {CODE[g]:<22} -> {CODE.get(l, l):<22} {n}")

    print(f"\n5. ITEMS QUE NADIE COLOCA DONDE EL BANCO DICE")
    off = [k for k in common if A[k] != gold[k] and B[k] != gold[k]]
    print(f"   {len(off)} de {len(common)}")
    for k in off:
        print(f"   {k} [{key[k]['orig_id']}] banco={CODE[gold[k]]:<20} "
              f"A={CODE.get(A[k], A[k])}  B={CODE.get(B[k], B[k])}")

    print(f"\n--- para el paper ---")
    print(f"Two raters classified the {len(common)} unmarked items and anchors into the five")
    print(f"constructs, blind to the bank's assignment and to each other. They agreed with each")
    print(f"other at kappa = {kappa(la, lb, ORDER):.3f} and reproduced the bank's assignment at")
    print(f"kappa = {kappa(la, lg, ORDER):.3f} and {kappa(lb, lg, ORDER):.3f}.")


if __name__ == "__main__":
    main()
