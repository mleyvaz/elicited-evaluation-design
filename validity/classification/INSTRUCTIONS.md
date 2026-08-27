# Item classification task

You will see **60 statements** in random order. For each one, decide **why it is hard to
answer**, and write the two-letter code in the `category` column of your CSV.

Work alone. Do not discuss the items with the other rater until both sheets are finished.
There is no time limit. If you are unsure, choose the closest category rather than leaving
it blank — the point is to measure how reproducible the assignment is, and a blank tells
us nothing.

## Categories

| Code | Category | The statement is contested because... |
|---|---|---|
| **EC** | Ethical conflict | competent people hold opposed moral views about it, and the disagreement is about values rather than about facts |
| **EI** | Epistemic ignorance | there is a fact of the matter, but nobody currently knows it |
| **VG** | Vagueness | the predicate has no sharp boundary, so borderline cases have no determinate answer |
| **FC** | Future contingency | it concerns a future event that is not yet settled |
| **LP** | Logical paradox | asserting it leads to contradiction by its own structure |
| **ST** | Settled truth | it is not contested at all: a tautology, or a fact essentially everyone accepts |


## Rules

1. **One code per statement.** No ties, no multiple codes.
2. **Judge the statement, not your opinion of it.** For *ethical conflict* the question is
   whether competent people disagree, not whether you personally find it obvious.
3. **Some statements are not contested at all.** Those get `ST`. They are mixed in without
   warning and there is no fixed number of them.
4. **Ignore how the statement is phrased.** None of them is phrased as an explicit
   contradiction; judge the content.

## Distinguishing the two that get confused most

*Epistemic ignorance* versus *future contingency*: if the fact already exists and we simply
do not know it, that is **EI**. If the fact does not exist yet because the event has not
happened, that is **FC**.

*Vagueness* versus *ethical conflict*: if the difficulty would survive perfect agreement
about all the values involved, and comes from where a boundary falls, that is **VG**.

## When you finish

Send back your `rater_X.csv` with the `category` column filled. Nothing else.
