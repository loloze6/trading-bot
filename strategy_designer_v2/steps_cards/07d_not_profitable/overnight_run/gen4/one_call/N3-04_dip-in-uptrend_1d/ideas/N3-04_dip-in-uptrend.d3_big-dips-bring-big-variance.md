---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-04_dip-in-uptrend
line: 7.d not profitable
backtest: N3-04_dip-in-uptrend_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In an uptrending coin, the next day's move after a drop of more than twice the typical daily move is much more dispersed than after a moderate drop, with a larger absolute size in both directions. The mean gain grows less than that dispersion.
Consequence: A trader should not raise exposure in proportion to the drop size, since the biggest drops carry most of the drawdown risk.
Why:
- F1: The book fails on Calmar (0.52 against 0.75) because its drawdowns are deep, from -42% on BTC to -82% on LTC, while its mean daily return passes (0.00058); its worst 5% of active days sum to -17.7 against a total active gain of +11.5 over 2411 active days, so a few days decide the result.
- F2: The losses come from the largest positions. The 50 worst book days had a mean allocation of 1.92, 94% of them at 1.5 or more, with a mean next-day coin move of -11.1%. The book's daily standard deviation rises from 0.011 at allocations up to 0.5 (1251 days) to 0.111 at allocations of 1.8 to 2.1 (551 days).
- F3: A larger forecast earns more before fees, but noisily. The mean next-day coin return is +0.72% at forecast 3–8 (n=427, t=2.75), +0.05% at 8–14 (n=268, t=0.14), +1.30% at 14–20 (n=155, t=2.96) and +0.78% at the 20 cap (n=525, t=3.18). By drop size it reaches +1.49% for drops over 3 typical moves (n=53, t=2.77).
