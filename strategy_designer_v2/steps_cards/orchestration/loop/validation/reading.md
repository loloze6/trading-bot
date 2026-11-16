# loop: validation on demo_run (2026-11-16)

**Call**: `loop.py --run demo_run --python VENV --budget 4`, resuming the run `run_idea` had validated (the starting
idea, the 002-03 repair from 7.d, already tested: 1.05 USD spent before the first turn).

| Turn | Idea (from the repair, `...d1_above-average-drift-near-highs`) | Why (select_next rank 1) | Step 5 | Step 6 | USD | Minutes |
|---|---|---|---|---|---|---|
| 1 | `.e1_near-high-drift-ten-days` | 0.75 (7.e) / (1 + 2) = 0.25 | confirmed (+3.08) | not profitable (mean daily return, Calmar) | 1.34 | 12.5 |
| 2 | `.e2_short-drift-after-strong-highs` | 0.75 (7.e) / (1 + 2) = 0.25; tie, lower number | confirmed (+3.32) | not profitable (mean daily return, Calmar) | 0.86 | 12.1 |
| 3 | `.g1_one-day-move-reversal` | 0.67 (7.g) / (1 + 2) = 0.22 | inconclusive (+4.24) | not profitable | 1.18 | 10.5 |
| stop | | budget reached (4.42 of 4.00 USD): the third idea, started at 3.24, was finished | | | | |

**Resumed call** (same command): rebuilt the queue from the files, stopped at once on the budget, no model call.

**Refused before any call**: a new run with no starting idea; a budget of 0.

**After the stop**: 19 candidates wait in the queue (2 from 7.b, 8 from 7.g, 8 from 7.d at generation 3; one from 7.a
at generation 2); 7.g's record went from 0.67 to 0.50 (its analysis of the repair found nothing confirmed or
profitable), which the next turn's ranking already uses.

**Met**: every turn ran the idea `select_next` ranked first, with its score and its parts in `loop.jsonl`; the budget
stop said so and finished the idea under way; the queue says what happened to each idea; a resumed call continued
where it stopped. No duplicate was proposed in this run, so the duplicate rule was met only by the tests.

**No goal reached**: two ideas confirmed, none with a profitable book.
