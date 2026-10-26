# Data dictionary: what the AI steps read

E-073 step 1 (P-CUL-81, D-081). Every field of the run outputs the analyst and the
other AI steps read: what it means, its unit, the code that computes or writes it
(`KEY:symbol`: a function, `Class.method`, a nested `outer.inner` or a module
constant of the file `KEY` names below), and **when it is known**. Audited against
the engine on 2026-10-08; the discrepancies found are in
[Audit findings](#audit-findings) (not fixed here).
D-198: the sections on the five category reports (6) and the readers' claim digest (8) were
removed with the readers; their numbers stay as headings so the other sections keep theirs.
The `bars.csv` table is parsed by `tools/analyst_queries.py`.

**Analyst:** use this file to know what a field means before you cite it. A number
whose field says `after` or `run` was computed with hindsight: it can describe a
result, never be a signal input. Fields listed under [Not recorded](#not-recorded-today)
do not exist; never infer them.

## How to read it

- **Time.** A bar's `timestamp` is the bar's **start** (`DM:CandleBuilder.get_candle_history`, `DM:CandleBuilder._align`). The
  engine sees the bar when it closes (`DM:CandleBuilder._ingest`), decides on that close and fills
  at that same close plus slippage (`EH:MockExecutionHandler.open_long_position`, `EH:MockExecutionHandler.open_short_position`). A trade's `entry_time`
  / `exit_time` is that decision bar's start timestamp (`EH:MockExecutionHandler.open_long_position`).
- **When known** (last column):
  `close` = known at this bar's close, before its trade (usable for this bar's decision);
  `fill` = this bar's own trade or its result, at the fill price (the close plus
  slippage): known right after the decision, never its input;
  `exit` = known when the trade (one LIFO-matched lot) is closed;
  `after` = uses later bars (hindsight; never a signal input);
  `run` = an aggregate over a window, a variant or the run, known after it;
  `end` = the value at the end of the run, repeated on every row (a defect, A1);
  `meta` = identifier, label or configuration.
- **A "trade"** is one LIFO-matched lot (`PM:EnhancedPerformanceTracker._process_executed_trades`), not one entry-to-flat round
  trip: a partial reduction closes a trade.
- **Units.** `%` = percent (1.0 = one percent); `bps` = basis points; `frac` =
  fraction (0.01 = one percent); `alloc` = position value / portfolio value
  (1.0 = 100% long, -1.0 = 100% short); `forecast` = units on the -20..+20 scale
  (10 = 100% allocation, `FM:FORECAST_FOR_100_INVESTMENT`); `USDT` = quote currency of the simulated
  account (starts at 1000); `bars` = bars of the run's timeframe.
- **Placeholders** in a field path: `<variant>`, `<symbol>`, `<window>`,
  `<regime>`, `<component>` (a component `id` of the config), `<metric>`,
  `<asset>` (`USDT` or the traded symbol), `<criterion>`, `<era>`, `<test>`,
  `<h>` (a horizon, in bars), `<slice>` (`overall`/`per_window`/`per_regime`/`per_symbol`),
  `<trade field>` (a numeric field of a trade record), `<reserved feed>`.

### Source files

<!-- data-dictionary-sources -->
| Key | File |
|---|---|
| `TB` | `trading-bot/core/trading_bot.py` |
| `BT` | `trading-bot/core/backtester.py` |
| `PI` | `trading-bot/execution/portfolio_info.py` |
| `EH` | `trading-bot/execution/execution_handler.py` |
| `FM` | `trading-bot/execution/forecast_manager.py` |
| `RM` | `trading-bot/risk/risk_manager.py` |
| `RG` | `trading-bot/risk/portfolio_risk_gate.py` |
| `SB` | `trading-bot/strategies/strategy_base.py` |
| `MS` | `trading-bot/strategies/main_strategy.py` |
| `SE` | `trading-bot/strategies/strategy_engine.py` |
| `RE` | `trading-bot/strategies/regime_engine.py` |
| `DM` | `trading-bot/data/data_manager.py` |
| `FR` | `trading-bot/data/feed_registry.py` |
| `RA` | `trading-bot/reporting/run_artifact.py` |
| `PM` | `trading-bot/performance/metrics.py` |
| `SS` | `trading-bot/performance/signal_statistics.py` |
| `RP` | `strategy-research/tools/run_protocol.py` |
| `CH` | `strategy-research/tools/cost_helpers.py` |
| `BR` | `strategy-research/tools/build_reports.py` (deleted in D-198; only the audit findings below cite it) |
| `VE` | `strategy-research/tools/verdict_criteria_evaluator.py` |
| `RF` | `strategy-research/tools/reader_findings.py` |
| `CF` | `strategy-research/tools/claim_findings.py` |
| `CM` | `strategy-research/tools/claim_measure.py` |
| `CT` | `strategy-research/tools/claim_tests.py` |
| `NB` | `strategy-research/tools/nearest_build.py` |
| `P1` | `strategy-research/workflow/run_phase1_research.py` |
<!-- /data-dictionary-sources -->

## 1. bars.csv (one per window and variant)

`variants/<variant>/results/<window run id>/bars.csv`: one row per traded bar of
the window (warm-up bars are not written, `TB:TradingBot._process_symbol_candle_completion`). Built from every
`record_state` row (`TB:TradingBot._process_symbol_candle_completion`, `PI:PortfolioStateTracker.record_state`), nested dicts flattened to dotted columns
(`PI:flatten_dict_columns`, `BT:BacktestEngine._end_of_backtest`), rounded to 6 decimals (`RA:write_bars_csv`). Columns appear only when
the run produces them (a feed column only with that feed; `risk_*` only with the
portfolio risk gate, which `run_protocol` never passes).

