# Data dictionary: what the AI steps read

E-073 step 1 (P-CUL-81, D-081). Every field of the run outputs the readers and the
other AI steps read: what it means, its unit, the code that computes or writes it,
and **when it is known**. Audited against the engine on 2026-10-08; the
discrepancies found are in [Audit findings](#audit-findings) (not fixed here).
`tests/test_e073_data_dictionary.py` derives each field list from the code that
writes it and fails when a field is missing here or an entry here is no longer
written.

**Readers:** use this file to know what a field means before you cite it. A number
whose field says `after` or `run` was computed with hindsight: it can describe a
result, never be a signal input. Fields listed under [Not recorded](#not-recorded-today)
do not exist; never infer them.

## How to read it

- **Time.** A bar's `timestamp` is the bar's **start** (`DM:479`, `DM:613`). The
  engine sees the bar when it closes (`DM:535`), decides on that close and fills
  at that same close plus slippage (`EH:369`, `EH:384`). A trade's `entry_time`
  / `exit_time` is that decision bar's start timestamp (`EH:373`).
- **When known** (last column):
  `close` = known at this bar's close, before its trade (usable for this bar's decision);
  `fill` = this bar's own trade or its result (known right after the decision, never its input);
  `exit` = known when the trade (one LIFO-matched lot) is closed;
  `after` = uses later bars (hindsight; never a signal input);
  `run` = an aggregate over a window, a variant or the run, known after it;
  `end` = the value at the end of the run, repeated on every row (a defect, A1);
  `meta` = identifier, label or configuration.
- **A "trade"** is one LIFO-matched lot (`PM:437`), not one entry-to-flat round
  trip: a partial reduction closes a trade.
- **Units.** `%` = percent (1.0 = one percent); `bps` = basis points; `frac` =
  fraction (0.01 = one percent); `alloc` = position value / portfolio value
  (1.0 = 100% long, -1.0 = 100% short); `forecast` = units on the -20..+20 scale
  (10 = 100% allocation, `FM:19`); `USDT` = quote currency of the simulated
  account (starts at 1000); `bars` = bars of the run's timeframe.
- **Placeholders** in a field path: `<variant>`, `<symbol>`, `<window>`,
  `<regime>`, `<component>` (a component `id` of the config), `<metric>`,
  `<asset>` (`USDT` or the traded symbol), `<criterion>`, `<era>`, `<test>`,
  `<h>` (a horizon, in bars), `<stat>` (`mean`/`median`/`p10`/`p90`),
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

## 1. bars.csv (one per window and variant)

`variants/<variant>/results/<window run id>/bars.csv`: one row per traded bar of
the window (warm-up bars are not written, `TB:403`). Built from every
`record_state` row (`TB:589`, `PI:429`), nested dicts flattened to dotted columns
(`PI:400`, `BT:452`), rounded to 6 decimals (`RA:195`). Columns appear only when
the run produces them (a feed column only with that feed; `risk_*` only with the
portfolio risk gate, which `run_protocol` never passes).

<!-- data-dictionary: bars.csv -->
| Field | Meaning | Unit | Code | When known |
|---|---|---|---|---|
| `timestamp` | Bar start time (UTC, naive). | time | `DM:479` | close |
| `open` | First price of the bar. | price | `DM:480` | close |
| `high` | Highest price of the bar. | price | `DM:481` | close |
| `low` | Lowest price of the bar. | price | `DM:482` | close |
| `close` | Last price of the bar; the decision and fill price. | price | `DM:483` | close |
| `volume` | Traded volume of the bar. | base units | `DM:484` | close |
| `fear_greed` | Fear and Greed index, latest value published at least 1 day before the bar start (as-of merge, publication delay 86400 s). | index 0-100 | `FR:48`, `DM:353` | close |
| `funding_rate` | Latest perpetual funding rate settled at or before the bar start (carried forward). | frac per settlement | `FR:43`, `DM:353` | close |
| `<reserved feed>` | A reserved feed's column (whale-footprint features), only when a caller registers it. | feed | `FR:116` | close |
| `forecast` | The strategy's final forecast for the bar, clipped to -20..+20; 0.0 while not ready or on an error. | forecast | `SE:572`, `SB:37`, `SB:373` | close |
| `confidence` | Always 0.0 (A2). | 0-1 | `MS:202` | meta |
| `regime` | Regime label used this bar (`trending`, `mean_reversion`, `chop`, `unknown`), or `NOT_READY` / `ERROR`. | label | `RE:116`, `SB:377`, `SB:401` | close |
| `strategy` | Always empty (A2). | label | `MS:202` | meta |
| `debug_info.regime` | Same as `regime` on a ready bar. | label | `MS:194` | close |
| `debug_info.forecast_delta` | This bar's forecast minus the previous ready bar's forecast. | forecast | `MS:190` | close |
| `debug_info.regime_scores` | Present instead of the per-regime columns when no bar had scores (threshold_rules mode): the text `{}`. | text | `MS:196` | close |
| `debug_info.regime_scores.<regime>` | Weighted regime score (score / score_product modes only). | score | `RE:194`, `RE:219` | close |
| `debug_info.regime_margin` | Best score minus second best (score modes only; empty in threshold_rules). | score | `RE:196`, `RE:221` | close |
| `debug_info.bars_in_regime` | Consecutive bars in the current regime, this bar included. | bars | `RE:241` | close |
| `debug_info.components` | Present instead of the per-component columns when no bar had component values: the text `{}`. | text | `MS:199` | close |
| `debug_info.components.<component>.last_history_value` | The component's latest raw output (before its transform pipeline). | component | `SE:596`, `SE:513` | close |
| `debug_info.components.<component>.post_pipeline_value` | The component's value after its transform pipeline. | forecast | `SE:597`, `SE:514` | close |
| `debug_info.components.<component>.weight_normalized` | Its weight / sum of the regime's weights. | frac | `SE:598`, `SE:515` | meta |
| `debug_info.components.<component>.weighted_contribution` | weight_normalized x post_pipeline_value; the sum over components (clipped) is the forecast. | forecast | `SE:599`, `SE:516` | close |
| `debug_info.components.<component>.active` | Block combiner only: 1.0 when the block is active this bar. | 0/1 | `SE:517` | close |
| `debug_info.components.not_ready_component` | Id of the first component without 2 values of history; the forecast is then 0.0. | id | `SE:591` | close |
| `debug_info.components.not_ready_block` | Same for a block of the block combiner. | id | `SE:505` | close |
| `debug_info.error` | Why the strategy gave 0.0: `Strategy not ready` (warm-up) or the exception text. | text | `SB:380`, `SB:403` | close |
| `total_portfolio_value` | Account value at this close, before this bar's trade (cash minus borrowed plus position x close; funding accrued first when modelled). | USDT | `TB:424`, `PI:253` | close |
| `portfolio_value` | Copy of `total_portfolio_value`. | USDT | `BT:418` | close |
| `previous_allocation` | Position value / account value at this close, before the trade. | alloc | `TB:435`, `PI:313` | close |
| `allocation_change` | Target allocation (forecast / 10, or the held allocation on a NaN forecast, 0 under a forced flatten) minus `previous_allocation`; set to 0 when a gap middle tier blocks a new entry. The target itself is not recorded. | alloc | `TB:443`, `TB:496`, `FM:58` | close |
| `approved_rebalance` | Risk manager's answer when `allocation_change` is non-zero (empty otherwise, and on a forced flatten). | bool | `TB:554`, `TB:596` | fill |
| `succcess_execute_portfolio_rebalance` | The order succeeded (empty when no order was attempted). Name misspelled in code (A3). | bool | `TB:598`, `TB:728` | fill |
| `postRebalance_total_value` | Account value after this bar's trade and its commission, at this close. | USDT | `TB:582` | fill |
| `postRebalance_current_allocation` | Allocation after this bar's trade. | alloc | `TB:584` | fill |
| `balances.<asset>.free` | Should be the asset held before the trade; is the END-of-run balance on every row (A1). | asset units | `TB:410`, `PI:330` | end |
| `balances.<asset>.locked` | Should be the asset borrowed (short or margin) before the trade; END-of-run value (A1). | asset units | `TB:410`, `PI:330` | end |
| `postRebalance_balances.<asset>.free` | Should be the asset held after the trade; END-of-run value (A1). | asset units | `TB:581` | end |
| `postRebalance_balances.<asset>.locked` | Should be the asset borrowed after the trade; END-of-run value (A1). | asset units | `TB:581` | end |
| `debug_approve_allocation_change` | Present instead of the dotted columns when no bar asked the risk manager: the text `{}`. | text | `TB:597` | fill |
| `debug_approve_allocation_change.symbol` | Symbol checked by the risk manager. | id | `RM:29` | fill |
| `debug_approve_allocation_change.time` | Bar timestamp checked. | time | `RM:28` | fill |
| `debug_approve_allocation_change.controls.max_allocation_change.passed` | abs(change) <= max (config `risk_management.controls`). Empty when an earlier control already failed. | bool | `RM:42` | fill |
| `debug_approve_allocation_change.controls.min_allocation_change.passed` | abs(change) >= threshold (default 0.20): the no-trade band. | bool | `RM:48` | fill |
| `debug_execute_portfolio_rebalance` | Present instead of the dotted columns when no order ran: the text `{}`. | text | `TB:599` | fill |
| `debug_execute_portfolio_rebalance.symbol` | Symbol of the order. | id | `EH:374` | fill |
| `debug_execute_portfolio_rebalance.price` | Fill price: close x (1 +/- slippage bps / 10000). | price | `EH:369`, `EH:384`, `EH:411` | fill |
| `debug_execute_portfolio_rebalance.quantity` | Order size: positive for LONG/SHORT/REDUCE_*, the signed position for CLOSE (A13). | base units | `EH:374`, `EH:389`, `EH:420` | fill |
| `debug_execute_portfolio_rebalance.trade_type` | `LONG`, `SHORT`, `REDUCE_LONG`, `REDUCE_SHORT` or `CLOSE`. | label | `EH:67` | fill |
| `debug_execute_portfolio_rebalance.error` | Exception text of a failed order. | text | `EH:377`, `EH:393` | fill |
| `risk_target_raw` | Risk gate only: the target before the gate (NaN on a NaN forecast). | alloc | `RG:309`, `TB:484` | close |
| `risk_cap_clamped` | Risk gate only: the cap clamped the target. | bool | `RG:309` | close |
| `risk_killed` | Risk gate only: drawdown kill latched. | bool | `RG:311` | close |
| `risk_drawdown` | Risk gate only: drawdown at this close. | frac | `RG:312` | close |
| `risk_daily_halted` | Risk gate only: daily loss halt latched. | bool | `RG:314` | close |
| `risk_daily_loss` | Risk gate only: loss since the day's anchor. | frac | `RG:315` | close |
| `risk_trip` | Risk gate only: what tripped this bar. | label | `RG:317` | close |
<!-- /data-dictionary -->

## 2. trade_diagnostics.json (one per variant)

`variants/<variant>/trade_diagnostics.json`, written by `run_protocol` (`RP:2533`)
from each window's `trades.json` and `bars.csv`. Trades from all windows, in order.
`summary` is also copied as `protocol_result.yaml` `trade_diagnostics_summary`.

<!-- data-dictionary: trade_diagnostics.json -->
| Field | Meaning | Unit | Code | When known |
|---|---|---|---|---|
| `trades[]` | One record per trade (LIFO lot). | list | `RP:650` | exit |
| `trades[].trade_id` | Engine trade id. | id | `RP:651` | meta |
| `trades[].symbol` | Symbol. | id | `RP:652` | meta |
| `trades[].window` | Protocol window label. | label | `RP:653` | meta |
| `trades[].regime_at_entry` | Regime label at the entry bar. | label | `RP:654` | close |
| `trades[].direction` | `long` or `short`. | label | `RP:655` | close |
| `trades[].entry_time` | Entry bar start timestamp (fill at that bar's close). | time | `RP:656`, `EH:373` | close |
| `trades[].exit_time` | Exit bar start timestamp. | time | `RP:657` | exit |
| `trades[].holding_bars` | exit_idx - entry_idx, at least 1. | bars | `RP:627` | exit |
| `trades[].realized_return` | Position return before commission: exit/entry - 1 (sign by side). Slippage is inside the prices. Not weighted by size. | % | `RP:661`, `PM:161` | exit |
| `trades[].profitable_net` | Position return net of both commissions > 0. | bool | `RP:665`, `PM:248` | exit |
| `trades[].net_portfolio_return_pct` | Net PnL of the lot / account value at entry. | % | `RP:666`, `PM:225` | exit |
| `trades[].mae` | Largest adverse move from entry over the entry..exit bars (highs/lows), entry bar included (A6). | % | `RP:306` | after |
| `trades[].mfe` | Largest favourable move, same bars (A6). | % | `RP:306` | after |
| `trades[].entry_efficiency` | Return from the actual entry minus return if entered at the next bar's open. Measures the entry slippage (A4). | % | `RP:328` | after |
| `trades[].exit_efficiency` | Realized return / best return available over the holding bars (hindsight optimum; A6). | ratio | `RP:350` | after |
| `trades[].exit_reason` | `end_of_window` when the exit is the window's last bar, else `signal_flip` by default (A5). | label | `RP:489` | exit |
| `trades[].post_exit_return_5bars` | Close 5 bars after exit vs exit price, signed by side. | % | `RP:378` | after |
| `trades[].post_exit_return_20bars` | Same, 20 bars. | % | `RP:378` | after |
| `trades[].cost_paid` | Configured one-way fee x 2 (A7): not the trade's actual cost. | bps | `RP:538` | meta |
| `trades[].entry_price` | Fill price at entry (slippage included). | price | `RP:677` | close |
| `trades[].exit_price` | Fill price at exit (slippage included). | price | `RP:678` | exit |
| `trades[].entry_idx` | Entry row in this window's bars.csv (-1 when not found). Window-local. | row | `RP:599` | meta |
| `trades[].exit_idx` | Exit row in this window's bars.csv. Window-local. | row | `RP:600` | meta |
| `trades[].pre_entry_drift_pct` | Move of the 6 bars before entry into the entry price, signed by side. | % | `RP:409` | close |
| `trades[].entered_earlier_better` | Previous bar's close was a better price than the fill. | bool | `RP:431` | close |
| `trades[].post_exit_drift_pct` | Move of the 6 bars after exit, signed by side. | % | `RP:447` | after |
| `trades[].held_longer_better` | Next bar's close was a better exit than the fill. | bool | `RP:470` | after |
| `summary` | Aggregates over all trades of the variant (empty without trades). | map | `RP:970` | run |
| `summary.mae_mfe_ratio_median` | Median of mae/mfe over trades with mfe > 0. | ratio | `RP:995` | run |
| `summary.entry_efficiency_median` | Median entry_efficiency. | % | `RP:1088` | run |
| `summary.exit_efficiency_median` | Median exit_efficiency. | ratio | `RP:1089` | run |
| `summary.win_rate_net` | Share of trades with profitable_net. | % | `RP:1043` | run |
| `summary.holding_period_distribution` | Holding bars percentiles (floor nearest rank). | map | `RP:1052` | run |
| `summary.holding_period_distribution.p10_bars` | 10th percentile. | bars | `RP:1092` | run |
| `summary.holding_period_distribution.p50_bars` | Median. | bars | `RP:1093` | run |
| `summary.holding_period_distribution.p90_bars` | 90th percentile. | bars | `RP:1094` | run |
| `summary.pnl_concentration` | How much of the summed net return comes from the extremes. | map | `RP:1002` | run |
| `summary.pnl_concentration.pct_pnl_from_top_decile_trades` | Sum of the best 10% of net_portfolio_return_pct / sum of all, x100 (null when the sum is 0). | % | `RP:1008` | run |
| `summary.pnl_concentration.pct_pnl_from_worst_decile_trades` | Same for the worst 10% (sign follows the total). | % | `RP:1013` | run |
| `summary.exit_reason_breakdown` | Share of trades per exit_reason (A5). | map | `RP:1100` | run |
| `summary.exit_reason_breakdown.signal_flip_pct` | Share labelled signal_flip. | % | `RP:1101` | run |
| `summary.exit_reason_breakdown.stop_loss_pct` | Always 0: nothing produces stop_loss (A5). | % | `RP:1102` | run |
| `summary.exit_reason_breakdown.time_stop_pct` | Always 0 (A5). | % | `RP:1103` | run |
| `summary.exit_reason_breakdown.end_of_window_pct` | Share ending on the window's last bar. | % | `RP:1104` | run |
| `summary.exit_reason_breakdown.inferred_classification_pct` | Share labelled by inference (= signal_flip_pct). | % | `RP:1108` | run |
| `summary.stop_loss_recovery_rate` | Always 0 (A5). | frac | `RP:1027` | run |
| `summary.per_trade_expectancy_bps` | Net portfolio return per trade. | map | `RP:1111` | run |
| `summary.per_trade_expectancy_bps.mean` | Mean of net_portfolio_return_pct x 100. | bps | `RP:1035` | run |
| `summary.per_trade_expectancy_bps.se` | Standard error of that mean. | bps | `RP:1036` | run |
| `summary.per_trade_expectancy_bps.t_stat` | mean / se (trades treated as independent). | t | `RP:1038` | run |
| `summary.per_trade_expectancy_bps.n` | Number of trades. | count | `RP:1115` | run |
| `summary.zero_trade_slot_pct` | Share of windows with no trade. | % | `RP:1046` | run |
| `summary.fee_reduction_metrics` | Four what-if levers on trading less (E-016). | map | `RP:859` | run |
| `summary.fee_reduction_metrics.lookback_bars` | N used by the levers (6). | bars | `RP:69` | meta |
| `summary.fee_reduction_metrics.combine_nearby_trades` | Same-direction re-entries. | map | `RP:908` | run |
| `summary.fee_reduction_metrics.combine_nearby_trades.same_direction_reentry_rate` | Share of consecutive trade pairs re-entering the same direction within 6 bars of the previous exit. | frac | `RP:879` | run |
| `summary.fee_reduction_metrics.combine_nearby_trades.avg_reentry_gap_bars` | Mean gap of those re-entries. | bars | `RP:880` | run |
| `summary.fee_reduction_metrics.exit_later` | Holding longer. | map | `RP:912` | after |
| `summary.fee_reduction_metrics.exit_later.avg_post_exit_drift_pct` | Mean post_exit_drift_pct. | % | `RP:885` | after |
| `summary.fee_reduction_metrics.exit_later.pct_better_exit_1bar_later` | Share with held_longer_better. | % | `RP:886` | after |
| `summary.fee_reduction_metrics.enter_earlier` | Entering earlier. | map | `RP:916` | run |
| `summary.fee_reduction_metrics.enter_earlier.avg_pre_entry_drift_pct` | Mean pre_entry_drift_pct. | % | `RP:894` | run |
| `summary.fee_reduction_metrics.enter_earlier.pct_better_entry_1bar_earlier` | Share with entered_earlier_better. | % | `RP:895` | run |
| `summary.fee_reduction_metrics.trade_less_often` | Whipsaw. | map | `RP:920` | run |
| `summary.fee_reduction_metrics.trade_less_often.boundary_recross_rate` | Mean over windows of the share of forecast crossings of the boundary level repeated within 6 bars. | frac | `RP:767`, `RP:903` | run |
| `summary.fee_reduction_metrics.trade_less_often.frequency_vs_volatility_ratio` | Mean over windows of trades per day / stdev of bar returns. | ratio | `RP:794`, `RP:904` | run |
| `summary.realized_edge_to_cost_ratio` | Mean realized_return (bps) / mean cost_paid over trades with a cost (A7). | ratio | `CH:116` | run |
| `summary.cost_components_measured` | Which costs are itemised in the trade records. | map | `RP:927` | meta |
| `summary.cost_components_measured.fees` | Every record carries cost_paid. | bool | `RP:964` | meta |
| `summary.cost_components_measured.funding` | Always false: trade records carry no funding (and run_protocol does not model funding). | bool | `RP:965` | meta |
| `summary.cost_components_measured.slippage` | Always false: slippage is inside the fill prices. | bool | `RP:966` | meta |
<!-- /data-dictionary -->

## 3. The window `core` block

`metrics.json` `core` of each window, copied into `protocol_result.yaml`
`results[].core` and the reports (`per_window[].core`). Trade-based fields use the
trade-exit basis (A9). `run_protocol` sets `sharpe` to null when the window has
fewer than 5 trades (`RP:2474`).

<!-- data-dictionary: core -->
| Field | Meaning | Unit | Code | When known |
|---|---|---|---|---|
| `net_return_pct` | First trade's entry account value to last trade's exit account value; 0.0 without trades (A8). | % | `PM:1407`, `RA:539` | run |
| `sharpe` | Annualised (sqrt 365) Sharpe of daily summed trade returns booked on exit dates, first to last exit; 0.0 when undefined (A8, A9). | ratio | `PM:1464`, `RA:540` | run |
| `max_drawdown_pct` | Drawdown of the trade-by-trade compounded curve (exit order); 0.0 without trades. | % | `PM:1444`, `RA:541` | run |
| `trade_count` | Number of trades (LIFO lots). | count | `RA:542` | run |
| `win_rate` | Share of trades with profitable_net; 0.0 without trades. | % | `PM:1377`, `RA:543` | run |
| `avg_trade_net_pnl` | Mean net PnL per trade. | USDT | `RA:233` | run |
| `fees_paid` | Sum of commissions. | USDT | `RA:236` | run |
| `gross_pnl` | Sum of PnL before commission (after slippage). | USDT | `RA:240` | run |
| `net_pnl` | Sum of PnL after commission. | USDT | `RA:241` | run |
| `cost_drag_pct` | (gross - net) / abs(gross) x 100. | % | `RA:242` | run |
| `forecast_return_corr` | Pearson correlation of forecast[t] with close[t+1]/close[t]-1 on bars with forecast != 0, gap-spanning pairs dropped. | corr | `RA:278`, `RA:330` | after |
| `forecast_return_corr_pvalue` | t-test p-value of that correlation (independent bars). | p | `RA:336` | after |
| `forecast_return_corr_pvalue_block_adjusted` | Same, with daily blocks (fewer effective observations). | p | `RA:359` | after |
| `forecast_return_corr_n_eff` | Effective sample size used by that p-value. | count | `RA:363` | after |
| `forecast_return_corr_all_bars` | Same correlation on all bars (forecast 0 included). | corr | `RA:383` | after |
| `forecast_return_corr_all_bars_pvalue_block_adjusted` | Its block-adjusted p-value. | p | `RA:405` | after |
| `forecast_return_corr_all_bars_n_eff` | Its effective sample size. | count | `RA:409` | after |
| `gap_skipped_pairs` | Bar pairs dropped because the next row is not the next bar. | count | `RA:303` | run |
| `gap_skipped_pct` | Those pairs / pairs reached. | % | `RA:317` | run |
| `avg_trade_duration_bars` | Mean trade duration / median bar spacing. | bars | `RA:412` | run |
| `sigma_bar_bps` | Stdev of next-bar returns over all bars. | bps | `RA:327`, `SS:295` | after |
| `sigma_bar_bps_is_placeholder` | sigma could not be measured and a default was used. | bool | `SS:295` | meta |
| `post_backtest_cost_check` | Estimated edge vs cost from IC x sigma x sqrt(holding) (prescreen formula). | map | `RA:441`, `SS:313` | run |
| `post_backtest_cost_check.estimated_gross_edge_bps_per_trade` | Estimated (here) or measured (`_real`) gross edge per trade. | bps | `SS:340`, `RA:513` | run |
| `post_backtest_cost_check.cost_bps_per_trade` | Round-trip cost per trade (cost model, or measured commission for `_real`). | bps | `SS:341`, `RA:514` | run |
| `post_backtest_cost_check.edge_to_cost_ratio` | abs(edge) / cost. | ratio | `SS:342`, `RA:515` | run |
| `post_backtest_cost_check.safety_factor_required` | Ratio needed to pass (cost model, default 2.0). | ratio | `RA:516` | meta |
| `post_backtest_cost_check.pass` | ratio >= safety factor. | bool | `RA:517` | run |
| `post_backtest_cost_check.basis` | `real` on the `_real` block. | label | `RA:518` | meta |
| `post_backtest_route` | Legacy route label from the estimated check (removed from reports when the legacy verdict is retired). | label | `RA:450` | run |
| `post_backtest_route_rationale` | Its text. | text | `RA:450` | run |
| `real_round_trip_cost_bps` | Mean (entry + exit commission rate) per trade. | bps | `RA:495` | run |
| `real_gross_edge_bps_per_trade` | Mean position return before commission per trade. | bps | `RA:498` | run |
| `post_backtest_cost_check_real` | The same check on measured numbers (same fields as `post_backtest_cost_check`). | map | `RA:507` | run |
| `post_backtest_route_real` | Legacy route from the measured check (removed when the legacy verdict is retired). | label | `RA:531` | run |
| `post_backtest_route_real_rationale` | Its text. | text | `RA:531` | run |
| `sharpe_annualization` | Fixed text: sqrt(365) daily Sharpe. | text | `RA:164` | meta |
<!-- /data-dictionary -->

## 4. Per-regime blocks

`per_regime.<regime>` (`RA:580`): bars grouped by the `regime` column, trades by
their entry regime. `regime_validity.<regime>` (`RA:640`).

<!-- data-dictionary: per_regime -->
| Field | Meaning | Unit | Code | When known |
|---|---|---|---|---|
| `<regime>.bar_count` | Bars with this label. | count | `RA:586` | run |
| `<regime>.avg_forecast` | Mean forecast on those bars. | forecast | `RA:588` | run |
| `<regime>.trade_count` | Trades entered in this regime. | count | `RA:593` | run |
| `<regime>.total_net_pnl` | Their summed net PnL. | USDT | `RA:594` | run |
<!-- /data-dictionary -->

<!-- data-dictionary: regime_validity -->
| Field | Meaning | Unit | Code | When known |
|---|---|---|---|---|
| `<regime>.forward_return_mean` | Mean close[t+1]/close[t]-1 over bars with this label (next row, no gap filter: A12). | frac | `RA:649` | after |
| `<regime>.forward_return_std` | Its stdev. | frac | `RA:657` | after |
| `<regime>.n_bars` | Bars counted. | count | `RA:658` | run |
| `<regime>.informative` | abs(mean) >= 0.0001. | bool | `RA:659` | after |
<!-- /data-dictionary -->

## 5. `diagnostics` (protocol_result.yaml hypothesis_verdict.diagnostics)

Over all windows of a variant (`RP:1681`); the profitability report's
`overall.diagnostics`.

<!-- data-dictionary: diagnostics -->
| Field | Meaning | Unit | Code | When known |
|---|---|---|---|---|
| `median_gross_pnl` | Median over windows of core.gross_pnl. | USDT | `RP:1749` | run |
| `median_cost_drag_pct` | Median of core.cost_drag_pct. | % | `RP:1750` | run |
| `median_forecast_return_corr` | Median of core.forecast_return_corr (Pearson, active bars). | corr | `RP:1751` | after |
| `median_avg_trade_duration_bars` | Median of core.avg_trade_duration_bars. | bars | `RP:1752` | run |
| `uninformative_regimes` | Regimes with informative false in any window. | list | `RP:1722` | after |
| `win_rate_vs_sharpe` | Legacy text from the old rule set (`N/A (no rule set)` without one). | text | `RP:1732` | meta |
| `below_floor_pct` | Share of windows with fewer than 5 trades. | % | `RP:1746` | run |
| `post_backtest_route_real` | Most common core route (ties broken by precedence). Legacy, removed when retired. | label | `RP:1716` | run |
| `post_backtest_route_real_tied` | That choice was a tie. | bool | `RP:1716` | run |
| `cost_dominated_real` | That route is a cost-hurdle route. Legacy, removed when retired. | bool | `RP:1717` | run |
| `per_trade_expectancy_bps` | Copy of trade_diagnostics summary.per_trade_expectancy_bps. | map | `RP:1763` | run |
| `zero_trade_slot_pct` | Copy of summary.zero_trade_slot_pct. | % | `RP:1764` | run |
| `fee_reduction_metrics` | Copy of summary.fee_reduction_metrics. | map | `RP:1769` | run |
<!-- /data-dictionary -->

## 6. The five category reports

`artifacts/reports/<category>.yaml` (`BR:896`). With the variant loop: one block per
graded variant under `variants.<variant>`; a single-run report has `slices` at the
top instead. A slice that cannot be built is `{unavailable: true, reason}`.
Reports re-project the blocks above; they add only the hindsight lag and the G7
aggregates. `<stat>` aggregates (`BR:212`) are over records, where `n` counts
records, numeric or not (A11).

<!-- data-dictionary: reports -->
| Field | Meaning | Unit | Code | When known |
|---|---|---|---|---|
| `category` | Report name. | label | `BR:156` | meta |
| `source_run_id` | Run id. | id | `BR:977` | meta |
| `generated_at` | When built (UTC). | time | `BR:978` | meta |
| `schema_version` | 2 with the variant loop. | int | `BR:1003` | meta |
| `variants.<variant>.kind` | Variant kind (base, design, asset) from the variant index. | label | `BR:992` | meta |
| `variants.<variant>.symbol` | Its symbol. | id | `BR:993` | meta |
| `variants.<variant>.status` | `graded` (backtested and graded; not a verdict). | label | `BR:994` | meta |
| `variants.<variant>.coverage` | Partial-coverage note, when given. | text | `BR:995` | meta |
| `variants.<variant>.slices` | The four slices of this variant. | map | `BR:997` | run |
| `failed_variants.<variant>` | Reason a variant produced no graded result. | text | `BR:1007` | meta |
| `untested_variants.<variant>` | Reason a variant of the idea was not run. | text | `BR:1009` | meta |
| `statistic_labels.forecast_return_corr` | What that statistic is (forecast_power, under reader_findings). | text | `BR:879` | meta |
| `statistic_labels.forecast_return_corr_pvalue` | Same. | text | `BR:881` | meta |
| `statistic_labels.median_forecast_return_corr` | Same. | text | `BR:882` | meta |
| `statistic_labels.prescreen_pooled_ic` | Same. | text | `BR:887` | meta |
| `slices.overall` | Whole-variant slice. | map | `BR:158` | run |
| `slices.per_window` | Per protocol window. | list/map | `BR:159` | run |
| `slices.per_regime` | Per regime label. | map | `BR:160` | run |
| `slices.per_symbol` | Per symbol. | map | `BR:161` | run |
| `<slice>.unavailable` | The slice could not be built. | bool | `BR:151` | meta |
| `<slice>.reason` | Why. | text | `BR:151` | meta |
| `profitability: slices.overall.source` | Where the block comes from. | text | `BR:352` | meta |
| `profitability: slices.overall.diagnostics` | Section 5. | map | `BR:354` | run |
| `profitability: slices.overall.verdict` | Legacy verdict (removed when retired). | label | `BR:355` | run |
| `profitability: slices.overall.verdict_reason` | Its text (removed when retired). | text | `BR:356` | run |
| `profitability: slices.per_window[].symbol` | Symbol. | id | `BR:368` | meta |
| `profitability: slices.per_window[].window` | Window label. | label | `BR:368` | meta |
| `profitability: slices.per_window[].run_id` | Window backtest run id (its bars.csv folder). | id | `BR:368` | meta |
| `profitability: slices.per_window[].core` | Section 3. | map | `BR:369` | run |
| `profitability: slices.per_regime.<regime>[]` | symbol, window and the section 4 per_regime fields. | list | `BR:376` | run |
| `profitability: slices.per_symbol.<symbol>[]` | window and run_id of each window (an index). | list | `BR:387` | meta |
| `trade_efficiency: slices.overall` | `source` plus every summary field of section 2. | map | `BR:458` | run |
| `trade_efficiency: slices.per_window.<window>.n` | Trades in the window. | count | `BR:220` | run |
| `trade_efficiency: slices.per_window.<window>.<trade field>.<stat>` | Stat of a numeric trade field (section 2) over the window's trades; booleans dropped (A10). | field | `BR:234` | run |
| `trade_efficiency: slices.per_regime.<regime>.<trade field>.<stat>` | Same by entry regime. | field | `BR:475` | run |
| `trade_efficiency: slices.per_symbol.<symbol>.<trade field>.<stat>` | Same by symbol. | field | `BR:473` | run |
| `<stat>: mean` | Mean. | field | `BR:235` | run |
| `<stat>: median` | Median. | field | `BR:236` | run |
| `<stat>: p10` | 10th percentile (linear). | field | `BR:237` | run |
| `<stat>: p90` | 90th percentile (linear). | field | `BR:238` | run |
| `forecast_power: slices.overall.median_forecast_return_corr` | Section 5 field. | corr | `BR:502` | after |
| `forecast_power: slices.overall.median_forecast_return_corr_source` | Where it comes from. | text | `BR:503` | meta |
| `forecast_power: slices.overall.prescreen_backtest_cross_check` | Legacy block, only when the run had a prescreen (stage removed). | map | `BR:506` | run |
| `forecast_power: slices.per_window[].forecast_return_corr` | core.forecast_return_corr of the window. | corr | `BR:521` | after |
| `forecast_power: slices.per_window[].forecast_return_corr_pvalue` | core p-value (not block-adjusted). | p | `BR:522` | after |
| `forecast_power: slices.per_regime.<regime>[]` | symbol, window and the section 4 regime_validity fields. | list | `BR:528` | after |
| `regime_power: slices.overall.note` | Fixed text: what this report computes. | text | `BR:662` | meta |
| `regime_power: slices.per_window[].per_regime` | Section 4 per_regime of the window. | map | `BR:692` | run |
| `regime_power: slices.per_window[].regime_validity` | Section 4 regime_validity of the window. | map | `BR:693` | after |
| `regime_power: slices.per_window[].hindsight_lag` | Lag of the live regime changes behind hindsight direction changes. | map | `BR:602` | after |
| `regime_power: hindsight_lag.live_transition_count` | Live label changes (unknown/blank excluded). | count | `BR:645` | run |
| `regime_power: hindsight_lag.hindsight_transition_count` | Changes of the 5-bar-ahead price direction label. | count | `BR:646` | after |
| `regime_power: hindsight_lag.lags_bars` | live index - nearest hindsight index within 20 bars. | bars | `BR:647` | after |
| `regime_power: hindsight_lag.median_lag_bars` | Their median. | bars | `BR:648` | after |
| `regime_power: hindsight_lag.reason` | Why no lag. | text | `BR:649` | meta |
| `component_attribution: slices.overall.components_discovered` | Component ids found in bars.csv columns. | list | `BR:771` | meta |
| `component_attribution: slices.overall.note` | Fixed text. | text | `BR:772` | meta |
| `component_attribution: slices.per_window.<window>.<component>.<metric>.<stat>` | Stat of a bars.csv component metric over the window's bars. | field | `BR:786` | run |
| `component_attribution: slices.per_window.<window>.<component>.n` | Bars x 1 records (A11). | count | `BR:220` | run |
<!-- /data-dictionary -->

## 7. grid_evaluation.yaml

`artifacts/grid_evaluation.yaml`: each pre-registered criterion on each graded
variant (`VE:1828`, written at `P1:2371`). Cells are `PASS`, `FAIL`,
`INCONCLUSIVE` or `SPEC_ERROR`.

<!-- data-dictionary: grid_evaluation.yaml -->
| Field | Meaning | Unit | Code | When known |
|---|---|---|---|---|
| `result` | `GRID_EVALUATED` or `SPEC_ERROR`. | label | `VE:2016` | run |
| `criteria` | Criterion ids in order. | list | `VE:2017` | meta |
| `variants` | Graded variant ids (the columns). | list | `VE:2018` | meta |
| `idea_status` | `validated` / `refuted` / `inconclusive` (any FAIL refutes; any INCONCLUSIVE, untested or failed variant blocks validated). | label | `VE:1988` | run |
| `reason` | Text of that status. | text | `VE:1990` | run |
| `failed_variants` | {variant: `refused:` or `backtest_failed:` reason}. | map | `VE:1970` | meta |
| `untested_variants` | {variant: reason} not run in this run. | map | `VE:1971` | meta |
| `partial_coverage_variants` | {variant: reason} graded on fewer windows (cap at inconclusive). | map | `VE:1972` | meta |
| `evaluated_at` | When evaluated (UTC). | time | `P1:2371` | meta |
| `grid.<criterion>.<variant>.result` | Cell result. | label | `VE:1327` | run |
| `grid.<criterion>.<variant>.value` | The reduced or pooled metric value. | metric | `VE:1327`, `VE:1362` | run |
| `grid.<criterion>.<variant>.threshold` | Pre-registered threshold. | metric | `VE:1327` | meta |
| `grid.<criterion>.<variant>.comparator` | Comparator applied. | label | `VE:1328` | meta |
| `grid.<criterion>.<variant>.n_windows` | Windows with a numeric value (window source) or in scope (pooled). | count | `VE:1288`, `VE:1341` | run |
| `grid.<criterion>.<variant>.n_trades` | Summed core.trade_count over those windows. | count | `VE:1289` | run |
| `grid.<criterion>.<variant>.reason` | Why INCONCLUSIVE / FAIL / SPEC_ERROR. | text | `VE:1292` | meta |
| `grid.<criterion>.<variant>.detail` | Era reducer detail. | map | `VE:1312` | run |
| `grid.<criterion>.<variant>.detail.era_medians.<era>` | Median of the metric over the era's windows (core.net_return_pct for sign_consistent_by_era; zero-trade windows count as 0.0, A8). | metric | `VE:1195` | run |
| `grid.<criterion>.<variant>.detail.era_signs.<era>` | Sign of that median (1, -1, 0). | sign | `VE:1196` | run |
| `grid.<criterion>.<variant>.per_symbol.<symbol>` | Cell per symbol (symbol_reducer per_symbol_all). | map | `VE:1548` | run |
| `grid.<criterion>.<variant>.n_eff` | residual_ic: effective sample size. | count | `VE:1395` | run |
| `grid.<criterion>.<variant>.p_value_one_sided` | residual_ic: one-sided p-value. | p | `VE:1396` | run |
| `grid.<criterion>.<variant>.max_p_value` | residual_ic: p needed to pass. | p | `VE:1396` | meta |
| `grid.<criterion>.<variant>.composite` | residual_ic: composite state (`STALE` when missing). | label | `VE:1397` | meta |
| `grid.<criterion>.<variant>.fully_explained` | residual_ic: duplicate of the composite. | bool | `VE:1397` | run |
| `grid.<criterion>.<variant>.source` | profit_bars cells: `profit_bars`. | label | `VE:1487` | meta |
| `grid.<criterion>.<variant>.bars` | profit_bars cells: the grader's bar rows. | list | `VE:1487` | run |
| `grid.<criterion>.<variant>.weight_schedule` | profit_bars cells: the grader's weight schedule. | map | `VE:1490` | meta |
<!-- /data-dictionary -->

## 8. claim_result_digest.yaml

`artifacts/claim_result_digest.yaml`, written by code for the v3 readers (`RF:221`).
Effect sizes are on bars after the fact: `after`.

<!-- data-dictionary: claim_result_digest.yaml -->
| Field | Meaning | Unit | Code | When known |
|---|---|---|---|---|
| `schema_version` | 1. | int | `RF:229` | meta |
| `label` | `measured, not proven`. | text | `RF:229`, `CF:57` | meta |
| `note` | Fixed text (information only). | text | `RF:229` | meta |
| `information_only` | true. | bool | `RF:230` | meta |
| `status` | `error` when the digest could not be built. | label | `RF:277` | meta |
| `detail` | Error text. | text | `RF:277` | meta |
| `approximation` | The run tested an approximation of the idea (nearest build). | map | `RF:238`, `NB:135` | meta |
| `approximation.line` | One-line summary. | text | `NB:155` | meta |
| `approximation.n_deviations` | Number of differences. | count | `NB:155` | meta |
| `approximation.deviations[].clause` | Claim clause approximated. | text | `NB:144` | meta |
| `approximation.deviations[].built_instead` | What was built. | text | `NB:144` | meta |
| `approximation.deviations[].missing` | What is missing to build it. | text | `NB:144` | meta |
| `approximation.deviations[].effect` | Expected effect of the difference. | text | `NB:144` | meta |
| `approximation.ref` | `artifacts/deviations.yaml`. | path | `NB:156` | meta |
| `variant_patches` | Each variant's exact change to the base config. | map | `RF:196` | meta |
| `variant_patches.note` | Fixed text. | text | `RF:217` | meta |
| `variant_patches.base_config_ref` | Base config path. | path | `RF:217` | meta |
| `variant_patches.variants[].variant_id` | Variant id. | id | `RF:213` | meta |
| `variant_patches.variants[].kind` | Variant kind. | label | `RF:213` | meta |
| `variant_patches.variants[].symbol` | Symbol. | id | `RF:214` | meta |
| `variant_patches.variants[].patch[].path` | JSON pointer changed. | path | `RF:215` | meta |
| `variant_patches.variants[].patch[].value` | New value. | value | `RF:215` | meta |
| `statement` | The claim, verbatim from the card. | text | `RF:251` | meta |
| `kind` | Claim kind. | label | `RF:252` | meta |
| `block_visibility` | Whether a test reads the block (ok / blind / not_applicable). | label | `RF:253` | meta |
| `manifest_kind` | Block kind of the manifest (forecast / regime). | label | `RF:254` | meta |
| `statistics_note` | Fixed text on the statistics. | text | `RF:255` | meta |
| `tests[].name` | Test name. | id | `RF:256` | meta |
| `tests[].spec_hash` | Hash of the test spec. | hash | `RF:256` | meta |
| `tests[].statistic` | `rank_ic`, `mean_diff`, `hit_rate` or `decay_curve`. | label | `RF:257` | meta |
| `tests[].statistic_label` | What that statistic is. | text | `RF:258` | meta |
| `tests[].direction` | `greater` or `less`. | label | `RF:259` | meta |
| `tests[].selector` | Which bars (card spec; reads bar t only, `CT:440`). | map | `RF:260` | meta |
| `tests[].outcome` | The forward outcome and horizons (card spec, `CT:536`). | map | `RF:260` | meta |
| `tests[].baseline` | Reference bars (card spec, `CT:587`). | map | `RF:260` | meta |
| `claim_status` | Run status from claim_measurement.yaml (`absent` without one). | label | `RF:268` | run |
| `reason` | Its reason. | text | `RF:269` | meta |
| `variants.<variant>.status` | `measured`, `no_events` or `not_measured`. | label | `RF:174` | run |
| `variants.<variant>.reason` | Why not measured (`stale` = not this attempt's bars). | text | `RF:160` | meta |
| `variants.<variant>.detail` | Detail of a stale reason. | text | `RF:164` | meta |
| `variants.<variant>.tests.<test>.status` | Test status. | label | `CF:140` | run |
| `variants.<variant>.tests.<test>.spec_hash` | Spec hash. | hash | `CF:140` | meta |
| `variants.<variant>.tests.<test>.reason` | Why not measured. | text | `CF:142` | meta |
| `variants.<variant>.tests.<test>.statistic_label` | What the effect is. | text | `RF:186` | meta |
| `variants.<variant>.tests.<test>.peak_horizon` | decay_curve: horizon of the largest claim-signed effect. | bars | `CF:160` | after |
| `variants.<variant>.tests.<test>.floor_not_met` | Floors of the card not reached. | list | `CF:161` | run |
| `variants.<variant>.tests.<test>.horizons.<h>.effect` | The test's statistic at horizon h over all windows (6 significant digits, raw sign). | stat | `CF:149`, `CM:186` | after |
| `variants.<variant>.tests.<test>.horizons.<h>.n_events` | Selected bars with an outcome. | count | `CF:149` | after |
| `variants.<variant>.tests.<test>.horizons.<h>.windows_claimed_sign` | Windows whose effect has the claimed sign. | count | `CF:150` | after |
| `variants.<variant>.tests.<test>.horizons.<h>.windows_with_value` | Windows with a defined effect. | count | `CF:151` | after |
| `variants.<variant>.tests.<test>.horizons.<h>.per_coin.<symbol>` | Same four numbers per coin (only with several coins). | map | `CF:154` | after |
<!-- /data-dictionary -->

## 9. claim_measurement.yaml

`artifacts/claim_measurement.yaml` (an older run: `claim_status.yaml`): the run's
measurement status (`CM:282`, error case `CM:322`). Per-variant detail lives in
`artifacts/variants/<variant>/claim_test.yaml`.

<!-- data-dictionary: claim_measurement.yaml -->
| Field | Meaning | Unit | Code | When known |
|---|---|---|---|---|
| `run_id` | Run id. | id | `CM:293` | meta |
| `label` | `measured, not proven`. | text | `CM:293` | meta |
| `note` | Fixed text: effect sizes only, no p-value. | text | `CM:293` | meta |
| `information_only` | true. | bool | `CM:293` | meta |
| `claim_status` | `measured` when any test was measured, else `not_measured`. | label | `CM:314` | run |
| `reason` | Why not measured (card gap, `no_graded_variants`, `error`, ...). | label | `CM:314` | meta |
| `detail` | Detail text. | text | `CM:314` | meta |
| `n_tests_measured` | (variant, test) pairs measured. | count | `CM:315` | run |
| `n_tests_no_events` | Pairs whose selector matched no bar (absent in the error document, A14). | count | `CM:316` | run |
| `n_tests_not_measured` | The other pairs. | count | `CM:317` | run |
| `variants.<variant>.status` | Variant status. | label | `CM:309` | run |
| `variants.<variant>.reason` | Its reason. | text | `CM:309` | meta |
| `variants.<variant>.file` | `variants/<variant>/claim_test.yaml`, or null. | path | `CM:310` | meta |
| `tests[].variant` | Variant id. | id | `CM:289` | meta |
| `tests[].test` | Test name. | id | `CM:289` | meta |
| `tests[].spec_hash` | Spec hash. | hash | `CM:289` | meta |
| `tests[].status` | `measured`, `no_events` or `not_measured`. | label | `CM:290` | run |
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
  into the last row, `PI:482`). The target allocation is not a column.
- **The decision behind each trade** (E-029): which rule opened or closed a lot,
  whether it was a full exit or a partial reduction, the forecast and band at the
  decision. `exit_reason` is inferred (A5).
- **Regime-rule inputs** (parked): the values each threshold rule compared, which
  veto fired (`forced_by_veto`, `RE:132`) and the score winner (`RE:195`) are
  computed and dropped (`MS:193`).
- **Transform steps** (parked): only a component's raw value and its value after
  the whole pipeline are recorded, not the intermediate steps.
- **Per-trade costs**: the slippage and commission a trade actually paid, and
  funding (funding is not modelled in protocol runs: `run_protocol` does not pass
  `model_funding`).
- **Bar-level equity statistics** in any report: metrics.json `bar_equity` exists
  (run_protocol passes `bar_equity=True`, `RP:2464`) but no report reads it.

## Audit findings

Found while writing this file (2026-10-08); none fixed here. Each is a follow-up.
"Measured" lines were checked on the saved runs run_070 to run_074 (66 window
bars.csv files, 6 trade_diagnostics.json).

- **A1. bars.csv balances are the end-of-run balances on every row.**
  `get_account_balance` returns the live balance dict (`PI:330`); `record_state`
  stores that reference (`TB:591`, `TB:600`, `PI:476`); trades mutate it in place
  (`PI:89`); flattening happens at the end (`BT:452`). Measured: in all 66 files
  every `balances.*.free` column has one value. The scalar columns
  (`total_portfolio_value`, `previous_allocation`, ...) are right. Fix: copy the
  dict at record time (declared output change of bars.csv / portfolio_states.csv).
- **A2. `confidence` is always 0.0 and `strategy` always empty** (`MS:202`; also
  `entry_confidence` in trades.json). Drop or fill.
- **A3. Column name `succcess_execute_portfolio_rebalance`** has three c's
  (`TB:598`, `TB:728`). Renaming breaks readers of saved runs; documented as is.
- **A4. `entry_efficiency` measures the entry slippage, not "waiting one bar".**
  The fill is bar t's close plus slippage (`EH:369`); the comparison is bar t+1's
  open (`RP:338`), which on 24/7 data is bar t's close. Measured: median -0.025%
  (BTC) and -0.075% (SOL, UNI), exactly the 2.5 / 7.5 bps slippage. The same
  slippage biases `entered_earlier_better` and `held_longer_better` (`RP:444`,
  `RP:486`). Fix: compare with the next bar's close, or drop.
- **A5. `exit_reason` is `signal_flip` for everything but the last bar**
  (`RP:535` default): no-trade-band rejections, partial LIFO reductions, NaN
  holds, gap and risk flattens included. Nothing produces `stop_loss` or
  `time_stop`, so `stop_loss_pct`, `time_stop_pct` and `stop_loss_recovery_rate`
  are always 0. Measured: 99% signal_flip. Fix: E-029.
- **A6. MAE, MFE and exit_efficiency include the entry bar's own high and low**,
  which happened before the fill at that bar's close (`RP:621`, `RP:306`,
  `RP:363`). With median holding of 1-2 bars this inflates both. Fix: start the
  holding window at entry_idx + 1.
- **A7. `cost_paid` is the configured fee x 2, not what the trade paid**
  (`RP:538`): no slippage, not size-dependent; and `realized_return`, called gross,
  is net of slippage (fill prices). So `realized_edge_to_cost_ratio` compares a
  post-slippage edge with a fee-only cost. Fix: itemise slippage, or rename.
- **A8. Trade-based core fields are 0.0, not null, when there are no trades**
  (`RA:539`-`RA:543` default 0.0; `PM:1372` returns nothing): `net_return_pct`,
  `max_drawdown_pct`, `win_rate`, and `sharpe` when it is undefined (`PM:1466`,
  `PM:1490`). A zero-trade window's 0.0 enters the grid's
  `sign_consistent_by_era` median as a real value (`VE:1287`). Fix: null.
- **A9. `sharpe`, `max_drawdown_pct` and `net_return_pct` use the trade-exit
  basis** (`PM:1407`-`PM:1499`): PnL booked on exit dates, open positions not
  marked. The bar-level figures exist (metrics.json `bar_equity`) but no report
  shows them. Fix: add them to the profitability report.
- **A10. trade_efficiency aggregates every numeric trade field** (`BR:225`),
  including `entry_idx` / `exit_idx` (window-local row numbers) and
  `entry_price` / `exit_price` across symbols, whose stats mean nothing; booleans
  are dropped (`BR:200`), so a slice has no win rate. Fix: a field list.
- **A11. Report `n` counts records, not values** (`BR:220`): component records
  include warm-up / not-ready bars with blank metrics, so `n` overstates the
  sample of the mean beside it. Fix: count per metric.
- **A12. `regime_validity` pairs each row with the next row** (`RA:649`),
  without the gap filter `forecast_return_corr` uses (`RA:296`), and includes
  `NOT_READY` bars. Minor.
- **A13. `debug_execute_portfolio_rebalance.quantity` is unsigned for opens and
  reductions but the signed position for CLOSE** (`EH:374`, `EH:389` vs `EH:420`).
- **A14. `claim_measurement.yaml` written by the safety net lacks
  `n_tests_no_events`** (`CM:322` vs `CM:316`).
- **A15. Stale comments and docstrings.** `BR:572` and `BR:788` say every
  window's bars.csv ends with an empty-`regime` row; measured: none of the 66
  files has one (the end-of-run close merges into the last row, `PI:482`).
  `FM:60`-`FM:66` says both -200%..+200% and -1.0..1.0; the code is forecast / 10.
  `RP:1052` (floor nearest-rank percentiles) and `BR:177` (linear) use two
  percentile definitions.
