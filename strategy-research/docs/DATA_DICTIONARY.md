# Data dictionary: what the AI steps read

E-073 step 1 (P-CUL-81, D-081). Every field of the run outputs the readers and the
other AI steps read: what it means, its unit, the code that computes or writes it
(`KEY:symbol`: a function, `Class.method`, a nested `outer.inner` or a module
constant of the file `KEY` names below), and **when it is known**. Audited against
the engine on 2026-10-08; the discrepancies found are in
[Audit findings](#audit-findings) (not fixed here).
`tests/test_e073_data_dictionary.py` derives each file's full field paths from the
code that writes it and fails when a path is missing here or an entry here is no
longer written, when a cited symbol does not exist, or when it does not contain
the field's key.

**Readers:** use this file to know what a field means before you cite it. A number
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
| `BR` | `strategy-research/tools/build_reports.py` |
| `VE` | `strategy-research/tools/verdict_criteria_evaluator.py` |
| `RF` | `strategy-research/tools/reader_findings.py` |
| `CF` | `strategy-research/tools/claim_findings.py` |
| `CM` | `strategy-research/tools/claim_measure.py` |
| `CT` | `strategy-research/tools/claim_tests.py` |
| `NB` | `strategy-research/tools/nearest_build.py` |
| `P1` | `strategy-research/workflow/run_phase1_research.py` |
<!-- /data-dictionary-sources -->

<!-- readers: omit -->
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
| `fear_greed` | Fear and Greed index, latest value published at least 1 day before the bar start (as-of merge, publication delay 86400 s). | index 0-100 | `FR:FEED_REGISTRY`, `DM:_merge_asof_with_causality_guard` | close |
| `funding_rate` | Latest perpetual funding rate settled at or before the bar start (carried forward). | frac per settlement | `FR:FEED_REGISTRY`, `DM:_merge_asof_with_causality_guard` | close |
| `<reserved feed>` | A reserved feed's column (whale-footprint features), only when a caller registers it. | feed | `FR:RESERVED_FEED_REGISTRY` | close |
| `forecast` | The strategy's final forecast for the bar, clipped to -20..+20; 0.0 while not ready or on an error. | forecast | `SE:ConfigDrivenStrategyEngine.forecast`, `SB:StrategyOutput`, `SB:MainStrategy.generate_signals` | close |
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
| `previous_allocation` | Position value / account value at this close, before the trade. | alloc | `TB:TradingBot._process_symbol_candle_completion`, `PI:CommonPortfolioDef._calculate_actual_allocation` | close |
| `allocation_change` | Target allocation (forecast / 10, or the held allocation on a NaN forecast, 0 under a forced flatten) minus `previous_allocation`; set to 0 when a gap middle tier blocks a new entry. The target itself is not recorded. | alloc | `TB:TradingBot._process_symbol_candle_completion`, `FM:ForecastManager.forecast_to_allocation` | close |
| `approved_rebalance` | Risk manager's answer when `allocation_change` is non-zero (empty otherwise, and on a forced flatten). | bool | `TB:TradingBot._process_symbol_candle_completion` | fill |
| `succcess_execute_portfolio_rebalance` | The order succeeded (empty when no order was attempted). Name misspelled in code (A3). | bool | `TB:TradingBot._process_symbol_candle_completion`, `TB:TradingBot._close_all_positions_at_end` | fill |
| `postRebalance_total_value` | Account value after this bar's trade and its commission, at this close. | USDT | `TB:TradingBot._process_symbol_candle_completion` | fill |
| `postRebalance_current_allocation` | Allocation after this bar's trade. | alloc | `TB:TradingBot._process_symbol_candle_completion` | fill |
| `balances.<asset>.free` | Should be the asset held before the trade; is the END-of-run balance on every row (A1). | asset units | `PI:_default_balance`, `TB:TradingBot._process_symbol_candle_completion`, `PI:CommonPortfolioDef.get_account_balance` | end |
| `balances.<asset>.locked` | Should be the asset borrowed (short or margin) before the trade; END-of-run value (A1). | asset units | `PI:_default_balance`, `TB:TradingBot._process_symbol_candle_completion`, `PI:CommonPortfolioDef.get_account_balance` | end |
| `postRebalance_balances.<asset>.free` | Should be the asset held after the trade; END-of-run value (A1). | asset units | `PI:_default_balance`, `TB:TradingBot._process_symbol_candle_completion` | end |
| `postRebalance_balances.<asset>.locked` | Should be the asset borrowed after the trade; END-of-run value (A1). | asset units | `PI:_default_balance`, `TB:TradingBot._process_symbol_candle_completion` | end |
| `debug_approve_allocation_change` | Present instead of the dotted columns when no bar asked the risk manager: the text `{}`. | text | `TB:TradingBot._process_symbol_candle_completion` | fill |
| `debug_approve_allocation_change.symbol` | Symbol checked by the risk manager. | id | `RM:RiskManager.approve_allocation_change` | fill |
| `debug_approve_allocation_change.time` | Bar timestamp checked. | time | `RM:RiskManager.approve_allocation_change` | fill |
| `debug_approve_allocation_change.controls.max_allocation_change.passed` | abs(change) <= max (config `risk_management.controls`). Empty when an earlier control already failed. | bool | `RM:RiskManager.approve_allocation_change`, `RM:RiskManager._ctrl_max_allocation_change` | fill |
| `debug_approve_allocation_change.controls.min_allocation_change.passed` | abs(change) >= threshold (default 0.20): the no-trade band. | bool | `RM:RiskManager.approve_allocation_change`, `RM:RiskManager._ctrl_min_allocation_change` | fill |
| `debug_execute_portfolio_rebalance` | Present instead of the dotted columns when no order ran: the text `{}`. | text | `TB:TradingBot._process_symbol_candle_completion` | fill |
| `debug_execute_portfolio_rebalance.symbol` | Symbol of the order. | id | `EH:MockExecutionHandler.open_long_position` | fill |
| `debug_execute_portfolio_rebalance.price` | Fill price: close x (1 +/- slippage bps / 10000). | price | `EH:MockExecutionHandler.open_long_position`, `EH:MockExecutionHandler.open_short_position`, `EH:MockExecutionHandler.close_position` | fill |
| `debug_execute_portfolio_rebalance.quantity` | Order size: positive for LONG/SHORT/REDUCE_*, the signed position for CLOSE (A13). | base units | `EH:MockExecutionHandler.open_long_position`, `EH:MockExecutionHandler.open_short_position`, `EH:MockExecutionHandler.close_position` | fill |
| `debug_execute_portfolio_rebalance.trade_type` | `LONG`, `SHORT`, `REDUCE_LONG`, `REDUCE_SHORT` or `CLOSE`. | label | `EH:BaseExecutionHandler._handle_allocation_change` | fill |
| `debug_execute_portfolio_rebalance.error` | Exception text of a failed order. | text | `EH:MockExecutionHandler.open_long_position`, `EH:MockExecutionHandler.open_short_position` | fill |
| `risk_target_raw` | Risk gate only: the target before the gate (NaN on a NaN forecast). | alloc | `RG:PortfolioRiskGate.apply`, `TB:TradingBot._process_symbol_candle_completion` | close |
| `risk_cap_clamped` | Risk gate only: the cap clamped the target. | bool | `RG:PortfolioRiskGate.apply` | close |
| `risk_killed` | Risk gate only: drawdown kill latched. | bool | `RG:PortfolioRiskGate.apply` | close |
| `risk_drawdown` | Risk gate only: drawdown at this close. | frac | `RG:PortfolioRiskGate.apply` | close |
| `risk_daily_halted` | Risk gate only: daily loss halt latched. | bool | `RG:PortfolioRiskGate.apply` | close |
| `risk_daily_loss` | Risk gate only: loss since the day's anchor. | frac | `RG:PortfolioRiskGate.apply` | close |
| `risk_trip` | Risk gate only: what tripped this bar. | label | `RG:PortfolioRiskGate.apply` | close |
<!-- /data-dictionary -->
<!-- /readers: omit -->

## 2. trade_diagnostics.json (one per variant)

`variants/<variant>/trade_diagnostics.json`, written by `run_protocol` (`RP:main`)
from each window's `trades.json` and `bars.csv`. Trades from all windows, in order.
`summary` is also copied as `protocol_result.yaml` `trade_diagnostics_summary`.

<!-- readers: omit -->
Per-trade labels: in `trade_diagnostics.json` only (no report carries them; the
readers' subset leaves this table out).

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
<!-- /readers: omit -->

Per-trade numbers (the trade_efficiency report aggregates each of them) and the summary.

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

## 6. The five category reports

`artifacts/reports/<category>.yaml` (`BR:build_reports`). With the variant loop: one block per
graded variant under `variants.<variant>`; a single-run report has `slices` at the
top instead. A slice that cannot be built is `{unavailable: true, reason}`.
Reports re-project the blocks above; they add only the hindsight lag and the G7
aggregates. The `mean` / `median` / `p10` / `p90` aggregates (`BR:_aggregate_records`)
are over records, where `n` counts records, numeric or not (A11). A field without a
`category:` prefix is in every report.

<!-- data-dictionary: reports -->
| Field | Meaning | Unit | Code | When known |
|---|---|---|---|---|
| `category` | Report name. | label | `BR:_wrap`, `BR:build_reports` | meta |
| `source_run_id` | Run id. | id | `BR:build_reports` | meta |
| `generated_at` | When built (UTC). | time | `BR:build_reports` | meta |
| `schema_version` | 2 with the variant loop. | int | `BR:build_reports` | meta |
| `variants.<variant>.kind` | Variant kind (base, design, asset) from the variant index. | label | `BR:build_reports` | meta |
| `variants.<variant>.symbol` | Its symbol. | id | `BR:build_reports` | meta |
| `variants.<variant>.status` | `graded` (backtested and graded; not a verdict). | label | `BR:build_reports` | meta |
| `variants.<variant>.coverage` | Partial-coverage note, when given. | text | `BR:build_reports` | meta |
| `variants.<variant>.slices` | The four slices of this variant (the `slices.*` rows below). | map | `BR:build_reports` | run |
| `failed_variants` | {variant: reason} for each variant that produced no graded result. | map | `BR:build_reports` | meta |
| `untested_variants` | {variant: reason} for each variant of the idea not run in this run. | map | `BR:build_reports` | meta |
| `slices.overall` | Whole-variant slice. | map | `BR:_wrap` | run |
| `slices.per_window` | Per protocol window. | list/map | `BR:_wrap` | run |
| `slices.per_regime` | Per regime label. | map | `BR:_wrap` | run |
| `slices.per_symbol` | Per symbol. | map | `BR:_wrap` | run |
| `slices.<slice>.unavailable` | The slice could not be built (any report, any slice). | bool | `BR:_unavailable` | meta |
| `slices.<slice>.reason` | Why. | text | `BR:_unavailable` | meta |
| `slices.overall.unavailable` | Readers' exploration copy only (E-072, `explore_confirm`): `true` in the profitability, trade_efficiency and forecast_power reports, because their `overall` slice is an aggregate over every window, the confirmation windows included. | bool | `BR:_withhold_pooled_overall`, `BR:_unavailable` | meta |
| `slices.overall.reason` | Readers' exploration copy only (E-072): why that `overall` slice is withheld (`WINDOWS_WITHHELD_REASON`). | text | `BR:_withhold_pooled_overall`, `BR:_unavailable` | meta |
| `windows_shown` | Readers' exploration copy only (E-072): the window labels this report was built from; every other window is left out. | list | `BR:build_reports` | meta |
| `profitability: slices.overall.source` | Where the block comes from. | text | `BR:build_profitability_report` | meta |
| `profitability: slices.overall.diagnostics` | Section 5. | map | `BR:build_profitability_report` | run |
| `profitability: slices.overall.verdict` | Legacy verdict (removed when retired). | label | `BR:build_profitability_report` | run |
| `profitability: slices.overall.verdict_reason` | Its text (removed when retired). | text | `BR:build_profitability_report` | run |
| `profitability: slices.per_window[].symbol` | Symbol. | id | `BR:build_profitability_report` | meta |
| `profitability: slices.per_window[].window` | Window label. | label | `BR:build_profitability_report` | meta |
| `profitability: slices.per_window[].run_id` | Window backtest run id (its bars.csv folder). | id | `BR:build_profitability_report` | meta |
| `profitability: slices.per_window[].core` | Section 3. | map | `BR:build_profitability_report` | run |
| `profitability: slices.per_regime.<regime>[].symbol` | Symbol. Each row also carries the window's section 4 `per_regime` fields for this regime. | id | `BR:build_profitability_report` | meta |
| `profitability: slices.per_regime.<regime>[].window` | Window label. | label | `BR:build_profitability_report` | meta |
| `profitability: slices.per_symbol.<symbol>[].window` | Window label (an index of the symbol's windows). | label | `BR:build_profitability_report` | meta |
| `profitability: slices.per_symbol.<symbol>[].run_id` | Window backtest run id. | id | `BR:build_profitability_report` | meta |
| `trade_efficiency: slices.overall.source` | Where the block comes from; the block also carries every `summary` field of section 2. | text | `BR:build_trade_efficiency_report` | meta |
| `trade_efficiency: slices.per_window.<window>.n` | Trades in the window's group. | count | `BR:_aggregate_records` | run |
| `trade_efficiency: slices.per_window.<window>.<trade field>.mean` | Mean of a numeric trade field (section 2) over the window's trades; booleans and labels dropped (A10). | field | `BR:_aggregate_records` | run |
| `trade_efficiency: slices.per_window.<window>.<trade field>.median` | Median, same trades. | field | `BR:_aggregate_records` | run |
| `trade_efficiency: slices.per_window.<window>.<trade field>.p10` | 10th percentile (linear interpolation), same trades. | field | `BR:_aggregate_records` | run |
| `trade_efficiency: slices.per_window.<window>.<trade field>.p90` | 90th percentile (linear interpolation), same trades. | field | `BR:_aggregate_records` | run |
| `trade_efficiency: slices.per_regime.<regime>.n` | Trades in the entry regime's group. | count | `BR:_aggregate_records` | run |
| `trade_efficiency: slices.per_regime.<regime>.<trade field>.mean` | Mean of a numeric trade field (section 2) over the entry regime's trades; booleans and labels dropped (A10). | field | `BR:_aggregate_records` | run |
| `trade_efficiency: slices.per_regime.<regime>.<trade field>.median` | Median, same trades. | field | `BR:_aggregate_records` | run |
| `trade_efficiency: slices.per_regime.<regime>.<trade field>.p10` | 10th percentile (linear interpolation), same trades. | field | `BR:_aggregate_records` | run |
| `trade_efficiency: slices.per_regime.<regime>.<trade field>.p90` | 90th percentile (linear interpolation), same trades. | field | `BR:_aggregate_records` | run |
| `trade_efficiency: slices.per_symbol.<symbol>.n` | Trades in the symbol's group. | count | `BR:_aggregate_records` | run |
| `trade_efficiency: slices.per_symbol.<symbol>.<trade field>.mean` | Mean of a numeric trade field (section 2) over the symbol's trades; booleans and labels dropped (A10). | field | `BR:_aggregate_records` | run |
| `trade_efficiency: slices.per_symbol.<symbol>.<trade field>.median` | Median, same trades. | field | `BR:_aggregate_records` | run |
| `trade_efficiency: slices.per_symbol.<symbol>.<trade field>.p10` | 10th percentile (linear interpolation), same trades. | field | `BR:_aggregate_records` | run |
| `trade_efficiency: slices.per_symbol.<symbol>.<trade field>.p90` | 90th percentile (linear interpolation), same trades. | field | `BR:_aggregate_records` | run |
| `forecast_power: statistic_labels.forecast_return_corr` | What that statistic is (a top-level key of this report, under reader_findings only). | text | `BR:FORECAST_POWER_STATISTIC_LABELS` | meta |
| `forecast_power: statistic_labels.forecast_return_corr_pvalue` | Same. | text | `BR:FORECAST_POWER_STATISTIC_LABELS` | meta |
| `forecast_power: statistic_labels.median_forecast_return_corr` | Same. | text | `BR:FORECAST_POWER_STATISTIC_LABELS` | meta |
| `forecast_power: statistic_labels.prescreen_pooled_ic` | Same. | text | `BR:FORECAST_POWER_STATISTIC_LABELS` | meta |
| `forecast_power: slices.overall.median_forecast_return_corr` | Section 5 field. | corr | `BR:build_forecast_power_report` | after |
| `forecast_power: slices.overall.median_forecast_return_corr_source` | Where it comes from. | text | `BR:build_forecast_power_report` | meta |
| `forecast_power: slices.overall.prescreen_backtest_cross_check` | Legacy block, only when the run had a prescreen (stage removed). | map | `BR:build_forecast_power_report` | run |
| `forecast_power: slices.per_window[].symbol` | Symbol. | id | `BR:build_forecast_power_report` | meta |
| `forecast_power: slices.per_window[].window` | Window label. | label | `BR:build_forecast_power_report` | meta |
| `forecast_power: slices.per_window[].run_id` | Window backtest run id. | id | `BR:build_forecast_power_report` | meta |
| `forecast_power: slices.per_window[].forecast_return_corr` | core.forecast_return_corr of the window. | corr | `BR:build_forecast_power_report` | after |
| `forecast_power: slices.per_window[].forecast_return_corr_pvalue` | core p-value (not block-adjusted). | p | `BR:build_forecast_power_report` | after |
| `forecast_power: slices.per_regime.<regime>[].symbol` | Symbol. Each row also carries the window's section 4 `regime_validity` fields for this regime. | id | `BR:build_forecast_power_report` | meta |
| `forecast_power: slices.per_regime.<regime>[].window` | Window label. | label | `BR:build_forecast_power_report` | meta |
| `forecast_power: slices.per_symbol.<symbol>[].window` | Window label. | label | `BR:build_forecast_power_report` | meta |
| `forecast_power: slices.per_symbol.<symbol>[].forecast_return_corr` | As in per_window. | corr | `BR:build_forecast_power_report` | after |
| `forecast_power: slices.per_symbol.<symbol>[].forecast_return_corr_pvalue` | As in per_window. | p | `BR:build_forecast_power_report` | after |
| `regime_power: slices.overall.note` | Fixed text: what this report computes. | text | `BR:build_regime_power_report` | meta |
| `regime_power: slices.per_window[].symbol` | Symbol. | id | `BR:build_regime_power_report` | meta |
| `regime_power: slices.per_window[].window` | Window label. | label | `BR:build_regime_power_report` | meta |
| `regime_power: slices.per_window[].run_id` | Window backtest run id. | id | `BR:build_regime_power_report` | meta |
| `regime_power: slices.per_window[].per_regime` | Section 4 per_regime of the window. | map | `BR:build_regime_power_report` | run |
| `regime_power: slices.per_window[].regime_validity` | Section 4 regime_validity of the window. | map | `BR:build_regime_power_report` | after |
| `regime_power: slices.per_window[].hindsight_lag` | Lag of the live regime changes behind hindsight direction changes. | map | `BR:build_regime_power_report`, `BR:_compute_hindsight_lag` | after |
| `regime_power: slices.per_window[].hindsight_lag.live_transition_count` | Live label changes (unknown/blank excluded). | count | `BR:_compute_hindsight_lag` | run |
| `regime_power: slices.per_window[].hindsight_lag.hindsight_transition_count` | Changes of the 5-bar-ahead price direction label. | count | `BR:_compute_hindsight_lag` | after |
| `regime_power: slices.per_window[].hindsight_lag.lags_bars` | live index - nearest hindsight index within 20 bars. | bars | `BR:_compute_hindsight_lag` | after |
| `regime_power: slices.per_window[].hindsight_lag.median_lag_bars` | Their median. | bars | `BR:_compute_hindsight_lag` | after |
| `regime_power: slices.per_window[].hindsight_lag.reason` | Why no lag, or why the lag could not be computed. | text | `BR:_compute_hindsight_lag`, `BR:_unavailable` | meta |
| `regime_power: slices.per_window[].hindsight_lag.unavailable` | The window's bars.csv is missing or has no usable close. | bool | `BR:_unavailable` | meta |
| `regime_power: slices.per_regime.<regime>[].symbol` | Symbol. | id | `BR:build_regime_power_report` | meta |
| `regime_power: slices.per_regime.<regime>[].window` | Window label. | label | `BR:build_regime_power_report` | meta |
| `regime_power: slices.per_regime.<regime>[].per_regime` | Section 4 per_regime block of this regime in the window. | map | `BR:build_regime_power_report` | run |
| `regime_power: slices.per_regime.<regime>[].regime_validity` | Section 4 regime_validity block of this regime in the window. | map | `BR:build_regime_power_report` | after |
| `regime_power: slices.per_symbol.<symbol>[]` | The symbol's per_window rows (same fields as `per_window[]`). | list | `BR:build_regime_power_report`, `BR:_wrap` | after |
| `component_attribution: slices.overall.components_discovered` | Component ids found in bars.csv columns. | list | `BR:build_component_attribution_report` | meta |
| `component_attribution: slices.overall.note` | Fixed text. | text | `BR:build_component_attribution_report` | meta |
| `component_attribution: slices.per_window.<window>.<component>.n` | Bar records of the component in the window's bars, warm-up and not-ready bars included (A11). | count | `BR:_aggregate_records` | run |
| `component_attribution: slices.per_window.<window>.<component>.<metric>.mean` | Mean of a bars.csv component metric (`last_history_value`, `post_pipeline_value`, ...) over the window's bars. | field | `BR:_aggregate_records` | run |
| `component_attribution: slices.per_window.<window>.<component>.<metric>.median` | Median, same bars. | field | `BR:_aggregate_records` | run |
| `component_attribution: slices.per_window.<window>.<component>.<metric>.p10` | 10th percentile (linear interpolation), same bars. | field | `BR:_aggregate_records` | run |
| `component_attribution: slices.per_window.<window>.<component>.<metric>.p90` | 90th percentile (linear interpolation), same bars. | field | `BR:_aggregate_records` | run |
| `component_attribution: slices.per_regime.<regime>.<component>.n` | Bar records of the component in the regime's (bar label) bars, warm-up and not-ready bars included (A11). | count | `BR:_aggregate_records` | run |
| `component_attribution: slices.per_regime.<regime>.<component>.<metric>.mean` | Mean of a bars.csv component metric (`last_history_value`, `post_pipeline_value`, ...) over the regime's (bar label) bars. | field | `BR:_aggregate_records` | run |
| `component_attribution: slices.per_regime.<regime>.<component>.<metric>.median` | Median, same bars. | field | `BR:_aggregate_records` | run |
| `component_attribution: slices.per_regime.<regime>.<component>.<metric>.p10` | 10th percentile (linear interpolation), same bars. | field | `BR:_aggregate_records` | run |
| `component_attribution: slices.per_regime.<regime>.<component>.<metric>.p90` | 90th percentile (linear interpolation), same bars. | field | `BR:_aggregate_records` | run |
| `component_attribution: slices.per_symbol.<symbol>.<component>.n` | Bar records of the component in the symbol's bars, warm-up and not-ready bars included (A11). | count | `BR:_aggregate_records` | run |
| `component_attribution: slices.per_symbol.<symbol>.<component>.<metric>.mean` | Mean of a bars.csv component metric (`last_history_value`, `post_pipeline_value`, ...) over the symbol's bars. | field | `BR:_aggregate_records` | run |
| `component_attribution: slices.per_symbol.<symbol>.<component>.<metric>.median` | Median, same bars. | field | `BR:_aggregate_records` | run |
| `component_attribution: slices.per_symbol.<symbol>.<component>.<metric>.p10` | 10th percentile (linear interpolation), same bars. | field | `BR:_aggregate_records` | run |
| `component_attribution: slices.per_symbol.<symbol>.<component>.<metric>.p90` | 90th percentile (linear interpolation), same bars. | field | `BR:_aggregate_records` | run |
<!-- /data-dictionary -->

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
| `grid.<criterion>.<variant>.weight_schedule` | profit_bars cells: the grader's weight schedule. | map | `VE:_evaluate_profit_bars_cell` | meta |
<!-- /data-dictionary -->

## 8. claim_result_digest.yaml

`artifacts/claim_result_digest.yaml`, written by code for the v3 readers (`RF:claim_result_digest`).
Effect sizes are on bars after the fact: `after`.

<!-- data-dictionary: claim_result_digest.yaml -->
| Field | Meaning | Unit | Code | When known |
|---|---|---|---|---|
| `schema_version` | 1. | int | `RF:claim_result_digest` | meta |
| `label` | `measured, not proven`. | text | `RF:claim_result_digest`, `CF:LABEL` | meta |
| `note` | Fixed text (information only). | text | `RF:claim_result_digest` | meta |
| `information_only` | true. | bool | `RF:claim_result_digest` | meta |
| `status` | `error` when the digest could not be built. | label | `RF:claim_result_digest` | meta |
| `detail` | Error text. | text | `RF:claim_result_digest` | meta |
| `approximation` | The run tested an approximation of the idea (nearest build). | map | `RF:claim_result_digest`, `NB:approximation_block` | meta |
| `approximation.line` | One-line summary. | text | `NB:approximation_block` | meta |
| `approximation.n_deviations` | Number of differences. | count | `NB:approximation_block` | meta |
| `approximation.deviations[].clause` | Claim clause approximated. | text | `NB:approximation_block` | meta |
| `approximation.deviations[].built_instead` | What was built. | text | `NB:approximation_block` | meta |
| `approximation.deviations[].missing` | What is missing to build it. | text | `NB:approximation_block` | meta |
| `approximation.deviations[].effect` | Expected effect of the difference. | text | `NB:approximation_block` | meta |
| `approximation.ref` | `artifacts/deviations.yaml`. | path | `NB:approximation_block` | meta |
| `variant_patches` | Each variant's exact change to the base config. | map | `RF:claim_result_digest`, `RF:variant_patches_digest` | meta |
| `variant_patches.note` | Fixed text. | text | `RF:variant_patches_digest` | meta |
| `variant_patches.base_config_ref` | Base config path. | path | `RF:variant_patches_digest` | meta |
| `variant_patches.variants[].variant_id` | Variant id. | id | `RF:variant_patches_digest` | meta |
| `variant_patches.variants[].kind` | Variant kind. | label | `RF:variant_patches_digest` | meta |
| `variant_patches.variants[].symbol` | Symbol. | id | `RF:variant_patches_digest` | meta |
| `variant_patches.variants[].patch[].path` | JSON pointer changed. | path | `RF:variant_patches_digest` | meta |
| `variant_patches.variants[].patch[].value` | New value. | value | `RF:variant_patches_digest` | meta |
| `statement` | The claim, verbatim from the card. | text | `RF:claim_result_digest` | meta |
| `kind` | Claim kind. | label | `RF:claim_result_digest` | meta |
| `block_visibility` | Whether a test reads the block (ok / blind / not_applicable). | label | `RF:claim_result_digest` | meta |
| `manifest_kind` | Block kind of the manifest (forecast / regime). | label | `RF:claim_result_digest` | meta |
| `statistics_note` | Fixed text on the statistics. | text | `RF:claim_result_digest` | meta |
| `tests[].name` | Test name. | id | `RF:claim_result_digest` | meta |
| `tests[].spec_hash` | Hash of the test spec. | hash | `RF:claim_result_digest` | meta |
| `tests[].statistic` | `rank_ic`, `mean_diff`, `hit_rate` or `decay_curve`. | label | `RF:claim_result_digest` | meta |
| `tests[].statistic_label` | What that statistic is. | text | `RF:claim_result_digest` | meta |
| `tests[].direction` | `greater` or `less`. | label | `RF:claim_result_digest` | meta |
| `tests[].selector` | Which bars (card spec; reads bar t only, `CT:SELECTORS`). | map | `RF:claim_result_digest` | meta |
| `tests[].outcome` | The forward outcome and horizons (card spec, `CT:OUTCOMES`). | map | `RF:claim_result_digest` | meta |
| `tests[].baseline` | Reference bars (card spec, `CT:BASELINES`). | map | `RF:claim_result_digest` | meta |
| `claim_status` | Run status from claim_measurement.yaml (`absent` without one). | label | `RF:claim_result_digest` | run |
| `reason` | Its reason. | text | `RF:claim_result_digest` | meta |
| `variants.<variant>.status` | `measured`, `no_events` or `not_measured`. | label | `RF:_variant_digest` | run |
| `variants.<variant>.reason` | Why not measured (`stale` = not this attempt's bars). | text | `RF:_variant_digest` | meta |
| `variants.<variant>.detail` | Detail of a stale reason. | text | `RF:_variant_digest` | meta |
| `variants.<variant>.tests.<test>.status` | Test status. | label | `CF:_compact_test` | run |
| `variants.<variant>.tests.<test>.spec_hash` | Spec hash. | hash | `CF:_compact_test` | meta |
| `variants.<variant>.tests.<test>.reason` | Why not measured. | text | `CF:_compact_test` | meta |
| `variants.<variant>.tests.<test>.statistic_label` | What the effect is. | text | `RF:_variant_digest` | meta |
| `variants.<variant>.tests.<test>.peak_horizon` | decay_curve: horizon of the largest claim-signed effect. | bars | `CF:_compact_test` | after |
| `variants.<variant>.tests.<test>.floor_not_met` | Floors of the card not reached. | list | `CF:_compact_test` | run |
| `variants.<variant>.tests.<test>.horizons.<h>.effect` | The test's statistic at horizon h over all windows (6 significant digits, raw sign). | stat | `CF:_compact_test`, `CM:measure_test` | after |
| `variants.<variant>.tests.<test>.horizons.<h>.n_events` | Selected bars with an outcome. | count | `CF:_compact_test` | after |
| `variants.<variant>.tests.<test>.horizons.<h>.windows_claimed_sign` | Windows whose effect has the claimed sign. | count | `CF:_compact_test` | after |
| `variants.<variant>.tests.<test>.horizons.<h>.windows_with_value` | Windows with a defined effect. | count | `CF:_compact_test` | after |
| `variants.<variant>.tests.<test>.horizons.<h>.per_coin.<symbol>.effect` | `effect` for this coin's bars (only with several coins). | stat | `CF:_compact_test` | after |
| `variants.<variant>.tests.<test>.horizons.<h>.per_coin.<symbol>.n_events` | `n_events` for this coin. | count | `CF:_compact_test` | after |
| `variants.<variant>.tests.<test>.horizons.<h>.per_coin.<symbol>.windows_claimed_sign` | `windows_claimed_sign` for this coin. | count | `CF:_compact_test` | after |
| `variants.<variant>.tests.<test>.horizons.<h>.per_coin.<symbol>.windows_with_value` | `windows_with_value` for this coin. | count | `CF:_compact_test` | after |
<!-- /data-dictionary -->

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

## Not recorded today

These do not exist in any file the AI steps read. Do not infer them.

- **Why a forecast is zero, or why no trade happened** (E-027). bars.csv shows the
  warm-up (`debug_info.error`), a component without history
  (`not_ready_component`) and a risk-manager rejection
  (`approved_rebalance: false` with its `controls`), but NOT: a NaN forecast that
  was held (only counted in metrics.json `nan_forecast`), a gap tier (middle-tier
  entry block, large-tier forced flatten; gap events only in metrics.json
  `data_quality`), a risk-gate kill, or the end-of-backtest forced close (merged
  into the last row, `PI:PortfolioStateTracker.record_state`). The target allocation is not a column.
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
