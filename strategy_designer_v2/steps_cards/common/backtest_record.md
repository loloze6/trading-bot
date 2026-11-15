What a backtest records. The same for every step that reads a backtest or plans what will be measured on it (steps 3,
5 and 7). A measure or check can use only what is recorded on the bars it uses.

The record is by coin and by window. The coins are venue symbols (`BTCUSD`, ...); the windows are `w1` to `wN`,
separate periods in the folds' order. A coin's windows are not contiguous: never join them into one series, never
compute a return across two windows. Only the coins and windows that ran are present. Warm-up bars are not recorded:
every bar is one the strategy was ready on.

Bars, one row per bar, in time order:
- `timestamp`: the bar's start time (UTC).
- `open`, `high`, `low`, `close`, `volume`: the bar's prices and traded volume. `close` is the price at which the
  strategy decides and trades. These exist on every bar.
- `forecast`: the strategy's forecast at the bar's close, from -20 to +20: positive long, negative short, 0 flat.
- `postRebalance_current_allocation`: the position held after the bar's trade, as a share of the book (negative is
  short), from this bar's close to the next. It differs from forecast / 10: the sizing scales it by the coin's
  volatility, and the engine skips a trade too small to matter. `previous_allocation`: the position before the trade.
- `total_portfolio_value`: the book's value at the bar's close, before the trade; `postRebalance_total_value`: after
  the trade and its fee.
- `regime`: the regime the regime detector chose on that bar (exists on every bar).
- `debug_info.components.<id>.last_history_value`: the raw value of the config's component `<id>` (after its history
  transforms, before the others); `debug_info.components.<id>.post_pipeline_value`: after all its transforms.
  **Limits:** only the components of the config's `strategies` are recorded, under their ids, and only on the bars
  where their regime was active (elsewhere the column is missing, which is not a value of zero). The regime
  detector's components are not recorded at all: its decision is `regime`. A measure on bars where a component is
  not recorded recomputes it from the prices.
- Do not use: `confidence`, `strategy`, `balances.*`, `postRebalance_balances.*` (known to be wrong), or other
  `debug_*` columns.

Trades, one row per trade: `side` (LONG or SHORT), `entry_time`, `exit_time`, `entry_price`, `exit_price`,
`duration_minutes`, `entry_forecast`, `exit_forecast`, `entry_regime`, `profit_loss_percent` (before fees),
`net_profit_loss_percent` (after fees), `total_commission`. A trade closed on a window's last bar was closed by the
window's end.
