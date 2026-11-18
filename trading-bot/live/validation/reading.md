# Live mode: validation reading

Against the card's quality criteria (`live/card.md`). Counts, not impressions; what is untested is said.

## Exercise 1: proof of the build, offline (2026-11-17, re-proven after merging master on 2026-11-18)

| Criterion | Check | Result |
|---|---|---|
| 5 Backtest unchanged | 3 fixed backtests rerun, compared file by file with the baseline | 24 of 24 files identical (run time, run id and commit id aside), after the build and again after merging master; two baseline runs also identical |
| 1 Parity | 60 simulated days of recorded Kraken candles through a live session, then the backtest engine on the session's candles | `local_book.csv` byte-identical, 60 bars, at least one trade |
| 2 No lookahead | every poll: last candle fed vs simulated clock | 0 candles fed before their hour ended |
| 3 Timing | decision time minus bar end | every bar within one poll (1,789 s) |
| - Test suites (after the merge) | bot suite; cards' suite | 1,530 passed; cards 75 passed, 2 failed: master's own tests on Windows (a `\` vs `/` path, a cp1252 read), the card files being byte-identical to master's |
| - Kraken helpers | paging past 2,000 rows, forming candle dropped, names, account parsing, target switch | 5 of 5 tests |
| - Real API smoke test | warm-up of 912 days on PF_XBTUSD | 21,910 hourly candles (912 x 24 + 22), none missing, about 10 s; strategy ready |

Found and fixed during the exercise: `is_ready()` on the live strategy moved one record column
(`debug_info.bars_in_regime`), so parity failed on that column alone; readiness is now checked on a throwaway copy.

## Exercise 2: the validating run `first_paper` (orders off), started 2026-11-17 23:19 UTC

Purpose: show the mechanism on real Kraken data with no money at stake. Pre-registered outcomes, read after about a
week: **A** one bar decided per day about one poll after 00:00 UTC, real book recorded, replay IDENTICAL (the
mechanism holds; step 4 next); **B** replay DIFFERENT (a live-path defect before step 4); **C** missing days or
failed polls (connection or PC problem first).

Setting: strategy and coin as the card's fixed inputs; local book from the real account's value, 105.94 USD,
no position; first traded bar 2026-11-17.

First checks, 2026-11-18 about 11:00 UTC (one live bar), script `tb-live-proof/checks_first_paper.py` (outside git):

| Check | Result |
|---|---|
| Hourly candles recorded (warm-up + live) | 21,924; 0 missing hours, 0 duplicates |
| The same period re-fetched from Kraken afterwards | 21,924 of 21,924 rows identical: no candle revised after live used it |
| Daily bars built from hourly vs Kraken's own daily candles | 913 of 913 days identical (open, high, low, close, volume) |
| Bar 2026-11-17: timing | decided 00:00:55 UTC |
| Bar 2026-11-17: decision path | regime unknown, forecast 0, sized target 0, previous allocation 0, change 0, no rebalance attempted, local and real book both 105.9386 |
| Bar 2026-11-17: the 30-day rule by hand | close 64,883 vs 82,008 thirty days before: -20.88%, so not trending, so forecast 0, as recorded |
| Engine on the same live candles, last 121 days | regime matches the hand rule on 121 of 121; forecast 0 on every non-trending day; 87 trending days (last 2026-10-20), 13 trades |
| Replay proof | IDENTICAL (1 bar) |
| Research data (Kraken spot) vs live (Kraken perp), 592 overlapping days | closes differ by +0.02% at the median, within 0.09% on 95% of days; the 30-day rule differs on 2 of 562 days (the deferred spot-vs-perp question, measured only) |

Untested so far: a bar that trades live (none until the 30-day change turns positive), a restart, a missed poll.
Reading of the run: pending (about a week).
