"""Elicita el CUADRUPLE (T, I, N, F) sobre el banco de 110 items.

Prueba la escalera de tres peldanos de Smarandache & Leyva-Vazquez (NSS 100, 2026)
sobre una muestra de items que permite conclusiones a nivel de fenomeno, en vez de
sobre las ocho oraciones del corpus v3.

    fuerte     : T + F > 1                                          (4)
    debil      : T + F <= 1  y  (T+F+I > 1  o  T+F+N > 1)           (5)
    muy debil  : T+F+I <= 1, T+F+N <= 1,  y  T+F+I+N > 1            (6)

Diseno: 110 items x 6 modelos x 3 glosas de N x 1 repeticion = 1.980 llamadas.
Con 110 items la varianza que importa es ENTRE items, no dentro de celda; se
cambian repeticiones por cobertura completa de las tres glosas al mismo costo.

Uso:
    set OPENROUTER_API_KEY=...
    python run_quad_bank.py --count-only
    python run_quad_bank.py --limit 4 --dry-run
    python run_quad_bank.py
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
RAW = OUT / "raw_quad_bank.jsonl"

MODELS = [
    {"id": "openai/gpt-4o", "label": "gpt-4o", "vendor": "openai"},
    {"id": "anthropic/claude-sonnet-4", "label": "claude-sonnet-4", "vendor": "anthropic"},
    {"id": "meta-llama/llama-4-maverick", "label": "llama-4-maverick", "vendor": "meta"},
    {"id": "deepseek/deepseek-chat", "label": "deepseek-chat", "vendor": "deepseek"},
    {"id": "qwen/qwen3-235b-a22b-2507", "label": "qwen3-235b", "vendor": "alibaba"},
    {"id": "mistralai/mistral-medium-3.1", "label": "mistral-medium-3.1", "vendor": "mistral"},
]

SYSTEM = (
    "You are an expert in Neutrosophic Logic. You evaluate statements using FOUR "
    "INDEPENDENT dimensions, each on [0.0, 1.0]. These dimensions are NOT constrained "
    "to sum to 1.0. A statement can be simultaneously partially true, partially false, "
    "partially indeterminate and partially neutral. Respond with ONLY a JSON object, "
    "no other text."
)

BASE = (
    'Evaluate this statement on four independent dimensions:\n\n'
    'Statement: "{stmt}"\n\n'
    '- Truth (T): To what degree is this statement true? [0.0 to 1.0]\n'
    '- Indeterminacy (I): To what degree is the truth value unknown, undetermined, '
    'or inherently uncertain? [0.0 to 1.0]\n'
    '- Neutrality (N): {n_gloss} [0.0 to 1.0]\n'
    '- Falsity (F): To what degree is this statement false? [0.0 to 1.0]\n\n'
    'Respond with ONLY this JSON: {{"T": <float>, "I": <float>, "N": <float>, "F": <float>}}'
)

# Las mismas tres glosas del estudio anterior, verbatim, para que los resultados
# sean comparables. La fuente no fija ninguna: por eso es un factor.
N_GLOSS = {
    "G1": "To what degree do you take no side on this statement, neither affirming nor "
          "denying it, independently of whether its truth value is knowable?",
    "G2": "To what degree does the predicate true-or-false simply not apply to this "
          "statement, so that assigning it a truth value would be a category error?",
    "G3": "To what degree do the grounds for and against this statement offset one "
          "another exactly, leaving a balanced position rather than a gap in knowledge?",
}

MAX_RETRIES = 4


def client() -> OpenAI:
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("OPENROUTER_API_KEY is not set.")
    return OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key)


def call(cl, model_id, user):
    for attempt in range(MAX_RETRIES):
        try:
            r = cl.chat.completions.create(
                model=model_id,
                messages=[{"role": "system", "content": SYSTEM},
                          {"role": "user", "content": user}],
                temperature=1.0, max_tokens=200,
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
            v = [float(d[k]) for k in ("T", "I", "N", "F")]
            if all(0.0 <= x <= 1.0 for x in v):
                return tuple(v)
        except Exception:                              # noqa: BLE001
            pass
    got = {}
    for k in ("T", "I", "N", "F"):
        mm = re.search(rf'"?{k}"?\s*[:=]\s*([01](?:\.\d+)?|\.\d+)', text)
        if mm:
            got[k] = float(mm.group(1))
    return tuple(got[k] for k in ("T", "I", "N", "F")) if len(got) == 4 else None


def rung(T, I, N, F):
    if T + F > 1:
        return "strong"
    if T + F + I > 1 or T + F + N > 1:
        return "weak"
    if T + F + I + N > 1:
        return "very_weak"
    return "classical"


def done_keys():
    seen = set()
    if RAW.exists():
        with RAW.open(encoding="utf-8") as fh:
            for line in fh:
                try:
                    d = json.loads(line)
                    seen.add((d["model"], d["item_id"], d["gloss"]))
                except Exception:                      # noqa: BLE001
                    continue
    return seen


def main(a):
    items = json.loads((HERE / "items.json").read_text(encoding="utf-8"))
    if a.limit:
        items = items[:a.limit]
    total = len(items) * len(MODELS) * len(N_GLOSS)
    print(f"diseno: {len(items)} items x {len(MODELS)} modelos x {len(N_GLOSS)} glosas")
    print(f"TOTAL LLAMADAS = {total}")
    if a.count_only:
        return

    cl = client()
    seen = done_keys()
    print(f"reanudando: {len(seen)} llamadas ya registradas")

    n = 0
    for it, model, gk in itertools.product(items, MODELS, N_GLOSS):
        key = (model["label"], it["id"], gk)
        if key in seen:
            continue
        text = call(cl, model["id"], BASE.format(stmt=it["text"], n_gloss=N_GLOSS[gk]))
        v = parse(text)
        rec = {
            "model": model["label"], "vendor": model["vendor"],
            "item_id": it["id"], "pair": it["pair"],
            "phenomenon": it["phenomenon"], "form": it["form"],
            "statement": it["text"], "gloss": gk, "response": text,
            "T": v[0] if v else None, "I": v[1] if v else None,
            "N": v[2] if v else None, "F": v[3] if v else None,
            "rung": rung(*v) if v else None,
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
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--count-only", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    main(p.parse_args())
