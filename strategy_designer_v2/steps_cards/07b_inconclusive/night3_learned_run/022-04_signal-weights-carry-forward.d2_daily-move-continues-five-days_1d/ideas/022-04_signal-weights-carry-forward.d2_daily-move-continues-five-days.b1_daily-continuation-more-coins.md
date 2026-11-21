---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.d2_daily-move-continues-five-days
line: 7.b inconclusive
backtest: 022-04_signal-weights-carry-forward.d2_daily-move-continues-five-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's move over the last day, the larger its move in the same direction over the next 5 days.
Consequence: A trader would treat a large daily move as the start of a short continuation and refuse to fade it.
Why:
- F1: The positive 5-day result does not hold at nearby horizons. On non-overlapping grids, the slope of the demeaned forward return on the forecast has t -5.64 over 1 day (17,380 cases), -1.62 over 2 days (8,650), -1.80 over 3 days (5,723), +1.46 over 5 days (3,419), -0.29 over 10 days (1,691) and -2.40 over 20 days (827), so the plan's t of 1.46 looks like a chance positive among mostly reversing horizons.
- F2: The 5-day effect is mixed across years and coins. By year the t is +3.76 in 2019 and +2.31 in 2023 but -2.23 in 2022, with five other years between -1.14 and +1.13. By coin only XRP reaches t 2.05 (570 cases), while BTC, ETH, LTC and XMR lie between -0.57 and +0.35.
- F4: Even if real, the idea is too small to pay. Its unusual move is +0.18 % per case over 5 days, a strength of 0.015 (about a third of the 0.05 that real ideas usually show, findings F10), and its total move of +0.17 % is 0.9 times the 0.19 % cost of a buy and a sell, where no confirmed idea below the cost has paid (0 of 40, findings F11).
