# Engine changes that can change a backtest's results

One line per change to the engine or its settings that can make a record made before it differ from one made after
it, with its date (UTC) and commit. A record keeps the results of the engine that made it (operator, 2026-11-21: old
runs stay as recorded); a record's `manifest.json` gives its date (`created_utc`) and commit (`git_sha`), to read
against this list. Changes proven to leave every result unchanged are not listed (for example the speed changes A to
D of 2026-11-20, the component standardisation of 2026-11-17). Started 2026-11-21, from 2026-11-16 on.

| Date (UTC) | Commit | Change | What it changes |
|---|---|---|---|
| 2026-11-19 00:12 | `0821b9211` | The gap rule: a hole of up to one day in a coin's bars is ignored, on any bar size (it was 3 bars) | books with holes of more than a day and up to 3 bars on daily bars, or of 4 bars to a day on hourly bars (`forecast.md`, point 8) |
| 2026-11-19 22:09 to 2026-11-20 09:30 | `b135b1d2d`, `5cc59a78e`, `2c4367cb7`, `0a21f891b`, `64d5c0059` | The holding period (`strategies.min_holding_bars`): three versions in a day, the last the corrected rule (`forecast.md`, point 7) | every plan made since then (step 3's code adds the key from the horizon); a plan made before has no key and holds nothing, even when rerun |
| 2026-11-20 23:57 | `8e350ab74` | The trading costs: the slippage measured per coin on Kraken futures' order books instead of a guess (topic 38) | every book's costs: lower on BTC, ETH and most coins, higher on XMR and the thinnest |
