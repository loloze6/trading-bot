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

## The score
**score = line record x novelty**

| Part | What it is | Why |
|---|---|---|
| **line record** | (p + 1) / (n + 2) for the line that proposed the idea: n its ideas tested so far, p the sum of their **progress**, 1 if the idea was confirmed and its book profitable, 0.5 if one of the two, 0 if neither | how often that line's ideas moved towards the goal; the +1 / +2 (Laplace) keeps a line with 2 of 2 from counting as certain, and an untried line at 0.5 |
| **novelty** | 1 / (1 + k), k the ideas of the same parent already tested in the run | one analysis with many ideas does not take the whole run; a parent's next idea waits behind other leads |

**Ties:** the newest generation first (the thread that is moving), then the order in which the line wrote its ideas.

**Where the line record comes from:** every named run's files: an idea's line is the letter in its id (`.e1_`: 7.e),
its progress is read from its verdict and its check. Computed afresh at every call, so the record grows with every run
and the order adapts by itself. A plan that was not testable counts as a test with progress 0.

**Not in the score:** step 7's own numbers (inflated by its search), a model's opinion (cost, not auditable).

**Today's line records** (validation run; 2026-11-16):

| Line | Tested | Progress | Record |
|---|---|---|---|
| 7.c | 2 | 2 | 0.75 |
| 7.e | 2 | 2 | 0.75 |
| 7.g | 3 | 0.5 | 0.30 |
| 7.a | 2 | 0 | 0.25 |
| 7.b | 9 | 1.5 | 0.23 |
| 7.d | 5 | 0.5 | 0.21 |

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
