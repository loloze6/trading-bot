# Step card 4: Backtest (2026-11-10)

## Business objective, one question
What did the market data do when this idea's test ran?

**Establish what the market data did under an idea's test: the plan's strategy run unchanged through the bot's own backtest, on the plan's coins, bar size and period, and recorded for the next steps.** (operator, 2026-11-15)

## Input
One test plan from step 3 whose outcome is `plan`: its config and its data (coins, bar size, one fold or several). A plan whose outcome is untestable or missing-components is not run, and its index line says so.

## Output
One backtest record per plan, or "not run", with the reason.

## What a backtest record is
**A backtest record is everything the bot's backtest wrote when it ran one plan's config on the plan's data: per coin and per window, every bar, every trade and the window's figures, with what ran and on which data.**

- The engine is the bot's, used as is. This step designs nothing in it and changes nothing in it.
- The record is kept whole: step 5 reads the bars (forecast, indicators, prices), not a summary.
- A coin or a window the engine cannot run is recorded as "not run", with the engine's reason. It is not dropped silently.

## The fields of a record
1. **`run.md`** (one per plan): the plan, the config, the data as run (coins as venue symbols, bar size, fold), the venue, and per coin a table of windows run (trades, the forecast's correlation with the next return, net return), plus every window not run with its reason.
   - For: says what ran, on what, and what did not run.
   - Used by: the operator, and step 5 to find the windows.
   - Without it: a missing coin or window looks like a result.
2. **`config.json`**: a copy of the plan's config.
   - For: the exact config that ran, next to its results.
   - Used by: step 5, and anyone who reruns it.
   - Without it: a later edit of the plan would leave results with no config.
3. **Per coin and window, `wK/`**: the engine's files.
   - `bars.csv.gz`: one row per bar, with prices, the forecast, each component's raw and transformed value, the position and the portfolio's value.
   - `trades.json.gz`, `metrics.json`, `manifest.json` (what ran: the config's hash, the data's hash, the costs, the engine's version), `forecast_distribution.csv`.
   - The wrapper call's `protocol_summary.json.gz`, `trade_diagnostics.json.gz` and `engine_log.txt`: in the call's folder (`<SYMBOL>/fold_<X>/`: one call per coin and fold; `<SYMBOL>/windows/` with `--windows`), or in the window's folder when the call's windows ran once per window.
   - For: the record itself.
4. **The chart files** (operator, 2026-11-17), beside `run.md`, for every backtest (written by `run_idea` after step 6, with `helper/chart_files.py`); their name says whether git keeps them: a backtest worth a chart (confirmed by step 5, or profitable enough by step 6) gets the committed names below; any other gets `chart_bars.local.csv.gz` and `chart_trades.local.csv.gz`, which git ignores (they stay on the disk where the run happened; on the operator's PC, size does not matter): `chart_bars.csv.gz` (coin, window, timestamp, close, forecast, position, value: one row per bar) and `chart_trades.csv.gz` (coin, window, entry and exit time, direction, entry and exit price, net return). About 220 KB for a daily 6-coin record.
   - For: the run viewer draws a backtest from them (price, trades, the book against holding, the forecast and position), from git, on a phone.
   - Used by: the run viewer only; no step reads them (why they cannot leak).
   - Without it: the viewer has nothing to draw, since the windows' files stay local.
   - Used by: step 5 (verification), step 6 (profitability).
   - Without it: there is nothing to judge.
4. **The index line** (in `INDEX.md`): `<plan id>: ran: BTCUSD 6/6; ETHUSD 6/6; BNBUSD not run (reason) [bar, fold]`, or `not run: the plan is untestable`.
   - For: the list of records and their completeness.
   - Used by: the operator, and step 5 to pick the records to read.
   - Without it: no view of which plans ran.

## Storage and naming
Modelled on the engine's own run folders, one folder per plan, named after the plan.

```
04_backtest/
  card.md                      this card
  helper/
    run_backtest.py            one plan -> the engine, once per coin and fold (once per window as fallback), the calls at the same time; stores the record; adds the index line
    chart_files.py             the chart files of a record (called by run_idea; --backfill for the records already made)
  windows/                     windows files for --windows (other dates than the folds: unseen_2026, unseen_2016_2017)
  backtests/                   created by the helper when it runs (default):
    INDEX.md                   one line per plan
    REVIEW.md                  the review of a real run
    run_log.txt                the log of a real run
    <plan id>/                 one record per plan (the plan id carries the bar size)
      run.md
      config.json
      chart_bars.csv.gz, chart_trades.csv.gz   a backtest worth a chart (committed); any other: chart_*.local.csv.gz (local only)
      <SYMBOL>/                one folder per coin
      <SYMBOL>/fold_<X>/       one wrapper call's summaries and engine_log.txt (one call per coin and fold)
      <SYMBOL>/wK/             one folder per coin and window, K in the folds' order
                               (committed: the summaries, metrics.json, manifest.json, engine_log.txt,
                               forecast_distribution.csv; kept local only: the *.gz files, which step 4
                               rebuilds from the plan; operator, 2026-11-15)
  validation/reading.md        the reading of the exercise that validated this card
  full_data_run/, hourly_run/, validation_run/   the records of named runs
```

- Windows are named `w1` to `wN`, in the fold's order; with several folds, their windows one after the other (folds A to D: `w1` to `w24`). My files (`run.md`, `INDEX.md`, the card, the readings) name periods by fold id only. The engine's own files carry their timestamps and window dates inside, as the engine wrote them.
- `tradesxl.xlsx` and `portfolio_states.csv` are not kept: they repeat `trades.json` and `bars.csv`.

## The engine and the helper
**No model call in this step.** It is mechanical: the engine runs the config. This is the one step that is not an AI step: the step order fixes step 4 as the existing engine.

**How it runs** (`helper/run_backtest.py`):
1. Reads the plan's header, including its outcome. When the plan's config and data are those of its stored record, the record is kept, not rerun: the plan's other fields (fidelity, forecast in words, criterion) do not change what the engine runs.
2. Builds the protocol with the pipeline's own fold loader, `trading-bot/backtest/research_folds.py` (`fold A`, or `folds A, B, C, D`: the windows of each, one after the other). The loader refuses any window touching the sealed holdout. It adds the pipeline's venue keys, from `trading-bot/backtest/venue_resolver.py`. The protocol holds dates, so it is written to a temporary folder only.
3. Runs `trading-bot/backtest/run_protocol.py`, the pipeline's wrapper around the bot's `run_backtest`. The wrapper keeps the warm-up prefetch and the holdout guard.
4. Runs one call per coin and fold, on the fold's windows (with `--windows`, one call per coin): Python and the bot load once per call, not once per window (2026-11-16, `topics/33_review/duration/3_plan.md`, change 1; per coin and fold since 2026-11-20, `12_round2_plan.md`, change C). The call is used only when every window got its own run folder. Otherwise the call's windows run again with one call per window, each in its own folder, and its record is that of a run made this way from the start. Two cases trigger it: the wrapper stops at the first window that fails, and two windows can share a run folder (see "Open").
   - **Why this can't leak:** each window still makes its own `run_backtest` call with its own dates, warm-up and holdout guard, and that call builds a new data manager. So no bar passes from one window to the next, and each window sees exactly the bars it saw when it ran alone. Checked on 297 windows: every window's data block in `manifest.json` (start, end, bar count, data hash) and its `bars.csv` are identical to one call per window (`topics/33_review/duration/6_change1_proof.md`, branch `sd2/run-idea-duration`).
   - **On the run machine (Linux container, 4 cores, 2026-11-16):** demo_run e1 (every window runs) took 559 s with one call per window and 288 s with one call per coin (−48%). The 144 windows match: bars, trades, metrics and forecast files byte for byte; the manifests differ only in run_id, created_utc and git_sha. With the coins at the same time (change 2; 4 cores, so 4 coins at once): 130 s (−77% from 559 s), the same 144 windows identical.
5. Runs the calls at the same time, as many at once as the machine has cores (the count Python reports; 2026-11-16, `topics/33_review/duration/3_plan.md`, change 2; one call per coin and fold since 2026-11-20, so 6 coins no longer run in two waves on 4 cores). The calls are separate processes with their own output folders. The wrapper's `--trades-file-in-out-dir` gives each call its own interim trades file instead of the engine's one shared `trading-bot/results/trades.json`; the campaign does not pass it, so its runs are unchanged. `run.md` and `INDEX.md` list the coins in the plan's order, whichever finishes first.
   - **Why this can't leak:** the coins share no memory: each runs in its own processes, which read only that coin's bars and the aux feeds, as when they ran one after another. The shared files they touch: the interim trades file (now one per call; it only feeds `tradesxl.xlsx`, which this step drops), the bot's log, and a data file the fetcher rewrites only when a read adds rows the file lacked (see "Open"). Checked on 299 windows, twice: every window's files are identical to one coin after another, manifests aside from run_id, created_utc and git_sha; no data file changed (`topics/33_review/duration/7_change2_proof.md`).

**Missing bars: the gap rule** (`../common/forecast.md`, point 8; topic 18). A hole of up to one day in a coin's bars is
read as it is; a longer one stops new positions for a warm-up of real bars; one as long as the warm-up flattens the
book. The engine applies it to every backtest; each window's `manifest.json` records it (`config.gap_rule`).

**The data: local files only** (2026-11-18, `trading-bot/data/coverage.py`). The engine reads the coins' files in
`trading-bot/local_data/` and never calls an exchange. A window whose days (warm-up included) were not fetched stops,
"the dates were not fetched (run the data tool)": a data tool fetches them first and records them in
`local_data/coverage.yaml`. A hole inside a fetched range (an hour without a trade) is read as it is.

**Any bar size** (2026-11-18): the plan's bar is the trading bar (when decisions are made). The data's bar is deduced
from the files, not set by the plan: the largest bar with a file for the coin that divides the trading bar
(`trading-bot/data/coverage.py`, `data_bar`); the engine builds the trading bars from it, as the live bot builds them
from hourly candles. A bar with its own file (1d, 1h) is read as it is. Checked on 4h: 4,380 bars equal the hourly
data added up by hand (open, high, low, close exactly; volume within the record's 6-decimal rounding).

**Other dates** (`--windows FILE`, 2026-11-18, `runs/UNSEEN_RUN.md`): the same plan and config on the windows of a JSON file
(`[{label, test: {start, end}}, ...]`, in `windows/`) in place of its folds; the record's data line names the file. Used
to test an idea on dates the research never saw.

**Other coins** (`--coins "ADA, DOGE"`, 2026-11-25, `runs/UNSEEN_COINS_RUN.md`): the same plan, config and folds on these
coins in place of the plan's `data-instruments`; the record's data line names them, and the rerun check reads them (a
record on other coins is not the plan's own). Used to test an idea on coins its plan never tested
(`common/unseen_coins.md`). A coin without data in a window is skipped there, as in-sample.

**The new data use** (`--data-use FILE`, 2026-11-26, `runs/BUILD_A4_RESEARCH.md`; `common/data_use.md`): the run's
`data_use.json` decides the data in place of the plan's coins and folds: its 8 research coins, on the windows of its
windows file (`windows/research_2016.json`, 32 windows, `w1` to `w32` in the file's order), one call per coin. Before the
engine runs, a coin is left out of a window by `data_use.md`'s section 3 (`common/coins.py`, `left_out`: one count,
the same in steps 9 and 12): the window starts before the coin's 91st day; or the coin's history is shorter than the
warm-up the wrapper will load for this plan before the window (twice the bars the plan's strategy needs, asked from
the bot's own strategy class on the plan's config, `coins.plan_warmup`; next steps A12, 2026-11-27, after pilot A4's 28
windows refused by the engine for a short history); or the coin's daily file misses more than one day in a row inside
the window (its edges included); a window left out keeps its number (the halves and step 6's "one window left out" read the same number
as the same dates on every coin). Left-out windows are counted in `run.md` (per coin, with the reason) and on the index
line (`ADAUSD 30/32 (2 left out by the data use)`); anything else the engine refuses is "not run" with the engine's
reason, as always. The record holds a copy of `data_use.json` (steps 5 and 7 read their halves from it); its data line names
`windows research_2016, data use 2`. Passed by `run_idea` for a run that holds `orchestration/loop/<run>/data_use.json`
(the one place that decides a run's backtest data). **Why this can't leak:** the left-out rule reads the coin's daily
file's dates and the plan's config (how many bars its strategy needs), never a price, and decides before any bar is read; each window runs as before, with its own warm-up.

The helper never opens the price data: only the engine reads bars. It needs a Python environment with `trading-bot/requirements.txt` (`--python`). `helper/summarise_backtests.py` prints one table of a backtests folder from the engine's `metrics.json` files, for the readings.

**Venue.** Binance is not reachable from this environment (HTTP 451). Kraken is reachable, and the repository holds Kraken caches for 19 coins, daily and hourly; six cover all four folds (BTC, ETH, LTC, XMR, XRP, ZEC: step 3's default). Coins run as `<COIN>USD`, with the pipeline's Kraken keys: Kraken spot prices, Kraken futures costs, no funding. Costs do not change the verification, which is judged before costs; branch 3 judges the book after them.

**Time and size.** On one fold, a daily plan takes 20 to 40 seconds and 0.2 to 0.5 MB per coin; an hourly plan about 2 minutes and 2 MB per coin. On the default data (6 coins, folds A to D), a daily plan runs 144 windows: 6 plans took about 25 minutes, three at a time, and 37 MB.

## Quality criteria on the record
- Every window of every coin with data is run. Every coin or window not run is recorded, with the engine's reason.
- The engine and the pipeline's wrapper are used unchanged, with warm-up and the holdout guard.
- A rerun of the same plan gives identical bars, window by window.
- No window shares a folder with another.
- My files carry no dates and no window labels: fold ids only.

## Fixed inputs for the iterations
The seven plans of step 3, exercise 10 (five testable, two untestable), on daily bars. One of them is also run on hourly bars (step 3's hourly plan for the same idea).

## Variants compared
Daily against hourly bars, for the same idea (`001-01`). Hourly is about 24 times the bars, in about 6 times the time.

## Production run
The named runs: `full_data_run/` (6 coins, folds A to D, daily; with the current steps), `hourly_run/` (BTC, ETH, fold A, hourly; 001-01 with the current steps, the nine others before the sizing rule), `validation_run/` (the step 7 validation loops' ideas; with the current steps).

## Who judges the output
The operator: "is this the run of my plan, complete and the same if run again?". Code records what ran and what did not. Each exercise has a one-page reading.

## Done when
On two exercises in a row, every criterion holds, and a full rerun of the fixed inputs is identical, bar for bar. Status: met by exercises 1 and 2 (`validation/reading.md`).

## Open
- **An engine defect, found by this step.** The engine names a run folder after the current second plus the config's hash (`reporting/run_artifact.py`). When two windows of one wrapper call finish within the same second, they share one folder, and the second overwrites the first. Daily windows run in under a second each, so this happens. A rerun check found two windows with the same run id. This helper detects it (fewer run folders than windows) and then runs that coin one window at a time. The research pipeline's own daily runs may be affected; that is for the operator to check.
- **BNB has no data on the reachable venue.** Ideas from briefs that name BNB run on BTC and ETH only.
- Fixed since, and removed from this list (git and their commits keep them): the warm-up refusal of a 0-bar component
  and the 400-against-250 rows wait (engine, `171902d`), the data file rewritten in place (written whole, then renamed).
- **The trial ledger.** The operator ruled no trial ledger for these runs (2026-11-10); their record is the backtests folders' `INDEX.md`.

## What this step does not do
It does not judge a result, compute profitability, or change the engine or the plan.