<!-- data-dictionary: bars.csv -->
| Field | Meaning | Unit | Code | When known |
|---|---|---|---|---|
| `timestamp` | Bar start time (UTC, naive). | time | `DM:CandleBuilder.get_candle_history` | close |
| `open` | First price of the bar. | price | `DM:CandleBuilder.get_candle_history` | close |
| `high` | Highest price of the bar. | price | `DM:CandleBuilder.get_candle_history` | close |
| `low` | Lowest price of the bar. | price | `DM:CandleBuilder.get_candle_history` | close |
| `close` | Last price of the bar; the decision and fill price. | price | `DM:CandleBuilder.get_candle_history` | close |
| `volume` | Traded volume of the bar. | base units | `DM:CandleBuilder.get_candle_history` | close |
| `fear_greed` | Fear and Greed index, latest value published at least 1 day before the bar start (as-of merge, publication delay 86400 s). Present only when the strategy reads this feed (D-146). | index 0-100 | `FR:FEED_REGISTRY`, `DM:_merge_asof_with_causality_guard` | close |
| `funding_rate` | Latest perpetual funding rate settled at or before the bar start (carried forward). Present only when the strategy reads this feed (D-146). | frac per settlement | `FR:FEED_REGISTRY`, `DM:_merge_asof_with_causality_guard` | close |
| `<reserved feed>` | A reserved feed's column (whale-footprint features), only when a caller registers it. | feed | `FR:RESERVED_FEED_REGISTRY` | close |
| `forecast` | The strategy's final forecast for the bar, clipped to -20..+20; 0.0 while not ready or on an error. Always the unsized signal: a `strategies.sizing` block (D-176) sizes the allocation, never this column. | forecast | `SE:ConfigDrivenStrategyEngine.forecast`, `SB:StrategyOutput`, `SB:MainStrategy.generate_signals` | close |
| `confidence` | Always 0.0 (A2). | 0-1 | `SB:StrategyOutput`, `MS:AdvancedStrategy.generate_forecast` | meta |
| `regime` | Regime label used this bar (`trending`, `mean_reversion`, `chop`, `unknown`), or `NOT_READY` / `ERROR`. | label | `RE:ConfigDrivenRegimeEngine.classify`, `SB:MainStrategy.generate_signals` | close |
| `strategy` | Always empty (A2). | label | `SB:StrategyOutput`, `MS:AdvancedStrategy.generate_forecast` | meta |
| `debug_info.regime` | Same as `regime` on a ready bar. | label | `MS:AdvancedStrategy.generate_forecast` | close |
| `debug_info.forecast_delta` | This bar's forecast minus the previous ready bar's forecast. | forecast | `MS:AdvancedStrategy.generate_forecast` | close |
| `debug_info.regime_scores` | Present instead of the per-regime columns when no bar had scores (threshold_rules mode): the text `{}`. | text | `MS:AdvancedStrategy.generate_forecast` | close |
| `debug_info.regime_scores.<regime>` | Weighted regime score (score / score_product modes only). | score | `MS:AdvancedStrategy.generate_forecast`, `RE:ConfigDrivenRegimeEngine._classify_score`, `RE:ConfigDrivenRegimeEngine._classify_score_product` | close |
| `debug_info.regime_margin` | Best score minus second best (score modes only; empty in threshold_rules). | score | `MS:AdvancedStrategy.generate_forecast`, `RE:ConfigDrivenRegimeEngine._classify_score`, `RE:ConfigDrivenRegimeEngine._classify_score_product` | close |
| `debug_info.bars_in_regime` | Consecutive bars in the current regime, this bar included. | bars | `RE:ConfigDrivenRegimeEngine._tick` | close |
| `debug_info.components` | Present instead of the per-component columns when no bar had component values: the text `{}`. | text | `MS:AdvancedStrategy.generate_forecast` | close |
| `debug_info.components.<component>.last_history_value` | The component's latest raw output (before its transform pipeline). | component | `SE:ConfigDrivenStrategyEngine.forecast`, `SE:ConfigDrivenStrategyEngine._forecast_blocks` | close |
| `debug_info.components.<component>.post_pipeline_value` | The component's value after its transform pipeline. | forecast | `SE:ConfigDrivenStrategyEngine.forecast`, `SE:ConfigDrivenStrategyEngine._forecast_blocks` | close |
| `debug_info.components.<component>.weight_normalized` | Its weight / sum of the regime's weights. | frac | `SE:ConfigDrivenStrategyEngine.forecast`, `SE:ConfigDrivenStrategyEngine._forecast_blocks` | meta |
| `debug_info.components.<component>.weighted_contribution` | weight_normalized x post_pipeline_value; the sum over components (clipped) is the forecast. | forecast | `SE:ConfigDrivenStrategyEngine.forecast`, `SE:ConfigDrivenStrategyEngine._forecast_blocks` | close |
| `debug_info.components.<component>.active` | Block combiner only: 1.0 when the block is active this bar. | 0/1 | `SE:ConfigDrivenStrategyEngine._forecast_blocks` | close |
| `debug_info.components.not_ready_component` | Id of the first component without 2 values of history; the forecast is then 0.0. | id | `SE:ConfigDrivenStrategyEngine.forecast` | close |
| `debug_info.components.not_ready_block` | Same for a block of the block combiner. | id | `SE:ConfigDrivenStrategyEngine._forecast_blocks` | close |
| `debug_info.error` | Why the strategy gave 0.0: `Strategy not ready` (warm-up) or the exception text. | text | `SB:MainStrategy.generate_signals` | close |
| `total_portfolio_value` | Account value at this close, before this bar's trade (cash minus borrowed plus position x close; funding accrued first when modelled). | USDT | `TB:TradingBot._process_symbol_candle_completion`, `PI:CommonPortfolioDef._calculate_total_portfolio_value` | close |
| `portfolio_value` | Copy of `total_portfolio_value`. | USDT | `BT:BacktestEngine._end_of_backtest` | close |
| `previous_allocation` | Position value / account value at this close, before the trade. Sized when a `strategies.sizing` block is present (it is the position the sizing built). | alloc | `TB:TradingBot._process_symbol_candle_completion`, `PI:CommonPortfolioDef._calculate_actual_allocation` | close |
| `allocation_change` | Target allocation (forecast / 10, or the held allocation on a NaN forecast, 0 under a forced flatten) minus `previous_allocation`; set to 0 when a gap middle tier blocks a new entry. The target itself is not recorded, except with a `strategies.sizing` block (D-176), where `allocation_change` is the SIZED target minus `previous_allocation` and the target is `sizing_target_allocation`. | alloc | `TB:TradingBot._process_symbol_candle_completion`, `FM:ForecastManager.forecast_to_allocation` | close |
| `approved_rebalance` | Risk manager's answer when `allocation_change` is non-zero (empty otherwise, and on a forced flatten). | bool | `TB:TradingBot._process_symbol_candle_completion` | fill |
| `succcess_execute_portfolio_rebalance` | The order succeeded (empty when no order was attempted). Name misspelled in code (A3). | bool | `TB:TradingBot._process_symbol_candle_completion`, `TB:TradingBot._close_all_positions_at_end` | fill |
| `postRebalance_total_value` | Account value after this bar's trade and its commission, at this close. | USDT | `TB:TradingBot._process_symbol_candle_completion` | fill |
| `postRebalance_current_allocation` | Allocation after this bar's trade. Sized when a `strategies.sizing` block is present. | alloc | `TB:TradingBot._process_symbol_candle_completion` | fill |
| `balances.<asset>.free` | Should be the asset held before the trade; is the END-of-run balance on every row (A1). | asset units | `PI:_default_balance`, `TB:TradingBot._process_symbol_candle_completion`, `PI:CommonPortfolioDef.get_account_balance` | end |
| `balances.<asset>.locked` | Should be the asset borrowed (short or margin) before the trade; END-of-run value (A1). | asset units | `PI:_default_balance`, `TB:TradingBot._process_symbol_candle_completion`, `PI:CommonPortfolioDef.get_account_balance` | end |
| `postRebalance_balances.<asset>.free` | Should be the asset held after the trade; END-of-run value (A1). | asset units | `PI:_default_balance`, `TB:TradingBot._process_symbol_candle_completion` | end |
| `postRebalance_balances.<asset>.locked` | Should be the asset borrowed after the trade; END-of-run value (A1). | asset units | `PI:_default_balance`, `TB:TradingBot._process_symbol_candle_completion` | end |
| `debug_approve_allocation_change` | Present instead of the dotted columns when no bar asked the risk manager: the text `{}`. | text | `TB:TradingBot._process_symbol_candle_completion` | fill |
| `debug_approve_allocation_change.symbol` | Symbol checked by the risk manager. | id | `RM:RiskManager.approve_allocation_change` | fill |
| `debug_approve_allocation_change.time` | Bar timestamp checked. | time | `RM:RiskManager.approve_allocation_change` | fill |
| `debug_approve_allocation_change.controls.min_allocation_change.passed` | abs(change) >= threshold (default 0.20): the no-trade band. With a `strategies.sizing` block (D-176) the band passes when either `sizing_signal_change` or `allocation_change` reaches the threshold (the debug entry then also records `passed_on`: signal, sized or both). | bool | `RM:RiskManager.approve_allocation_change`, `RM:RiskManager._ctrl_min_allocation_change` | fill |
| `debug_approve_allocation_change.controls.min_allocation_change.passed_on` | `strategies.sizing` block only (D-176): which change reached the band: `signal` (`sizing_signal_change`), `sized` (`allocation_change`) or `both`; empty when the band refused. | text | `RM:RiskManager.approve_allocation_change` | fill |
| `debug_execute_portfolio_rebalance` | Present instead of the dotted columns when no order ran: the text `{}`. | text | `TB:TradingBot._process_symbol_candle_completion` | fill |
| `debug_execute_portfolio_rebalance.symbol` | Symbol of the order. | id | `EH:MockExecutionHandler.open_long_position` | fill |
| `debug_execute_portfolio_rebalance.price` | Fill price: close x (1 +/- slippage bps / 10000). | price | `EH:MockExecutionHandler.open_long_position`, `EH:MockExecutionHandler.open_short_position`, `EH:MockExecutionHandler.close_position` | fill |
| `debug_execute_portfolio_rebalance.quantity` | Order size: positive for LONG/SHORT/REDUCE_*, the signed position for CLOSE (A13). | base units | `EH:MockExecutionHandler.open_long_position`, `EH:MockExecutionHandler.open_short_position`, `EH:MockExecutionHandler.close_position` | fill |
| `debug_execute_portfolio_rebalance.trade_type` | `LONG`, `SHORT`, `REDUCE_LONG`, `REDUCE_SHORT` or `CLOSE`. | label | `EH:BaseExecutionHandler._handle_allocation_change` | fill |
| `debug_execute_portfolio_rebalance.error` | Exception text of a failed order. | text | `EH:MockExecutionHandler.open_long_position`, `EH:MockExecutionHandler.open_short_position` | fill |
| `risk_target_raw` | Risk gate only: the target before the gate (NaN on a NaN forecast). With a `strategies.sizing` block it is the SIZED target (the gate sees what sizing produced). | alloc | `RG:PortfolioRiskGate.apply`, `TB:TradingBot._process_symbol_candle_completion` | close |
| `risk_cap_clamped` | Risk gate only: the cap clamped the target. | bool | `RG:PortfolioRiskGate.apply` | close |
| `risk_killed` | Risk gate only: drawdown kill latched. | bool | `RG:PortfolioRiskGate.apply` | close |
| `risk_drawdown` | Risk gate only: drawdown at this close. | frac | `RG:PortfolioRiskGate.apply` | close |
| `risk_daily_halted` | Risk gate only: daily loss halt latched. | bool | `RG:PortfolioRiskGate.apply` | close |
| `risk_daily_loss` | Risk gate only: loss since the day's anchor. | frac | `RG:PortfolioRiskGate.apply` | close |
| `risk_trip` | Risk gate only: what tripped this bar. | label | `RG:PortfolioRiskGate.apply` | close |
| `sizing_realised_vol` | `strategies.sizing` block only (D-176): the annualised realised volatility the bar was sized with (stdev of the last `window` simple close returns x sqrt(`periods_per_year`)); empty when the closes could not give one (warm-up, a bad close, zero vol: the bar is sized to 0.0). | frac | `TB:TradingBot._process_symbol_candle_completion`, `FM:ForecastManager.forecast_to_allocation` | close |
| `sizing_target_allocation` | `strategies.sizing` block only (D-176): the sized target allocation, clipped to +/- `max_allocation` (what `allocation_change` is measured towards). Campaign default block (D-176): kind `vol_target`, window 60 bars, `periods_per_year` 365 for daily bars and 8760 for hourly bars, `target_annual_vol` 0.2, `max_allocation` 2; unmeasurable volatility: flat, remembered (held) signal 0.0; the sizing window does not follow D-166; it changes only by an operator D-row. | alloc | `TB:TradingBot._process_symbol_candle_completion`, `FM:ForecastManager.forecast_to_allocation` | close |
| `sizing_signal_change` | `strategies.sizing` block only (D-176): the change in the unsized signal (forecast / 10) since the position was last set, which is one of the two changes the min_allocation_change band accepts (the other is `allocation_change`). Empty on a NaN-forecast bar. | alloc | `TB:TradingBot._process_symbol_candle_completion`, `RM:RiskManager.approve_allocation_change` | close |
<!-- /data-dictionary -->

## 2. trade_diagnostics.json (one per variant)

`variants/<variant>/trade_diagnostics.json`, written by `run_protocol` (`RP:main`)
from each window's `trades.json` and `bars.csv`. Trades from all windows, in order.
`summary` is also copied as `protocol_result.yaml` `trade_diagnostics_summary`.

Per-trade labels: in `trade_diagnostics.json` only.

