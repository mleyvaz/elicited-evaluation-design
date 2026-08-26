"""Elicita la tripleta (T, I, F) sobre el banco de 110 items.

Usa el protocolo S1 del corpus v3 PALABRA POR PALABRA, para que los resultados
sean comparables con lo ya publicado. La condicion fuerte T+F>1 no contiene N,
asi que el cuadruple no aporta nada aqui y anadirlo introduciria la dependencia
de la glosa que ya documentamos.

Diseno: 110 items x 6 modelos x R repeticiones.  A R=3 son 1.980 llamadas.

Uso:
    set OPENROUTER_API_KEY=...
    python run_bank.py --count-only
    python run_bank.py --limit 4 --dry-run
    python run_bank.py
"""

from __future__ import annotations

import argparse
import itertools
import json
import os
import re
import sys
import time
from pathlib import Path

from openai import OpenAI

HERE = Path(__file__).resolve().parent
OUT = HERE / "results"
OUT.mkdir(exist_ok=True)
RAW = OUT / "raw_bank.jsonl"

MODELS = [
    {"id": "openai/gpt-4o", "label": "gpt-4o", "vendor": "openai"},
    {"id": "anthropic/claude-sonnet-4", "label": "claude-sonnet-4", "vendor": "anthropic"},
    {"id": "meta-llama/llama-4-maverick", "label": "llama-4-maverick", "vendor": "meta"},
    {"id": "deepseek/deepseek-chat", "label": "deepseek-chat", "vendor": "deepseek"},
    {"id": "qwen/qwen3-235b-a22b-2507", "label": "qwen3-235b", "vendor": "alibaba"},
    {"id": "mistralai/mistral-medium-3.1", "label": "mistral-medium-3.1", "vendor": "mistral"},
]

# Protocolo S1 del corpus v3, verbatim.
SYS = ("You are an expert in Neutrosophic Logic. You evaluate "
       "statements using three INDEPENDENT dimensions: Truth (T), "
       "Indeterminacy (I), and Falsity (F), each on [0.0, 1.0]. "
       "These dimensions are NOT constrained to sum to 1.0. A "
       "statement can be simultaneously partially true AND partially "
       "false AND partially indeterminate. Respond with ONLY a JSON "
       "object, no other text.")

USR = ('Evaluate this statement on three independent dimensions:\n\n'
       'Statement: "{stmt}"\n\n'
       '- Truth (T): To what degree is this statement true? [0.0 to 1.0]\n'
       '- Indeterminacy (I): To what degree is the truth value '
       'unknown, undetermined, or inherently uncertain? [0.0 to 1.0]\n'
       '- Falsity (F): To what degree is this statement false? '
       '[0.0 to 1.0]\n\n'
       'Respond with ONLY this JSON: {{"T": <float>, "I": <float>, "F": <float>}}')

MAX_RETRIES = 4


def client() -> OpenAI:
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("OPENROUTER_API_KEY is not set.")
    return OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key)


def call(cl, model_id, stmt):
    for attempt in range(MAX_RETRIES):
        try:
            r = cl.chat.completions.create(
                model=model_id,
                messages=[{"role": "system", "content": SYS},
                          {"role": "user", "content": USR.format(stmt=stmt)}],
                temperature=1.0, max_tokens=150,
            )
            return (r.choices[0].message.content or "").strip()
        except Exception as exc:                       # noqa: BLE001
            if attempt == MAX_RETRIES - 1:
                return f"__ERROR__ {exc}"
            time.sleep(3.0 * (attempt + 1))
    return "__ERROR__ unreachable"


def parse(text: str):
    m = re.search(r"\{[^{}]*\}", text, re.S)
    if m:
        try:
            d = json.loads(m.group(0))
            v = [float(d[k]) for k in ("T", "I", "F")]
            if all(0.0 <= x <= 1.0 for x in v):
                return tuple(v)
        except Exception:                              # noqa: BLE001
            pass
    got = {}
    for k in ("T", "I", "F"):
        mm = re.search(rf'"?{k}"?\s*[:=]\s*([01](?:\.\d+)?|\.\d+)', text)
        if mm:
            got[k] = float(mm.group(1))
    return tuple(got[k] for k in ("T", "I", "F")) if len(got) == 3 else None


def done_keys():
    seen = set()
    if RAW.exists():
        with RAW.open(encoding="utf-8") as fh:
            for line in fh:
                try:
                    d = json.loads(line)
                    seen.add((d["model"], d["item_id"], d["rep"]))
                except Exception:                      # noqa: BLE001
                    continue
    return seen


def main(a):
    items = json.loads((HERE / "items.json").read_text(encoding="utf-8"))
    if a.limit:
        items = items[:a.limit]
    total = len(items) * len(MODELS) * a.reps
    print(f"diseno: {len(items)} items x {len(MODELS)} modelos x {a.reps} reps")
    print(f"TOTAL LLAMADAS = {total}")
    if a.count_only:
        return

    cl = client()
    seen = done_keys()
    print(f"reanudando: {len(seen)} llamadas ya registradas")

    n = 0
    for it, model, rep in itertools.product(items, MODELS, range(a.reps)):
        key = (model["label"], it["id"], rep)
        if key in seen:
            continue
        text = call(cl, model["id"], it["text"])
        v = parse(text)
        rec = {
            "model": model["label"], "vendor": model["vendor"],
            "item_id": it["id"], "pair": it["pair"],
            "phenomenon": it["phenomenon"], "form": it["form"],
            "statement": it["text"], "rep": rep, "response": text,
            "T": v[0] if v else None, "I": v[1] if v else None, "F": v[2] if v else None,
            "strong": (int(v[0] + v[2] > 1.0) if v else None),
            "parsed": v is not None, "error": text.startswith("__ERROR__"),
        }
        if a.dry_run:
            print(json.dumps(rec, ensure_ascii=False)[:200])
        else:
            with RAW.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        n += 1
        if n % 50 == 0:
            print(f"  {n}/{total} ...", flush=True)

    print(f"listo. llamadas en esta corrida: {n}. ANOTAR ESTE NUMERO EN EL PAPER.")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--reps", type=int, default=3)
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--count-only", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    main(p.parse_args())
