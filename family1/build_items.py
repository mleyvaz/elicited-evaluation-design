"""Construye el banco de items para separar CONTENIDO de MARCA SINTACTICA.

El corpus v3 tiene un enunciado por fenomeno, y el item etico
  "Lying to save an innocent life is morally right and wrong at the same time."
contiene literalmente la conjuncion de opuestos. Con n=1 no se puede saber si el
66% de T+F>1 se debe al conflicto de valores o a que el modelo lee "right and
wrong at the same time" como instruccion.

Diseno 2 x 5:
  fenomeno (5)  x  forma (2: bare / marked)  x  10 stems  =  100 items
  + 10 anclas (5 tautologias, 5 consensos)                =  110 items

La forma MARKED envuelve exactamente el mismo contenido en "both P and not-P".
Asi:
  - etico BARE que aun da T+F>1  -> el fenomeno es real
  - no-etico MARKED que da T+F>1 -> la marca sola dispara la firma

Se elicita la TRIPLETA (T, I, F), no el cuadruple: la condicion fuerte T+F>1 no
contiene N, y usar el triple mantiene comparabilidad con el corpus publicado.

Uso:  python build_items.py   ->  items.json
"""

import json
from pathlib import Path

# Cada stem: (sujeto/contenido, predicado bare, predicado negado para la forma marked)
STEMS = {
    "ethical": [
        ("Lying to protect a refugee from deportation",
         "is morally permissible", "is both permissible and impermissible"),
        ("Breaking a promise in order to prevent a serious injury",
         "is the right action", "is both the right and the wrong action"),
        ("Diverting scarce medicine from an elderly patient to a child",
         "is justified", "is both justified and unjustified"),
        ("Reporting a colleague who falsified data but would lose their visa",
         "is the correct choice", "is both the correct and the incorrect choice"),
        ("Withholding a terminal diagnosis at a family's request",
         "respects the patient", "both respects and disrespects the patient"),
        ("Paying a bribe to release medical supplies held at customs",
         "is defensible", "is both defensible and indefensible"),
        ("Publishing a leak that exposes corruption and endangers a source",
         "is ethical journalism", "is both ethical and unethical journalism"),
        ("Conscripting citizens to defend against an invasion",
         "is legitimate", "is both legitimate and illegitimate"),
        ("Using a dying language's sacred texts to train a public model",
         "honours the community", "both honours and dishonours the community"),
        ("Refusing life support that the patient once requested in writing",
         "follows their wishes", "both follows and violates their wishes"),
    ],
    "ignorance": [
        ("The number of grains of sand on Earth",
         "is odd", "is both odd and even"),
        ("The total number of species that existed before the Cambrian",
         "is a prime number", "is both prime and not prime"),
        ("The number of atoms in the observable universe",
         "ends in a seven", "both ends and does not end in a seven"),
        ("The exact number of words spoken on Earth yesterday",
         "is divisible by nine", "is both divisible and not divisible by nine"),
        ("The number of undiscovered shipwrecks in the Pacific",
         "exceeds one hundred thousand", "both exceeds and does not exceed one hundred thousand"),
        ("The count of raindrops that fell on Quito in 1804",
         "is a multiple of four", "is both a multiple and not a multiple of four"),
        ("The number of prime numbers below the largest integer ever written down",
         "is odd", "is both odd and even"),
        ("The quantity of gold still buried in unmapped deposits",
         "exceeds all gold ever mined", "both exceeds and does not exceed all gold ever mined"),
        ("The number of distinct human languages ever spoken",
         "is greater than thirty thousand", "is both greater and not greater than thirty thousand"),
        ("The number of neurons in the brain of the last mammoth",
         "was even", "was both even and odd"),
    ],
    "vagueness": [
        ("A man who is 1.75 metres tall",
         "is tall", "is both tall and not tall"),
        ("A cup of coffee at 55 degrees Celsius",
         "is hot", "is both hot and not hot"),
        ("A person with 1,300 hairs on their head",
         "is bald", "is both bald and not bald"),
        ("A heap of 12 grains of wheat",
         "is a heap", "is both a heap and not a heap"),
        ("A dialect understood by 60 per cent of neighbouring speakers",
         "is a separate language", "is both a separate language and not one"),
        ("A river that runs dry for four months a year",
         "is a permanent river", "is both permanent and not permanent"),
        ("A student who answered 59 out of 100 correctly",
         "has passed", "has both passed and not passed"),
        ("A settlement of 4,000 inhabitants",
         "is a city", "is both a city and not a city"),
        ("A meal costing eight per cent of a daily wage",
         "is expensive", "is both expensive and not expensive"),
        ("A forest that has lost 40 per cent of its canopy",
         "is deforested", "is both deforested and not deforested"),
    ],
    "contingency": [
        ("Snow", "will fall in Quito next January",
         "will both fall and not fall in Quito next January"),
        ("The price of copper", "will exceed ten thousand dollars a tonne in 2031",
         "will both exceed and not exceed ten thousand dollars a tonne in 2031"),
        ("A woman", "will be elected president of Peru in the next election",
         "will both be and not be elected president of Peru in the next election"),
        ("The Amazon", "will lose a fifth of its remaining canopy by 2040",
         "will both lose and not lose a fifth of its remaining canopy by 2040"),
        ("A magnitude eight earthquake", "will strike Chile before 2035",
         "will both strike and not strike Chile before 2035"),
        ("Sea level at Guayaquil", "will rise by half a metre this century",
         "will both rise and not rise by half a metre this century"),
        ("A treaty on autonomous weapons", "will be signed before 2030",
         "will both be and not be signed before 2030"),
        ("The next pandemic", "will originate in a non-human mammal",
         "will both originate and not originate in a non-human mammal"),
        ("Quechua", "will have more speakers in 2075 than today",
         "will both have and not have more speakers in 2075 than today"),
        ("A crewed mission", "will reach Mars before 2045",
         "will both reach and not reach Mars before 2045"),
    ],
    "paradox": [
        ("This sentence", "is false", "is both true and false"),
        ("The claim written on the other side of this card",
         "is untrue", "is both true and untrue"),
        ("The barber who shaves exactly those who do not shave themselves",
         "shaves himself", "both shaves and does not shave himself"),
        ("The set of all sets that are not members of themselves",
         "is a member of itself", "both is and is not a member of itself"),
        ("The smallest positive integer not definable in under twelve words",
         "has just been defined", "both has and has not just been defined"),
        ("This statement", "cannot be proved", "both can and cannot be proved"),
        ("A prisoner told they will be hanged on a day they cannot expect",
         "can be surprised", "both can and cannot be surprised"),
        ("The sentence that asserts its own unbelievability",
         "should be believed", "both should and should not be believed"),
        ("A map contained entirely within the territory it depicts",
         "depicts itself accurately", "both does and does not depict itself accurately"),
        ("The rule that every rule has an exception",
         "has an exception", "both has and does not have an exception"),
    ],
}

