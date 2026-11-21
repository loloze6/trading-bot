---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The narrower a coin's past two days of price range and the quieter its average four-hour range over the past 7 days, both compared with its past 30 days, the lower its return over the next three days.
Consequence: A trader should refuse or shrink long positions taken out of quiet, narrow stretches, and weight longs toward coins whose recent week was turbulent.
Why:
- F2: A quiet past week is followed by underperformance, the opposite of the brief. The fifth of grid cases whose 7-day average 4h range is smallest against its 30-day average ends the next 3 days -0.77 % below the normal drift (t -3.13, strength -0.084). The loudest fifth ends +0.60 % above it (t 1.95). The quiet fifth is below drift in all 6 coins (t -0.29 to -2.27) and in 7 of 8 years (2024 t -5.54).
- F3: A narrow preceding two-day stretch is also followed by underperformance. On the grid, the narrowest fifth (stretch range against the 30-day mean 4h range) ends the next 3 days -0.70 % below drift (t -2.65). The widest two fifths end +0.41 % and +0.40 % above it. The per-coin Spearman correlation of narrowness with the next 3 days' excess return is negative in all 6 coins (-0.038 to -0.084).
- F4: Quiet weeks do not lead to larger moves. The mean absolute 3-day move after the quietest fifth of weeks is 5.55 %, against 6.57 % after the loudest fifth.
