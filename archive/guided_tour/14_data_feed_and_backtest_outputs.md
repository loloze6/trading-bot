# Stop 14: The data feed and the backtest's outputs

## Speech (verbatim)

**Stop 14 of 29: The data feed and the backtest's outputs.** Open on the side: `trading-bot/data/data_manager.py`, `data/fetchers/ccxt_fetcher.py`, `core/backtester.py`, `reporting/run_artifact.py`, `performance/metrics.py`, `execution/portfolio_info.py`, `strategy-research/docs/DATA_DICTIONARY.md` (§1-5), one window folder of run_102.

**In one sentence.**
The data feed hands the engine stored price bars for one coin and one test window, refusing any bar from the sealed holdout; the backtester replays them bar by bar and leaves seven files per window: what was run, every bar, every trade, and the window's figures.

**Why it exists.**
Every judgement later in the run (the pass/fail grid, the profit bars, the claim test, the analyst) reads these files, not the engine. So they must hold everything needed to explain a result, bar by bar, and be traceable to exactly what ran.
The data guard exists so that no backtest can ever touch the holdout (the final, single-use test period), even by mistake.

**What comes in, what goes out.**
- In: the strategy config (stop 12), the coin, the window's start and end, the bar size, the costs (stop 13); price bars from the local cache.
- Out, one folder per window and variant: a manifest (what ran and with which settings), `bars.csv` (one line per bar), `trades.json` and `tradesxl.xlsx` (every trade), `metrics.json` (the window's figures), `forecast_distribution.csv`, `portfolio_states.csv`.
- Next: the research backtest tool gathers these into the run's results (stop 18); the three judges read them (stops 19-21).

**What happens here, step by step.**
1. The data manager looks for the coin's bars in the local cache. A Kraken cache file is named after the venue, the coin and the bar size (for example `kraken_<coin>USD_1h.csv`); Binance files carry no venue prefix.
2. Before fetching, it refuses a window that reaches into the sealed holdout; after loading, it refuses any returned bar inside it. That refusal is never turned into an empty result.
3. Extra bars before the window are loaded for warm-up (so the strategy is ready at the window's start), and are not traded.
4. The backtester feeds the bars one by one into the per-bar cycle (stop 13).
5. At the end it closes any position, then writes the files. The manifest records the config's fingerprint, coin, window, costs, the gap rule and the engine version. `bars.csv` records, per bar, prices, forecast, the allocation steps, the sizing figures, the band's decision, the trade result, the portfolio value, and a debug column per component (its value before and after transforms, its weight). `metrics.json` holds the window's "core" block: return, Sharpe ratio (return per unit of risk), drawdown, trade count, win rate, fees, gross and net profit, cost drag, the forecast's correlation with the next bar's return (active bars and all bars, at several horizons), gaps skipped, average trade duration, and cost checks.
6. Trades are matched last-in first-out into completed trades with their profit and fees.
7. The data dictionary (`DATA_DICTIONARY.md`) describes every column and field, for the analyst (stop 21).

Example: run_102's base variant has 6 window folders (fold B, six 4-month blocks across 2018-2021), each with the 7 files; its `bars.csv` has 50 columns, `portfolio_states.csv` 49; a window holds about 2,900 hourly bars.

**What it costs and how long it takes.**
No AI call. Duration per window is not recorded in the run's audit log.
7 files per window; run_102 tested 4 variants on 6 windows each (`runs/run_102/variants/*/results/`).

**What is switched off or not used here.**
- Every backtest also rewrites one shared trade log, `trading-bot/results/trades.json`, the tracker's default file.
- The forecast analyser (`performance/forecast_analyzer.py`) is not run by research.
- Funding data is dropped for Kraken runs (stop 13).

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| Data manager | `trading-bot/data/data_manager.py:712-765` | Construction, fetch resolution |
| Historical fetch | `trading-bot/data/data_manager.py:1237-1343` | Request seal guard (`:1286-1292`), returned-rows guard (`:1325-1330`), propagation |
| Cache name | `trading-bot/data/fetchers/ccxt_fetcher.py:101-124` | `kraken_<SYM>_1h`; Binance unprefixed |
| Backtester | `trading-bot/core/backtester.py:216-293` | `load_data`, feeds, warm-up |
| Replay | `trading-bot/core/backtester.py:299-382` | `simulate_on_loaded_data` |
| End of backtest | `trading-bot/core/backtester.py:384-729` | Close, analysis, write files (`:592-616`) |
| Run folder and manifest | `trading-bot/reporting/run_artifact.py:122-129`, `:162-285` | Folder naming; manifest |
| Core block | `trading-bot/reporting/run_artifact.py:292` | `build_core` |
| Bar equity | `trading-bot/reporting/run_artifact.py:753-815` | Bar-level equity block |
| Trades | `trading-bot/performance/metrics.py:121-317` | `CompletedTrade`, positions |
| Tracker | `trading-bot/performance/metrics.py:319-329`, `:821`, `:1444-1499` | Shared log `results/trades.json` (`:322-329`), metrics, drawdown |
| Bar states | `trading-bot/execution/portfolio_info.py:415-534` | `PortfolioStateTracker`, `to_csv` (`:493-507`) |
| Not run | `trading-bot/performance/forecast_analyzer.py:54-66` | Forecast analyser |
| Dictionary | `strategy-research/docs/DATA_DICTIONARY.md:79-366` | §1 bars.csv, §2 trade diagnostics, §3 core block, §4 per-regime, §5 diagnostics |
| Example | `runs/run_102/variants/base/results/<ts>_<hash>/` | 7 files; 50 and 49 columns |

Remarks: send them as "stop 14: <remark>"; mark "direct" for an answer.

## Operator remarks (verbatim, with the guide's direct answers)

Stop15. 
Wait, trades.json should be read as an output by further post backtest steps, no ?? 
Here it is key to make sure that backtest output is generating complete details of the backtest : per bar (bar file), per trade (trade file).
Each of this file should have a line per element (resp. bar, trade) and associated details around it until low granularity (eg: forecast component sub details on the bar and trade lines, 

(Guide's note: sent labelled "Stop15"; recorded here because the backtest's output files and the shared trades.json are described in this stop, sections 3 and 6. The last line arrived as written above; it appears cut off.)

## Inspector notes

### (1) Design and mechanism

1. The seal is enforced twice on the read path and the refusal cannot be swallowed: a window reaching into the holdout is refused before any fetch (`data_manager.py:1291-1292`), returned rows inside it are refused after (`:1328-1329`), and `SealedDataError` is re-raised past the blanket handler that turns every other failure into an empty frame (`:1334-1340`). The cache name is venue-qualified for every venue but Binance (`ccxt_fetcher.py:123-124`). The provenance is complete for a replay: the manifest carries the config with the cost model, gap rule and fetch resolution folded in and hashed (`backtester.py:472-568`, `run_artifact.py:173-192`), the data hash, the git SHA with a dirty marker (`:143-155`; run_102's reads `-dirty`, manifest `:100`), and the engine's lookback and warm-up (`:188-191`). This is the part of the pipeline that lets a result be found again.
2. The window's record confirms three earlier readings on real numbers (run_102 base, first window). The band passed on the signal path with a sized change below the band: first bar `allocation_change 0.1623`, `passed_on signal`, `sizing_signal_change 0.4947` (`bars.csv` row 2) -- stop 13 note 1.1. The stretch leg sits at the standardise cap on that bar (`post_pipeline_value 20.0`) and the trend leg's `post_pipeline_value` has std 10.8 over the window (`metrics.json:126-130`, `:150-154`) -- stop 12a note 1.2. And the prefetch worked: `n_bars_warmup_excluded 0` (`:184`) -- stop 12b note 1.1. The window itself: 383 trades in 2,952 bars (one every 7.7 bars), fees 17.6 on 1,000, `cost_drag_pct 56` (`:6-12`), `turnover 35.5` (`:182`), net return 1.4%: the cost structure stop 13 predicted. One gap, one bar, tier ignore (`:189-201`): the 288-bar middle tier did not bite here.
3. The record carries documented defects that no one fixes. The dictionary's audit (2026-10-08, `DATA_DICTIONARY.md:584-595`) lists A1 (`balances.*` are the end-of-run values on every row, `:597-604`): run_102's first bar reads `balances.USDT.free 1013.78`, the window's final equity (`bars.csv` row 2, `metrics.json:11`), eighteen days after the audit. A2 (`confidence` always 0, `strategy` empty), A3 (the triple-c column), A5 (`exit_reason` is `signal_flip` for every non-final exit, 99%), A6 (MAE/MFE include the entry bar), A7 HIGH ("the mandatory cost bar is looser than stated": `cost_paid` is fee x 2 without slippage while `realized_return` is net of slippage, `:632-639`), A8 (zero-trade windows vote). Of `bars.csv`'s 50 columns, 8 (`balances.*`, `postRebalance_balances.*`) are wrong, 2 are constant, and the core block still writes three legacy route labels (`metrics.json:37-38`, `:49-50`, `kill_no_ic`) the dictionary says are "removed when the legacy verdict is retired" (`:305-306`, `:316-317`). The analyst is told to read around them (`:13-16`). For a loop whose judges read these files, A7 is the one that bears on the goal: the profit bar's cost ratio (stop 20) is built on a cost that omits slippage; whether `cost_bar_all_costs` (flag on, stop 03a) closes it is stop 20's check (`:210-212`, `:259` say the all-costs fields exist under the flag).
4. Two Sharpe ratios, two drawdowns, neither the one a trader would quote. `core.sharpe` is the daily sum of trade returns booked on exit dates, zero-filled on no-trade days, sqrt(365) (`metrics.py:1464-1499`); `core.max_drawdown_pct` is the trade-by-trade compounded curve (`:1444-1462`); `bar_equity` (on, `run_protocol.py:2684`) resamples the real equity to daily closes (`run_artifact.py:753-817`): 0.46 vs 0.35, -8.1% vs -10.0% on this window (`metrics.json:4-5`, `:178-179`). The dictionary says which is which (A9); the grid's `whole_test_sharpe` and the bars use a third, chained definition (stop 20). Three definitions of the same word in one record is the kind of thing that fools a reader more than a model.
5. The shared `results/trades.json` is written by every backtest (`metrics.py:322`, `:594`) and read back to build `tradesxl.xlsx` (`:600-602`); `load_trades` only logs a count (`:610-621`) and the existence check is against the CWD, not the resolved path (`:340` vs `:329`), so nothing leaks between runs today. The guard is the house rule "one test process at a time" (`SR/CLAUDE.md:115`): two concurrent backtests would write one file. A per-run path exists (`trades_log_file`, `launcher.py:676-682`); `run_protocol.py` does not pass it (`:2682-2688`).
6. The per-window outputs are the right granularity for the judges, and the engine's lazy end-of-run assembly (`backtester.py:384-729`) is one function of 345 lines doing twelve things (close, resample, merge state, five provenance folds, manifest, trades, Excel, metrics, bars, states, integrity check). It works; it is also where a defect like A1 lives unnoticed, because the balances dict is stored by reference at `record_state` (`portfolio_info.py:476-480`, dictionary `:599-601`) and flattened only here (`:464-465`).

### (2) Legacy or simplifiable (leads)

1. `bars.csv` columns with no live reader or wrong content: `balances.*` and `postRebalance_balances.*` (A1, 8 columns), `confidence`, `strategy` (A2), `portfolio_value` (a copy of `total_portfolio_value`, `backtester.py:429-430`), `debug_info.regime_scores`/`regime_margin` (empty for threshold_rules, 2 columns). About 13 of 50. The dictionary marks them; the writer keeps them.
2. `metrics.json` `core`: `post_backtest_route`, `post_backtest_route_rationale`, `post_backtest_route_real`, `post_backtest_route_real_rationale`, `post_backtest_cost_check` (the prescreen formula, `run_artifact.py` per dictionary `:299-306`): legacy labels of the deleted prescreen and the retired verdict; `forecast_bins` (`:61-118`, per-trade success by forecast bin): not in the dictionary's sections 1-5; whether any live reader uses it was not checked.
3. `tradesxl.xlsx` and `export_metrics_to_excel`'s "Performance_Metrics" sheet with Pardo-2012 comments (`metrics.py:599-640`): a human report written for every window of every variant (24 per run); no code reads an xlsx (not checked beyond the dictionary, which lists none).
4. `ForecastAnalyzer` constructed in every tracker (`metrics.py:334-336`) and run only under `human_reports` (`backtester.py:701-705`): construction for nothing.
5. `backtester.py:392-467` ("TRADE REGIME AGREEMENT ANALYSIS", the resample and merge of price data with state): the resampled `price_data` feeds only `get_performance_metrics(price_data=... if self.human_reports else None)` (`:613-615`); the merge's `print(...)` fallbacks (`:437`, `:441`, `:445`) are debugging left in.
6. `EnhancedPerformanceTracker.load_trades` (`:610-621`): loads nothing; delete with the `os.path.exists(log_file)` check (`:340-341`).
7. `PortfolioStateTracker.get_tracker_summary` (`portfolio_info.py:516-534`): reads `btc_borrowed`/`usdt_borrowed` columns that `record_state` never writes; not checked for a caller.
8. The dictionary's section 2 trade-diagnostics fields marked `after` (`:203-208`, `:218`, `:249-251`): hindsight labels the analyst is warned about; `cost_paid` (A7) and `exit_reason` (A5) are known wrong and still written by `run_protocol` (stop 18).

### (3) Disagreements between the speech and the element

1. Step 2, the two seal guards and "never turned into an empty result": `:1286-1292`, `:1328-1329`, `:1334-1340`; correct.
2. Step 5, the manifest "records the config's fingerprint, coin, window, costs, the gap rule and the engine version": `config_sha256`, `data`, `cost_model`, `gap_rule`, `git_sha` and `engine.lookback/warmup` (manifest `:89-104`); "engine version" is the git SHA with `-dirty` on run_102 (`:100`), which the speech does not say: every run_102 window was produced from a tree with uncommitted tracked changes (stop 06 note 1.4, the flag set).
3. Step 5, `bars.csv` "records, per bar ... balances": the balances columns are the end-of-run values on every row (A1, note 1.3); the speech lists them as a bar-level fact. Wrong as stated, and the dictionary the speech cites says so.
4. Step 5, `metrics.json` "holds the window's core block: return, Sharpe ratio ..., drawdown ...": the speech does not say these are trade-exit based and that `bar_equity` holds the bar-based pair (note 1.4). Omission that matters for a reader comparing the two numbers.
5. Step 6, LIFO matching: `metrics.py:320` and the dictionary (`:33-34`); correct.
6. Section 6, "Every backtest also rewrites one shared trade log": correct (`:594`); also read back for the xlsx (note 1.5). "Funding data is dropped for Kraken runs": manifest `:107-109`; correct.
7. Section 5, "7 files per window": the folder lists 7 (`manifest.json`, `trades.json`, `tradesxl.xlsx`, `metrics.json`, `bars.csv`, `forecast_distribution.csv`, `portfolio_states.csv`). "`bars.csv` has 50 columns, `portfolio_states.csv` 49": 50 and 49 by header count (the extra is `portfolio_value`). "about 2,900 hourly bars": 2,952 (`metrics.json:55`). Correct.
8. Reading-map ranges verified: `data_manager.py:712-765`, `:1237-1343` (guards `:1291-1292`, `:1328-1329`; the map's `:1286-1292`, `:1325-1330` are the comment blocks around them); `ccxt_fetcher.py:101-124`; `backtester.py:216-293`, `:299-382`, `:384-729` (`:592-616`); `run_artifact.py:122-129`, `:162-285`, `:292`, `:753-817`; `metrics.py:319-329` (`:322-329`), `:1444-1499`; `portfolio_info.py:415-534`, `:493-507`; `forecast_analyzer.py:54-66`; `DATA_DICTIONARY.md:79-366`. `metrics.py:121-317` and `:821` not read.