<!-- data-dictionary: trade_diagnostics.json -->
| Field | Meaning | Unit | Code | When known |
|---|---|---|---|---|
| `trades[].trade_id` | Engine trade id. | id | `RP:_compute_trade_records_for_window` | meta |
| `trades[].symbol` | Symbol. | id | `RP:_compute_trade_records_for_window` | meta |
| `trades[].window` | Protocol window label. | label | `RP:_compute_trade_records_for_window` | meta |
| `trades[].regime_at_entry` | Regime label at the entry bar. | label | `RP:_compute_trade_records_for_window` | close |
| `trades[].direction` | `long` or `short`. | label | `RP:_compute_trade_records_for_window` | fill |
| `trades[].entry_time` | Entry bar start timestamp (fill at that bar's close). | time | `RP:_compute_trade_records_for_window`, `EH:MockExecutionHandler.open_long_position` | close |
| `trades[].exit_time` | Exit bar start timestamp. | time | `RP:_compute_trade_records_for_window` | exit |
| `trades[].profitable_net` | Position return net of both commissions > 0. | bool | `RP:_compute_trade_records_for_window`, `PM:CompletedTrade.profitable_net` | exit |
| `trades[].exit_reason` | `end_of_window` when the exit is the window's last bar, else `signal_flip` by default (A5). | label | `RP:_compute_trade_records_for_window`, `RP:_infer_exit_reason` | exit |
| `trades[].entered_earlier_better` | Previous bar's close was a better price than the fill. | bool | `RP:_compute_trade_records_for_window`, `RP:_compute_entered_earlier_better` | fill |
| `trades[].held_longer_better` | Next bar's close was a better exit than the fill. | bool | `RP:_compute_trade_records_for_window`, `RP:_compute_held_longer_better` | after |
<!-- /data-dictionary -->

Trade-level claim tests (E-075 PR-3, gated; `tools/claim_tests.py`, guide
`workflow_artifacts/skills/hypothesis-design/CLAIM_TESTS_TRADE.md`) do not read the labels
above. They read each window's `trades.json` and `bars.csv` and derive their own fields: the
entry-time fields `side`, `entry_hour`, `entry_weekday` (UTC, from `entry_time`),
`regime_at_entry` (`entry_regime`) and `entry_forecast` (the entry bar's `forecast`, known at
that close), and the exit-time `holding_bars` and `exit_cause`. `exit_cause` is the interim
classifier of E-074 phase A 4.2, from the lot's `exit_forecast` and the exit row's
`postRebalance_current_allocation`; it is `end_of_window` only when the exit bar is the
window's last bar (not its last calendar day, finding A5), and it does not change
`exit_reason`. Outcomes: `trade_net_return` (the all-costs basis, `gross_return_before_costs`
minus `cost_paid_all`, when `trade_diagnostics.json` carries them for every lot of the window;
else `net_profit_loss_percent` of `trades.json`, after the commission with the slippage already
in the fill prices; the basis used is recorded per window and windows on different bases are
not pooled) and `post_exit_return` (exit bar's close to the close h bars later, signed by side;
lots closing on one bar on one side are one event). MAE and MFE are not used (A6).

Per-trade numbers and the summary.

<!-- data-dictionary: trade_diagnostics.json -->
| Field | Meaning | Unit | Code | When known |
|---|---|---|---|---|
| `trades[]` | One record per trade (LIFO lot). | list | `RP:main`, `RP:_compute_trade_records_for_window` | exit |
| `trades[].holding_bars` | exit_idx - entry_idx, at least 1. | bars | `RP:_compute_trade_records_for_window` | exit |
| `trades[].realized_return` | Position return before commission: exit/entry - 1 (sign by side). Slippage is inside the prices. Not weighted by size. | % | `RP:_compute_trade_records_for_window`, `PM:CompletedTrade.profit_loss_percent` | exit |
| `trades[].net_portfolio_return_pct` | Net PnL of the lot / account value at entry. | % | `RP:_compute_trade_records_for_window`, `PM:CompletedTrade.net_portfolio_profit_loss_percent` | exit |
| `trades[].mae` | Largest adverse move from entry over the entry..exit bars (highs/lows), entry bar included (A6). | % | `RP:_compute_trade_records_for_window`, `RP:_compute_mae_mfe` | after |
| `trades[].mfe` | Largest favourable move, same bars (A6). | % | `RP:_compute_trade_records_for_window`, `RP:_compute_mae_mfe` | after |
| `trades[].entry_efficiency` | Return from the actual entry minus return if entered at the next bar's open. Measures the entry slippage (A4). | % | `RP:_compute_trade_records_for_window`, `RP:_compute_entry_efficiency` | after |
| `trades[].exit_efficiency` | Realized return / best return available over the holding bars (hindsight optimum; A6). | ratio | `RP:_compute_trade_records_for_window`, `RP:_compute_exit_efficiency` | after |
| `trades[].post_exit_return_5bars` | Close 5 bars after exit vs exit price, signed by side. | % | `RP:_compute_trade_records_for_window`, `RP:_compute_post_exit_returns` | after |
| `trades[].post_exit_return_20bars` | Same, 20 bars. | % | `RP:_compute_trade_records_for_window`, `RP:_compute_post_exit_returns` | after |
| `trades[].cost_paid` | Configured one-way fee x 2 (A7): not the trade's actual cost. | bps | `RP:_compute_trade_records_for_window`, `RP:_cost_paid_bps` | meta |
| `trades[].gross_return_before_costs` | Only under `orchestrator.cost_bar_all_costs` (A7 fix): the return at the bar closes the two fills were priced from, before fees and slippage (sign by side; null when a leg's bar is not found). | % | `RP:_compute_trade_records_for_window`, `RP:_all_costs_fields` | exit |
| `trades[].slippage_paid` | Only under the same flag: slippage of both legs, each the fill's adverse move from its bar close (signed). | bps | `RP:_compute_trade_records_for_window`, `RP:_all_costs_fields` | exit |
| `trades[].cost_paid_all` | Only under the same flag: cost_paid + slippage_paid, fees and slippage of both legs. | bps | `RP:_compute_trade_records_for_window`, `RP:_all_costs_fields` | exit |
| `trades[].entry_price` | Fill price at entry (slippage included). | price | `RP:_compute_trade_records_for_window` | fill |
| `trades[].exit_price` | Fill price at exit (slippage included). | price | `RP:_compute_trade_records_for_window` | exit |
| `trades[].entry_idx` | Entry row in this window's bars.csv (-1 when not found). Window-local. | row | `RP:_compute_trade_records_for_window` | meta |
| `trades[].exit_idx` | Exit row in this window's bars.csv. Window-local. | row | `RP:_compute_trade_records_for_window` | meta |
| `trades[].pre_entry_drift_pct` | Move of the 6 bars before entry into the entry price, signed by side. | % | `RP:_compute_trade_records_for_window`, `RP:_compute_pre_entry_drift` | fill |
| `trades[].post_exit_drift_pct` | Move of the 6 bars after exit, signed by side. | % | `RP:_compute_trade_records_for_window`, `RP:_compute_post_exit_drift` | after |
| `summary` | Aggregates over all trades of the variant (empty without trades). | map | `RP:main`, `RP:_aggregate_trade_diagnostics` | run |
| `summary.mae_mfe_ratio_median` | Median of mae/mfe over trades with mfe > 0. | ratio | `RP:_aggregate_trade_diagnostics` | run |
| `summary.entry_efficiency_median` | Median entry_efficiency. | % | `RP:_aggregate_trade_diagnostics` | run |
| `summary.exit_efficiency_median` | Median exit_efficiency. | ratio | `RP:_aggregate_trade_diagnostics` | run |
| `summary.win_rate_net` | Share of trades with profitable_net. | % | `RP:_aggregate_trade_diagnostics` | run |
| `summary.holding_period_distribution` | Holding bars percentiles (floor nearest rank). | map | `RP:_aggregate_trade_diagnostics`, `RP:_aggregate_trade_diagnostics._pct_val` | run |
| `summary.holding_period_distribution.p10_bars` | 10th percentile. | bars | `RP:_aggregate_trade_diagnostics` | run |
| `summary.holding_period_distribution.p50_bars` | Median. | bars | `RP:_aggregate_trade_diagnostics` | run |
| `summary.holding_period_distribution.p90_bars` | 90th percentile. | bars | `RP:_aggregate_trade_diagnostics` | run |
| `summary.pnl_concentration` | How much of the summed net return comes from the extremes. | map | `RP:_aggregate_trade_diagnostics` | run |
| `summary.pnl_concentration.pct_pnl_from_top_decile_trades` | Sum of the best 10% of net_portfolio_return_pct / sum of all, x100 (null when the sum is 0). | % | `RP:_aggregate_trade_diagnostics` | run |
| `summary.pnl_concentration.pct_pnl_from_worst_decile_trades` | Same for the worst 10% (sign follows the total). | % | `RP:_aggregate_trade_diagnostics` | run |
| `summary.exit_reason_breakdown` | Share of trades per exit_reason (A5). | map | `RP:_aggregate_trade_diagnostics` | run |
| `summary.exit_reason_breakdown.signal_flip_pct` | Share labelled signal_flip. | % | `RP:_aggregate_trade_diagnostics` | run |
| `summary.exit_reason_breakdown.stop_loss_pct` | Always 0: nothing produces stop_loss (A5). | % | `RP:_aggregate_trade_diagnostics` | run |
| `summary.exit_reason_breakdown.time_stop_pct` | Always 0 (A5). | % | `RP:_aggregate_trade_diagnostics` | run |
| `summary.exit_reason_breakdown.end_of_window_pct` | Share ending on the window's last bar. | % | `RP:_aggregate_trade_diagnostics` | run |
| `summary.exit_reason_breakdown.inferred_classification_pct` | Share labelled by inference (= signal_flip_pct). | % | `RP:_aggregate_trade_diagnostics` | run |
| `summary.stop_loss_recovery_rate` | Always 0 (A5). | frac | `RP:_aggregate_trade_diagnostics` | run |
| `summary.per_trade_expectancy_bps` | Net portfolio return per trade. | map | `RP:_aggregate_trade_diagnostics` | run |
| `summary.per_trade_expectancy_bps.mean` | Mean of net_portfolio_return_pct x 100. | bps | `RP:_aggregate_trade_diagnostics` | run |
| `summary.per_trade_expectancy_bps.se` | Standard error of that mean. | bps | `RP:_aggregate_trade_diagnostics` | run |
| `summary.per_trade_expectancy_bps.t_stat` | mean / se (trades treated as independent). | t | `RP:_aggregate_trade_diagnostics` | run |
| `summary.per_trade_expectancy_bps.n` | Number of trades. | count | `RP:_aggregate_trade_diagnostics` | run |
| `summary.zero_trade_slot_pct` | Share of windows with no trade. | % | `RP:_aggregate_trade_diagnostics` | run |
| `summary.fee_reduction_metrics` | Four what-if levers on trading less (E-016). | map | `RP:_aggregate_trade_diagnostics`, `RP:_aggregate_fee_reduction_diagnostics` | run |
| `summary.fee_reduction_metrics.lookback_bars` | N used by the levers (6). | bars | `RP:_aggregate_fee_reduction_diagnostics`, `RP:_FEE_REDUCTION_LOOKAHEAD_BARS` | meta |
| `summary.fee_reduction_metrics.combine_nearby_trades` | Same-direction re-entries. | map | `RP:_aggregate_fee_reduction_diagnostics` | run |
| `summary.fee_reduction_metrics.combine_nearby_trades.same_direction_reentry_rate` | Share of consecutive trade pairs re-entering the same direction within 6 bars of the previous exit. | frac | `RP:_aggregate_fee_reduction_diagnostics` | run |
| `summary.fee_reduction_metrics.combine_nearby_trades.avg_reentry_gap_bars` | Mean gap of those re-entries. | bars | `RP:_aggregate_fee_reduction_diagnostics` | run |
| `summary.fee_reduction_metrics.exit_later` | Holding longer. | map | `RP:_aggregate_fee_reduction_diagnostics` | after |
| `summary.fee_reduction_metrics.exit_later.avg_post_exit_drift_pct` | Mean post_exit_drift_pct. | % | `RP:_aggregate_fee_reduction_diagnostics` | after |
| `summary.fee_reduction_metrics.exit_later.pct_better_exit_1bar_later` | Share with held_longer_better. | % | `RP:_aggregate_fee_reduction_diagnostics` | after |
| `summary.fee_reduction_metrics.enter_earlier` | Entering earlier. | map | `RP:_aggregate_fee_reduction_diagnostics` | run |
| `summary.fee_reduction_metrics.enter_earlier.avg_pre_entry_drift_pct` | Mean pre_entry_drift_pct. | % | `RP:_aggregate_fee_reduction_diagnostics` | run |
| `summary.fee_reduction_metrics.enter_earlier.pct_better_entry_1bar_earlier` | Share with entered_earlier_better. | % | `RP:_aggregate_fee_reduction_diagnostics` | run |
| `summary.fee_reduction_metrics.trade_less_often` | Whipsaw. | map | `RP:_aggregate_fee_reduction_diagnostics` | run |
| `summary.fee_reduction_metrics.trade_less_often.boundary_recross_rate` | Mean over windows of the share of forecast crossings of the boundary level repeated within 6 bars. | frac | `RP:_compute_window_fee_reduction_diagnostics`, `RP:_aggregate_fee_reduction_diagnostics` | run |
| `summary.fee_reduction_metrics.trade_less_often.frequency_vs_volatility_ratio` | Mean over windows of trades per day / stdev of bar returns. | ratio | `RP:_compute_window_fee_reduction_diagnostics`, `RP:_aggregate_fee_reduction_diagnostics` | run |
| `summary.realized_edge_to_cost_ratio` | Mean realized_return (bps) / mean cost_paid over trades with a cost (A7). | ratio | `RP:_aggregate_trade_diagnostics`, `CH:realized_edge_to_cost_ratio_unrounded` | run |
| `summary.realized_edge_to_cost_ratio_all_costs` | Only under `orchestrator.cost_bar_all_costs`: mean gross_return_before_costs (bps) / mean cost_paid_all, the D-038 ratio the menu criterion reads under the flag (A7 fix). Null when any trade lacks either field (never a ratio over a subset). | ratio | `RP:_aggregate_trade_diagnostics`, `CH:edge_to_all_costs_ratio_unrounded` | run |
| `summary.realized_edge_to_cost_ratio_all_costs_missing_trades` | Only under the same flag: how many trade records lack gross_return_before_costs or cost_paid_all (any > 0 makes the ratio above null). | count | `RP:_aggregate_trade_diagnostics` | run |
| `summary.cost_components_measured` | Which costs are itemised in the trade records. | map | `RP:_aggregate_trade_diagnostics`, `RP:_compute_cost_basis` | meta |
| `summary.cost_components_measured.fees` | Every record carries cost_paid. | bool | `RP:_compute_cost_basis` | meta |
| `summary.cost_components_measured.funding` | Always false: trade records carry no funding (and run_protocol does not model funding). | bool | `RP:_compute_cost_basis` | meta |
| `summary.cost_components_measured.slippage` | Always false: slippage is inside the fill prices. | bool | `RP:_compute_cost_basis` | meta |
<!-- /data-dictionary -->

## 3. The window `core` block

`metrics.json` `core` of each window, copied into `protocol_result.yaml`
`results[].core` and the reports (`per_window[].core`). Trade-based fields use the
trade-exit basis (A9). `run_protocol` sets `sharpe` to null when the window has
fewer than 5 trades (`RP:main`).

<!-- data-dictionary: core -->
| Field | Meaning | Unit | Code | When known |
|---|---|---|---|---|
| `net_return_pct` | First trade's entry account value to last trade's exit account value; 0.0 without trades (A8). | % | `PM:EnhancedPerformanceTracker._calculate_standard_metrics`, `RA:build_core` | run |
| `sharpe` | Annualised (sqrt 365) Sharpe of daily summed trade returns booked on exit dates, first to last exit; 0.0 when undefined (A8, A9). | ratio | `PM:EnhancedPerformanceTracker.calculate_sharpe_ratio`, `RA:build_core` | run |
| `max_drawdown_pct` | Drawdown of the trade-by-trade compounded curve (exit order); 0.0 without trades. | % | `PM:EnhancedPerformanceTracker.calculate_max_drawdown`, `RA:build_core` | run |
| `trade_count` | Number of trades (LIFO lots). | count | `RA:build_core` | run |
| `win_rate` | Share of trades with profitable_net; 0.0 without trades. | % | `PM:EnhancedPerformanceTracker._calculate_standard_metrics`, `RA:build_core` | run |
| `avg_trade_net_pnl` | Mean net PnL per trade. | USDT | `RA:build_core` | run |
| `fees_paid` | Sum of commissions. | USDT | `RA:build_core` | run |
| `gross_pnl` | Sum of PnL before commission (after slippage). | USDT | `RA:build_core` | run |
| `net_pnl` | Sum of PnL after commission. | USDT | `RA:build_core` | run |
| `cost_drag_pct` | (gross - net) / abs(gross) x 100. | % | `RA:build_core` | run |
| `forecast_return_corr` | Pearson correlation of forecast[t] with close[t+1]/close[t]-1 on bars with forecast != 0, gap-spanning pairs dropped. | corr | `RA:build_core` | after |
| `forecast_return_corr_pvalue` | t-test p-value of that correlation (independent bars). | p | `RA:build_core` | after |
| `forecast_return_corr_pvalue_block_adjusted` | Same, with daily blocks (fewer effective observations). | p | `RA:build_core` | after |
| `forecast_return_corr_n_eff` | Effective sample size used by that p-value. | count | `RA:build_core` | after |
| `forecast_return_corr_all_bars` | Same correlation on all bars (forecast 0 included). | corr | `RA:build_core` | after |
| `forecast_return_corr_all_bars_pvalue_block_adjusted` | Its block-adjusted p-value. | p | `RA:build_core` | after |
| `forecast_return_corr_all_bars_n_eff` | Its effective sample size. | count | `RA:build_core` | after |
| `gap_skipped_pairs` | Bar pairs dropped because the next row is not the next bar. | count | `RA:build_core` | run |
| `gap_skipped_pct` | Those pairs / pairs reached. | % | `RA:build_core` | run |
| `avg_trade_duration_bars` | Mean trade duration / median bar spacing. | bars | `RA:build_core` | run |
| `sigma_bar_bps` | Stdev of next-bar returns over all bars. | bps | `RA:build_core`, `SS:sigma_bar_bps_from_returns` | after |
| `sigma_bar_bps_is_placeholder` | sigma could not be measured and a default was used. | bool | `RA:build_core`, `SS:sigma_bar_bps_from_returns` | meta |
| `post_backtest_cost_check` | Estimated edge vs cost from IC x sigma x sqrt(holding) (prescreen formula). | map | `RA:build_core`, `SS:cost_check` | run |
| `post_backtest_cost_check.estimated_gross_edge_bps_per_trade` | Estimated gross edge per trade (IC x sigma x sqrt(holding)). | bps | `SS:cost_check` | run |
| `post_backtest_cost_check.cost_bps_per_trade` | Round-trip cost per trade from the cost model. | bps | `SS:cost_check` | run |
| `post_backtest_cost_check.edge_to_cost_ratio` | abs(edge) / cost. | ratio | `SS:cost_check` | run |
| `post_backtest_cost_check.safety_factor_required` | Ratio needed to pass (cost model, default 2.0). | ratio | `SS:cost_check` | meta |
| `post_backtest_cost_check.pass` | ratio >= safety factor. | bool | `SS:cost_check` | run |
| `post_backtest_route` | Legacy route label from the estimated check (removed from reports when the legacy verdict is retired). | label | `RA:build_core` | run |
| `post_backtest_route_rationale` | Its text. | text | `RA:build_core` | run |
| `real_round_trip_cost_bps` | Mean (entry + exit commission rate) per trade. | bps | `RA:build_core` | run |
| `real_gross_edge_bps_per_trade` | Mean position return before commission per trade. | bps | `RA:build_core` | run |
| `post_backtest_cost_check_real` | The same check on measured numbers. | map | `RA:build_core` | run |
| `post_backtest_cost_check_real.estimated_gross_edge_bps_per_trade` | Measured: `real_gross_edge_bps_per_trade` (after slippage, A7). | bps | `RA:build_core` | run |
| `post_backtest_cost_check_real.cost_bps_per_trade` | Measured: `real_round_trip_cost_bps` (commission only, A7). | bps | `RA:build_core` | run |
| `post_backtest_cost_check_real.edge_to_cost_ratio` | abs(edge) / cost. | ratio | `RA:build_core` | run |
| `post_backtest_cost_check_real.safety_factor_required` | Ratio needed to pass (cost model, default 2.0). | ratio | `RA:build_core` | meta |
| `post_backtest_cost_check_real.pass` | ratio >= safety factor. | bool | `RA:build_core` | run |
| `post_backtest_cost_check_real.basis` | Always `real`. | label | `RA:build_core` | meta |
| `post_backtest_route_real` | Legacy route from the measured check (removed when the legacy verdict is retired). | label | `RA:build_core` | run |
| `post_backtest_route_real_rationale` | Its text. | text | `RA:build_core` | run |
| `sharpe_annualization` | Fixed text: sqrt(365) daily Sharpe. | text | `RA:write_metrics_json` | meta |
<!-- /data-dictionary -->

## 4. Per-regime blocks

`per_regime.<regime>` (`RA:build_per_regime`): bars grouped by the `regime` column, trades by
their entry regime. `regime_validity.<regime>` (`RA:build_regime_validity`).

<!-- data-dictionary: per_regime -->
| Field | Meaning | Unit | Code | When known |
|---|---|---|---|---|
| `<regime>.bar_count` | Bars with this label. | count | `RA:build_per_regime` | run |
| `<regime>.avg_forecast` | Mean forecast on those bars. | forecast | `RA:build_per_regime` | run |
| `<regime>.trade_count` | Trades entered in this regime. | count | `RA:build_per_regime` | run |
| `<regime>.total_net_pnl` | Their summed net PnL. | USDT | `RA:build_per_regime` | run |
<!-- /data-dictionary -->

<!-- data-dictionary: regime_validity -->
| Field | Meaning | Unit | Code | When known |
|---|---|---|---|---|
| `<regime>.forward_return_mean` | Mean close[t+1]/close[t]-1 over bars with this label (next row, no gap filter: A12). | frac | `RA:build_regime_validity` | after |
| `<regime>.forward_return_std` | Its stdev. | frac | `RA:build_regime_validity` | after |
| `<regime>.n_bars` | Bars counted. | count | `RA:build_regime_validity` | run |
| `<regime>.informative` | abs(mean) >= 0.0001. | bool | `RA:build_regime_validity` | after |
<!-- /data-dictionary -->

## 5. `diagnostics` (protocol_result.yaml hypothesis_verdict.diagnostics)

Over all windows of a variant (`RP:_build_diagnostics`); the profitability report's
`overall.diagnostics`.

<!-- data-dictionary: diagnostics -->
| Field | Meaning | Unit | Code | When known |
|---|---|---|---|---|
| `median_gross_pnl` | Median over windows of core.gross_pnl. | USDT | `RP:_build_diagnostics` | run |
| `median_cost_drag_pct` | Median of core.cost_drag_pct. | % | `RP:_build_diagnostics` | run |
| `median_forecast_return_corr` | Median of core.forecast_return_corr (Pearson, active bars). | corr | `RP:_build_diagnostics` | after |
| `median_avg_trade_duration_bars` | Median of core.avg_trade_duration_bars. | bars | `RP:_build_diagnostics` | run |
| `uninformative_regimes` | Regimes with informative false in any window. | list | `RP:_build_diagnostics` | after |
| `win_rate_vs_sharpe` | Legacy text from the old rule set (`N/A (no rule set)` without one). | text | `RP:_build_diagnostics` | meta |
| `below_floor_pct` | Share of windows with fewer than 5 trades. | % | `RP:_build_diagnostics` | run |
| `post_backtest_route_real` | Most common core route (ties broken by precedence). Legacy, removed when retired. | label | `RP:_build_diagnostics` | run |
| `post_backtest_route_real_tied` | That choice was a tie. | bool | `RP:_build_diagnostics` | run |
| `cost_dominated_real` | That route is a cost-hurdle route. Legacy, removed when retired. | bool | `RP:_build_diagnostics` | run |
| `per_trade_expectancy_bps` | Copy of trade_diagnostics summary.per_trade_expectancy_bps. | map | `RP:_build_diagnostics` | run |
| `zero_trade_slot_pct` | Copy of summary.zero_trade_slot_pct. | % | `RP:_build_diagnostics` | run |
| `fee_reduction_metrics` | Copy of summary.fee_reduction_metrics. | map | `RP:_build_diagnostics` | run |
<!-- /data-dictionary -->

## 6. (removed)

D-198: the five category reports (`artifacts/reports/<category>.yaml`) are no longer built; this
section described them and was removed from the dictionary the analyst reads.

## 7. grid_evaluation.yaml

`artifacts/grid_evaluation.yaml`: each pre-registered criterion on each graded
variant (`VE:evaluate_grid`, written at `P1:run_tool_worker`). Cells are `PASS`, `FAIL`,
`INCONCLUSIVE` or `SPEC_ERROR`.

<!-- data-dictionary: grid_evaluation.yaml -->
| Field | Meaning | Unit | Code | When known |
|---|---|---|---|---|
| `result` | `GRID_EVALUATED` or `SPEC_ERROR`. | label | `VE:evaluate_grid` | run |
| `criteria` | Criterion ids in order. | list | `VE:evaluate_grid` | meta |
| `variants` | Graded variant ids (the columns). | list | `VE:evaluate_grid` | meta |
| `idea_status` | `validated` / `refuted` / `inconclusive` (any FAIL refutes; any INCONCLUSIVE, untested or failed variant blocks validated). | label | `VE:evaluate_grid` | run |
| `reason` | Text of that status. | text | `VE:evaluate_grid` | run |
| `failed_variants` | {variant: `refused:` or `backtest_failed:` reason}. | map | `VE:evaluate_grid` | meta |
| `untested_variants` | {variant: reason} not run in this run. | map | `VE:evaluate_grid` | meta |
| `partial_coverage_variants` | {variant: reason} graded on fewer windows (cap at inconclusive). | map | `VE:evaluate_grid` | meta |
| `evaluated_at` | When evaluated (UTC). | time | `P1:run_tool_worker` | meta |
| `grid.<criterion>.<variant>.result` | Cell result. | label | `VE:_evaluate_grid_cell_for_symbol` | run |
| `grid.<criterion>.<variant>.value` | The reduced (window source) or pooled value of the metric the criterion names (`metric`: the menu's, or the card's override). | metric | `VE:_evaluate_grid_cell_for_symbol` | run |
| `grid.<criterion>.<variant>.threshold` | The criterion's threshold (the menu's, or the card's override). | metric | `VE:_evaluate_grid_cell_for_symbol` | meta |
| `grid.<criterion>.<variant>.comparator` | The criterion's comparator (the menu's, or the card's override). | label | `VE:_evaluate_grid_cell_for_symbol` | meta |
| `grid.<criterion>.<variant>.n_windows` | Windows with a numeric value (window source; a zero-trade window's 0.0 counts, A8, unless `orchestrator.zero_trade_windows_not_computed` skips it) or in scope (pooled). | count | `VE:_evaluate_grid_cell_for_symbol` | run |
| `grid.<criterion>.<variant>.n_trades` | Summed core.trade_count over those windows. | count | `VE:_evaluate_grid_cell_for_symbol` | run |
| `grid.<criterion>.<variant>.reason` | Why INCONCLUSIVE / FAIL / SPEC_ERROR. | text | `VE:_evaluate_grid_cell_for_symbol` | meta |
| `grid.<criterion>.<variant>.skipped_windows` | Only under `orchestrator.zero_trade_windows_not_computed`, on a window-source cell whose metric is computed from trades (`VE:ZERO_TRADE_NOT_COMPUTED_FIELDS`): the windows with `core.trade_count` 0, not computed (A8 fix): they neither vote in the reducer nor count in `n_windows` / `floor.min_windows`. | map | `VE:_zero_trade_windows_cell` | run |
| `grid.<criterion>.<variant>.skipped_windows.count` | How many windows were skipped (a window whose value is already null is not counted). | count | `VE:_zero_trade_windows_cell` | run |
| `grid.<criterion>.<variant>.skipped_windows.windows` | Those windows, as `<symbol> <window>`. | list | `VE:_zero_trade_windows_cell` | run |
| `grid.<criterion>.<variant>.skipped_windows.reason` | Why (`VE:ZERO_TRADE_SKIP_REASON`). | text | `VE:_zero_trade_windows_cell` | meta |
| `grid.<criterion>.<variant>.skipped_windows.eras_left_empty` | sign_consistent_by_era cells only: the eras the cell compared before the skip that have no window left after it (review fix, PR #349). Not empty: the cell is INCONCLUSIVE (`era <e>: every window had no trades ...`), never PASS; a FAIL the remaining eras decide stays FAIL. | list | `VE:_zero_trade_windows_cell` | run |
| `grid.<criterion>.<variant>.detail` | Era reducer detail. | map | `VE:_evaluate_grid_cell_for_symbol` | run |
| `grid.<criterion>.<variant>.detail.era_medians.<era>` | Median, over the era's windows, of the metric the criterion names (`metric`: the menu's `net_return_pct` by default, or the card's override: the review found run_074's card used `forecast_return_corr`). A zero-trade window's 0.0 in a trade-based core field counts as a value (A8), unless `orchestrator.zero_trade_windows_not_computed` skips it (`skipped_windows`). | metric | `VE:_reduce_sign_consistent_by_era` | run |
| `grid.<criterion>.<variant>.detail.reason` | Why the era reducer did not pass: an era median exactly 0, eras disagreeing in sign, or no window with both a value and an era. | text | `VE:_reduce_sign_consistent_by_era` | meta |
| `grid.<criterion>.<variant>.detail.era_signs.<era>` | Sign of that median (1, -1, 0). | sign | `VE:_reduce_sign_consistent_by_era` | run |
| `grid.<criterion>.<variant>.detail.ruin` | D-141: the ruined account behind a FAIL `whole_test_sharpe_positive` cell (value null); present only on that cell. | map | `VE:_evaluate_grid_cell_for_symbol` | run |
| `grid.<criterion>.<variant>.detail.ruin.file` | D-141: path of the equity file in which the account reached zero or below. | path | `VE:_evaluate_grid_cell_for_symbol` | run |
| `grid.<criterion>.<variant>.detail.ruin.timestamp` | D-141: timestamp of the first row at or below zero equity. | time | `VE:_evaluate_grid_cell_for_symbol` | run |
| `grid.<criterion>.<variant>.detail.ruin.equity` | D-141: the equity value at that row. | value | `VE:_evaluate_grid_cell_for_symbol` | run |
| `grid.<criterion>.<variant>.per_symbol.<symbol>` | Cell per symbol (symbol_reducer per_symbol_all). | map | `VE:_evaluate_grid_cell` | run |
| `grid.<criterion>.<variant>.n_eff` | residual_ic: effective sample size. | count | `VE:_evaluate_residual_ic_cell` | run |
| `grid.<criterion>.<variant>.p_value_one_sided` | residual_ic: one-sided p-value. | p | `VE:_evaluate_residual_ic_cell` | run |
| `grid.<criterion>.<variant>.max_p_value` | residual_ic: the criterion's p needed to pass. | p | `VE:_evaluate_residual_ic_cell` | meta |
| `grid.<criterion>.<variant>.composite` | residual_ic: composite state (`STALE` when missing). | label | `VE:_evaluate_residual_ic_cell` | meta |
| `grid.<criterion>.<variant>.fully_explained` | residual_ic: duplicate of the composite. | bool | `VE:_evaluate_residual_ic_cell` | run |
| `grid.<criterion>.<variant>.source` | profit_bars cells: `profit_bars`. | label | `VE:_evaluate_profit_bars_cell` | meta |
| `grid.<criterion>.<variant>.bars` | profit_bars cells (composition runs): the profit-bars grader's rows, one per bar. | list | `VE:_evaluate_profit_bars_cell` | run |
| `grid.<criterion>.<variant>.bars[].name` | Bar name, as in `config/profitability_bars.yaml` (`sharpe_min`, `max_drawdown_pct_max`, ...). | label | `P1:_grade_profit_bars._bar`, `P1:_grade_profit_bars_v2` | meta |
| `grid.<criterion>.<variant>.bars[].threshold` | The bar's threshold from that file. | metric | `P1:_grade_profit_bars._bar`, `P1:_grade_profit_bars_v2` | meta |
| `grid.<criterion>.<variant>.bars[].actual` | The variant's measured value for the bar; how it is defined is in `basis` and `note` (drawdown: the equal-weight portfolio on bars; v2 Sharpe: the whole-test daily equity curve). | metric | `P1:_grade_profit_bars._bar`, `P1:_grade_profit_bars_v2` | run |
| `grid.<criterion>.<variant>.bars[].result` | `PASS`, `FAIL` or `NOT_EVALUABLE`. | label | `P1:_grade_profit_bars._bar`, `P1:_grade_profit_bars_v2`, `P1:_hold_rows_not_evaluable` | run |
| `grid.<criterion>.<variant>.bars[].basis` | The definition that produced `actual` (only under profit_bars_every_backtest or v2). | label | `P1:_grade_profit_bars._bar`, `P1:_grade_profit_bars_v2` | meta |
| `grid.<criterion>.<variant>.bars[].comparator` | v2: `>=`, `<=` or `>`. | label | `P1:_grade_profit_bars_v2` | meta |
| `grid.<criterion>.<variant>.bars[].note` | Where `actual` comes from. | text | `P1:_grade_profit_bars._bar`, `P1:_grade_profit_bars_v2` | meta |
| `grid.<criterion>.<variant>.bars[].detail` | v2: the computation's detail (per-coin counts, DSR inputs). | map | `P1:_grade_profit_bars_v2` | run |
| `grid.<criterion>.<variant>.bars[].not_evaluable_reason` | Why `NOT_EVALUABLE`. | text | `P1:_grade_profit_bars._bar`, `P1:_grade_profit_bars_v2`, `P1:_hold_rows_not_evaluable` | meta |
| `grid.<criterion>.<variant>.bars[].reason` | v2, the Calmar row (D-188) only: `no drawdown` when the row PASSes because the drawdown is zero and the total return positive (`actual` is then null). | text | `P1:_grade_profit_bars_v2` | meta |
| `grid.<criterion>.<variant>.weight_schedule` | profit_bars cells: the grader's weight schedule. | map | `VE:_evaluate_profit_bars_cell` | meta |
<!-- /data-dictionary -->

## 8. (removed)

D-198: `claim_result_digest.yaml` (the readers' digest of the claim's measured numbers) is no
longer written; this section described it and was removed from the dictionary the analyst reads.
The claim's measured numbers are in `claim_measurement.yaml` (section 9).

## 9. claim_measurement.yaml

`artifacts/claim_measurement.yaml` (an older run: `claim_status.yaml`): the run's
measurement status (`CM:run_doc`, error case `CM:error_doc`). Per-variant detail lives in
`artifacts/variants/<variant>/claim_test.yaml`.

<!-- data-dictionary: claim_measurement.yaml -->
| Field | Meaning | Unit | Code | When known |
|---|---|---|---|---|
| `run_id` | Run id. | id | `CM:run_doc` | meta |
| `label` | `measured, not proven`. | text | `CM:run_doc` | meta |
| `note` | Fixed text: effect sizes only, no p-value. | text | `CM:run_doc` | meta |
| `information_only` | true. | bool | `CM:run_doc` | meta |
| `claim_status` | `measured` when any test was measured, else `not_measured`. | label | `CM:run_doc` | run |
| `reason` | Why not measured (card gap, `no_graded_variants`, `error`, ...). | label | `CM:run_doc` | meta |
| `detail` | Detail text. | text | `CM:run_doc` | meta |
| `n_tests_measured` | (variant, test) pairs measured. | count | `CM:run_doc` | run |
| `n_tests_no_events` | Pairs whose selector matched no bar (absent in the error document, A14). | count | `CM:run_doc` | run |
| `n_tests_not_measured` | The other pairs. | count | `CM:run_doc` | run |
| `variants.<variant>.status` | Variant status. | label | `CM:run_doc` | run |
| `variants.<variant>.reason` | Its reason. | text | `CM:run_doc` | meta |
| `variants.<variant>.file` | `variants/<variant>/claim_test.yaml`, or null. | path | `CM:run_doc` | meta |
| `tests[].variant` | Variant id. | id | `CM:run_doc` | meta |
| `tests[].test` | Test name. | id | `CM:run_doc` | meta |
| `tests[].spec_hash` | Spec hash. | hash | `CM:run_doc` | meta |
| `tests[].status` | `measured`, `no_events` or `not_measured`. | label | `CM:run_doc` | run |
<!-- /data-dictionary -->

## 10. The analyst's economics tools (PR-B, orchestrator.analyst.enabled)

Not run-artifact fields: figures the analyst's query engine (`tools/analyst_queries.py`)
reports per window. Most are READ from the run's own record: the window's `core` block (section 3;
`protocol_result.yaml` `results[].core`) and `metrics.json` `bar_equity`. Only four are computed
here, from `bars.csv` and `trades.json`. This section has no `data-dictionary` marker, so no
code parses it.

**`window_economics`** (`tools/window_economics.py`; counts 0 comparisons; refused above 12
cells). Returns `windows.<symbol>/<window>` and `total`, one cell each. The same object is
stored per graded variant beside `forecast_shape` in `artifacts/profit_bars_evaluation.yaml`
under `variants.<variant>.window_economics` (information only; the key exists only with the
analyst flag on; null when the windows cannot be read). All figures are post-run accounting
(`run`), never a signal input. Bar fields read the bars with `regime` other than `NOT_READY`.

| Field | Exact definition | Unit | Source |
|---|---|---|---|
| `n_bars` | Bars read: the `bars.csv` rows with `regime` other than `NOT_READY` (stripped, upper case). | count | computed (`bars.csv`) |
| `trades` | `core.trade_count`. | count | read (`core`) |
| `turnover` | `bar_equity.turnover` of the window's `metrics.json` (`RA:build_bar_equity`, `run_artifact.py` :729): the sum over the ready bars of `abs(postRebalance_current_allocation - previous_allocation)`, as the run rounded it. Not in the `core` block. | alloc | read (`metrics.json`) |
| `direction_changes` | Sign flips of `postRebalance_current_allocation`. A bar with `abs(alloc) <= 1e-6` is flat and has no sign, and flat stretches are skipped: long, flat, short counts 1; long, flat, long counts 0. | count | computed (`bars.csv`) |
| `mean_abs_allocation` | Mean of `abs(postRebalance_current_allocation)` over the ready bars. | alloc | computed (`bars.csv`) |
| `max_abs_allocation` | Max of `abs(postRebalance_current_allocation)` over the ready bars. | alloc | computed (`bars.csv`) |
| `gross_pct` | 100 x `core.gross_pnl` / V0. | % of V0 | read (`core`), converted |
| `fees_pct` | 100 x `core.fees_paid` / V0. | % of V0 | read (`core`), converted |
| `net_pct` | 100 x `core.net_pnl` / V0 (= `gross_pct` - `fees_pct`, within the run's rounding). | % of V0 | read (`core`), converted |
| `cost_drag_pct` | `core.cost_drag_pct`, verbatim: (gross - net) / abs(gross) x 100 as the run computed it; null when the run's gross was 0. In this view only, it is reported only when `abs(gross_pct)` >= 5 x `fees_pct`; otherwise null, with `cost_drag_note` set (a cell with no gross or no fees figure keeps the run's figure). The run-level `cost_drag_pct` (section 3) is unchanged. | % | read (`core`) |
| `avg_trade_duration_bars` | `core.avg_trade_duration_bars`, verbatim: mean trade duration / median bar spacing; null when the run had no trades. | bars | read (`core`) |
| `median_holding_bars` | Median over the lots of `trades.json` of `duration_minutes` x 60 / step, step = the median spacing of the window's bar timestamps; null without lots. | bars | computed (`trades.json`, `bars.csv`) |
| `fees_pct_annualised` | `fees_pct` x 365 / `n_bars`: fees as a percent of the window's starting account per 365 bars of the window. Null when `fees_pct` is null. | % of V0 per 365 bars | derived |
| `gross_per_lot_pct` | `gross_pct` / `trades`: the mean over the window's lots of the lot's gross, as a percent of the window's starting account. Null without lots or without a gross. | % of V0 per lot | derived |
| `fees_per_lot_pct` | `fees_pct` / `trades`: the same for fees. Read it against `gross_per_lot_pct`. Null without lots or without fees. | % of V0 per lot | derived |
| `turnover_annualised` | `turnover` x 365 / `n_bars`. Null when `turnover` is null. | alloc per 365 bars | derived |
| `cost_drag_note` | "gross near zero: a signal finding, not a cost finding" when `cost_drag_pct` was withheld by the 5 x `fees_pct` test (see `cost_drag_pct`); otherwise null. | text | derived |

Read, not recomputed (operator ruling 2026-10-19): a figure marked read is the run's own number.
Nothing is summed from the lots of `trades.json` and nothing is re-derived from the bars. A
figure the run did not record (no `core` block in an older run, no `metrics.json` or no
`bar_equity` block) is null, never filled in by a recomputation. A percent of V0 is the read
dollar figure divided once by V0, nothing else. V0 is the `total_portfolio_value` of the
window's first `bars.csv` row, the account at the window's start. `net_pct` is the window's
realised account change from closed lots: when the window ends flat (every lot closed by the
last bar) it equals 100 x (E_end - V0) / V0, where E_end is the `postRebalance_total_value` of
the window's last `bars.csv` row (the account after the window's last action; the last row's
`total_portfolio_value` is that bar's value before its rebalance and is not E_end).
`total` sums `trades`, `turnover`, `direction_changes` and the three `*_pct` over the cells
(each window is its own account; null when any cell's figure is null), pools the bars for
`mean_abs_allocation` and `max_abs_allocation`, and pools every lot for `median_holding_bars`.
The five derived fields (D-168) are arithmetic on the cell's own figures above, with no new
input; in `total` they use the total's figures (summed percents, trades and turnover, pooled
`n_bars`), and the same 5 x `fees_pct` test governs the total's `cost_drag_pct`. "Per 365 bars"
is a year on a daily timeframe and 365 bars on any other.
Two `total` figures are not the run's own numbers; each is stated as derived from the read
window figures (operator ruling 2026-10-19, Q3), by these formulas:

- `cost_drag_pct` (total): derived from the read window figures, = (sum of the read
  `core.gross_pnl` - sum of the read `core.net_pnl`) / abs(sum of the read `core.gross_pnl`) x 100;
  null when that sum is 0 or any window lacks a gross or net figure.
- `avg_trade_duration_bars` (total): derived from the read window figures, =
  sum(`core.trade_count`_i x `core.avg_trade_duration_bars`_i) / sum(`core.trade_count`_i) over
  the windows with at least one trade; null when no window has a trade, when any window lacks a
  `trade_count`, or when a window with trades lacks its average.

`turnover` (per window and `total`) is read from `metrics.json` `bar_equity.turnover` in each
window folder; it is not in `protocol_result.yaml`.

**`trade_slice` fields** (aggregates of the lots, one value per lot of `trades.json`):

| Field | Exact definition | Unit | Counts as a comparison |
|---|---|---|---|
| `trade_gross_return` | The lot's return before costs on the window's return basis, the same per-lot number the claim outcome `trade_gross_return` sees: `all_costs` -> the cost record's `gross_return_before_costs` / 100 (at the bar closes, before fees and slippage); otherwise `profit_loss_percent` / 100 (at the fill prices, before commission). The reply's `return_basis` lists the bases of the windows with lots. A per-lot return on the lot's own notional, not a share of the account. | frac | yes, like `trade_net_return` (an outcome) |
| `trade_cost_pct` | `total_commission_percent`: (entry + exit commission rate) x 100, in percent of the lot's notional (the cost model's rate). | % | no (not a market outcome) |

**Derived bar columns** (for `describe` / `distribution`; `list_columns` lists them; each uses
bar t, plus bar t-1 where stated, never a later bar):

| Column | Exact definition | Unit | When known |
|---|---|---|---|
| `abs_forecast` | `abs(forecast_t)`. | forecast | close |
| `allocation_abs` | `abs(postRebalance_current_allocation_t)`, the allocation held after bar t's trade. | alloc | fill |
| `forecast_sign_change` | 1.0 when `forecast_(t-1)` and `forecast_t` are of strictly opposite signs, else 0.0. A zero forecast has no sign: + then 0 and 0 then - are not changes. NaN when the bar stamped ts_t - step is not in the window (the first bar, a gap) or either forecast is not finite. | 0/1 | close |

`describe` / `distribution` grouped by hour, weekday or regime still charge comparisons on
these columns, as on any other.

Claim fields: a claim selector reads forecast, close, past_return, trailing_vol, abs_forecast or forecast_sign_change; a trade test's outcome is trade_net_return, post_exit_return or trade_gross_return (see CLAIM_TESTS.md). allocation_abs, trade_cost_pct and the window_economics figures are not claim fields.

**The `signal` key** (D-193; optional on a bar claim test, on `conditional_effect` and, for the derived columns `abs_forecast` and `forecast_sign_change`, on `describe` / `distribution`; default `forecast`). A test reads the forecast array of its signal: `forecast`, or any `bars.csv` column of section 1 whose Unit is `forecast` and whose When known is `close` or `fill` (today the component columns `debug_info.components.<component>.post_pipeline_value` and `.weighted_contribution`, and `debug_info.forecast_delta`). The allowed values are read from the Unit column of that table, not from a list in code. A component the variant does not have is refused ("no component <id> in this variant"). A trade test takes no signal. The key is written into a test block only when it is not `forecast`.

## Not recorded today

These do not exist in any file the AI steps read. Do not infer them.

- **Why a forecast is zero, or why no trade happened** (E-027). bars.csv shows the
  warm-up (`debug_info.error`), a component without history
  (`not_ready_component`) and a risk-manager rejection
  (`approved_rebalance: false` with its `controls`), but NOT: a NaN forecast that
  was held (only counted in metrics.json `nan_forecast`), a gap tier (middle-tier
  entry block, large-tier forced flatten; gap events only in metrics.json
  `data_quality`), a risk-gate kill, or the end-of-backtest forced close (merged
  into the last row, `PI:PortfolioStateTracker.record_state`). The target allocation is not a column (except `sizing_target_allocation`, only with a `strategies.sizing` block).
- **The decision behind each trade** (E-029): which rule opened or closed a lot,
  whether it was a full exit or a partial reduction, the forecast and band at the
  decision. `exit_reason` is inferred (A5).
- **Regime-rule inputs** (parked): the values each threshold rule compared, which
  veto fired (`forced_by_veto`, `RE:ConfigDrivenRegimeEngine.classify`) and the score winner (`RE:ConfigDrivenRegimeEngine._classify_score`) are
  computed and dropped (`MS:AdvancedStrategy.generate_forecast`).
- **Transform steps** (parked): only a component's raw value and its value after
  the whole pipeline are recorded, not the intermediate steps.
- **Per-trade costs**: the slippage and commission a trade actually paid, and
  funding (funding is not modelled in protocol runs: `run_protocol` does not pass
  `model_funding`).
- **Bar-level equity statistics in the category reports**: metrics.json
  `bar_equity` exists (run_protocol passes `bar_equity=True`, `RP:main`) but no
  report reads it. The one place a reader sees bar-level figures is the grid of a
  composition run: its profit_bars cells' `bars[].actual` (section 7) carry the
  equal-weight portfolio's drawdown measured on bars and, under
  `orchestrator.profit_bars_v2`, the Sharpe of the whole-test daily equity curve.

## Audit findings

Found while writing this file (2026-10-08); none fixed here (no engine code
changes in E-073 step 1). Each is a follow-up. "Measured" lines were checked on the
saved runs run_070 to run_074 (66 window bars.csv files, 6 trade_diagnostics.json).
The impact levels, and the figures marked "review", come from the independent
review of PR #342 (2026-10-08).

**By impact:** A7 HIGH (the mandatory cost bar is looser than stated), A8
MEDIUM-HIGH (zero-trade windows vote in the era grid), A6 MEDIUM (MAE / MFE /
exit-efficiency conclusions flip without the entry bar), A1 LOW (no consumer);
the others are labelling or documentation defects.

- **A1. bars.csv balances are the end-of-run balances on every row.** Impact
  LOW: no step reads these columns today.
  `get_account_balance` returns the live balance dict (`PI:CommonPortfolioDef.get_account_balance`); `record_state`
  stores that reference (`TB:TradingBot._process_symbol_candle_completion`, `PI:PortfolioStateTracker.record_state`); trades mutate it in place
  (`PI:CommonPortfolioDef.update_local_balance`); flattening happens at the end (`BT:BacktestEngine._end_of_backtest`). Measured: in all 66 files
  every `balances.*.free` column has one value. The scalar columns
  (`total_portfolio_value`, `previous_allocation`, ...) are right. Fix: copy the
  dict at record time (declared output change of bars.csv / portfolio_states.csv).
- **A2. `confidence` is always 0.0 and `strategy` always empty** (`MS:AdvancedStrategy.generate_forecast`; also
  `entry_confidence` in trades.json). Drop or fill.
- **A3. Column name `succcess_execute_portfolio_rebalance`** has three c's
  (`TB:TradingBot._process_symbol_candle_completion`, `TB:TradingBot._close_all_positions_at_end`). Renaming breaks readers of saved runs; documented as is.
- **A4. `entry_efficiency` measures the entry slippage, not "waiting one bar".**
  The fill is bar t's close plus slippage (`EH:MockExecutionHandler.open_long_position`); the comparison is bar t+1's
  open (`RP:_compute_entry_efficiency`), which on 24/7 data is bar t's close. Measured: median -0.025%
  (BTC) and -0.075% (SOL, UNI), exactly the 2.5 / 7.5 bps slippage. The same
  slippage biases `entered_earlier_better` and `held_longer_better` (`RP:_compute_entered_earlier_better`,
  `RP:_compute_held_longer_better`). Fix: compare with the next bar's close, or drop.
- **A5. `exit_reason` is `signal_flip` for every exit but the window's last bar**
  (`RP:_infer_exit_reason`, its default branch). A trade is a closed LIFO lot, so
  the label covers every exit that is not at the window's end: a real sign flip,
  but also a same-sign partial reduction (a lot closed while the position keeps
  its side) and a gap or risk-gate flatten. Nothing produces `stop_loss` or
  `time_stop`, so `stop_loss_pct`, `time_stop_pct` and `stop_loss_recovery_rate`
  are always 0. Measured: 99% signal_flip. Splitting a flip from a reduction is
  possible today: trades.json carries `exit_forecast`, whose sign against the
  lot's side tells them apart (review: about 73% of run_074 base's exits are
  same-sign reductions). Fix: classify from `exit_forecast`, or E-029.
- **A6. MAE, MFE and exit_efficiency include the entry bar's own high and low**,
  which happened before the fill at that bar's close (`RP:_compute_trade_records_for_window`, `RP:_compute_mae_mfe`,
  `RP:_compute_exit_efficiency`). With median holding of 1-2 bars this inflates both. Impact
  MEDIUM: conclusions flip when the entry bar is excluded (review): median
  mae/mfe 0.75 -> 1.26 on run_070 and 1.49 -> 0.69 on run_071; median
  exit_efficiency 0.28 -> 0.41 on run_074. Fix: start the holding window at
  entry_idx + 1.
