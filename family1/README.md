# Family I — epistemic states · provenance

**These generations were not collected for this paper.** They were collected for two companion
studies on a four-valued logic and are reproduced here so that this repository is self-contained
and every number in the paper can be checked without chasing a second repository.

Original repository, which is the citable source:
**[`mleyvaz/paraconsistent-signature-itembank`](https://github.com/mleyvaz/paraconsistent-signature-itembank)**

- Smarandache, F. & Leyva-Vázquez, M. Y. (2026). *Is the Ladder Measurable? Graded Paraconsistency
  Tested on Eight Statements and Then on a Bank.*
- Smarandache, F. & Leyva-Vázquez, M. Y. (2026). *One Item Is Not a Phenomenon: Separating Ethical
  Content from Syntactic Marking in Paraconsistent Signature Detection.*

If you are citing the epistemic-state bank itself, cite those. Cite this repository for the
methods paper and for Family II.

## What is here

| File | Elicitations | What it is |
|---|---|---|
| `results/raw_bank.jsonl` | 1,980 | the item bank, three wordings |
| `results/raw_quad_bank.jsonl` | 1,980 | the same bank, three repetitions |
| `results/raw_quadruple_pilot.jsonl` | 1,440 | the eight-statement pilot, ten repetitions |
| `results/raw_nolicense_system.jsonl` | 360 | ablation A — the permission sentence removed |
| `results/raw_neutral_system.jsonl` | 360 | ablation B — the framing removed |
| `items.json` | — | 110 items: ten per construct across five constructs, plus ten anchors |

Total 6,120. Each record carries the model, vendor, item, construct, elicitation form, the raw
response text, the parsed components and the derived label.

The elicitation and analysis scripts are copied alongside, unmodified, so the derived numbers can
be regenerated here. One file from the original repository is deliberately **not** reproduced:
`results/fig1_per_item.json`, a hand-made intermediate that no script produced. The figure that
consumed it now computes the same values from `raw_quad_bank.jsonl`, verified identical across all
five constructs — see `figures/make_fig1_between_items.py`.

## What is not here

The companion repository also carries the independent re-analysis script commissioned after an
adversarial audit, and the record of the claims that audit corrected. That material belongs to the
companion studies and is left where it is.

## Licence

CC BY 4.0, as released by the companion studies.
