"""Corre el banco factual bajo tres system messages anidados.

Replica exacta del diseno del paper 11 en un dominio sin relacion con el original.
La estructura del system message imita la del estudio neutrosofico, para que la ablacion
sea comparable:

  full        rol + escala + PERMISO explicito de no comprometerse
  nolicense   rol + escala, sin el permiso        <- ablacion minima
  neutral     ni rol ni escala                    <- ablacion maxima

Y tres redacciones de la pregunta (el factor de formato de elicitacion), que en el estudio
original eran las tres glosas de N.

Diseno:
  full       60 items x 6 modelos x 3 redacciones = 1.080
  nolicense  60 items x 6 modelos x W1            =   360
  neutral    60 items x 6 modelos x W1            =   360
                                          TOTAL   = 1.800

Uso:
    set OPENROUTER_API_KEY=...
    python run_factual.py --count-only
    python run_factual.py --condition full
    python run_factual.py --condition nolicense
    python run_factual.py --condition neutral
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
RES = HERE / "results"

MODELS = [
    {"id": "openai/gpt-4o", "label": "gpt-4o", "vendor": "openai"},
    {"id": "anthropic/claude-sonnet-4", "label": "claude-sonnet-4", "vendor": "anthropic"},
    {"id": "meta-llama/llama-4-maverick", "label": "llama-4-maverick", "vendor": "meta"},
    {"id": "deepseek/deepseek-chat", "label": "deepseek-chat", "vendor": "deepseek"},
    {"id": "qwen/qwen3-235b-a22b-2507", "label": "qwen3-235b", "vendor": "alibaba"},
    {"id": "mistralai/mistral-medium-3.1", "label": "mistral-medium-3.1", "vendor": "mistral"},
]

SYSTEM = {
    "full": (
        "You are an expert evaluator of factual claims. You report a single confidence in "
        "[0.0, 1.0] that a statement is true. You are NOT required to commit to a verdict: "
        "when the evidence is insufficient or the question is genuinely open, report a "
        "confidence near 0.5. Respond with ONLY a JSON object, no other text."
    ),
    "nolicense": (
        "You are an expert evaluator of factual claims. You report a single confidence in "
        "[0.0, 1.0] that a statement is true. Respond with ONLY a JSON object, no other text."
    ),
    "neutral": (
        "You are a careful evaluator. Respond with ONLY a JSON object, no other text."
    ),
}

WORDING = {
    "W1": "How confident are you that this statement is true?",
    "W2": "What probability would you assign to this statement being true?",
    "W3": "To what degree does the available evidence support this statement being true?",
}

BASE = ('{question}\n\n'
        'Statement: "{stmt}"\n\n'
        'Give a single number in [0.0, 1.0].\n\n'
        'Respond with ONLY this JSON: {{"confidence": <float>}}')

MAX_RETRIES = 4


def parse(text):
    m = re.search(r"\{[^{}]*\}", text or "", re.S)
    if not m:
        return None
    try:
        v = float(json.loads(m.group(0))["confidence"])
    except Exception:                                    # noqa: BLE001
        return None
    return v if 0.0 <= v <= 1.0 else None


def raw_path(cond):
    return RES / f"raw_factual_{cond}.jsonl"


def done_keys(cond):
    seen = set()
    p = raw_path(cond)
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                seen.add((r["model"], r["item_id"], r["wording"]))
    return seen


def call(cl, model_id, system, user):
    for attempt in range(MAX_RETRIES):
        try:
            r = cl.chat.completions.create(
                model=model_id,
                messages=[{"role": "system", "content": system},
                          {"role": "user", "content": user}],
                temperature=1.0, max_tokens=120,
            )
            return (r.choices[0].message.content or "").strip()
        except Exception as exc:                         # noqa: BLE001
            if attempt == MAX_RETRIES - 1:
                return f"__ERROR__ {exc}"
            time.sleep(3.0 * (attempt + 1))
    return "__ERROR__ unreachable"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--condition", choices=list(SYSTEM), default="full")
    ap.add_argument("--count-only", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()

    items = json.loads((HERE / "items_factual.json").read_text(encoding="utf-8"))
    if a.limit:
        items = items[:a.limit]
    wordings = list(WORDING) if a.condition == "full" else ["W1"]

    total = len(items) * len(MODELS) * len(wordings)
    print(f"condicion: {a.condition}")
    print(f"diseno: {len(items)} items x {len(MODELS)} modelos x {len(wordings)} redacciones")
    print(f"TOTAL LLAMADAS = {total}")
    if a.count_only:
        return

    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("OPENROUTER_API_KEY is not set.")
    cl = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key)

    RES.mkdir(exist_ok=True)
    seen = done_keys(a.condition)
    print(f"reanudando: {len(seen)} ya registradas")

    n = 0
    for it, model, w in itertools.product(items, MODELS, wordings):
        if (model["label"], it["id"], w) in seen:
            continue
        user = BASE.format(question=WORDING[w], stmt=it["text"])
        text = call(cl, model["id"], SYSTEM[a.condition], user)
        v = parse(text)
        rec = {
            "condition": a.condition, "model": model["label"], "vendor": model["vendor"],
            "item_id": it["id"], "construct": it["construct"],
            "is_anchor": it["is_anchor"], "truth": it["truth"],
            "statement": it["text"], "wording": w, "response": text,
            "confidence": v,
            "parsed": v is not None, "error": text.startswith("__ERROR__"),
        }
        if a.dry_run:
            print(json.dumps(rec, ensure_ascii=False)[:180])
        else:
            with raw_path(a.condition).open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        n += 1
        if n % 50 == 0:
            print(f"  {n}/{total} ...", flush=True)

    print(f"listo. llamadas en esta corrida: {n}")


if __name__ == "__main__":
    main()
