The data. `data` is a dict of three tables, each by coin and by window, all pandas DataFrames:
- `data["bars"][coin][window]` and `data["trades"][coin][window]`: the record's bars and trades, with the columns
  described in WHAT A BACKTEST RECORDS (below);
- `data["days"][coin][window]`: one row per UTC day, built from the bars: `day`, `book_value` and `close` (their last
  values of the day), `book_return` and `coin_return` (their returns from the previous day of the same window; NaN on
  a window's first day).
