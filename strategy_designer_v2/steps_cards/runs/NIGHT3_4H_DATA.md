# Night 3: the 4-hour Kraken files, built from the hourly ones (2026-11-21, before `night3_4h_run`)

**Why:** the operator asked for 4h runs tonight (`NIGHT3_RUN.md`, session 2). The Kraken coins had 1h and 1d files,
no 4h files. Shared code under the operator's night go for 4h runs: on branch `night3-4h` only, never merged into master.

## What was built
| File | What it is |
|---|---|
| `trading-bot/tools/derive_kraken_bars.py` | the data tool: `kraken_<PAIR>_4h.csv` from the local `kraken_<PAIR>_1h.csv` only (never an exchange, never `local_data/holdout_sealed/`); records the coverage |
| `trading-bot/tests/test_derive_kraken_bars.py` | 7 tests: UTC blocks, the aggregation, empty blocks, nothing past the coverage, the rerun, the order check, the daily comparison |
| `trading-bot/local_data/kraken_*USD_4h.csv` | 19 files, 29 MB in all (BTC: 25,724 bars, 2013-10 to 2025-12-31) |
| `trading-bot/local_data/coverage.yaml` | 19 entries added (start null, end 2025-12-31, as their hourly files); no line changed or removed |

A 4h bar is the block of 4 hours starting at 00, 04, 08, 12, 16 or 20 UTC: open = first hour's open, high = highest
high, low = lowest low, close = last hour's close, volume and trade count = sums, quote volume = volume x close (the
archive files' convention), stamped with its opening time and `close_time` = its end less 1 ms (the hourly files'
convention). A block with no trade has no row, as in Kraken's own files.

## Why this can't leak
A 4h bar holds only the hours inside its block and is stamped with its opening time, so its close is known at its
`close_time`, exactly as a Kraken 4h bar would be; the engine hands each bar's decision the rows up to that bar. The tool
reads nothing but the local hourly files and writes no day past their coverage (2025-12-31, before the sealed holdout).

## Proof
| Check | Result |
|---|---|
| 1d bars built the same way (24-hour UTC blocks), against Kraken's own 1d files, on the days both have (`--compare-daily`) | **43,504 coin-days, 19 coins: open, high, low, close, volume and trade count identical on every day** |
| Allowed differences | 1 day built from the hours that Kraken's 1d file lacks (BTC 2024-03-31: a hole in Kraken's daily archive); 0 days the other way |
| Rerun of the tool | the same files; coverage.yaml unchanged (nothing recorded twice) |
| Steps 3 and 4 and the engine on bar 4h | one plan (night_run's 003-03, copied with `data-bar: 4h`, its 60-day vol window as 360 bars, 2190 bars a year, horizon 5 bars), run by step 4 in a scratch folder: **6 coins x 24 windows, all run**. Bars every 4 h at 00..20 UTC (17,520 BTC bars, 720 per window = 120 days x 6); every engine bar's OHLC equal to the 4h file; forecast and 60-day vol present from the window's first bar (warm-up loaded) |
| Step 3 | bar-general in code: `bars_per_day('4h')` = 6; sizing and horizon converted to bars; the brief's `bar: 4h` wins in step 2 |
| The bot's tests (`cd trading-bot && pytest -q`) | **1585 passed, 16 skipped, 0 failed** |

## What it changes elsewhere
- Nothing that runs today: every existing plan is 1h (101) or 1d (203); their files and coverage lines are unchanged.
- A Kraken backtest on 4h bars now reads the 4h file as it is (`data/coverage.data_bar` returns None when the bar has
  its own file). Before, the engine built 4h bars from the 1h file (CandleBuilder), anchored on the first row's hour
  and re-anchored after a gap, not on UTC blocks. No run used that path.
- A bar of 8h or 12h would now be built from the 4h file instead of the 1h one (same content when blocks align).
