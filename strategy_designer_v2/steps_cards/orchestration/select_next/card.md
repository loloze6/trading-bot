# Function card: select_next (orchestration, proposed 2026-11-16, for the operator's review)

A function card (no model of its own): what it selects, its score, where its numbers come from, how to call it.

## Business objective, one question
Which idea should the workflow test next?

**Establish, among the ideas the analysis lines proposed in a run and not yet tested, the one most likely to bring
the workflow closer to an idea that is real with a book that pays, by one score fixed in advance, computed from the
workflow's own recorded results, and shown with its parts.**

## Input and output
- **Input:** a run name.
- **Output:** the run's candidates, ranked: each with its score, the parts of the score, and why it is or is not a
  candidate. The first is the next idea.

## What a candidate is
**A candidate is an idea a step 7 line proposed in the run, not yet tested in the run, and not a duplicate.**
- **Proposed in the run:** in a line's `<run>/<backtest>/ideas/`.
- **Not tested:** no plan for it in the run (`03_test_plan/<run>/plans/`).
- **Not a duplicate:** its text and its data are not those of an idea already tested or already a candidate (the same
  text on other data, a `same-idea-on:` proposal, is not a duplicate). A duplicate is listed, with the idea it repeats.
- The words (created from, line, analysis, ideas written together, generation) are those of
  `../../common/idea_created_from.md`.

## The score
In the words of `../../common/idea_created_from.md`. A candidate's id is `F.lN_name`: `F` the idea it was created
from, `l` the line's letter, `N` its number in that analysis.

**score = record of line l x novelty of the candidate**

| Part | In id terms | Why |
|---|---|---|
| **record of line l** | over every analysis of line `l` with at least one tested idea (every id `F'.lM`, in any run): (s + 1) / (n + 2), n the number of these analyses, s the sum of their **progress**; an analysis's progress is the best of its tested ideas': 1 if confirmed and its book profitable, 0.5 if one of the two, 0 if neither (a plan that was not testable: 0) | how often line `l`'s analyses moved an idea towards the goal; counted per analysis, because the ideas written together are not independent; the +1 / +2 (Laplace) keeps 1 of 1 from counting as certain, and puts a line with no analysis yet at 0.5 |
| **novelty** | 1 / (1 + k), k the ideas `F.lM` (written together with it) already tested in the run | one analysis with several ideas does not take the whole run: its next idea waits behind other leads |

**Ties:** the higher generation first (the thread that is moving), then the lower `N` (the order the line wrote them).

**Where the numbers come from:** the ids, and each tested idea's verdict and check, in every named run; computed
afresh at every call, so the record grows with every run and the order adapts by itself.

**Not in the score:** step 7's own numbers (inflated by its search), a model's opinion (cost, not auditable).

**Today's records** (validation run, 2026-11-16):

| Line | Analyses | Progress | Record |
|---|---|---|---|
| 7.e | 2 | 2.0 | 0.75 |
| 7.c | 1 | 1.0 | 0.67 |
| 7.b | 2 | 1.5 | 0.62 |
| 7.g | 1 | 0.5 | 0.50 |
| 7.d | 3 | 0.5 | 0.30 |
| 7.a | 2 | 0.0 | 0.25 |

## Storage
```
orchestration/select_next/
  card.md                    this card
  helper/select_next.py, test_select_next.py
  validation/reading.md      once validated
(it writes nothing of its own: loop writes its choice and the ranking in its queue)
```

## How to call it
```
python3 orchestration/select_next/helper/select_next.py --run NAME_run [--top N]
```
Prints the ranking (score and its parts, candidates and duplicates). `loop` imports it.

## Checks in code
A run name not ending in `_run` is refused. An idea file it cannot read is listed as "unreadable", not ranked.

## Done when
On a run with known proposals: every candidate is listed with its score parts, the duplicates are found, the ranking
follows the score, and a second call on the same files gives the same ranking.

## Open (for the operator)
1. Progress: confirmed 0.5, profitable 0.5 (the two answers weigh the same).
2. Novelty: 1 / (1 + k).

## What this function does not do
It does not test an idea, judge one, or change a step.
