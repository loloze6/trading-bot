# Function card: forward_record (orchestration, 2026-11-27)

(Function card, `../../HOW_WE_DESIGN_A_CARD.md`; no model call, so no prompt, model or variant sections. Next steps A9,
the operator's go of 2026-11-27. Build record: `../../runs/BUILD_A9.md`.)

## Business objective, one question
**What does a portfolio version earn, against holding its coins, on the days that came after it was built: days
nobody had seen when it was chosen?**
Why: the final coins give one clean test (`common/data_use.md`, step 12); every other result was read on data that the
research, or the choice of the portfolio, had already looked at. New days are the only clean data that renews, and they
cost nothing but waiting. v4 by year on the common records: +18 to +54 % a year in 2016-2021, 2023 and 2024; +6.7 % in
2022, -1.7 % in 2025, +0.8 % in 2026: the last two years are the ones to watch.

## The words
| Word | Meaning |
|---|---|
| Portfolio version | a folder of `orchestration/combine/portfolios/`: its strategies and their weights (`portfolio.json`) |
| Frozen | the version's strategies (each one's plan and config) and weights, as they are at the record's first call; never changed after |
| Start day | the UTC day the version was built: the date of `made_utc` in its `portfolio.json` |
| Forward day | a complete UTC day **after** the start day. The start day itself is not one: the version was built during it |
| Last complete day | the latest day in the portfolio coins' daily files (the data tool writes finished days only). A coin whose file ends earlier is refused by the engine for that update, and named |
| Warm-up | the earlier days a strategy reads to compute its measures; they are before the first forward day and are not counted |
| Portfolio coins | `common/coins.py`, `portfolio_group()`: 25 coins; the final coins are not among them |
| A day's portfolio return | coin by coin, the sum of the strategies' returns that day at the version's weights; then the mean over the coins (`combine/card.md`, rule 6) |
| A day's holding return | on the same coins that day, each coin's close-to-close return; their mean (equal weight) |
| Forward record | one version's file of forward days, each with the portfolio's return and holding's |

## Input
- The version: `orchestration/combine/portfolios/<version>/portfolio.json` (`made_utc`, `commit`, `books`: key and weight).
- Each strategy's plan and config: the plan its common record ran (`orchestration/common_record/<run>/<id>.json`,
  field `plan`), and the config beside it.
- The portfolio coins' daily data, `trading-bot/local_data/`; with `--update-data`, extended first by
  `trading-bot/tools/extend_kraken_daily.py` (unchanged).
- A Python environment with `trading-bot/requirements.txt`.

## Output
`orchestration/forward_record/<version>/`: `frozen.json`, `days.csv`, `record.md` (see Storage).

## What a forward record is
**One portfolio version, frozen, run by the bot's backtest on every day after it was built, with each day's return and
holding's return on the same coins added to one file as the days come.**

- **It belongs to one version.** A later version starts its own record on the day it is built; the earlier version's
  record goes on. Two records can then be read side by side on the same days.
- **It starts flat on the start day**, like a portfolio funded that day: no position from before is carried in. The
  engine's window opens on the start day, whose close is the base; the first return counted is the next day's.
- **Each update, in this order:**
  1. (with `--update-data`) the daily data of the portfolio coins is extended to the last complete day;
  2. the forward window (start day to last complete day) is given to the holdout guard; refused: nothing is run or
     written, the guard's message is printed (see "The holdout dates");
  3. each strategy is checked against `frozen.json` (its plan and config, byte for byte), then run unchanged on the
     forward window, on the portfolio coins, with `common_record.backtest` (step 9's runner: one runner);
  4. the portfolio's and holding's daily returns are computed, and the days after the file's last day are appended
     to `days.csv`, **except the window's last day, which waits for the next update**;
  5. `record.md` is rewritten from `days.csv`.
- **Days already in the file are never rewritten:** an update only appends lines. Every update runs the window again
  from the start day (the engine is deterministic, and a record that restarted flat at each update would depend on
  when the updates were made); the days recomputed are compared with the file and the count of equal and different
  days is shown in `record.md`. A different day is shown, not corrected.
- **Why the window's last day waits:** the engine closes every position on a window's last bar, so that day's
  return holds a closing cost the portfolio would not pay (measured: -0.033 % written against -0.021 % once the day
  was inside a longer window, `runs/BUILD_A9.md`). Written at the next update, the day is the one a portfolio that
  keeps its positions earned. The record is therefore one day behind the data.
- **A strategy or coin the engine cannot run** (no data for its bar size on these days, a coin in its first 90 days)
  is not run and is named in `record.md` with the engine's reason, as in steps 4 and 9. Each day's line says how many
  strategies and coins it holds.
- **It decides nothing.** No step reads it; it stops nothing.

**Not a ledger of trials.** CLAUDE.md: "No trial ledger. Do not write to `research/TRIALS.csv` or any ledger. A run's
own files are its record." A forward record is that: the own record of one frozen portfolio, one line per calendar day,
whatever the day shows. It lists no idea, no attempt and no choice, and nothing is selected from it.

## Why this cannot leak
- The version is frozen before its first forward day: its strategies and weights were fixed during the start day, and
  every day counted is after it. `frozen.json` keeps each plan's and config's fingerprint (SHA-256); an update stops,
  writing nothing, when a file no longer matches.
- Every bar's decision is the engine's, on data up to that bar's close, as in every backtest; the warm-up is read from
  earlier days only. No rule here changes how a bar is read.
- **How the code makes sure no forward day is at or before `made_utc`:** the start day is the date of `made_utc`; the
  returns are computed only between two closes of the forward window, so the first one ends on the day after the start
  day; then the code keeps only days strictly after the start day and refuses to append any other (two tests).
- The data tool writes finished days only, and never changes a row it already has.
- **The final coins are never read:** the coins come from `portfolio_group()`, the data tool is called with those coins
  by name, and the helper's code never names the final group (a test says so, as `common_record`'s).

