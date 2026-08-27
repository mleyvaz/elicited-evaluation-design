"""Acuerdo entre clasificadores y contra la asignacion de los bancos.

Dos tareas, porque las dos familias plantean preguntas de validez distintas:

  A  familia I, seis categorias: por que es dificil de contestar este enunciado
  B  familia II, binaria: tiene respuesta conocida o esta genuinamente abierto

La B es la que mas pesa. Los resultados 2 y 3 de la replica viven enteros en el
subconjunto abierto de la familia II, asi que si esos diez items no son de verdad
preguntas sin respuesta, los dos efectos no se encogen: se quedan sin sitio donde
ocurrir.

Uso:  python analyze_classification.py
      (requiere las hojas taskX_rater_A.csv y taskX_rater_B.csv con la columna llena)
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

import numpy as np

CL = Path(__file__).resolve().parent / "classification"

TASKS = {
    "taskA": {"name": "Familia I - seis categorias",
              "codes": {"EC": "ethical conflict", "EI": "epistemic ignorance",
                        "VG": "vagueness", "FC": "future contingency",
                        "LP": "logical paradox", "ST": "settled truth"}},
    "taskB": {"name": "Familia II - abierto o resuelto",
              "codes": {"K": "has a known answer", "O": "genuinely open"}},
}


def read(tag, rater):
    p = CL / f"{tag}_rater_{rater}.csv"
    if not p.exists():
        return None
    out = {}
    with p.open(encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            c = (row.get("category") or "").strip().upper()
            if c:
                out[row["item"]] = c
    return out or None


def kappa(a, b, cats):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum((ca[c] / n) * (cb[c] / n) for c in cats)
    return (po - pe) / (1 - pe) if pe < 1 else float("nan")


def run(tag, spec):
    codes = spec["codes"]
    inv = {v: k for k, v in codes.items()}
    order = list(codes)

    kp = CL / f"{tag}_key.json"
    if not kp.exists():
        print(f"  {tag}: sin clave, corre build_classification_task.py")
        return
    key = json.loads(kp.read_text(encoding="utf-8"))
    gold = {k: inv[v["gold"]] for k, v in key.items()}

    A, B = read(tag, "A"), read(tag, "B")
    if not A or not B:
        miss = [r for r, d in (("A", A), ("B", B)) if not d]
        print(f"  {spec['name']}: faltan hojas rellenas ({', '.join(miss)}). "
              f"El instrumento esta listo; esto se corre cuando vuelvan.")
        return

    common = [k for k in key if k in A and k in B]
    la = [A[k] for k in common]
    lb = [B[k] for k in common]
    lg = [gold[k] for k in common]

    print(f"--- {spec['name']} — {len(common)}/{len(key)} items ---")
    print(f"  entre clasificadores : acuerdo {np.mean([x == y for x, y in zip(la, lb)]):.3f}"
          f"   kappa {kappa(la, lb, order):.3f}")
    for lab, l in (("A vs banco", la), ("B vs banco", lb)):
        print(f"  {lab:<20} : acuerdo {np.mean([x == y for x, y in zip(l, lg)]):.3f}"
              f"   kappa {kappa(l, lg, order):.3f}")

    print(f"  por categoria (recuperacion de la asignacion del banco):")
    for c in order:
        ks = [k for k in common if gold[k] == c]
        if not ks:
            continue
        print(f"    {codes[c]:<22}{len(ks):>4}"
              f"   A {np.mean([A[k] == c for k in ks]):.2f}"
              f"   B {np.mean([B[k] == c for k in ks]):.2f}")

    off = [k for k in common if A[k] != gold[k] and B[k] != gold[k]]
    print(f"  items que ninguno coloca donde el banco dice: {len(off)}")
    for k in off:
        print(f"    {k} [{key[k]['orig_id']}] banco={codes[gold[k]]}"
              f"  A={codes.get(A[k], A[k])}  B={codes.get(B[k], B[k])}")
    print()


def main():
    print("=" * 70)
    print("VALIDEZ DE CONSTRUCTO")
    print("=" * 70)
    for tag, spec in TASKS.items():
        run(tag, spec)


if __name__ == "__main__":
    main()
