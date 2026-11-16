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
   - The wrapper call's `protocol_summary.json.gz`, `trade_diagnostics.json.gz` and `engine_log.txt`: in the coin's folder (one call per coin), or in the window's folder when the coin ran once per window.
   - For: the record itself.
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
    run_backtest.py            one plan -> the engine, once per coin (once per window as fallback); stores the record; adds the index line
  backtests/                   created by the helper when it runs (default):
    INDEX.md                   one line per plan
    REVIEW.md                  the review of a real run
    run_log.txt                the log of a real run
    <plan id>/                 one record per plan (the plan id carries the bar size)
      run.md
      config.json
      <SYMBOL>/                one folder per coin: the call's summaries and engine_log.txt (one call per coin)
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
2. Builds the protocol with the pipeline's own fold loader, `strategy-research/tools/research_folds.py` (`fold A`, or `folds A, B, C, D`: the windows of each, one after the other). The loader refuses any window touching the sealed holdout. It adds the pipeline's venue keys, from `tools/venue_resolver.py`. The protocol holds dates, so it is written to a temporary folder only.
3. Runs `strategy-research/tools/run_protocol.py`, the pipeline's wrapper around the bot's `run_backtest`. The wrapper keeps the warm-up prefetch and the holdout guard.
4. Runs one call per coin, on all its windows: Python and the bot load once per coin, not once per window (2026-11-16, `orchestration/duration/3_plan.md`, change 1). The call is used only when every window got its own run folder. Otherwise the coin runs again with one call per window, each in its own folder, and its record is that of a run made this way from the start. Two cases trigger it: the wrapper stops at the first window that fails, and two windows can share a run folder (see "Open").
   - **Why this can't leak:** each window still makes its own `run_backtest` call with its own dates, warm-up and holdout guard, and that call builds a new data manager. So no bar passes from one window to the next, and each window sees exactly the bars it saw when it ran alone. Checked on 297 windows: every window's data block in `manifest.json` (start, end, bar count, data hash) and its `bars.csv` are identical to one call per window (`orchestration/duration/6_change1_proof.md`, branch `sd2/run-idea-duration`).

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
- **A config pattern the engine's warm-up check refuses.** Volume plans (five in the first run; `003-01_1d` and `003-02_1d` in the current production) gate the strategy with a veto on a constant (`BuyAndHoldStrategy` with `volume_filter`) and leave the default regime flat. The validator accepts this, but the engine stops at its warm-up check: "strategy not ready after 48 prefetch bars". Their record says "not run", with the engine's message. Step 3 could avoid the pattern (the same ideas run when the gate is a rule on `VolumeExpansionHedgeComponent`, or a veto on `PriceEvolutionComponent`).
- **BNB has no data on the reachable venue.** Ideas from briefs that name BNB run on BTC and ETH only.
- **Data gaps before a window.** On the full data, 1 XMR and 2 XRP windows were refused at the warm-up check: fewer rows before them than the engine waits for (400, while it declares 250: an engine defect, `../POTENTIAL_ADJUSTMENTS.md`, Parked B). Only XRP w13 has fewer than the 250 the config needs. Recorded as "not run".
- **The trial ledger.** The operator ruled no trial ledger for these runs (2026-11-10); their record is the backtests folders' `INDEX.md`.

## What this step does not do
It does not judge a result, compute profitability, or change the engine or the plan.
