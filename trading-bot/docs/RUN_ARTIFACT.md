# RUN_ARTIFACT.md
Each backtest writes `runs/<id>/` where `<id>` = `<UTC-timestamp>_<config-sha8>`.

## Files

### manifest.json
Fields: `run_id`, `created_utc`, `config` (full strategy_config snapshot), `config_sha256`,
`data` (symbols, timeframe, start, end, bar_count, data_sha256), `git_sha`,
`engine` (lookback, warmup).
Use: pin the exact config and data range; diff `config_sha256` to detect silent config drift between runs.

### metrics.json
Fields: `core` (net_return_pct, sharpe, max_drawdown_pct, trade_count, win_rate,
avg_trade_net_pnl, fees_paid), `per_regime` (bar_count, avg_forecast, trade_count,
total_net_pnl per regime), `forecast_bins`, `dynamic` (per-component per-regime mean/std).
Use: compare runs on `core` — these are config-independent and stable across runs.
`dynamic` component stats may differ across configs by design; use them to diagnose
component behavior, not as a cross-run comparison metric.

### trades.json
Fields: one record per completed trade — entry/exit price, entry_regime, entry_forecast,
net_profit_loss_absolute, total_commission, profitable_net, side, duration, ...
Use: drill into individual trades; slice by regime or forecast range for custom analysis.

### bars.csv
Columns: timestamp, regime, forecast, allocation, plus per-component debug values
(prefixed `debug_info.components.*`).
Use: per-bar drill-down; verify regime assignments and forecast values bar by bar.

### forecast_distribution.csv
Columns: `regime`, `bin` (e.g. `-5_0`, `5_10`), `count_final_forecast`.
Use: calibrate `threshold_filter min_abs` — confirm signal mass sits above the threshold
before tightening it; bins span (-inf, -15, -10, -5, 0, 5, 10, 15, +inf).

### tradesxl.xlsx
Excel export of the same records as trades.json.
Use: quick manual inspection; pivot tables for regime/forecast breakdowns without code.