# Anclas. Deben salir en el regimen clasico: T alto, F bajo, sin exceso.
ANCHORS = [
    ("tautology", "Two plus two equals four."),
    ("tautology", "Every bachelor is unmarried."),
    ("tautology", "It is raining or it is not raining."),
    ("tautology", "Every triangle has three sides."),
    ("tautology", "Nothing is both entirely red and entirely green all over."),
    ("consensus", "Water freezes at zero degrees Celsius at sea-level pressure."),
    ("consensus", "The Earth completes one orbit of the Sun in about 365 days."),
    ("consensus", "Smoking tobacco raises the risk of lung cancer."),
    ("consensus", "Guayaquil is a city in Ecuador."),
    ("consensus", "Human beings require oxygen to survive."),
]


def build():
    items = []
    for phen, stems in STEMS.items():
        for i, (subj, bare, marked) in enumerate(stems, 1):
            items.append({"id": f"{phen[:4]}-{i:02d}-bare", "phenomenon": phen,
                          "form": "bare", "pair": f"{phen[:4]}-{i:02d}",
                          "text": f"{subj} {bare}."})
            items.append({"id": f"{phen[:4]}-{i:02d}-mark", "phenomenon": phen,
                          "form": "marked", "pair": f"{phen[:4]}-{i:02d}",
                          "text": f"{subj} {marked}."})
    for i, (kind, text) in enumerate(ANCHORS, 1):
        items.append({"id": f"anch-{i:02d}", "phenomenon": kind,
                      "form": "anchor", "pair": f"anch-{i:02d}", "text": text})

    Path("items.json").write_text(json.dumps(items, indent=1, ensure_ascii=False),
                                  encoding="utf-8")

    import statistics as st
    lens = {}
    for it in items:
        lens.setdefault((it["phenomenon"], it["form"]), []).append(len(it["text"].split()))
    print(f"items: {len(items)}")
    print(f"  contested pairs: {sum(1 for i in items if i['form']=='bare')}")
    print(f"  anchors:         {sum(1 for i in items if i['form']=='anchor')}")
    print("\nlongitud media en palabras (control de emparejamiento superficial):")
    for k in sorted(lens):
        v = lens[k]
        print(f"  {k[0]:12s} {k[1]:7s} n={len(v):3d}  media={st.mean(v):5.1f}  "
              f"rango={min(v)}-{max(v)}")


if __name__ == "__main__":
    build()
