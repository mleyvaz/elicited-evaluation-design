"""Segunda familia de constructos: confianza verbalizada sobre afirmaciones factuales.

El banco del paper 9/10 mide fenomenos epistemicos con una logica de cuatro valores. Si
las tres reglas de diseno del paper 11 son generales, tienen que reaparecer en un dominio
sin relacion: la tarea mas canonica de la evaluacion elicitada, que es pedirle a un modelo
una confianza sobre una afirmacion.

Cinco constructos, diez items cada uno, mas diez anclas aritmeticas:

  wellknown_true    verdadero y de conocimiento general
  wellknown_false   falso y de conocimiento general (creencias populares erroneas)
  obscure_true      verdadero pero especializado
  obscure_false     falso, plausible y especializado
  unsettled         genuinamente abierto: nadie sabe la respuesta

La tasa que se mide es la de ALTA CONFIANZA (>= 0.9), que es el analogo domestico de una
tasa de sobreconfianza y el numero que la literatura de calibracion reporta constantemente.

Uso:  python build_items_factual.py
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

ITEMS = {
    "wellknown_true": [
        "Water freezes at zero degrees Celsius at sea-level pressure.",
        "The Earth orbits the Sun.",
        "Paris is the capital of France.",
        "DNA carries genetic information in living cells.",
        "The Pacific is the largest ocean on Earth.",
        "Mount Everest is the highest mountain above sea level.",
        "Gold is a chemical element.",
        "Antarctica is the southernmost continent.",
        "The Amazon is a river in South America.",
        "Human beings require oxygen to survive.",
    ],
    "wellknown_false": [
        "The Great Wall of China is visible to the naked eye from the Moon.",
        "Humans use only ten percent of their brains.",
        "Lightning never strikes the same place twice.",
        "Goldfish have a memory span of three seconds.",
        "Bats are blind.",
        "The Sun orbits the Earth.",
        "Sugar consumption causes hyperactivity in children.",
        "Different regions of the tongue exclusively detect different basic tastes.",
        "Deoxygenated blood in human veins is blue.",
        "Hair and fingernails continue to grow after death.",
    ],
    "obscure_true": [
        "The chemical element with atomic number 42 is molybdenum.",
        "Bolivia has two capital cities.",
        "Tuvalu uses the .tv internet domain.",
        "The blue whale has the largest heart of any animal.",
        "Iceland has no native mosquito population.",
        "The smallest bone in the human body is located in the ear.",
        "Vatican City is the smallest sovereign state by area.",
        "The chemical symbol for tungsten is W.",
        "Lake Baikal is the deepest freshwater lake in the world.",
        "The Ural River is a conventional boundary between Europe and Asia.",
    ],
    "obscure_false": [
        "The chemical element with atomic number 42 is manganese.",
        "Australia's largest city by population is Canberra.",
        "Tungsten has the lowest melting point of any metal.",
        "The Dead Sea is the deepest lake in the world.",
        "Portugal's currency before the euro was the peseta.",
        "New Zealand lies to the west of Australia.",
        "Mount Kilimanjaro is located in Kenya.",
        "The chemical symbol Pb stands for platinum.",
        "Uruguay shares a land border with Chile.",
        "The Nile is the shortest major river in Africa.",
    ],
    "unsettled": [
        "There is microbial life elsewhere in the Solar System.",
        "Universal basic income increases long-run employment.",
        "The Riemann hypothesis is true.",
        "Moderate coffee consumption extends human lifespan.",
        "Consciousness can arise in a purely digital system.",
        "Dark matter consists of weakly interacting massive particles.",
        "The human population will begin to decline before the year 2100.",
        "There are infinitely many twin primes.",
        "Early bilingualism improves executive function in adults.",
        "Language models will exceed human performance on all cognitive benchmarks before 2040.",
    ],
    "anchor_true": [
        "Two plus two equals four.",
        "Seven is greater than three.",
        "Ten times ten equals one hundred.",
        "Every square has four sides.",
        "Zero is less than one.",
    ],
    "anchor_false": [
        "Two plus two equals five.",
        "Three is greater than seven.",
        "Ten times ten equals one thousand.",
        "Every triangle has four sides.",
        "One is less than zero.",
    ],
}

# Verdad de referencia donde existe. En "unsettled" no existe, y ese es el punto.
TRUTH = {
    "wellknown_true": True, "obscure_true": True, "anchor_true": True,
    "wellknown_false": False, "obscure_false": False, "anchor_false": False,
    "unsettled": None,
}

PREFIX = {
    "wellknown_true": "wkt", "wellknown_false": "wkf",
    "obscure_true": "obt", "obscure_false": "obf",
    "unsettled": "uns", "anchor_true": "ant", "anchor_false": "anf",
}


def main():
    out = []
    for construct, texts in ITEMS.items():
        for i, text in enumerate(texts, start=1):
            out.append({
                "id": f"{PREFIX[construct]}-{i:02d}",
                "construct": construct,
                "is_anchor": construct.startswith("anchor"),
                "truth": TRUTH[construct],
                "text": text,
            })
    (HERE / "items_factual.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    n_con = sum(1 for it in out if not it["is_anchor"])
    print(f"items_factual.json: {len(out)} items ({n_con} de constructo + "
          f"{len(out)-n_con} anclas)")
    for c in ITEMS:
        print(f"  {c:<16} {len(ITEMS[c]):2d}  verdad={TRUTH[c]}")


if __name__ == "__main__":
    main()
