"""Genera los instrumentos de clasificacion de items, ciegos y aleatorizados.

Para que decir "estos diez items miden conflicto etico" sea una afirmacion verificable
y no una asignacion del autor, hacen falta clasificadores independientes que reciban los
items sin etiqueta y un coeficiente de acuerdo.

Son DOS tareas, no una, porque las dos familias plantean preguntas de validez distintas
y mezclarlas produciria una tarea que nadie puede contestar bien.

TAREA A - familia I, seis categorias
  50 items en forma BARE mas las 10 anclas = 60. Los MARKED se excluyen: llevan dentro
  "both P and not-P", que delata la estructura e inflaria el acuerdo, y el resultado
  titular del paper esta medido sobre items sin marcar.

TAREA B - familia II, binaria
  Los 50 items de constructo mas las 10 anclas aritmeticas = 60. La pregunta es solo si
  el enunciado tiene respuesta conocida o esta genuinamente abierto. Esa es la que
  importa: los resultados 2 y 3 de la replica viven ENTEROS en el subconjunto abierto,
  asi que si esos diez items no son de verdad preguntas sin respuesta, los dos efectos
  no se encogen, se quedan sin sitio donde ocurrir.

En las dos: anclas mezcladas sin avisar, orden barajado con semilla fija e identico para
los dos clasificadores, e identificadores originales sustituidos por codigos neutros.

Uso:  python build_classification_task.py
"""
from __future__ import annotations

import csv
import json
import random
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "classification"
SEED = 20260827

LABELS_A = {
    "ethical": "ethical conflict", "ignorance": "epistemic ignorance",
    "vagueness": "vagueness", "contingency": "future contingency",
    "paradox": "logical paradox",
    "tautology": "settled truth", "consensus": "settled truth",
}
LABELS_B = {
    "wellknown_true": "has a known answer", "wellknown_false": "has a known answer",
    "obscure_true": "has a known answer", "obscure_false": "has a known answer",
    "anchor_true": "has a known answer", "anchor_false": "has a known answer",
    "unsettled": "genuinely open",
}

DEFS_A = """\
| Code | Category | The statement is contested because... |
|---|---|---|
| **EC** | Ethical conflict | competent people hold opposed moral views about it, and the disagreement is about values rather than about facts |
| **EI** | Epistemic ignorance | there is a fact of the matter, but nobody currently knows it |
| **VG** | Vagueness | the predicate has no sharp boundary, so borderline cases have no determinate answer |
| **FC** | Future contingency | it concerns a future event that is not yet settled |
| **LP** | Logical paradox | asserting it leads to contradiction by its own structure |
| **ST** | Settled truth | it is not contested at all: a tautology, or a fact essentially everyone accepts |
"""

DEFS_B = """\
| Code | Category | Use it when... |
|---|---|---|
| **K** | Has a known answer | the statement is true or false, and which one is established. It does not matter whether *you* know the answer, or whether it is obscure; what matters is that the answer exists and is settled |
| **O** | Genuinely open | nobody currently knows whether it is true. An unsolved problem, an unresolved empirical question, or a claim about a future that has not happened |
"""


def emit(tag, rows, key, defs, header, extra):
    for r in ("A", "B"):
        p = OUT / f"{tag}_rater_{r}.csv"
        with p.open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["item", "statement", "category"])
            w.writeheader()
            w.writerows(rows)
        print(f"  {p.name}: {len(rows)} items en blanco")
    (OUT / f"{tag}_key.json").write_text(
        json.dumps(key, indent=1, ensure_ascii=False), encoding="utf-8")
    (OUT / f"{tag}_INSTRUCTIONS.md").write_text(f"""\
# {header}

You will see **{len(rows)} statements** in random order. {extra}

Work alone. Do not discuss the items with the other rater until both sheets are finished.
There is no time limit. If you are unsure, choose the closest category rather than leaving
it blank: the point is to measure how reproducible the assignment is, and a blank tells us
nothing.

## Categories

{defs}

## Rules

1. **One code per statement.** No ties, no multiple codes.
2. **Judge the statement, not your opinion of it.**
3. **Ignore how the statement is phrased.** Judge the content.

## When you finish

Send back your `{tag}_rater_X.csv` with the `category` column filled. Nothing else.
""", encoding="utf-8")
    c = Counter(v["gold"] for v in key.values())
    for k, n in sorted(c.items(), key=lambda x: -x[1]):
        print(f"      {k:<22} {n}")


def main():
    OUT.mkdir(exist_ok=True)
    rng = random.Random(SEED)

    # ---------- tarea A: familia I ----------
    items = json.loads((HERE.parent / "family1" / "items.json").read_text(encoding="utf-8"))
    sel = [it for it in items if it["form"] in ("bare", "anchor")]
    assert len(sel) == 60, f"familia I: esperaba 60, hay {len(sel)}"
    rng.shuffle(sel)
    key, rows = {}, []
    for n, it in enumerate(sel, start=1):
        code = f"A{n:02d}"
        key[code] = {"orig_id": it["id"], "phenomenon": it["phenomenon"],
                     "gold": LABELS_A[it["phenomenon"]]}
        rows.append({"item": code, "statement": it["text"], "category": ""})
    print("TAREA A - familia I, seis categorias")
    emit("taskA", rows, key, DEFS_A,
         "Item classification task A: why is this hard to answer?",
         "For each one, decide **why it is hard to answer**, and write the two-letter code "
         "in the `category` column. Some statements are not contested at all; those get `ST`, "
         "and they are mixed in without warning.")

    # ---------- tarea B: familia II ----------
    f2 = HERE.parent / "family2" / "items_factual.json"
    if not f2.exists():
        print("\n  familia II: items_factual.json no encontrado, tarea B omitida")
        return
    it2 = json.loads(f2.read_text(encoding="utf-8"))
    assert len(it2) == 60, f"familia II: esperaba 60, hay {len(it2)}"
    rng.shuffle(it2)
    key, rows = {}, []
    for n, it in enumerate(it2, start=1):
        code = f"B{n:02d}"
        key[code] = {"orig_id": it["id"], "construct": it["construct"],
                     "gold": LABELS_B[it["construct"]]}
        rows.append({"item": code, "statement": it["text"], "category": ""})
    print("\nTAREA B - familia II, binaria")
    emit("taskB", rows, key, DEFS_B,
         "Item classification task B: does this have a known answer?",
         "For each one, decide whether the answer is **established** or **genuinely open**, "
         "and write `K` or `O` in the `category` column.")


if __name__ == "__main__":
    main()
