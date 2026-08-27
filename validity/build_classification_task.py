"""Genera el instrumento de clasificacion de items, ciego y aleatorizado.

Para que decir "estos diez items miden conflicto etico" sea una afirmacion verificable
y no una asignacion del autor, hacen falta clasificadores independientes que reciban
los items sin etiqueta y los asignen a los constructos, y un coeficiente de acuerdo.

DISENO
  - Se clasifican los 50 items en forma BARE mas las 10 anclas = 60 items.
    Los 50 en forma MARKED se excluyen a proposito: llevan dentro "both P and not-P",
    que delata la estructura y inflaria el acuerdo. Ademas el resultado titular del
    paper esta medido sobre items sin marcar.
  - Las anclas van dentro sin avisar. Si un clasificador no separa una tautologia de
    un item de constructo, el problema no es el margen de error, es el banco.
  - Orden barajado con semilla fija, identico para los dos clasificadores, para que
    sus hojas sean comparables linea a linea.
  - Los identificadores originales (ethi-01-bare) se sustituyen por codigos neutros.

SALIDA
  classification/INSTRUCTIONS.md   definiciones y tarea
  classification/rater_A.csv       hoja en blanco
  classification/rater_B.csv       identica
  classification/key.json          la asignacion real, no se entrega a los clasificadores

Uso:  python build_classification_task.py
"""
from __future__ import annotations

import csv
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
BANK = HERE.parent / "family1" / "items.json"
OUT = HERE / "classification"
SEED = 20260827

LABELS = {
    "ethical": "ethical conflict",
    "ignorance": "epistemic ignorance",
    "vagueness": "vagueness",
    "contingency": "future contingency",
    "paradox": "logical paradox",
    "tautology": "settled truth",
    "consensus": "settled truth",
}

DEFS = """\
| Code | Category | The statement is contested because... |
|---|---|---|
| **EC** | Ethical conflict | competent people hold opposed moral views about it, and the disagreement is about values rather than about facts |
| **EI** | Epistemic ignorance | there is a fact of the matter, but nobody currently knows it |
| **VG** | Vagueness | the predicate has no sharp boundary, so borderline cases have no determinate answer |
| **FC** | Future contingency | it concerns a future event that is not yet settled |
| **LP** | Logical paradox | asserting it leads to contradiction by its own structure |
| **ST** | Settled truth | it is not contested at all: a tautology, or a fact essentially everyone accepts |
"""


def main():
    items = json.loads(BANK.read_text(encoding="utf-8"))
    sel = [it for it in items if it["form"] in ("bare", "anchor")]
    assert len(sel) == 60, f"esperaba 60, hay {len(sel)}"

    rng = random.Random(SEED)
    rng.shuffle(sel)

    OUT.mkdir(exist_ok=True)
    key = {}
    rows = []
    for n, it in enumerate(sel, start=1):
        code = f"S{n:02d}"
        key[code] = {"orig_id": it["id"], "phenomenon": it["phenomenon"],
                     "form": it["form"], "gold": LABELS[it["phenomenon"]]}
        rows.append({"item": code, "statement": it["text"], "category": ""})

    for r in ("A", "B"):
        p = OUT / f"rater_{r}.csv"
        with p.open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["item", "statement", "category"])
            w.writeheader()
            w.writerows(rows)
        print(f"  {p.name}: {len(rows)} items en blanco")

    (OUT / "key.json").write_text(json.dumps(key, indent=1, ensure_ascii=False),
                                  encoding="utf-8")
    print(f"  key.json: la asignacion real (NO entregar a los clasificadores)")

    (OUT / "INSTRUCTIONS.md").write_text(f"""\
# Item classification task

You will see **60 statements** in random order. For each one, decide **why it is hard to
answer**, and write the two-letter code in the `category` column of your CSV.

Work alone. Do not discuss the items with the other rater until both sheets are finished.
There is no time limit. If you are unsure, choose the closest category rather than leaving
it blank — the point is to measure how reproducible the assignment is, and a blank tells
us nothing.

## Categories

{DEFS}

## Rules

1. **One code per statement.** No ties, no multiple codes.
2. **Judge the statement, not your opinion of it.** For *ethical conflict* the question is
   whether competent people disagree, not whether you personally find it obvious.
3. **Some statements are not contested at all.** Those get `ST`. They are mixed in without
   warning and there is no fixed number of them.
4. **Ignore how the statement is phrased.** None of them is phrased as an explicit
   contradiction; judge the content.

## Distinguishing the two that get confused most

*Epistemic ignorance* versus *future contingency*: if the fact already exists and we simply
do not know it, that is **EI**. If the fact does not exist yet because the event has not
happened, that is **FC**.

*Vagueness* versus *ethical conflict*: if the difficulty would survive perfect agreement
about all the values involved, and comes from where a boundary falls, that is **VG**.

## When you finish

Send back your `rater_X.csv` with the `category` column filled. Nothing else.
""", encoding="utf-8")
    print("  INSTRUCTIONS.md")

    from collections import Counter
    c = Counter(v["gold"] for v in key.values())
    print("\n  composicion real (para tu control, no para ellos):")
    for k, n in sorted(c.items(), key=lambda x: -x[1]):
        print(f"    {k:<22} {n}")


if __name__ == "__main__":
    main()
