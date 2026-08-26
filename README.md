# Three Ways an Elicited Evaluation Measures Its Own Design

Item sampling, instruction effects, and threshold artifacts, quantified on **7,920 elicitations**
across six frontier model families and two unrelated construct families.

This repository is the complete artifact for the paper: both item banks, every raw generation
including response text, the elicitation and analysis scripts, and the code that produces every
figure and table.

**Paper:** [`paper/main.pdf`](paper/main.pdf) · **Author:** Maikel Y. Leyva-Vázquez

---

## What the paper measures

A large class of evaluations asks a model to report a number about a statement — a confidence, a
rating, a degree of some property — and then treats the number as a measurement. Three features of
that design produce the number as much as the model does. Each is individually well known; the
contribution here is measuring all three on a common corpus, and then again on a second corpus
that shares the design and nothing else.

**1 · Item sampling.** A rate computed on one statement per construct is a property of that
statement. In the worked case a published figure of `0.661`, obtained from one sentence, becomes
`0.223` over ten — and `0.661` is the ceiling of the ten-item range. Reaching a ±0.05 half-width
takes **69 items** in one family and **1 to 20** in the other, depending on the construct. The
rule is not that between-item variance is large; it is that the required item count varies by
almost seventy-fold across ordinary evaluation targets and cannot be assumed.

**2 · Instruction effects, where the obvious ablation fails.** Deleting the sentence that names
the measured behaviour barely moves the result (`0.077 → 0.060`, overlapping intervals). Deleting
the surrounding framing takes it to `0.004`. Ablating the sentence you suspect is not enough —
the question itself is the treatment. On the second family the framing ablation does **not**
replicate, and the reason generalises the rule: *framing is worth what the model could not have
inferred without it.*

**3 · Threshold artifacts.** Models answer on a coarse grid — 46 distinct values across 7,852
elicited components, 89.5% of them multiples of 0.1 — so a threshold placed on a modal value
adjudicates a large share of cases by rounding. Moving a comparison from strict to non-strict
moves a control condition from `0.000` to `0.778`. On the second family, moving a high-confidence
cut from 0.60 to 0.90 changes the rate on the only construct with dispersion by a **factor of 16**.

Each result closes with a design rule, which is what makes the paper prescriptive rather than
merely cautionary. A fourth, shorter section separates inter-model disagreement from single-model
stochastic variation.

## The two construct families

| | Family I — epistemic states | Family II — factual confidence |
|---|---|---|
| Task | four components per statement | one confidence per statement |
| Constructs | ethical conflict, epistemic ignorance, vagueness, future contingency, logical paradox | well-known true / false, obscure true / false, genuinely open |
| Items | 110 (incl. anchors) | 60 (incl. arithmetic anchors) |
| Elicitations | 6,120 | 1,800 |
| Provenance | collected for the companion studies — see [`family1/README.md`](family1/README.md) | collected for **this** paper |

Family II exists to answer the question that decides whether a methods paper is worth anything:
are these properties of the elicited design, or of the subject matter the first corpus happened to
be about? The answer is not uniform — one of the three effects does not survive the move — and
that non-replication is reported as a finding, not buried.

## Layout

```
paper/      LaTeX source, compiled PDF, and the figure files it includes
family1/    epistemic-state bank: items, raw generations, elicitation and analysis scripts
family2/    factual-confidence bank: the same, collected for this paper
figures/    the three figure generators; each writes into paper/
```

## Reproducing

Analysis and figures run from the released data with no API access:

```bash
python family1/analyze_quad_bank.py                # Family I, the bank study
python family1/analyze_system_conditions.py        # Family I, the three instruction conditions
python family2/analyze_factual.py                  # Family II, all four rules
python figures/make_figures.py                     # figA_precision, figB_grid
python figures/make_fig1_between_items.py          # fig1_between_items
python figures/make_figure_factual.py              # figC_threshold
cd paper && pdflatex main && bibtex main && pdflatex main && pdflatex main
```

Re-collecting the generations needs `OPENROUTER_API_KEY` and costs real money:

```bash
python family2/build_items_factual.py              # rebuild items_factual.json
python family2/run_factual.py --count-only         # 1,080 calls in the full condition
python family2/run_factual.py --condition full
python family2/run_factual.py --condition nolicense
python family2/run_factual.py --condition neutral
python family2/dedupe_results.py                   # if two runs ever overlap
```

`run_factual.py` resumes: it reads what is already recorded and skips those cells. Do **not** run
two processes against the same condition at once — each reads the completed set at startup and
cannot see the other's work.

## A note on `analyze_factual_v1.py`

The first version of the Family II analysis is released unrepaired, alongside the version the
paper reports. It took the **high-confidence rate (≥ 0.9)** as its primary outcome, by analogy
with the overconfidence rates the calibration literature reports. On the real data that choice
turned out to be the very artifact the threshold rule predicts: four of five constructs pin to
0.000 or 1.000, and the one construct with genuine between-model dispersion collapses to a rate
of 0.028.

The primary quantity was inverted to the continuous confidence, with the binarised rate kept only
to show what it costs. Both scripts are here because the sequence is part of the evidence, and
quietly replacing the first one would have removed it.

## Companion papers

The Family I corpus was built for two companion studies on a four-valued logic. This is a methods
paper and makes no claim about the logic under test there; that subject matter is a worked example
rather than the topic.

- Smarandache, F. & Leyva-Vázquez, M. Y. (2026). *Is the Ladder Measurable? Graded Paraconsistency
  Tested on Eight Statements and Then on a Bank.*
- Smarandache, F. & Leyva-Vázquez, M. Y. (2026). *One Item Is Not a Phenomenon: Separating Ethical
  Content from Syntactic Marking in Paraconsistent Signature Detection.*

Their own repository, including an independent re-analysis script written by a party who did not
author the studies, is at
[`mleyvaz/paraconsistent-signature-itembank`](https://github.com/mleyvaz/paraconsistent-signature-itembank).

## Models

Six frontier families, one per vendor, through a single router at temperature 1.0: GPT-4o,
Claude Sonnet 4, Llama 4 Maverick, DeepSeek Chat, Qwen3 235B, Mistral Medium 3.1.

## Licence

Code (`*.py`) is MIT. The item banks and all generations are CC BY 4.0. Both are stated in
[`LICENSE`](LICENSE).
