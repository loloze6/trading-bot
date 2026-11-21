---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.d2_daily-move-continues-five-days
line: 7.b inconclusive
backtest: 022-04_signal-weights-carry-forward.d2_daily-move-continues-five-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's move over the last day, the larger its move in the opposite direction over the next day.
Consequence: A trader would refuse to chase a large daily move into the next day and would lean against it for one day.
Why:
- F7: Over the next day, large daily moves reverse in proportion to their size. The move in the day's direction is -0.06 %, -0.06 %, -0.12 % and -0.40 % from the smallest to the largest quartile of the forecast (mean sizes 1.6, 5.0, 9.9 and 18.3; 4,345 cases each). The largest quartile has t -4.74 and moves 2.1 times the 0.19 % cost.
- F1: The positive 5-day result does not hold at nearby horizons. On non-overlapping grids, the slope of the demeaned forward return on the forecast has t -5.64 over 1 day (17,380 cases), -1.62 over 2 days (8,650), -1.80 over 3 days (5,723), +1.46 over 5 days (3,419), -0.29 over 10 days (1,691) and -2.40 over 20 days (827), so the plan's t of 1.46 looks like a chance positive among mostly reversing horizons.
- F3: The two sides disagree over 5 days. After down days the slope has t -2.25 (1,756 cases): the largest down-day decile, forecast -19.2, is followed by +0.75 % above the coin's drift, a rebound. After up days the slope has t +1.73 (1,660 cases): the largest up-day decile, forecast +19.3, is followed by +1.27 %, a continuation.
