"""Aislamiento del factor: quita SOLO la licencia, conserva todo lo demas.

La corrida neutra (run_neutral_system.py) quito dos cosas a la vez: la licencia y el
encuadre de experto. Por tanto demostro que el BLOQUE produce la firma, no que la
produzca la licencia. Este script aisla el factor.

  ORIGINAL (licenciado):
    "You are an expert in Neutrosophic Logic. You evaluate statements using FOUR
     INDEPENDENT dimensions, each on [0.0, 1.0]. These dimensions are NOT constrained
     to sum to 1.0. A statement can be simultaneously partially true, partially false,
     partially indeterminate and partially neutral. Respond with ONLY a JSON object,
     no other text."

  ESTA CORRIDA (sin licencia): identico, menos las dos frases centrales.
    "You are an expert in Neutrosophic Logic. You evaluate statements using FOUR
     INDEPENDENT dimensions, each on [0.0, 1.0]. Respond with ONLY a JSON object,
     no other text."

  NEUTRO (ya corrido): sin rol, sin dimensiones, sin licencia.

Tres condiciones sobre los mismos 60 items x 6 modelos x G1. Si la tasa fuerte cae
aqui igual que en la neutra, la licencia es la causa. Si no cae, la causa es el
encuadre y no la licencia.

Uso:
    python run_nolicense_system.py --count-only
    python run_nolicense_system.py
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

from openai import OpenAI

HERE = Path(__file__).resolve().parent
RAW = HERE / "results" / "raw_nolicense_system.jsonl"

MODELS = [
    {"id": "openai/gpt-4o", "label": "gpt-4o", "vendor": "openai"},
    {"id": "anthropic/claude-sonnet-4", "label": "claude-sonnet-4", "vendor": "anthropic"},
    {"id": "meta-llama/llama-4-maverick", "label": "llama-4-maverick", "vendor": "meta"},
    {"id": "deepseek/deepseek-chat", "label": "deepseek-chat", "vendor": "deepseek"},
    {"id": "qwen/qwen3-235b-a22b-2507", "label": "qwen3-235b", "vendor": "alibaba"},
    {"id": "mistralai/mistral-medium-3.1", "label": "mistral-medium-3.1", "vendor": "mistral"},
]

# Identico al original salvo por la supresion de las dos frases de licencia.
SYSTEM_NOLICENSE = (
    "You are an expert in Neutrosophic Logic. You evaluate statements using FOUR "
    "INDEPENDENT dimensions, each on [0.0, 1.0]. Respond with ONLY a JSON object, "
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

GLOSS_G1 = ("To what degree do you take no side on this statement, neither affirming nor "
            "denying it, independently of whether its truth value is knowable?")

MAX_RETRIES = 4


def rung(T, I, N, F):
    if T + F > 1:
        return "strong"
    if T + F + I > 1 or T + F + N > 1:
        return "weak"
    if T + F + I + N > 1:
        return "very_weak"
    return "classical"


def parse(text):
    m = re.search(r"\{[^{}]*\}", text or "", re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
        v = [float(d[k]) for k in ("T", "I", "N", "F")]
    except Exception:                                   # noqa: BLE001
        return None
    return v if all(isinstance(x, float) for x in v) else None


def done_keys():
    seen = set()
    if RAW.exists():
        for line in RAW.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                seen.add((r["model"], r["item_id"]))
    return seen


def call(cl, model_id, user):
    for attempt in range(MAX_RETRIES):
        try:
            r = cl.chat.completions.create(
                model=model_id,
                messages=[{"role": "system", "content": SYSTEM_NOLICENSE},
                          {"role": "user", "content": user}],
                temperature=1.0, max_tokens=200,
            )
            return (r.choices[0].message.content or "").strip()
        except Exception as exc:                        # noqa: BLE001
            if attempt == MAX_RETRIES - 1:
                return f"__ERROR__ {exc}"
            time.sleep(3.0 * (attempt + 1))
    return "__ERROR__ unreachable"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count-only", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()

    items = [it for it in json.loads((HERE / "items.json").read_text(encoding="utf-8"))
             if it["form"] in ("bare", "anchor")]
    if a.limit:
        items = items[:a.limit]

    total = len(items) * len(MODELS)
    print(f"diseno: {len(items)} items x {len(MODELS)} modelos x G1 x 1 rep")
    print(f"TOTAL LLAMADAS = {total}")
    print("system message: SIN LICENCIA (conserva rol y dimensiones)")
    if a.count_only:
        return

    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("OPENROUTER_API_KEY is not set.")
    cl = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key)

    RAW.parent.mkdir(exist_ok=True)
    seen = done_keys()
    print(f"reanudando: {len(seen)} llamadas ya registradas")

    n = 0
    for it in items:
        for model in MODELS:
            if (model["label"], it["id"]) in seen:
                continue
            text = call(cl, model["id"], BASE.format(stmt=it["text"], n_gloss=GLOSS_G1))
            v = parse(text)
            rec = {
                "model": model["label"], "vendor": model["vendor"],
                "item_id": it["id"], "pair": it.get("pair"),
                "phenomenon": it["phenomenon"], "form": it["form"],
                "statement": it["text"], "gloss": "G1", "system": "nolicense",
                "response": text,
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
            if n % 25 == 0:
                print(f"  {n}/{total} ...", flush=True)

    print(f"listo. llamadas en esta corrida: {n}")


if __name__ == "__main__":
    main()