## The holdout dates
The helper never reads `trading-bot/config/campaign_data_policy.yaml` and writes none of its dates. Before any run it
hands the forward window to the existing guard (`trading-bot/backtest/holdout_policy.py`, `check_windows_before`, the
check the engine's wrapper applies again by itself). If the guard refuses, because forward days fall in the frozen
half-year, the helper stops with the guard's message and writes nothing: the operator decides.
Status 2026-11-27: the guard accepts v4's coming forward days; it refuses a window reaching half a year ahead. So some
future update will be refused (Open 1).

## The fields
`days.csv`, one line per forward day:
1. **day:** the UTC day.
   - For: the record's time line. Used by: `record.md`, any reader. Without it: returns with no date cannot be compared with another version's.
2. **portfolio, holding:** the day's two returns (fractions: 0.01 is 1 %).
   - For: the question. Used by: `record.md`. Without it: no evidence.
3. **coins, strategies:** how many coins and strategies had a return that day.
   - For: knowing what the day's number holds. Used by: the reader. Without it: a day computed without a strategy looks like any other.
4. **added_utc, commit:** when the line was added and by which code.
   - For: the audit (the engine can change between two updates). Used by: the operator. Without it: no way to say which code made a day.

`frozen.json`, written once: the version, its `made_utc` and commit, the start day, and for each strategy its key,
weight, run, id, plan path, and the SHA-256 of its plan and config.
- For: running the same thing at every update. Used by: the helper. Without it: a plan edited later would enter the record unseen.

`record.md`, rewritten at each update: since the start, the days, the portfolio's and holding's return (compounded),
Sharpe (daily, on 365 days a year) once at least 60 days exist, before that "too few days", and the worst fall (peak
to trough); then the last update: the days added, each strategy's coins run and not run, the earlier days recomputed.

## Storage and naming
```
orchestration/forward_record/
  card.md
  helper/forward_record.py        the helper
  helper/test_forward_record.py   its tests (no backtest: the runner is replaced by a fake)
  <version>/frozen.json           written once
  <version>/days.csv              appended only
  <version>/record.md             rewritten at each update
The engine's files of the last update, in each strategy's run, beside its common record:
  04_backtest/<run>/forward_<version>/backtests/<plan id>/   run.md, config.json, <SYMBOL>/w1/, chart_bars.csv.gz
```
The engine's files are replaced at each update (the window is run again from the start day); the chart files are
committed with the update, the windows' large files stay local, as in every record. `run.md` is the runner's: its Data
line names the research windows file (the runner's fixed text); the window run is the forward one.

## How to call it
```
python3 orchestration/forward_record/helper/forward_record.py VERSION --python VENV_PYTHON [--update-data]
```
- The first call writes `frozen.json` and an empty `days.csv`. A call with no new complete day adds nothing.
- `--update-data` needs the network (Kraken's public API, no key).
- Engine time only, 0 USD. One update of v4 (11 strategies, 25 coins, 60 or 122 days): 9 to 10 minutes on 4 cores
  (`runs/BUILD_A9.md`); the time is the engine's start for each coin, not the number of days.

## Quality criteria
- No day at or before the start day is in the file.
- A second update leaves every earlier line byte for byte.
- On past days the mechanism gives the common records' numbers: equal on a whole research window; from a start day
  inside a window, equal where the positions are the same (`runs/BUILD_A9.md`).
- No final coin is read.

## Fixed inputs for the iterations
v4 (`orchestration/combine/portfolios/v4/`), with a pretended start day, in a folder outside the repository.

## Who judges the output
Code records; the operator reads `record.md`.

## Done when
The tests pass; v4's record exists; the proof on past days is in `runs/BUILD_A9.md`. Status: see there.

## Open (for the operator)
1. **The frozen half-year.** The guard will refuse an update whose forward days reach it. Then: stop the records
   there, or open those days to the forward records (they would be read once, by frozen portfolios, never by the
   research). `data_use.md`, section 6, already lists the frozen holdout for removal.
2. **v4's hourly strategy** (`retest_weekend_run`, weight 0.2) will not run on forward days as things are: the data
   tool extends the daily files only. The hourly files of 6 portfolio coins (BTC, ETH, LTC, XMR, XRP, ZEC) stop on
   2026-11-17, those of 10 others at the end of 2025. Until they are extended, the record holds v4's 10 daily
   strategies, and each day's line says so (`strategies`). Kraken's public API serves the last 30 days of hourly bars:
   an hourly extension of the 6 coins is possible **until about 2026-12-17**, after which the gap needs Kraken's
   archive. It is a change to the data tool (shared code: the operator's go). A day written without the strategy stays
   so: the file is never rewritten.
3. **How the monthly update is started:** by hand, by the batch command, or by a schedule (`runs/BUILD_A9.md` proposes).
4. **The start is flat.** A strategy that would have been in a position on the start day (entered earlier) is not in
   it here; on the 60-day proof this explains the gap with the common records (-1.905 % against -1.901 %).
5. **Holding** here is the mean of the coins the portfolio has a return on that day; if next steps A10 fixes one
   holding bar, this definition follows it.

## What this function does not do
It does not choose or change a version, a strategy or a weight; it does not read the final coins, judge the version,
or trade.
