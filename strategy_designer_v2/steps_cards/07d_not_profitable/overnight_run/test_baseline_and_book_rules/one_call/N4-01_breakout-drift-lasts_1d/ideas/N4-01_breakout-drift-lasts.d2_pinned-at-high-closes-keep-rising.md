---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-01_breakout-drift-lasts
line: 7.d not profitable
backtest: N4-01_breakout-drift-lasts_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin whose close stays in the top of its 20-day range keeps rising on the following days. The excess return lives in closes pinned at the high, not in closes that drift back into the middle of the range.
Consequence: Hold only while the close sits at the very top of its range, and let the weak, mid-range readings go flat rather than entering and exiting on them.
Why:
- F7: A larger forecast earns more. Next-bar returns were 0.00266 when the forecast was 15-20 (5,047 bars) and 0.00209 when it was 10-15 (2,155 bars). They were -0.00026 at 0-5 (1,319 bars) and 0.00003 at 5-10 (1,734 bars).
- F6: Fees are not the cause; whipsaw is. There were 3,269 long trades with a median hold of 16 days, and their mean gross was +4.37% against 0.29% commission. The 1,563 trades held 15 days or less all lost: net sums of -403, -1,072, -2,027 and -2,872 across the shorter hold buckets. The 1,705 trades held longer than 15 days carried +20,336.
