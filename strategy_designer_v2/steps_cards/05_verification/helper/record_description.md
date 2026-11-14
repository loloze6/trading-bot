How a backtest record is given to your function.

`bars` is a dict: `bars[coin][window]` is a pandas DataFrame, one row per bar of that window, in time order. The coins are
venue symbols (for example `BTCUSD`, `ETHUSD`); the windows are `w1` to `wN`, separate periods (the windows of one fold, or of several folds one after the other). Only the
coins and windows that ran are present. Warm-up bars are not in the frames: every row is a bar the strategy was ready on.

Columns you may use:
- `timestamp`: the bar's start time (a pandas Timestamp).
- `open`, `high`, `low`, `close`, `volume`: the bar's prices and traded volume. `close` is the price at which the strategy
  decides and trades.
- `forecast`: the strategy's forecast at that bar's close, from -20 to +20. Positive means long, negative short, 0 no
  position. The strategy targets a position of forecast / 10 of the portfolio.
- `postRebalance_current_allocation`: the position actually held after that bar's trade, as a share of the portfolio
  (negative is short). It is the position held from this bar's close to the next bar's close. It can differ from
  forecast / 10, because the engine skips a trade smaller than 0.2 of the portfolio.
- `previous_allocation`: the position held before that bar's trade.
- `total_portfolio_value`: the account's value at that bar's close, before the trade; `postRebalance_total_value`: after
  the trade and its fee.
- `regime`: the regime label the strategy used on that bar.
- `debug_info.components.<id>.last_history_value`: the raw value of the config's component `<id>` on that bar (after its
  history transforms, before its other transforms). For `RSIPullbackComponent` it is (50 - RSI) x scaling_factor, with
  scaling_factor 0.4 unless the config sets it, so RSI = 50 - value / 0.4.
  Only the components of the config's `strategies` are recorded, under their ids, and only in windows where their
  regime was active (a window where it never was has no such column). The regime detector's components are not
  recorded at all: the detector's decision is the `regime` column. When the plan's situation is the detector's rule,
  check it on `regime`, or recompute the detector's measure from the prices. A missing column is not a value of zero.
- `debug_info.components.<id>.post_pipeline_value`: the component's value after its transforms.

Do not use: `confidence`, `strategy`, `balances.*`, `postRebalance_balances.*` (known to be wrong), or other `debug_*` columns.

How returns, holding, t-statistics and differences are measured: see HOW THE WORKFLOW MEASURES.
