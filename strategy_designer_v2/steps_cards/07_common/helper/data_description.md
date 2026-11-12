The data. `data` is a dict of three tables, each by coin and by window: `data["bars"][coin][window]`,
`data["trades"][coin][window]` and `data["days"][coin][window]`, all pandas DataFrames. The coins are venue symbols
(for example `BTCUSD`); the windows are `w1` to `wN`, separate periods, in the folds' order. A coin's windows are not
contiguous: never join them into one series, and never compute a return across two windows.

- `bars`: one row per bar the strategy was ready on, in time order. `timestamp` (UTC), `open`, `high`, `low`,
  `close`, `volume`; `forecast` (the idea's signal: positive long, negative short, 0 flat; capped at +/-20);
  `regime` (the regime detector's label); `postRebalance_total_value` (the book's value after the bar's rebalance and
  its fees); `postRebalance_current_allocation` (the position after the rebalance); and, per component of the config,
  `debug_info.components.<id>.last_history_value` (its raw value) and `...post_pipeline_value` (after its
  transforms).
- `trades`: one row per trade. `side` (LONG or SHORT), `entry_time`, `exit_time`, `entry_price`, `exit_price`,
  `duration_minutes`, `entry_forecast`, `exit_forecast`, `entry_regime`, `profit_loss_percent` (before fees),
  `net_profit_loss_percent` (after fees), `total_commission`. A trade closed on a window's last bar was closed by the
  window's end.
- `days`: one row per UTC day: `day`, `book_value` and `close` (their last values of the day), `book_return` and
  `coin_return` (their returns from the previous day of the same window; NaN on a window's first day).
