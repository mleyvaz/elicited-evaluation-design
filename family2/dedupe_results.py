"""Deduplica los .jsonl crudos por celda (modelo, item, redaccion).

Hizo falta porque dos procesos de run_factual.py escribieron a la vez sobre el mismo
fichero: cada uno leyo done_keys al arrancar y ninguno vio el trabajo del otro. Se
conserva la PRIMERA aparicion de cada celda, que es la que cualquier reanudacion
posterior habria respetado. Idempotente.

Uso:  python dedupe_results.py
"""
from __future__ import annotations

import json
from pathlib import Path

RES = Path(__file__).resolve().parent / "results"


def main():
    for p in sorted(RES.glob("raw_factual_*.jsonl")):
        rows = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
        seen, keep = set(), []
        for r in rows:
            k = (r["model"], r["item_id"], r["wording"])
            if k in seen:
                continue
            seen.add(k)
            keep.append(r)
        if len(keep) == len(rows):
            print(f"{p.name}: {len(rows)} celdas, sin duplicados")
            continue
        p.with_suffix(".jsonl.bak").write_text(
            "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
        p.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in keep) + "\n",
                     encoding="utf-8")
        print(f"{p.name}: {len(rows)} -> {len(keep)} ({len(rows)-len(keep)} duplicados; "
              f"crudo original en {p.name}.bak)")


if __name__ == "__main__":
    main()
