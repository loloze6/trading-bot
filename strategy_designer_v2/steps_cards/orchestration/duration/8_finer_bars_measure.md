# Measurement 8: where a finer-bar backtest spends its time, and what the gap rule blocks (2026-11-18)

Purpose (operator, 2026-11-18, finer bars, plan item 1): find the relevant optimization points of the engine before
any change, and what the gap rule does on 1h bars. Measuring only: nothing was changed.

**How.** The engine's `run_backtest`, called as the wrapper calls it (Kraken, warm-up prefetch, gap rule on), on one
4-month window (fold A's first, 2022-01 to 2022-04), timed and profiled with cProfile, on the run machine (4 cores).
Configs: an hourly RSI plan (`hourly_run` 001-01, sizing window 60 days = 1,440 bars, `required_bars` 1,441);
night_013's nearness-to-high trend idea (daily, `required_bars` 456) and the same idea planned on 1h the way step 3
converts durations (365 days = 8,760 bars, `required_bars` 10,944). ZEC (the coin with the most holes) on all six
fold-A windows with the RSI plan.

## Time
| Window | Time | Bars | Per bar |
|---|---|---|---|
| BTC, RSI plan, 1h | 108 s | 2,880 | 37 ms |
| BTC, trend idea, 1d | 5.4 s | 120 | 45 ms |
| BTC, trend idea on 1h (one-year history) | 1,130 s | 2,880 | 392 ms |
| ZEC, RSI plan, 1h, 2023-09 window | 494 s | 2,697 | 183 ms |

The cost per bar is about the same on daily and hourly bars; it grows with the history's length and with the
cached data's holes.

## Where the time goes (profiles)
| # | Point | Share | Why |
|---|---|---|---|
| 1 | The history table rebuilt from scratch at every bar (`strategy_base.RollingBuffer.get_df`: `pd.DataFrame(list of bar dicts)`) | 34% (BTC RSI), 89% (one-year history) | the whole buffer (up to 2 x `required_bars` rows) is converted again for each new bar: the cost per bar grows with the lookback |
| 2 | The warm-up replayed twice (`launcher.run_backtest`, the readiness probe) | about half the strategy updates when the warm-up is long (46,636 updates for 24,758 bars) | a throwaway strategy replays the whole warm-up to assert readiness; the real strategy then replays it again |
| 3 | Writing the record (`portfolio_info.flatten_dict_columns`) | 28% (BTC RSI, 30 s of 108) | each bar's nested details are expanded one row at a time (`Series.apply(pd.Series)`) |
| 4 | Remote calls to fill the cache's holes (`ccxt_fetcher._fetch_remote`, Kraken, throttled) | 82% (ZEC 2023-09: 401 calls, 400 s) | every hole in a cached series triggers a call to Kraken, which cannot fill it (it serves the last 720 bars only, and the holes are hours without trades); the backtest then uses the cache as it was. It also makes a backtest's time depend on the network |
| - | The idea's own calculations (components, transforms) | about 23% (BTC RSI) | the work itself |

All four are in shared code (`trading-bot/`); all four also slow daily backtests (points 1 to 3 per bar, point 4
per hole).

## The gap rule on 1h (ZEC, fold A, RSI plan)
- 1,343 holes in 16,548 bars: 1,319 of 1 to 3 hours (ignored), 24 of 4 to 6 hours (the middle tier).
- A middle-tier hole blocks new entries for `required_bars` real bars: 1,441 hours (60 days) here.
- **47% of fold A's hours are under the no-new-entry rule** (by window: 0%, 9%, 87%, 2%, 98%, 86%).
- On daily bars the rule almost never acts (1 missing day per coin, 2018 to 2025).
- Kraken's 1h data omits the hours without a trade (the gap rule's own comment, `core/launcher.py`): most holes are
  quiet hours, not missing data.
