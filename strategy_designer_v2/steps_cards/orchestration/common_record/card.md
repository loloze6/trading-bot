# Function card: common_record (orchestration, 2026-11-26)

(Step 9 of `common/data_use.md`, build plan part 4; built from `unseen_test --coins`, the closest existing mechanism.)

## Business objective, one question
**What does a candidate do on every portfolio coin, over every research window, so that every candidate is measured
on the same data and the portfolio is built from records that compare?**

Why (`common/data_use.md`, 1.2 and 4): each run finds and checks its strategies on its own 8 coins; a portfolio built
from records on different coins compares strategies on different markets. Step 9 gives every candidate one record on
the same 25 coins and the same windows. It records; it decides nothing (steps 10 to 12 read it).

## Input
- One candidate's plan: `03_test_plan/<run>/plans/<id>.md` (and its config beside it), and its in-sample
  `05_verification/<run>/verdicts/<id>/measure.py` (step 5's criterion, applied again unchanged).
- The coins: `common/coins.py`, `portfolio_group()` (25 coins; the final group left out).
- The windows: `04_backtest/windows/research_2016.json` (32 windows of 4 months, 2016 onward).
- The 90-day rule: `coins.usable(coin, window start)`.
- A Python environment with `trading-bot/requirements.txt`.

## Output
The candidate's common record, its step 5 and step 6, and its result file and index line (see Storage). The fixed
interface: the portfolio's builders read these paths and fields.

## What a common record is
**The candidate's plan, config unchanged, run by the bot's backtest on every portfolio coin over the research windows,
a coin in a window only when the window starts after the coin's first 90 days; then step 5's measure on it (the plan's
own `measure.py`, no model call: information) and step 6's check.**
- **Same windows, same numbers:** `wK` is the K-th window of `research_2016.json` for every coin, so one K is one
  period (step 6's "one window left out" needs it). A coin listed later starts at a later K: SUI at w23.
- **A coin or window the engine cannot run** (no file for the bar size, a window refused by the engine) is written in
  `run.md` with the engine's reason, as in step 4; it is not dropped silently.
- **It decides nothing:** no step 3 to 8 reads it. It stops nothing and gates nothing.

## The fields of the result (`<id>.json`)
1. **plan, run, id, record, windows_file:** what ran and where its files are.
   - For: the builders find the record and its plan. Without it: the record cannot be traced to its plan.
2. **coins_asked, coins_run, coin_windows, windows_run:** the 25 coins asked, those that ran at least one window,
   the windows each ran, and the (coin, window) pairs in all.
   - For: the record's completeness. Without it: a coin missing looks like a result.
3. **step5:** step 5's status, main measure and its statistic on the common data (information only).
   - For: whether the effect keeps its direction on all coins. Without it: four folders to read.
4. **step6:** step 6's status, its measures (Sharpe, minus holding, mean daily return, one window left out, Calmar,
   trades per day) and its informative measures.
   - For: steps 10 and 11 (the portfolio). Without it: each builder recomputes the book.
5. **seconds, made_utc, commit:** the engine time, when the record was made, and the code that made it.
   - For: the time estimates and the audit. Without it: no way to say which code made a record.

## Storage and naming
```
orchestration/common_record/
  card.md                      this card
  INDEX.md                     one line per record: <run>/<id>: coins, coin-windows, step 5, step 6, seconds
  helper/
    common_record.py           one plan -> step 4 on the common data, chart files, step 5 (--measure), step 6;
                               --register --shard i/n: the register's paying books
    test_common_record.py      tests of its own logic (no backtest, no model call)
  <name>_run/<id>.json         one candidate's result
The steps' files, in the run's usual folders, under common/:
  04_backtest/<name>_run/common/backtests/<id>/        run.md, config.json, <SYMBOL>/wK/, <SYMBOL>/windows/,
                                                       chart_bars.csv.gz, chart_trades.csv.gz (committed names)
  05_verification/<name>_run/common/verdicts/<id>/     result.json, verdict.md, measure.py, size.json
  06_profitability/<name>_run/common/checks/<id>/      result.json, check.md
```
As in every record, the windows' large files (`wK/*.gz`) stay local; the chart files are committed (a candidate is
worth a chart), so the record is read on any machine (`orchestration/combine/helper/boxes.py`, `coin_days`).

