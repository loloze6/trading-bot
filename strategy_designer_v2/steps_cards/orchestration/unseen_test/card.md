# Function card: unseen_test (orchestration, 2026-11-18; validated: `validation/reading.md`)

## Business objective, one question
Does an idea that is real and pays still hold on dates the research never used?

**Establish, for every idea step 5 confirmed and step 6 found profitable enough, whether it holds on each unseen
period, its plan, config and criterion unchanged, so that no idea reaches live trading on the evidence of the dates
it was found and judged on alone** (operator, 2026-11-18; `UNSEEN_RUN.md`: 8 of the first 12 such ideas failed step 6
on at least one unseen period, 2 did not hold at all).

## Input
One idea's plan (`03_test_plan/<run>/plans/<id>.md`) and its in-sample verdict (`05_verification/<run>/verdicts/<id>/`,
`result.json` and `measure.py`); the unseen periods (`common/unseen_dates.md`: one windows file each in
`04_backtest/windows/unseen_*.json`).

## Output
Per period, the steps' usual files under the run; the idea's result `orchestration/unseen_test/<run>/<id>.json` and
one line in `orchestration/unseen_test/<run>/INDEX.md`; in `run_idea`'s row, the field "unseen dates".

## What an unseen test is
**The idea's plan run once on each unseen period by steps 4, 5 and 6, as validated: step 4 on the period's windows
(`--windows`), step 5 with the idea's own `measure.py` (`--measure`, no model call: the same criterion, not a new
one), step 6 unchanged; then, per period, whether the idea holds** (`common/unseen_dates.md`: the main measure has
its in-sample sign AND the book's Sharpe after costs is above 0).
- **It records; it decides nothing.** No step reads its result: step 7 and `select_next` work on the folds only, so
  the unseen dates stay unseen. Visibility, not a gate: the operator reads it.
- **It does not search.** Every idea meets the same few periods; choosing ideas by their unseen result would make
  those dates seen.

## The fields of the result (`<id>.json`)
1. **in_sample:** the main measure and its statistic from the in-sample verdict. For: the sign the rule compares to.
2. **periods.<period>:** step 5's status, the main measure and its statistic, step 6's status, the book's Sharpe and
   holding's Sharpe (step 6's numbers), and **holds**. For: the operator's reading. Without it: four folders to read
   per period.

## When it is called
By `run_idea`, after step 7 (step 7 never reads its files), for an idea step 5 confirmed and step 6 found
profitable enough: the rule is steps 5 and 6's results. By the operator, on any idea with an in-sample verdict.

## How to call it
```
python3 orchestration/unseen_test/helper/unseen_test.py PLAN --run NAME_run --python VENV_PYTHON
```
A step whose output exists is not called again (a resumed run costs nothing).

## Storage and naming
```
orchestration/unseen_test/
  card.md                 this card
  helper/
    unseen_test.py        one plan -> steps 4, 5, 6 on each unseen period; the holds rule; the result and index
    test_unseen_test.py   tests of its own logic (no backtest, no model call)
  validation/reading.md   the validation
  <name>_run/
    <id>.json             one idea's result
    INDEX.md              one line per idea: holds or does not hold, per period
The steps' files, per period P (unseen_2026, unseen_2016_2017), in the run's usual folders:
  04_backtest/<name>_run/P/backtests/<id>/
  05_verification/<name>_run/P/verdicts/<id>/
  06_profitability/<name>_run/P/checks/<id>/
```

## The AI
None: code only; step 5 is called with `--measure`, so it makes no model call. Cost: 0 USD; about a minute per idea
(two periods, 6 coins).

## Quality criteria
- The same files as the steps called by hand on the same plan and period (proof below).
- Every status read from the step's own result file.
- A second call makes no step call.

## Fixed inputs
`night_rsi_run` 010-03 e1 (confirmed, profitable enough), whose unseen periods were run by hand in `UNSEEN_RUN.md`.

## Variants compared
None.

## Who judges the output
Code: the holds rule. The operator: what to do with an idea that holds or does not.

## Validation (once)
Status: **validated** (`validation/reading.md`): through `run_idea` (resumed: steps 3 to 7 skipped), the function
gave files identical to the hand run's: 72 engine files, both verdicts and both checks.

## What it changes elsewhere
- `run_idea`: the call after step 7, the row's field "unseen dates" (a column of `table.md`).
- `04_backtest` (`--windows`) and `05_verification` (`--measure`): the two options it calls, in their cards.

## What this function does not do
It does not choose ideas, change a plan, write a new criterion, or stop a run.
