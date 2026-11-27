# Seeded run A4 (2026-11-27): the three pieces the pilot never reached, on real data, with no model call (written before the run)

**The operator (2026-11-27, "Ok go"):** next steps A12, part 4. Proof session, branch `seeded-a4` from the working
branch at 26b53af8185. **Evidence only: never merged; a portfolio version it writes is not a version of the portfolio.**

## Purpose
The pilot (`PILOT_A4_RUN.md`) confirmed no idea, so three pieces of the new chain "did not occur". Show each on real
data, in one run in data use 2 (`seeded_a4_run`), through `run_idea`, with no model call:
- **(a) Steps 9 and 10:** a confirmed and profitable strategy gets its common record, then `update.py` is called.
- **(b) B12:** a confirmed strategy failing 3 or more of step 6's measures gets no 7.d call (one failing 1 or 2 would).
- **(c) The direction check:** step 5's check of a confirmation on the check half (the windows from 2022).

## Method
1. `orchestration/loop/seeded_a4_run/data_use.json` written by `common/coins.py`'s `new_data_use` (the function
   `run_brief --data-use 2` uses): 8 coins drawn by the run's name, the 32 windows.
2. **Strategy S (strong):** confirmed and profitable in its own run, and on its common record (25 coins) with room.
   Seeded: its plan and config, step 7's index lines (and 7.g's outputs). **Not seeded: its verdict.** `run_idea`
   cannot pass `--measure`, so steps 4 and 5 are run by their own helpers on the run's folders first (step 5 with the
   plan's stored `measure.py`, as `common_record` does), then `run_idea` finds their outputs and goes on.
3. **Strategy W (weak):** confirmed in its own run, failing 3 or more of step 6's measures there. The same seeding,
   but nothing for line 7.d: its entry condition is evaluated for real. Step 6 is read before `run_idea`: if W fails
   2 or fewer measures on the new data, 7.d would call the model, so another W is taken.
4. `run_idea` on S and on W; then the files are read.

## Expected outcomes
| # | Outcome | Shown by |
|---|---|---|
| E1 | The three pieces work | S confirmed, the direction check stated on the check half, profitable on the run's coins; then `common_record` called and its record written on the portfolio coins; then `update.py` called (a version v5 if the list of candidates changed, or its line says why not); no unseen test. W: 7.d "not run" with the count of failed measures; no model call |
| E2 | S is not confirmed or not profitable on the run's 8 coins | steps 9 and 10 rightly not called; a second strong strategy, then a third; each reported. None passing is a finding about the drawn coins |
| E3 | A step fails or is called in the wrong order | the journal's lines |

Also reported: the coin-windows run and not run in S's step 4 record, with their reasons; the direction check's text;
the common record's line; what `update.py` printed; every file the three pieces wrote.

## What was done
(after the run)

## Reading
(after the run)
