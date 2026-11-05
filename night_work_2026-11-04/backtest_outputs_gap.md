# Backtest outputs: per-bar and per-trade detail, gap analysis

Read-only analysis, 2026-11-05. SR = `strategy-research/`, TB = `trading-bot/`. Facts from code, file:line. No build proposal.

## Operator remark (stop 14, sent as "Stop15", verbatim)

> Wait, trades.json should be read as an output by further post backtest steps, no ??
> Here it is key to make sure that backtest output is generating complete details of the backtest : per bar (bar file), per trade (trade file).
> Each of this file should have a line per element (resp. bar, trade) and associated details around it until low granularity (eg: forecast component sub details on the bar and trade lines,

(The last line is cut off in the source, `guided_tour/14_data_feed_and_backtest_outputs.md:63-66`.)

## Sources used for real headers (all fixtures unless said otherwise)

- `SR/tests/fixtures/d201_run_102/` and `SR/tests/fixtures/d203_run_102/` hold **no** window files. They hold only proposal/config/manifest/memory YAML and run artifacts (13 files in total), so they have no column headers to show.
- `SR/tests/fixtures/run_viewer/runs/run_098/` and `run_099/` (fixture: copies of run_098/run_099 passed through `sanitize_text`, `SR/tests/test_run_viewer.py:4-5`). Each window folder keeps only `bars.csv` and `trades.json`. The `bars.csv` files have 42 columns and 123 lines. Window folders are named `<stamp>` below.
- `SR/tests/fixtures/d141/run_095_base/.../portfolio_states.csv` (fixture). It is column-trimmed to 5 columns (`timestamp, close, regime, total_portfolio_value, postRebalance_total_value`).
- For `tradesxl.xlsx`, `forecast_distribution.csv`, `manifest.json` and `metrics.json` no fixture exists. I read headers and keys only from the newest folder under `TB/results/runs/`. That folder is **not a fixture**: it is an older committed artifact that predates the current `core` keys. I used it only for the sheet names, the xlsx header and the CSV header.

---

## 1. Files a backtest writes per window and variant

All of these are written by `BacktestEngine._end_of_backtest` (`TB/core/backtester.py:384-729`) into one run folder:

- The folder is made by `new_run_dir`, `TB/reporting/run_artifact.py:122-129`, called at `backtester.py:573`. It is named `<UTC stamp>_<config sha8>`.
- Research passes `runs_root=<out_dir>/results` (`SR/tools/run_protocol.py:2594`, `:2653`). In a research run the folder is therefore `runs/<run>/variants/<vid>/results/<stamp>_<hash>/`, with one folder per (coin, window).
- Research calls `run_backtest` at `run_protocol.py:2610` and `:2682-2688`.

### 1.1 manifest.json

- **Writer:** `write_manifest`, `run_artifact.py:162-195`, called at `backtester.py:592-603`.
- **Rows:** one JSON object per window run.
- **Fields:**
  - `run_id`, `created_utc`
  - `config`: the strategy config, plus these provenance folds when they apply:
    - `risk_management.portfolio_controls` (`backtester.py:492`)
    - `model_funding` (`:509-515`)
    - `fetch_interval_seconds` (`:527`)
    - `gap_rule{gap_detection, gap_policy, indicator_fill?}` (`:546`)
    - `cost_model` (`:565`)
  - `config_sha256`
  - `data{symbols, timeframe, start, end, bar_count, data_sha256}`
  - `git_sha`
  - `engine{lookback, warmup}`
  - optional `feeds{registered, dropped, required}` (`run_artifact.py:193-194`)
- **Live readers:**
  - `SR/tools/composite_cache.py:310-314` reads `git_sha`.
  - `SR/workflow/run_phase1_research.py:14300-14311` (`_v2_manifest_slippage`, profit bars v2) reads the slippage bps from the manifest.
  - Tests: 8 SR test files and 7 TB test files mention it.

### 1.2 bars.csv

- **Writer:**
  1. `write_bars_csv`, `run_artifact.py:263-264`, called at `backtester.py:692`. It writes `flat_state_df.round(6)`.
  2. `flat_state_df` is `flatten_dict_columns(state_df)` (`backtester.py:464`; flattener at `TB/execution/portfolio_info.py:400-412`).
  3. `state_df` is `PortfolioStateTracker.states` (`backtester.py:423`) plus a `portfolio_value` copy of `total_portfolio_value` (`:430`).
- **One row per what:**
  - One row per bar that reached `record_state` (`TB/core/trading_bot.py:637-653`).
  - Warm-up prefetch bars before the cutoff return early and are **not written** (`trading_bot.py:408-410`).
  - A bar whose per-bar body raised is not written (`trading_bot.py:658`).
  - The end-of-backtest forced close is merged into the last bar's row, not appended (`trading_bot.py:767-780`; `portfolio_info.py:482-488`).
- **Row content:** `{**data row, **signal fields, **record_state kwargs}` (`portfolio_info.py:467-480`). Nested dicts are flattened to dot-names. An empty dict stays as one unflattened column; for example `debug_info.regime_scores` in the fixture.
- **Columns in the fixture** (`run_viewer/runs/run_098/variants/base/results/<stamp>/bars.csv`, 42 columns):
  `timestamp, open, high, low, close, volume, forecast, confidence, regime, strategy, total_portfolio_value, previous_allocation, allocation_change, approved_rebalance, succcess_execute_portfolio_rebalance, postRebalance_total_value, postRebalance_current_allocation, portfolio_value, debug_info.regime, debug_info.forecast_delta, debug_info.regime_scores, debug_info.regime_margin, debug_info.bars_in_regime, debug_approve_allocation_change.symbol, debug_approve_allocation_change.time, debug_execute_portfolio_rebalance.symbol, debug_execute_portfolio_rebalance.price, debug_execute_portfolio_rebalance.quantity, debug_execute_portfolio_rebalance.trade_type, balances.USDT.free, balances.USDT.locked, balances.BTCUSD.free, balances.BTCUSD.locked, postRebalance_balances.USDT.free, postRebalance_balances.USDT.locked, postRebalance_balances.BTCUSD.free, postRebalance_balances.BTCUSD.locked, debug_info.components.anchor_position.last_history_value, debug_info.components.anchor_position.post_pipeline_value, debug_info.components.anchor_position.weight_normalized, debug_info.components.anchor_position.weighted_contribution, debug_approve_allocation_change.controls.min_allocation_change.passed`
- **Conditional columns** (not in the fixture):

  | Column(s) | When it appears | Where |
  |---|---|---|
  | aux-feed columns of the data row | the run has aux feeds | `portfolio_info.py:467`, `:476-480` |
  | `debug_info.components.<id>.*`, one group of 4 per component | always, per component | `TB/strategies/strategy_engine.py:625-630` |
  | 5 keys per block, including `active` | block combiner on | `strategy_engine.py:537-543` |
  | `debug_info.components.not_ready_component` / `not_ready_block` | a component or block is not ready | `strategy_engine.py:621`, `:530` |
  | `debug_info.error` | the strategy is not ready or raised | `TB/strategies/strategy_base.py:376-385`, `:400-406` |
  | `debug_info.regime_scores.<regime>` | the scores dict is non-empty | `TB/strategies/regime_engine.py:194`, `:219` |
  | `risk_target_raw, risk_cap_clamped, risk_killed, risk_drawdown, risk_daily_halted, risk_daily_loss, risk_trip` | risk gate on | `TB/risk/portfolio_risk_gate.py:309-317` |
  | `sizing_realised_vol, sizing_target_allocation, sizing_signal_change` | sizing block on | `trading_bot.py:458-461`, `:542` |
  | `debug_approve_allocation_change.controls.min_allocation_change.passed_on` | sizing block on | `TB/risk/risk_manager.py:55` |

- **Live readers:**
  - `SR/tools/run_protocol.py`:
    - `_load_bars` `:182-247` reads OHLC and timestamp for trade diagnostics.
    - pooled IC `:1443`.
  - `SR/tools/window_economics.py:98-99`, `:151-153`, `:313`. Columns: `timestamp, regime, total_portfolio_value, postRebalance_current_allocation, previous_allocation`.
  - `SR/tools/claim_tests.py`:
    - `read_bars_csv` `:416`
    - `load_variant_bars` `:523-540`
    - `postRebalance_current_allocation` `:1463`
    - Through `claim_tests`, these modules read it too: `claim_measure.py`, `fold_confirm.py`, `explore_confirm.py`, `claim_findings.py:122`.
  - `SR/tools/analyst_queries.py:617-621`. It reads any column that the data dictionary types, including component columns.
  - `SR/tools/residual_ic.py:351-354`.
  - `SR/tools/composite_cache.py:270-317` (OHLCV fingerprint).
  - `SR/workflow/run_phase1_research.py:15318-15330` (`_variant_forecast_shape`) and `:15377-15390` (window economics, analyst flag).
  - Run viewer `SR/tools/run_viewer/loaders.py:75-82`, `:300-330`, `:1667-1673`. It reads `timestamp, close, forecast, postRebalance_current_allocation, portfolio_value, approved_rebalance`.
  - Not imported by any workflow or tool, so standalone CLIs: `SR/tools/fragment_patterns.py:60-63`.
  - Tests: 35 SR and 7 TB test files mention it.
- **In-engine (in memory, not the file):** `build_core`, `build_per_regime`, `build_dynamic`, `build_regime_validity` and `build_bar_equity` take `flat_state_df` (`backtester.py:621-633`).

### 1.3 portfolio_states.csv

- **Writer:** `PortfolioStateTracker.to_csv`, `portfolio_info.py:493-507`. It is called at `backtester.py:696-698` after `tracker.output_dir = str(run_dir)`.
- **Content:** the same state rows as `bars.csv`, flattened the same way, with two differences:
  - no `portfolio_value` column (added only to `state_df` at `backtester.py:430`);
  - not rounded (full precision).
- **Rows:** one per bar, as `bars.csv`. Stop 14 quotes 50 vs 49 columns for run_102.
- **Live readers:**
  - `SR/tools/portfolio_daily.py:66-79` (`postRebalance_total_value`) → profit bars portfolio basis, `run_phase1_research.py:14079-14105`, `:14398`.
  - `SR/tools/portfolio_whole_test.py:242` (`close`).
  - `SR/tools/run_protocol.py:621-645` (full-precision closes for the all-costs fields).
  - `SR/tools/curve_cost_ratio.py:149-169` (not imported by workflow).
  - Tests: 14 SR and 8 TB test files.

### 1.4 trades.json (per window)

- **Writer:**
  - `write_trades_json`, `run_artifact.py:202-209`, called at `backtester.py:607`.
  - It writes `[t.to_dict() for t in performance_tracker.completed_trades]` from memory, with `profitable_absolute` and `profitable_net` coerced to bool.
  - The format is a JSON array with `indent=2`, so one trade spans many lines (`run_artifact.py:209`).
- **One row per what:** one record per **LIFO-matched lot**: one `(entry execution, exit execution, matched_quantity)` triple. It is not one record per position or round trip.
  - Built in `EnhancedPerformanceTracker._process_executed_trades`, `TB/performance/metrics.py:437-570`; `CompletedTrade(...)` at `:520`, appended at `:527`.
  - A position built over several bars and closed in one fill yields several records.
- **Fields** (`CompletedTrade.to_dict`, `metrics.py:284-317`; confirmed in the fixture `run_viewer/.../run_098/.../trades.json`, 52 records):
  `trade_id, symbol, side, entry_price, exit_price, entry_time, exit_time, matched_quantity, duration_minutes, profit_loss_percent, profit_loss_absolute, entry_commission, exit_commission, total_commission, total_commission_percent, net_profit_loss_absolute, net_profit_loss_percent, net_portfolio_profit_loss_percent, initial_portfolio_value, final_portfolio_value, profitable_absolute, profitable_net, entry_forecast, entry_regime, entry_confidence, exit_forecast, exit_regime, exit_confidence, entry_debug_info, exit_debug_info`.
  - `entry_debug_info` / `exit_debug_info` = the signal's `debug_info` at that execution (`metrics.py:363`). In the fixture it contains `{regime, forecast_delta, regime_scores, regime_margin, bars_in_regime, components{<id>{last_history_value, post_pipeline_value, weight_normalized, weighted_contribution}}}`.
- **Live readers:**
  - `SR/tools/run_protocol.py:173-180` (`_load_trades`) → `_compute_trade_records_for_window` `:665-794` → `trade_diagnostics.json` (`:2749-2767`).
  - `SR/tools/window_economics.py:175`, `:314` (`duration_minutes`).
  - `SR/tools/claim_tests.py:1458-1462`.
  - `SR/tools/analyst_queries.py:617`, `:1155-1158`.
  - Run viewer `loaders.py:83-84`, `:1694-1696` (`entry_time, exit_time, side, entry_price, exit_price, net_profit_loss_percent, duration_minutes`).
  - Not imported by any workflow or tool: `fragment_patterns.py:53-56`, `curve_cost_ratio.py:168-173`.
  - Tests: 18 SR and 21 TB test files.

### 1.5 tradesxl.xlsx

- **Writer:**
  - `export_trades_to_excel`, `metrics.py:599-607`, called at `backtester.py:610`:
    1. It calls `save_trades()`, which writes the **shared** log file (`metrics.py:600`, `:590-597`).
    2. It **reads that shared file back** (`:601-602`).
    3. It writes `Sheet1`.
  - `export_metrics_to_excel`, `metrics.py:623-...`, called at `backtester.py:616`, then inserts a `Performance_Metrics` sheet at index 0 (`:632`).
- **Content:**
  - Sheets: `Performance_Metrics`, `Sheet1`.
  - `Sheet1` has one row per lot and the same 30 columns as `trades.json`.
  - `entry_debug_info` and `exit_debug_info` are each one cell holding a stringified dict. I saw this on the older committed artifact, which is not a fixture.
- **Readers:** none in SR or TB code. Its name appears only in TB docs and in `SR/tools/run_viewer/SHAPES_run_099.md`. 0 test files.

### 1.6 metrics.json

- **Writer:** `write_metrics_json`, `run_artifact.py:216-256`, called at `backtester.py:681-688`.
- **Rows:** one object per window run.
- **Top-level blocks:**
  - `core` (`build_core`, return at `run_artifact.py:624-666`, plus `sharpe_annualization` at `:233`). Its keys:
    - Returns and trades: `net_return_pct, sharpe, max_drawdown_pct, trade_count, win_rate, avg_trade_net_pnl, fees_paid, gross_pnl, net_pnl, cost_drag_pct`.
    - Forecast correlation: `forecast_return_corr, forecast_return_corr_pvalue, forecast_return_corr_pvalue_block_adjusted, forecast_return_corr_n_eff, forecast_return_corr_all_bars, forecast_return_corr_all_bars_pvalue_block_adjusted, forecast_return_corr_all_bars_n_eff`, and `forecast_return_corr_all_bars_h<N>` only when horizons are requested (`:47-49`).
    - Gaps and duration: `gap_skipped_pairs, gap_skipped_pct, avg_trade_duration_bars`.
    - Cost checks: `sigma_bar_bps, sigma_bar_bps_is_placeholder, post_backtest_cost_check, post_backtest_route, post_backtest_route_rationale, real_round_trip_cost_bps, real_gross_edge_bps_per_trade, post_backtest_cost_check_real, post_backtest_route_real, post_backtest_route_real_rationale`.
  - `per_regime`: `{regime: {bar_count, avg_forecast, trade_count, total_net_pnl}}` (`:669-687`).
  - `forecast_bins`: per entry-forecast range, `{total_forecasts, profitable_trades, success_rate_pct, total_net_pnl_usd, avg_pnl_per_trade_usd, ...}` (`:690-704`; `TB/performance/forecast_analyzer.py:19-50`).
  - `dynamic`: `{debug_info.components.* column: {regime: {mean, std}}}` (`:707-726`).
  - `regime_validity`: `{regime: {forward_return_mean, forward_return_std, n_bars, informative}}` (`:729-750`).
  - Optional `bar_equity`: `{max_drawdown_pct, sharpe, sortino, exposure_pct, turnover, n_bars_total, n_bars_warmup_excluded, n_daily_returns, n_downside_days, basis}` (`:812-830`). Research passes `bar_equity=True` (`run_protocol.py:2684`).
  - Optional `risk_controls`: `{portfolio_controls, n_cap_clamped_bars, ...stateful_summary}` (`backtester.py:650-664`).
  - Optional `data_quality`: `{gaps_detected, events[]}` (`:667-672`).
  - `component_errors`: `{count, samples}` (`:684-689`).
  - Optional `nan_forecast`: `{policy, bars, bars_by_symbol, samples}` (`backtester.py:56-69`).
- **Live readers:**
  - `SR/tools/run_protocol.py:2616`, `:2689-2691`. It copies `core`, `per_regime`, `regime_validity`, `data_quality`, `nan_forecast` and `component_errors` into `protocol_result.yaml` results, which the grid (`SR/tools/verdict_criteria_evaluator.py:2096`) and profit bars (`run_phase1_research.py:13727-13762`, `:15105`) read.
  - `SR/tools/window_economics.py:202-207` (`bar_equity.turnover`).
  - Tests: 15 SR and 13 TB test files.

### 1.7 forecast_distribution.csv

- **Writer:** `write_forecast_distribution`, `run_artifact.py:271-285`, called at `backtester.py:693`.
- **Rows:** one per (regime, forecast bin); 8 bins per regime.
- **Columns:** `regime, bin, count_final_forecast`. I confirmed this header on the older committed artifact, which is not a fixture.
- **Readers:** none in SR or TB code. 0 test files.

### 1.8 Conditional, off in research

- `forecast_analysis.xlsx` in the run folder is written only when `human_reports` is set (`backtester.py:701-705`). That flag defaults to False (`backtester.py:88`) and the launcher never sets it.
- With `human_reports`, `get_performance_metrics(price_data=...)` can also write `results/strategy_dashboard.html` and `results/trade_snapshots/` (`metrics.py:883`, `:1123`, `:1140`).

### 1.9 Not written by the backtest, but per variant by SR after it

- `trade_diagnostics.json` (`run_protocol.py:2749-2767`): one record per lot, built from `trades.json` + `bars.csv`.
- `protocol_result.yaml`.

Both are listed here because they hold per-trade fields that `trades.json` lacks (§3).

### 1.10 Shared TB/results/trades.json

See §4.

---

## 2. Per-bar detail today (one bars.csv row)

| Element | Status on the bar line | Evidence |
|---|---|---|
| Price / OHLCV | **Present** | `timestamp, open, high, low, close, volume` from the data row (`portfolio_info.py:467`, `:476-480`); fixture columns 1-6 |
| Component raw value | **Present, partial** | `debug_info.components.<id>.last_history_value` = `h[-1]` (`strategy_engine.py:626`). That is the value **after** the component's history transforms (`:421-425`). The pre-transform `comp.raw_value()` is not logged when history transforms exist. For blocks: `b.raw` (`:538`). |
| Transformed / normalised value | **Present** | `...post_pipeline_value` (`strategy_engine.py:622`, `:627`). Only the final value; intermediate pipeline steps are not logged. |
| Weight | **Present** | `...weight_normalized`, `...weighted_contribution` (`strategy_engine.py:623-629`) |
| Combined forecast | **Present** | `forecast` (`StrategyOutput`, `strategy_base.py:26-37`), plus `confidence`, `strategy`, `debug_info.forecast_delta` (`TB/strategies/main_strategy.py:205-210`) |
| Cap | **Absent** | `forecast` is post-clip. The pre-clip ensemble (`strategy_engine.py:624` before `:631`; `strategy_base.py:37`) is not logged and there is no clip flag. The sizing cap at `TB/execution/forecast_manager.py:110-112` has no flag. Only the risk-gate cap logs `risk_cap_clamped` and `risk_target_raw` (gate on). |
| Target position | **Absent** (derivable) | `target_allocation` (`trading_bot.py:457/463`, `:491`, `:501`, `:515`) is not passed to `record_state`. It equals `previous_allocation + allocation_change` (`:517`). The column `sizing_target_allocation` appears only with sizing. |
| Actual position | **Present** | `previous_allocation`, `postRebalance_current_allocation` (`trading_bot.py:440`, `:632`), and quantities `balances.<SYM>.free/locked`, `postRebalance_balances.*` |
| Band decision | **Present, partial** | `approved_rebalance`, `debug_approve_allocation_change.controls.min_allocation_change.passed` (`risk_manager.py:59-61`), `passed_on` with sizing. The threshold value is not on the line (`risk_manager.py:63-66`). All are null when `allocation_change == 0` (`trading_bot.py:644-645`). |
| Fills | **Present, partial** | `debug_execute_portfolio_rebalance.{symbol, price, quantity, trade_type}` and `succcess_execute_portfolio_rebalance`. **One fill per bar only.** On a sign flip, the close leg's debug is overwritten by the open leg (`TB/execution/execution_handler.py:104-116`). |
| Fees | **Absent**; present elsewhere: `trades.json` per lot (`entry_commission`, `exit_commission`) | The commission is applied inside `update_local_balance` (`portfolio_info.py:89-190`, rate at `:105`) and not returned |
| Slippage | **Absent**; present elsewhere: `manifest.json` `config.cost_model` (bps), and fill prices include it | bps resolved per fill (`execution_handler.py:368`, `:383`, `:404`) and not returned in the fill dict |
| Funding | **Absent** (only inside equity) | `apply_funding` returns the cash flow (`portfolio_info.py:204-251`). The caller discards it (`trading_bot.py:425-427`). |
| Equity | **Present** | `total_portfolio_value` (pre-rebalance, `trading_bot.py:429`), `postRebalance_total_value`, `portfolio_value` (`backtester.py:430`) |
| Drawdown | **Absent**; present elsewhere: `metrics.json` `core.max_drawdown_pct`, `bar_equity.max_drawdown_pct` | Per-bar `risk_drawdown` only with the risk gate on (`portfolio_risk_gate.py:312`) |
| Regime / gate states | **Present, partial** | `regime`, `debug_info.regime`, `regime_scores`, `regime_margin`, `bars_in_regime` (`main_strategy.py:208-215`). Risk-gate states when on (`portfolio_risk_gate.py:309-317`). Not logged: the gap tier, and each block's own gate regime (`block.regime`, `strategy_engine.py:473-474`). |
| Warm-up flag | **Absent** (inferable) | No flag column. Prefetch warm-up bars are not written (`trading_bot.py:408-410`). Not-ready bars carry `regime = "NOT_READY"` (`strategy_base.py:376-385`), which readers use as the marker (`run_artifact.py:753-760`; `window_economics.py:36`). |
| Gap flags | **Absent**; present elsewhere: `metrics.json` `data_quality.events` (timestamped) | `gap_detected_this_bar` (`trading_bot.py:356`), tier (`:382`), `gap_forced_flat` (`:513`) and the middle-tier block (`:524-530`) are not recorded per bar |

**Count (18 elements):**
- 10 present: OHLCV, raw, transformed, weight, combined forecast, actual position, band, fills, equity, regime/gate. Of these, 4 are partial: raw, band, fills, regime/gate.
- 8 absent: cap, target, fees, slippage, funding, drawdown, warm-up flag, gap flags. Of these, 4 are present in another file: fees, slippage, drawdown, gap flags.

Also not on the bar line: a per-bar NaN-forecast flag (`trading_bot.py:481`). Only a count and at most 20 samples reach `metrics.json` `nan_forecast`.

---

## 3. Per-trade detail today (one trades.json record = one LIFO lot)

| Element | Status on the trade record | Evidence |
|---|---|---|
| Entry / exit bar | **Present, partial** | `entry_time`, `exit_time` (`metrics.py:292-293`). There is no bar index. `entry_idx`/`exit_idx` exist only in SR `trade_diagnostics.json` (`run_protocol.py:782-783`). |
| Prices | **Present** | `entry_price`, `exit_price`: fill prices, including slippage (`execution_handler.py:369`, `:384`, `:411-413`) |
| Size | **Present** | `matched_quantity` (`metrics.py:294`) |
| Fees | **Present** | `entry_commission`, `exit_commission`, `total_commission`, `total_commission_percent` (`metrics.py:181-212`). These are computed from the rate, not recorded from the fill. |
| Slippage | **Absent**; present elsewhere: `manifest.json` `config.cost_model`; `trade_diagnostics.json` all-costs fields only under `--cost-bar-all-costs` (`run_protocol.py:789-791`) | |
| Holding time | **Present** | `duration_minutes` (`metrics.py:152-154`). Holding bars appear only in `trade_diagnostics.json` (`run_protocol.py:730-732`). |
| PnL gross | **Present** | `profit_loss_percent`, `profit_loss_absolute` (`metrics.py:160-180`) |
| PnL net | **Present** | `net_profit_loss_absolute`, `net_profit_loss_percent`, `net_portfolio_profit_loss_percent` (`metrics.py:214-231`) |
| Forecast at entry and at exit | **Present** | `entry_forecast`, `exit_forecast`, plus regime and confidence (`metrics.py:309-314`) |
| Each component's contribution at entry and at exit | **Present** | `entry_debug_info.components.<id>.{last_history_value, post_pipeline_value, weight_normalized, weighted_contribution}`, and the same under `exit_debug_info` (`metrics.py:315-316`, `:363`). Same caveats as the bar line. Nested, not flat. |
| Exit reason | **Absent**; present elsewhere: SR `trade_diagnostics.json` `exit_reason` (**inferred** after the run: `run_protocol.py:489-536`, `:776`; "the engine does not record exit_reason directly", `:1214-1215`) | |
| Forced end-of-window close flag | **Absent** (inferable) | The forced close passes `signal={}` (`trading_bot.py:733`), so `exit_forecast`, `exit_regime`, `exit_confidence` and `exit_debug_info` are null (`metrics.py:360-363`). In the fixtures, 38 of 272 lots have a null `exit_forecast`. Risk-gate and gap flattens pass the real signal (`trading_bot.py:565-579`), so they are not distinguishable from other exits. |

**Count (12 elements):** 9 present (entry/exit bar is partial), 3 absent (slippage, exit reason, forced-close flag). All 3 absent elements are present or inferred elsewhere.

---

## 4. The shared trades.json

- **Who writes it:**
  - `EnhancedPerformanceTracker` defaults to `log_file='results/trades.json'`, resolved under TB (`metrics.py:322`, `:329`).
  - Research never overrides it: `run_protocol.py` calls `run_backtest` without `trades_log_file` (`:2610`, `:2682-2688`), so `_build_mock_stack` keeps the default (`TB/core/launcher.py:265-276`).
  - Only tests pass `trades_log_file`.
- **When it is written:**
  - every 100 lots (`metrics.py:394-395`);
  - in full at the end, in `export_trades_to_excel` → `save_trades` (`metrics.py:600`, `:590-597`, mode `'w'`).
  - It therefore holds the last backtest's lots only. The path is git-ignored (`.gitignore:33`).
- **Readers in the live path:**
  1. `export_trades_to_excel` reads it back to build `tradesxl.xlsx` `Sheet1` (`metrics.py:601-607`).
  2. `load_trades` at tracker construction (`metrics.py:340-341`, `:610-620`) reads it but only logs a count; it loads nothing. The existence check uses the unresolved relative path (`:340`).
- **No SR reader.** Every post-backtest step reads the **per-window** file: `runs/<run>/variants/<vid>/results/<stamp>_<hash>/trades.json`, written from memory at `backtester.py:607`. The readers are listed in §1.4, and SR paths are built at, for example, `claim_tests.py:540` and `analyst_queries.py:618-619`.
- So the operator's premise holds for the per-window file. The shared file is only an intermediate for `tradesxl.xlsx`, which itself has no reader.

---

## 5. Gap table: operator's wish vs today

| Wish | Today | Where the missing data exists at run time |
|---|---|---|
| A line per bar (bar file) | **Met** by `bars.csv` / `portfolio_states.csv`: one CSV row per traded bar. Warm-up prefetch bars and bars whose body raised are not written. | Warm-up bars: `trading_bot.py:408-410` (strategy updated, then return) |
| A line per trade (trade file) | **Partly met.** `trades.json` has one record per LIFO lot, not per position. It is a JSON array with `indent=2`, so not one line per trade. `tradesxl.xlsx` has one row per lot. | Lots: `metrics.py:520-527`. Executions (fills) with their own ids: `TradeExecution`, `metrics.py:47-60`, built at `:367-379` |
| Component sub-details on the bar line | **Mostly met.** 4 values per component (5 per block). Not logged: the pre-history-transform raw value, intermediate transform steps, the pre-clip ensemble, per-block gate regime. | Raw: `strategy_engine.py:421`, `:463`. History transform: `:424`, `:466`. Pipeline: `TB/strategies/registry.py:354`, called at `strategy_engine.py:622`, `:484`. Pre-clip ensemble: `:624`, `:533`. Block pre-cap: `:484-485`. Block regime: `:473-474` |
| Component sub-details on the trade line | **Met at entry and exit** (nested `entry_debug_info` / `exit_debug_info.components`), with the same gaps as the bar line. Forced closes have none at exit. | Signal at the fill: `execution_handler.py:373`, `:388`, `:419` → `metrics.py:363`. Forced-close call: `trading_bot.py:725-734` |
| Cap on the bar | Absent (§2) | `strategy_engine.py:631`/`:544` (clip ±20), `strategy_base.py:37`, `forecast_manager.py:110-112` |
| Target position on the bar | Absent as a column (§2) | `trading_bot.py:457`, `:463`, `:491`, `:501`, `:515` |
| Every fill on the bar | One fill only (§2) | `execution_handler.py:104-116` (close leg's debug dropped) |
| Fees / slippage / funding per bar | Absent (§2) | Fees `portfolio_info.py:89-190`; slippage `execution_handler.py:368`, `:383`, `:404`; funding `portfolio_info.py:241-251` (returned, discarded at `trading_bot.py:427`) |
| Drawdown, gap flags, warm-up flag per bar | Absent (§2) | Equity `trading_bot.py:429`; gap state `:356`, `:382`, `:513`, `:524-530`; not-ready `strategy_base.py:376` |
| Exit reason, forced close, slippage per trade | Absent in the backtest output; exit reason is inferred later by SR (§3) | The exit path is known in `trading_bot.py`: band path `:588-600`, risk/gap flatten `:561-579`, end close `:697-734`. `record_trade` receives only the signal (`metrics.py:343-363`). |

---

## Not checked

- `SR/docs/DATA_DICTIONARY.md` content against the columns above (§1 bars.csv, §2 trade diagnostics).
- The full `bars.csv` / `portfolio_states.csv` header of a real run_102 window. No run_102 window folder exists locally and the run_102 fixtures carry none. The 50/49 column counts are quoted from stop 14's speech, not verified.
- Whether the `run_viewer` fixtures' rows were trimmed from full windows. They have 123 lines; I did not check whether that is the full window.
- The exact layout of the `Performance_Metrics` sheet (`metrics.py:623-...`) beyond its first tables.
- `TB/results/regime_debug.csv`: no writer found in `.py`; its writer was not traced.
- Whether `debug_info.error` columns appear in real research `bars.csv` (warm-up prefetch may mean no recorded bar is ever not-ready).
- Readers outside `SR/tools`, `SR/workflow` and TB, for example agent skill or prompt text that tells an agent to open these files.
- The engineering scripts `SR/engineering/FOLD-FLOORS-2026-10-19/regrade.py` and `SR/engineering/roadmap/E-027/artifacts/measure_exit_causes.py`, which reference these files but are not in the live path.
- Live (non-mock) execution handler differences for fills and fees.