- **A7. `cost_paid` is the configured fee x 2, not what the trade paid**
  (`RP:_cost_paid_bps`): no slippage, not size-dependent; and `realized_return`, called gross,
  is net of slippage (fill prices). So `realized_edge_to_cost_ratio`
  (`CH:realized_edge_to_cost_ratio_unrounded`) compares a post-slippage edge with
  a fee-only cost. Impact HIGH: D-038's mandatory bar "survives 2x costs" (ratio
  > 2.2: the menu criterion `realized_edge_to_cost_ratio` and profit_bars_v2's
  `cost_edge_ratio_min`, `pooled_edge_to_cost_ratio`) is looser than stated. With
  the run_070-074 costs (perp fee 5 bps a side; slippage 2.5 bps a side on BTC,
  7.5 on SOL and UNI) the bar passes at a mean gross edge per trade above about
  27 bps (BTC) / 37 bps (SOL, UNI), that is 4.4 x fee + 2 x slippage, where
  "2x all costs" is about 30 / 50 bps, 2 x (2 x fee + 2 x slippage). Fix: put
  the slippage in `cost_paid`, or rename and restate the bar.
  **Fixed behind `orchestrator.cost_bar_all_costs`** (CUL-414, D-082; off by
  default): run_protocol `--cost-bar-all-costs` adds `gross_return_before_costs`,
  `slippage_paid` and `cost_paid_all` to every trade record
  (`RP:_all_costs_fields`) and `realized_edge_to_cost_ratio_all_costs` to the
  summary; the menu criterion reads that field (`VE:evaluate_grid`, and the
  legacy pass rule the same way, `VE:evaluate_pass_rule_criteria`) and
  `pooled_edge_to_cost_ratio` uses the new fields. If any trade lacks them,
  neither ratio is computed (never a subset). The bar is then
  gross before all costs / all costs > 2.2: about 33 bps (BTC) / 55 bps
  (SOL, UNI). `cost_paid` and `realized_edge_to_cost_ratio` keep their values.
