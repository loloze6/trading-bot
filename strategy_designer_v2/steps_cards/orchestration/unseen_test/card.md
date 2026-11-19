# Function card: unseen_test (orchestration, 2026-11-18)

## Business objective, one question
Does an idea that is real and pays still hold on dates the research never used?

**Establish, for every idea step 5 confirmed and step 6 found profitable enough, whether it holds on each unseen
period, its plan, config and criterion unchanged, so that no idea reaches live trading on the evidence of the dates it
was found and judged on alone** (operator, 2026-11-18). Why: in `UNSEEN_RUN.md`, 8 of the first 12 such ideas failed
step 6 on at least one unseen period, and 2 did not hold at all.

## Input
- One idea's plan: `03_test_plan/<run>/plans/<id>.md` (with its config beside it).
- Its in-sample verdict: `05_verification/<run>/verdicts/<id>/result.json` (the main measure's sign) and `measure.py`
  (the criterion, applied again unchanged).
- The unseen periods: every `04_backtest/windows/unseen_*.json` (`common/unseen_dates.md`).
- A run name and a Python environment with `trading-bot/requirements.txt`.

## Output
- Per period, the steps' usual files, under the run (see Storage).
- The idea's result: `orchestration/unseen_test/<run>/<id>.json`, and one line in `orchestration/unseen_test/<run>/INDEX.md`
  (per period: holds, or does not hold).
- In `run_idea`'s row: the field "unseen dates" (that index line).

## What an unseen test is
**The idea's plan run once on each unseen period by steps 4, 5 and 6, as validated: step 4 on the period's windows
(`--windows`), step 5 with the idea's own `measure.py` (`--measure`, no model call: the same criterion, not a new
one), step 6 unchanged; then, per period, whether the idea holds** (`common/unseen_dates.md`: the main measure has its
in-sample sign AND the book's Sharpe after costs is above 0).
- **It records; it decides nothing.** No step reads its result: step 7 and `select_next` work on the folds only, so
  the unseen dates stay unseen. It stops nothing and gates nothing; the operator reads it.
- **It does not search.** Every idea meets the same few periods; choosing ideas by their unseen result would make
  those dates seen.

## The fields of the result (`<id>.json`)
1. **in_sample:** the main measure and its statistic, from the in-sample verdict.
   - For: the sign the rule compares to. Without it: "holds" cannot be computed.
2. **periods.<period>:** step 5's status, the main measure and its statistic, step 6's status, the book's Sharpe and
   holding's Sharpe on the same coins and dates (step 6's numbers), and **holds** (true or false).
   - For: the operator's reading, and the index line. Without it: four folders to read per period.

## Storage and naming
```
orchestration/unseen_test/
  card.md                 this card
  helper/
    unseen_test.py        one plan -> steps 4, 5, 6 on each unseen period; the holds rule; the result and the index
    test_unseen_test.py   tests of its own logic (no backtest, no model call)
  validation/reading.md   the validation
  <name>_run/
    <id>.json             one idea's result
    INDEX.md              one line per idea: per period, holds or does not hold
The steps' files, per period P (unseen_2016_2017, unseen_2026), in the run's usual folders:
  04_backtest/<name>_run/P/backtests/<id>/
  05_verification/<name>_run/P/verdicts/<id>/
  06_profitability/<name>_run/P/checks/<id>/
```

## Who calls it, and when
- **`run_idea`, on its own**, after step 7, for an idea step 5 confirmed and step 6 found profitable enough (the rule is
  steps 5 and 6's result files, not a judgment). After step 7 so that no line can read its files. So `loop` and
  `run_brief`, which call `run_idea`, get it for every such idea.
- **The operator**, on any idea with an in-sample verdict (for example the ideas of runs made before this function).

## How to call it
```
python3 orchestration/unseen_test/helper/unseen_test.py PLAN --run NAME_run --python VENV_PYTHON
```
- `PLAN`: the idea's plan file; `--run`: the run that holds its verdict, where the files go; `--python`: the venv.
- It calls, per period: `04_backtest/helper/run_backtest.py PLAN --out-root ... --windows ...`,
  `05_verification/helper/make_verdict.py PLAN --records-root ... --verdicts-dir ... --measure .../measure.py`,
  `06_profitability/helper/check_profitability.py RECORD --checks-dir ...`.
- A step whose output exists is not called again: a second call makes no step call (a resumed run costs nothing).

## When a step fails
Nothing stops: the other periods go on, and the result says what each step gave.
- **No in-sample verdict or no `measure.py`:** refused before any step (exit 1, its message in the log); `run_idea`'s
  row reads "no answer".
- **Step 4 runs no window for a coin** (no data there, for example a coin listed later): written in its `run.md`, as
  in-sample; no window for any coin: no record, so no verdict.
- **Step 5 refuses** (the measure fails on the record, or returns a result its checks refuse): one attempt only (no
  model to ask again); no `result.json`, so "no verdict" and "does not hold".
- **Step 6 fails:** "not checked", and "does not hold".
- **No data for the period** (no verdict and no check, e.g. the hourly bars of 2026 not fetched): "no data", not "does
  not hold" (`holds` null): the idea was not judged there (night 1h, 2026-11-19).
- A failed step leaves no output, so the next call tries it again (after a fix, for example).

## Checks in code
- The plan's in-sample verdict and `measure.py` must exist (else refused, above).
- Steps 4, 5 and 6 apply their own checks, unchanged (step 5's result checks: status, situation check, main measure,
  counts).
- "Holds" needs a main measure, its in-sample sign (a measure of exactly 0 has none), and a Sharpe: any missing means
  "does not hold".

## Visibility
- `run_idea`'s journal: one line `unseen_test` (called or skipped, seconds, 0 USD).
- `run_idea`'s log, `logs/<id>/unseen_test.txt`: every step's whole output, headed by the period, the step and its exit
  code, then the result line.
- The steps' own files and index lines in each period's folders.

## The AI
None: code only. Step 5 is called with `--measure`, so it makes no model call. Cost: 0 USD; about a minute per idea
(two periods, 6 coins).

## Quality criteria
- **The same files as the steps called by hand** on the same plan and period.
- **Every status is read from the step's own result file.**
- **A second call makes no step call**, and `run_idea`'s journal says so.
- **No step reads its files** (step 7 runs before it; `select_next` reads the folds' results only).

## Fixed inputs for the iterations
`night_rsi_run` 010-03 e1 (confirmed, profitable enough), whose unseen periods were run by hand in `UNSEEN_RUN.md`.

## Variants compared
None.

## Who judges the output
Code: the holds rule. The operator: what to do with an idea that holds or does not.

## Done when
Through `run_idea` on the fixed input, the function's files are identical to the hand run's, the row and the index
say what the steps' files say, and a second call makes no step call.
Status: **met** (`validation/reading.md`): 72 engine files, both verdicts and both checks identical; 3 tests of its
own logic.

## What it changes elsewhere (each in its own card)
- `run_idea`: the call after step 7, the row's field "unseen dates" (a column of `table.md`).
- Step 4 (`--windows`) and step 5 (`--measure`): the two options it calls.

## What this function does not do
It does not choose ideas, change a plan, write a new criterion, stop a run, or extend the unseen periods (adding days
is `trading-bot/tools/extend_kraken_daily.py` and a new windows file, by the operator).
