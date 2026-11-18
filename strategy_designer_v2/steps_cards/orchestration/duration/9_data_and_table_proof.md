# Proof 9: the four speed points of measurement 8, proven, and the time before and after (2026-11-18)

The four changes measurement 8 led to, each on the operator's go, in shared code (`trading-bot/`). Each was proven
the same way: backtests rerun on fixed inputs and compared file by file with their records (the engine's files per
window: bars, trades, metrics, forecast distribution), and the bot's suite.

## Point 4: data gathering separate from the backtest
**Rule** (`trading-bot/data/coverage.py`, `local_data/coverage.yaml`): a data tool fetches and records the days it
fetched; a backtest reads the local file only and never calls an exchange; its days (warm-up included) must be inside
the file's coverage, else it stops ("the dates were not fetched (run the data tool)"). A hole inside a covered range
is the exchange's own (an hour without a trade) and is read as it is.

| Backtest rerun | Files compared | Result |
|---|---|---|
| night_rsi 010-03 e1, daily, BTC and ETH, 24 windows | 192 | identical |
| hourly_run 001-01 on BTC, 1h, fold A | 24 | identical |
| the same plan on ZEC, 1h, window 2023-09 (401 holes) | 4 | identical; 7 min 54 s -> 50 s |
| night_013 b1, daily, 19 coins, 24 windows | 1,036 | identical; the windows run and not run, and their reasons, identical |

One expected change: a coin with no file at all (BNB) now reads "the dates were not fetched (run the data tool)"
instead of "no historical data on the venue". Removed as obsolete: the backtest loader's `localStorage` option and its
fill-failure switch (no production caller); four tests restated for the new rule. Bot suite: 1,543 passed.

## Point 1: the history table built from typed columns
**Change** (`strategies/strategy_base.RollingBuffer`): each column kept in a typed array, one value written per bar;
the table built from the last rows, instead of `pd.DataFrame(list of bar dicts)` at every bar. Only for bars of plain
values (float, int, bool, a tz-naive Timestamp) with the same keys; any other bar falls back to the old construction.

- Exactness: 8,008 tables compared bar by bar with the old construction on real data (daily BTC, 1h ZEC with its
  holes, a small buffer wrapping 8 times), all identical.
- Backtests: the same four as above, 192 + 24 + 4 + 1,036 files, all identical. Bot suite: 1,547 passed (4 new tests).

| One window (as in measurement 8, run alone) | Before | After |
|---|---|---|
| BTC daily, trend idea | 5.4 s | 3.3 s |
| BTC 1h, RSI plan | 108 s | 32 s |
| BTC 1h, trend idea with a one-year history (profiled) | 1,130 s | 194 s |

## Point 2: the warm-up checked once
**Change** (`core/trading_bot.py`, `core/backtester.py`, `core/launcher.py`): at the first bar after the warm-up, the
readiness check runs on a copy of the real strategy (`is_ready()` classifies a bar); a strategy not ready stops the run
as before. The throwaway strategy that replayed the whole warm-up a second time is removed.
- Backtests: the same four, 192 + 24 + 4 + 1,036 files identical; the 19 coins' windows run and not run, and their
  reasons, identical. Bot suite 1,547; 2 tests on real data (SOL: a warm-up too short stops the run, a long one runs).

## Point 3: the record's nested details expanded per column
**Change** (`execution/portfolio_info.flatten_dict_columns`): one construction per column; each row's single dtype (as
`pd.Series(row)` gives it) reproduced, found once per kind of row. Measured without the profiler before the change:
26% of a 1h window (8.2 s of 31.5 s).
- Exactness: the 4 real frames of two windows identical to the former code; a test keeps the former code as reference.
- Backtests: the same four, all identical. Bot suite 1,551.

## Time, before and after (each run alone on the run machine, old code at 4a1af354, new code with all four points)
| Run | Before | After | |
|---|---|---|---|
| 1h BTC, fold A (6 windows) | 329 s | 135 s | 2.4x |
| 1h ZEC window 2023-09 (401 holes) | 446 s | 18 s | 25x |
| 19 coins daily (24 windows) | 701 s | 458 s | 1.5x |
| 1h window with a one-year history | 683 s | 57 s | 12x |