- **A8. Trade-based core fields are 0.0, not null, when there are no trades**
  (`RA:build_core`, `overall.get(..., 0.0)`; `PM:EnhancedPerformanceTracker._calculate_standard_metrics` returns nothing): `net_return_pct`,
  `max_drawdown_pct`, `win_rate`, and `sharpe` when it is undefined (`PM:EnhancedPerformanceTracker.calculate_sharpe_ratio`).
  Impact MEDIUM-HIGH: in the grid a zero-trade window's 0.0 is a numeric value,
  so it counts as a sign vote in the `sign_consistent_by_era` median
  (`VE:_evaluate_grid_cell_for_symbol` keeps it, `VE:_reduce_sign_consistent_by_era`
  takes the median) and toward `floor.min_windows` (`n_windows`). Latent in
  run_070 to run_074 (review). Fix: null.
  **Fixed behind `orchestrator.zero_trade_windows_not_computed`** (CUL-415, D-084;
  off by default): in a window-source grid criterion whose metric is computed
  from trades (`VE:ZERO_TRADE_NOT_COMPUTED_FIELDS`), a window with
  `trade_count` 0 is skipped: no vote, not counted toward `floor.min_windows`,
  listed in the cell's `skipped_windows` (`VE:_zero_trade_windows_cell`); too
  few windows left is INCONCLUSIVE; an era left with no window makes a
  sign_consistent_by_era cell INCONCLUSIVE, never PASS (`skipped_windows.eras_left_empty`).
  The engine still writes 0.0, and the
  per-symbol summaries of `run_protocol` (`median_win_rate`,
  `max_abs_drawdown_pct`, `median_gross_pnl`) still include it: not on the
  grid's path, left open.
