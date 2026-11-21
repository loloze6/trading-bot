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
- **Not tested:** no plan for it in the run (`03_test_plan/<run>/plans/`), or a missing-components refusal the
  components step has unblocked (every wish answered built or exists, the catalogue changed since the refusal:
  `../../components/card.md`, "Unblocking"; 2026-11-17).
- **Not a duplicate:** its text and its data are not those of an idea already tested or already a candidate (the same
  text on other data, a `same-idea-on:` proposal, is not a duplicate). A duplicate is listed, with the idea it repeats.
- The words (created from, line, analysis, generation) are those of `../../common/idea_created_from.md`.

## The score
In the words of `../../common/idea_created_from.md`.

**score = record of the line that wrote the idea / (1 + the idea's generation)**

| Part | What it is | Why |
|---|---|---|
| **record of the line** | the line is the step 7 line that wrote the idea (its last letter in the id), or step 2 for an idea created from a brief. Over every analysis of that line with at least one tested idea (tested: it has a verdict from step 5; an idea step 3 could not plan is not evidence about the line, 2026-11-17), in every run (the same idea read by the line in two runs is two analyses; for step 2, an analysis is one brief in one run): (s + 1) / (n + 2), n the number of these analyses, s the number of them with a **success**: at least one of their tested ideas with a profitable book (step 6's "profitable enough"; operator, 2026-11-19; until then confirmed or profitable, 2026-11-16) | how often that line's analyses moved an idea towards the goal; counted per analysis, because the ideas written together are not independent; the +1 / +2 (Laplace) keeps 1 of 1 from counting as certain, and puts a line with no analysis yet at 0.5 |
| **1 + generation** | the generation is the number of analyses between the idea and its brief (0 for a brief's idea) | ideas close to the theory first; a deeper idea goes first only if its line's record is clearly better, so one thread does not take the run |

**Order (operator, 2026-11-17): a brief's own ideas first.** The candidates of generation 0 (a brief's ideas) come
first, ranked by the score among themselves; then every other candidate, by the score. Every idea of a theory is tested
once before the workflow goes deep on one of them. Why: with the score alone, a brief's idea scored 0.09 (step 2's
record) against 0.15 to 0.33 for the lines' children, so one lineage took 26 of 30 turns in night_run and 28 of 33 in
night_013_run, and 7 unblocked RSI ideas waited behind 010-01's children (the operator's options A to D, 2026-11-17, in git: `ranking_discussion.md`, removed once ruled).

**Ties:** the lower number first (the order in which the brief or the line wrote them).

**Why a success is a book that pays, not a confirmation (operator, 2026-11-19; `topics/30_why-hourly-ideas-rarely-pay.md`).**
The goal is an idea that is real and pays. On hourly bars a small effect is confirmed easily (a short horizon's random
move is small) and is too small to pay its costs: in slow_1h_run and intraday_1h_run, 7.g's ideas were often confirmed
and never profitable, so its record rose to 0.80 and it took the runs, while line 7.d's 80 ideas (why a book does not
pay, and what would) were never tested. Under the new rule, every run's records and rankings compared with the old
(2026-11-19, every named run and intraday_1h_run):

| Line | Analyses | Successes before | Record before | Successes after | Record after |
|---|---|---|---|---|---|
| 7.g | 62 | 50 | 0.797 | 4 | 0.078 |
| 7.e | 10 | 7 | 0.667 | 5 | 0.500 |
| 7.c | 3 | 3 | 0.800 | 1 | 0.400 |
| 7.b | 12 | 7 | 0.571 | 4 | 0.357 |
| 7.d | 10 | 4 | 0.417 | 3 | 0.333 |
| 7.a | 2 | 0 | 0.250 | 0 | 0.250 |
| step 2 | 16 | 9 | 0.556 | 1 | 0.111 |

The next 10 candidates of each run: before, mostly 7.g in 10 of 11 runs; after, 7.d and 7.b (slow_1h_run: 10 of 7.b;
intraday_1h_run's next 20: 10 of 7.b, 8 of 7.d, 2 of 7.c). The first candidate changes in 9 of 11 runs.

**Where the numbers come from:** the ids, and each tested idea's verdict and check, in every named run; computed
afresh at every call, so the records grow with every run and the order adapts by itself.

**Not in the score:** step 7's own numbers (inflated by its search), a model's opinion (cost, not auditable).

**Today's records** (every named run, 2026-11-16, after the loop's test on demo_run; ideas renamed by hand during the overnight run,
`N2-04` and the like, do not follow the id convention and are left out):

| Line | Analyses | With a success | Record |
|---|---|---|---|
| 7.e | 3 | 3 | 0.80 |
| 7.b | 2 | 2 | 0.75 |
| 7.c | 1 | 1 | 0.67 |
| 7.g | 2 | 1 | 0.50 |
| 7.d | 4 | 2 | 0.50 |
| 7.a | 2 | 0 | 0.25 |
| step 2 | 3 (brief 001 in hourly_run; brief 002 in hourly_run and in full_data_run) | 0 | 0.20 |

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
Status: **met** on demo_run (`validation/reading.md`); the duplicate rule met by the tests only (no duplicate in that
run).

## What this function does not do
It does not test an idea, judge one, or change a step.
