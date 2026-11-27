# Pilot A4 (2026-11-27): the whole new chain, watched, in two short runs (written before the runs)

**The operator (2026-11-26, next steps A4 part 7):** "a watched pilot of the whole chain before the next batch";
2026-11-27: "Go with B": two runs in parallel, 2 hours, about 12 USD each. Standing rules: `NIGHT_RULES.md`.

## Purpose
One question: **does every piece built on 2026-11-26 and 27 work on real data, in one run, in the order the cards say?**
Not: does the run find a strategy (the pilot is too small to say).

## The runs
| | Run 1 | Run 2 |
|---|---|---|
| Run | `pilot_a4_auto_run`, branch `pilot-a4-auto` | `pilot_a4_named_run`, branch `pilot-a4-named` |
| Box | `--target-box auto` (the rule on the 25 portfolio coins: falling calm, long at the start) | `--target-box "rising agitated, short"` (named by the operator) |
| Brief | written by step 1 from the box alone, with the box's note: `--theme` names only the box | the same |
| Data | `--data-use 2`: 8 research coins drawn by the run's name, the 32 windows 2016-2026, explore half to the analysts, check half for step 5's direction | the same |
| Budget, time | 12 USD; no new idea after 21:30 UTC (22:30 Paris), the idea in progress finished | the same |
Each run in its own session, on its own branch from the working branch at 7faa7092853 (never on the working branch while it runs); the designer reads both journals.

## What must be seen (one line each, from the run's files)
| # | Piece | Seen when |
|---|---|---|
| 1 | Data use 2 | `data_use.json`: 8 coins, one per category plus one; step 4's records on those coins and the 2016 windows; coins' first 90 days and holes left out, counted |
| 2 | Explore and check halves | step 7's exploration on w1-w18 only; step 5's direction on w19-w32 |
| 3 | The box | `target_box.json`; the brief's `profile:` and `side:` holding it; the box's note in step 1's, 2's and 7's prompts; `in_box` on every turn |
| 4 | B13 | the untested ideas naming the box taken before the first turn (`taken` lines), ranked with the run's own |
| 5 | B11 | at least one answer "no effect", and its follow-up written by 7.c, not 7.b |
| 6 | B12 | a confirmed, unprofitable strategy failing 3 or more measures gets no 7.d call (if one occurs) |
| 7 | B10 | at least one "not called" line for 7.g, with its scores |
| 8 | Steps 9 and 10 | a candidate (confirmed and profitable) gets its common record, then `update.py` (a new version only if the list changed) |
| 9 | No unseen test | no `unseen_test` call in the run |
| 10 | Cost and time | every step's USD and seconds in the table; nothing refused or failed without a line saying why |

## Expected outcomes
| # | Outcome | Shown by |
|---|---|---|
| P1 | The chain works | rows 1 to 4, 9 and 10 seen in both runs; rows 5 to 8 seen in at least one, or "did not occur" with the reason (then covered only by the builds' proofs on stored files) |
| P2 | A piece fails | a row not seen where its case occurred: named, fixed by its rule, the pilot rerun on that piece |
| P3 | The machinery stops | a failed turn, a refusal, a step with no output |
Also counted: ideas tested, confirmed, profitable; ideas outside the box (`in_box` false); spend per step.