## Who calls it, and when
- **`run_idea`**, right after a strategy becomes a candidate (step 5 confirmed and step 6 profitable enough, read
  from their result files) and its chart files, **only when** `orchestration/loop/<run>/data_use.json` exists with
  `"version": 2` (the loop's data-use mode). Any other run is unchanged. Journal line `common_record`; the row's field
  `common_record` (in `table.json`, not a column of `table.md`).
- **The operator, for the existing candidates:** `--register --shard i/n`, every `paying` book of
  `orchestration/ideas_similarities_check/register/books.json` (120 on 2026-11-26). **Its plan and `measure.py`**
  (designer, 2026-11-27): each found by the plan id in the book's own run first; else in the one other run whose
  plan's config equals the book's record config (`04_backtest/<run>/backtests/<id>/config.json`); none or several:
  refused, the message naming them, and the shard goes on. Why: a run that reran other runs' plans
  (`paying_rerun_run`) holds only steps 4 and 6. On 2026-11-27: 85 books in their own run, 32 in another, 3 refused
  (two runs, `hold2_rerun_run` and `hold_paying_run`, hold the same config). The result's `plan` and `measure` say
  which files were used.

## How to call it
```
python3 orchestration/common_record/helper/common_record.py PLAN --run NAME_run --python VENV_PYTHON
python3 orchestration/common_record/helper/common_record.py --register --shard i/n --python VENV_PYTHON [--only KEYS]
```
- A step whose output exists is not called again (step 4's: `run.md` and one window run); a book whose result exists
  is not run again. So a stopped shard is resumed by calling it again.
- Step 4 is step 4's own code (`04_backtest/helper/run_backtest.py`: `protocol` and `run_part`, unchanged), called
  once per coin on its usable windows, as many coins at once as the machine has cores.
- Shards run at the same time on one machine: each index (step 4's, 5's, 6's, this function's) is written under a lock
  file in the system's temporary folder.

## Why this cannot leak
No rule changes how a bar is read: each window is its own `run_backtest` call with its own dates, warm-up and holdout
guard, as in step 4. The 90-day rule reads each coin's first day only. **The final group's coins are never read:** the
coins come from `portfolio_group()`, which leaves them out, and the helper's code never names them (a test says so).

## The AI
None: code only; step 5 is called with `--measure`, so no model call. Cost: 0 USD; engine time only (see the build
record `runs/BUILD_A4_COMMON.md` for the time per candidate).

## Quality criteria
- Every (coin, window) pair after the coin's first 90 days is run, or recorded as not run with the engine's reason.
- `wK` is the same period for every coin.
- A second call makes no step call.
- No final coin is read.
- `run_idea` without `data_use.json` gives the same files as before.

## Fixed inputs for the iterations
night 8's `060-01.g1.d2.d1_own-range-close-height-fade_1d` and `058-03.e1_calm-rise-stretch-ten-days_1d`
(`night8_risingagitated_run`, both paying).

## Variants compared
None.

## Who judges the output
Code records; steps 10 to 12 and the operator read it.

## Done when
The two fixed inputs have their records with every field; the tests pass; `run_idea` without `data_use.json` gives the
same files as before on a fixed plan. Status: see `runs/BUILD_A4_COMMON.md`.

## Open (for the operator)
- **Data quality rules 3.2 and 3.4 of `data_use.md`** (a hole longer than a day leaves the coin out of that window; a
  coin that stops trading in a window): not applied here; the engine's gap rule applies as in every backtest. They
  belong with step 4's draw (build part 3), then here, so that the research and the common record read data the same way.
- **The 90-day rule reads the daily file's first day**, for every bar size; an hourly plan on a coin whose hourly file
  starts later gets "the dates were not fetched" in the windows before it (recorded, not dropped).
- **The candidate of A2** (confirmed, failing step 6 on Calmar alone) is not called: A2 is not agreed.

## What this function does not do
It does not choose candidates, change a plan, build or judge a portfolio, or read the final coins.
