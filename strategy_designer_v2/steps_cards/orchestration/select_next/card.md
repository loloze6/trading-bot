# Function card: select_next (orchestration, agreed 2026-11-16; met on demo_run, `validation/reading.md`)

A function card (no model of its own): what it selects, its score, where its numbers come from, how to call it.

## Business objective, one question
Which idea should the workflow test next?

**Establish, among the ideas written in a run and not yet tested, whether step 2 wrote them from a brief or a step 7
line from another idea, the one most likely to bring the workflow closer to an idea that is real with a book that pays,
by one score fixed in advance, computed from the workflow's own recorded results, and shown with its parts.**

## Input and output
- **Input:** a run name.
- **Output:** the run's candidates, ranked: each with its score, the parts of the score, and why it is or is not a
  candidate. The first is the next idea.

## What a candidate is
**A candidate is an idea written in the run, by step 2 from a brief or by a step 7 line from another idea, not yet
tested in the run, and not a duplicate.**
- **Written in the run:** in step 2's `02_ideation/<run>/ideas/`, or in a line's `<run>/<backtest>/ideas/`.
- **Not tested:** no plan for it in the run (`03_test_plan/<run>/plans/`).
- **Not a duplicate:** its text and its data are not those of an idea already tested or already a candidate (the same
  text on other data, a `same-idea-on:` proposal, is not a duplicate). A duplicate is listed, with the idea it repeats.
- The words (created from, line, analysis, generation) are those of `../../common/idea_created_from.md`.

## The score
In the words of `../../common/idea_created_from.md`.

**score = record of the line that wrote the idea / (1 + the idea's generation)**

| Part | What it is | Why |
|---|---|---|
| **record of the line** | the line is the step 7 line that wrote the idea (its last letter in the id), or step 2 for an idea created from a brief. Over every analysis of that line with at least one tested idea, in every run (for step 2, an analysis is one brief): (s + 1) / (n + 2), n the number of these analyses, s the number of them with a **success**: at least one of their tested ideas confirmed or with a profitable book (operator, 2026-11-16) | how often that line's analyses moved an idea towards the goal; counted per analysis, because the ideas written together are not independent; the +1 / +2 (Laplace) keeps 1 of 1 from counting as certain, and puts a line with no analysis yet at 0.5 |
| **1 + generation** | the generation is the number of analyses between the idea and its brief (0 for a brief's idea) | ideas close to the theory first; a deeper idea goes first only if its line's record is clearly better, so one thread does not take the run |

**Ties:** the lower number first (the order in which the brief or the line wrote them).

**Where the numbers come from:** the ids, and each tested idea's verdict and check, in every named run; computed
afresh at every call, so the records grow with every run and the order adapts by itself.

**Not in the score:** step 7's own numbers (inflated by its search), a model's opinion (cost, not auditable).

**Today's records** (every named run, 2026-11-16; ideas renamed by hand during the overnight run,
`N2-04` and the like, do not follow the id convention and are left out):

| Line | Analyses | With a success | Record |
|---|---|---|---|
| 7.b | 2 | 2 | 0.75 |
| 7.e | 2 | 2 | 0.75 |
| 7.c | 1 | 1 | 0.67 |
| 7.g | 1 | 1 | 0.67 |
| 7.d | 3 | 1 | 0.40 |
| step 2 | 2 (briefs 001, hourly, and 002, daily) | 0 | 0.25 |
| 7.a | 2 | 0 | 0.25 |

**Simulated** (2026-11-16; a new brief with 4 ideas, assumed results, 8 turns): the brief's ideas are tested at turns
1, 6 and 8 (the fourth would come at turn 9), mixed with the best leads; no thread is followed down more than two
analyses. Without the generation in the score, it dived down one thread for 7 turns and never came back to the brief.

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

## What this function does not do
It does not test an idea, judge one, or change a step.
