"""Genera las dos versiones alternativas desde paper/main.tex.

El cuerpo NO se toca: se sustituyen titulo, resumen y los dos parrafos de encuadre que
dependen del publico. Asi las tres versiones comparten datos, cifras, figuras y reglas
byte a byte, y solo difieren en como se presentan.

Se compilan dentro de paper/ para que las rutas de figuras y refs.bib funcionen sin
tocar nada, y los PDF resultantes se copian a alternates/.

Uso:  python build_variants.py
"""
from __future__ import annotations

import io
import re
import shutil
import subprocess
from pathlib import Path

B = chr(92)
HERE = Path(__file__).resolve().parent
PAPER = HERE.parent / "paper"

SRC = (PAPER / "main.tex").read_text(encoding="utf-8")

TITLE_OLD = (B + "title{Three Ways an Elicited Evaluation Measures Its Own Design" + B + B + "\n"
             + B + "large Item sampling, instruction effects, and threshold artifacts," + B + B + "\n"
             "with a worked case and 7{,}920 elicitations}")

# el parrafo que ancla la contribucion en psicometria; cambia de anclaje por publico
NOTNEW_OLD = """\\paragraph{What is not new.} That elicitation format moves elicited confidence is established
\\citep{protocolsens2026}, as is the unreliability of LLM judges \\citep{coinflip2026}; that
few-item instruments are imprecise is elementary psychometrics \\citep{cronbach1972}. What we
add is the size of each effect measured on a common corpus, the fact that the second one
defeats the natural ablation, the conversion of the first into a number of items, and a
replication on an unrelated construct family that shows which of the three magnitudes
transfer---none of them---and why."""

VARIANTS = {
    "ipm": {
        "title": (B + "title{When the Instrument Produces the Score" + B + B + "\n"
                  + B + "large Item sampling, instruction framing and threshold placement" + B + B + "\n"
                  "in {LLM}-based evaluation}"),
        "abstract": HERE / "abstract_IPM.txt",
        "notnew": """\\paragraph{What is not new.} That elicitation format moves elicited confidence is established
\\citep{protocolsens2026}, as is the unreliability of LLM judges \\citep{coinflip2026}; that a
test set of a few items estimates those items rather than the construct behind them is older
still \\citep{cronbach1972}. What we add is the size of each effect measured on a common corpus,
the fact that the second one defeats the natural ablation, the conversion of the first into a
bank size, and a replication on an unrelated construct family that shows which of the three
magnitudes transfer---none of them---and why. The audience we have in mind is whoever has to
size, instruct and threshold an evaluation pipeline before running it.""",
    },
    "nlp": {
        "title": (B + "title{How Much of an Elicited Evaluation Is the Protocol?" + B + B + "\n"
                  + B + "large Three measured artifacts and the design rules they imply}"),
        "abstract": HERE / "abstract_NLP_Cambridge.txt",
        "notnew": """\\paragraph{What is not new.} That elicitation format moves elicited confidence is established
\\citep{protocolsens2026}, and the unreliability of LLM judges is by now a standard caveat
\\citep{coinflip2026}; that few-item test sets are imprecise is older than either
\\citep{cronbach1972}. This paper continues that line rather than opening one. What it adds is
the size of the three effects measured together on a common corpus, the fact that the second
defeats the natural ablation, the conversion of the first into a number of items, and a
replication on an unrelated construct family that shows which magnitudes
transfer---none of them---and why.""",
    },
}


def latex_abstract(path: Path) -> str:
    """Pasa el abstract en texto plano a LaTeX, respetando parrafos."""
    t = path.read_text(encoding="utf-8")
    paras = [" ".join(p.split()) for p in t.split("\n\n") if p.strip()]
    out = []
    for p in paras:
        p = p.replace("%", B + "%")
        p = p.replace("+/-", "$" + B + "pm$ ")
        p = re.sub(r"\b(\d),(\d\d\d)\b", r"$\1{,}\2$", p)
        p = p.replace(" — ", "---").replace("—", "---")
        out.append(p)
    return "\n\n".join(out)


def build(tag: str, spec: dict) -> Path:
    s = SRC
    assert TITLE_OLD in s, "titulo no encontrado"
    s = s.replace(TITLE_OLD, spec["title"], 1)

    i = s.index(B + "begin{abstract}") + len(B + "begin{abstract}")
    j = s.index(B + "end{abstract}")
    s = s[:i] + "\n" + latex_abstract(spec["abstract"]) + "\n" + s[j:]

    assert NOTNEW_OLD in s, "parrafo 'What is not new' no encontrado"
    s = s.replace(NOTNEW_OLD, spec["notnew"], 1)

    tex = PAPER / f"main_{tag}.tex"
    tex.write_text(s, encoding="utf-8", newline="\n")

    for _ in range(2):
        subprocess.run(["pdflatex", "-interaction=nonstopmode", tex.name],
                       cwd=PAPER, capture_output=True)
    subprocess.run(["bibtex", f"main_{tag}"], cwd=PAPER, capture_output=True)
    for _ in range(2):
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", tex.name],
                           cwd=PAPER, capture_output=True, text=True)

    log = (PAPER / f"main_{tag}.log").read_text(encoding="utf-8", errors="replace")
    pdf = PAPER / f"main_{tag}.pdf"
    ok = "Output written" in r.stdout
    print(f"  {tag}: {'compila' if ok else 'FALLA'}  "
          f"undefined={log.lower().count('undefined')}  "
          f"overfull-align={len(re.findall(r'Overfull.*in alignment', log))}")
    return pdf


def main():
    import fitz
    made = []
    for tag, spec in VARIANTS.items():
        pdf = build(tag, spec)
        dst = HERE / f"main_{tag}.pdf"
        shutil.copy2(pdf, dst)
        made.append(dst)

    print("\n=== verificacion de figuras e integridad ===")
    ref = PAPER / "main.pdf"
    for p in [ref] + made:
        d = fitz.open(p)
        imgs = sum(len(pg.get_images(full=True)) for pg in d)
        draws = sum(len(pg.get_drawings()) for pg in d)
        txt = "".join(pg.get_text() for pg in d)
        figs = len(re.findall(r"Figure \d", txt))
        tabs = len(re.findall(r"Table \d", txt))
        print(f"  {p.name:<16} {d.page_count:>3} pp  "
              f"figuras-referidas {figs:>2}  tablas {tabs:>2}  "
              f"vectores {draws:>5}  palabras {len(txt.split()):>5}")


if __name__ == "__main__":
    main()