- **A9. `sharpe`, `max_drawdown_pct` and `net_return_pct` use the trade-exit
  basis** (`PM:EnhancedPerformanceTracker._calculate_standard_metrics`, `PM:EnhancedPerformanceTracker.calculate_max_drawdown`, `PM:EnhancedPerformanceTracker.calculate_sharpe_ratio`): PnL booked on exit dates, open positions not
  marked. The bar-level figures exist (metrics.json `bar_equity`) but no report
  shows them. Fix: add them to the profitability report.
- **A10. trade_efficiency aggregates every numeric trade field** (`BR:_aggregate_records`),
  including `entry_idx` / `exit_idx` (window-local row numbers) and
  `entry_price` / `exit_price` across symbols, whose stats mean nothing; booleans
  are dropped (`BR:_numeric_or_none`), so a slice has no win rate. Fix: a field list.
- **A11. Report `n` counts records, not values** (`BR:_aggregate_records`): component records
  include warm-up / not-ready bars with blank metrics, so `n` overstates the
  sample of the mean beside it. Fix: count per metric.
- **A12. `regime_validity` pairs each row with the next row** (`RA:build_regime_validity`),
  without the gap filter `forecast_return_corr` uses (`RA:build_core`), and includes
  `NOT_READY` bars. Minor.
- **A13. `debug_execute_portfolio_rebalance.quantity` is unsigned for opens and
  reductions but the signed position for CLOSE** (`EH:MockExecutionHandler.open_long_position`, `EH:MockExecutionHandler.open_short_position` vs `EH:MockExecutionHandler.close_position`).
- **A14. `claim_measurement.yaml` written by the safety net lacks
  `n_tests_no_events`** (`CM:error_doc` vs `CM:run_doc`).
- **A15. Stale comments and docstrings.** `BR:_transition_indices` and `BR:build_component_attribution_report` say every
  window's bars.csv ends with an empty-`regime` row; measured: none of the 66
  files has one (the end-of-run close merges into the last row, `PI:PortfolioStateTracker.record_state`).
  `FM:ForecastManager.forecast_to_allocation`'s docstring says both -200%..+200% and -1.0..1.0; the code is forecast / 10.
  `RP:_aggregate_trade_diagnostics._pct_val` (floor nearest-rank percentiles) and `BR:_percentile` (linear) use two
  percentile definitions.
