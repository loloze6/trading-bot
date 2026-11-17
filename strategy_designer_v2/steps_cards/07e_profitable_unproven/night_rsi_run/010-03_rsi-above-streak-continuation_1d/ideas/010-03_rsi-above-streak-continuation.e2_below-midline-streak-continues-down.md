---
brief: 010_rsi-midline-regime-direction
source-idea: 010-03_rsi-above-streak-continuation
line: 7.e profitable but not proven
backtest: 010-03_rsi-above-streak-continuation_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The longer a coin's 14-day RSI has stayed below 50 without a break, counted in days up to the close, the lower its return over the next 7 days.
Consequence: A long unbroken stretch of seller control is a reason to stay out of or short the coin for the following week.
Why:
- F5: Below 50, a longer run below the midpoint gives a slightly lower 7-day excess return (slope t -1.15, 406 cases). The below-50 bucket's 7-day excess mean is -0.0101 (t -1.90), so the information sits on both sides of the midpoint.
- F1: The book earns from RSI(14) being above 50, not from how long it has stayed there, and at horizons shorter than the plan's 14 days. On a non-overlapping grid, the coin's forward return is higher when RSI is above 50 than when it is at or below 50: 0.0029 vs -0.0004 at 1 day (t 3.03, 2929/2865 cases), 0.0081 vs -0.0004 at 3 days (t 2.67, 962/945), and 0.0195 vs -0.0006 at 7 days (t 2.58, 409/406). At 14 days the difference is no longer significant: 0.0249 vs 0.0118 (t 0.79, 199/185).
