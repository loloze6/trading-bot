---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.d2_daily-move-continues-five-days
line: 7.b inconclusive
backtest: 022-04_signal-weights-carry-forward.d2_daily-move-continues-five-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's move over the last day against the direction of its 20-day return, the larger its move over the next 20 days in the direction of that 20-day return, undoing the day's move.
Consequence: A trader would fade a large day that goes against the coin's 20-day trend and expect the trend to resume over the following weeks.
Why:
- F5: A day against the coin's 20-day return reverses over the next 20 days, and the reversal grows with the day's size: slope t -4.76 on 417 independent cases, a mean move in the day's direction of -3.11 % (16 times the 0.19 % cost). The same split shows it already over 10 days (t -2.36, -0.80 %, 921 cases) and over 3 days (t -2.87, 3,134 cases).
- F1: The positive 5-day result does not hold at nearby horizons. On non-overlapping grids, the slope of the demeaned forward return on the forecast has t -5.64 over 1 day (17,380 cases), -1.62 over 2 days (8,650), -1.80 over 3 days (5,723), +1.46 over 5 days (3,419), -0.29 over 10 days (1,691) and -2.40 over 20 days (827), so the plan's t of 1.46 looks like a chance positive among mostly reversing horizons.
- F4: Even if real, the idea is too small to pay. Its unusual move is +0.18 % per case over 5 days, a strength of 0.015 (about a third of the 0.05 that real ideas usually show, findings F10), and its total move of +0.17 % is 0.9 times the 0.19 % cost of a buy and a sell, where no confirmed idea below the cost has paid (0 of 40, findings F11).
