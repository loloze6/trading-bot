---
brief: 010_rsi-midline-regime-direction
source-idea: 010-03_rsi-above-streak-continuation
line: 7.e profitable but not proven
backtest: 010-03_rsi-above-streak-continuation_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 14-day RSI sits above 50 at the close, the higher its return over the next 1 to 7 days. The lower it sits below 50, the lower that return.
Consequence: A trader would lean the position toward the side of the midpoint RSI is on, sized by its distance from 50, and hold it for days rather than weeks.
Why:
- F1: The book earns from RSI(14) being above 50, not from how long it has stayed there, and at horizons shorter than the plan's 14 days. On a non-overlapping grid, the coin's forward return is higher when RSI is above 50 than when it is at or below 50: 0.0029 vs -0.0004 at 1 day (t 3.03, 2929/2865 cases), 0.0081 vs -0.0004 at 3 days (t 2.67, 962/945), and 0.0195 vs -0.0006 at 7 days (t 2.58, 409/406). At 14 days the difference is no longer significant: 0.0249 vs 0.0118 (t 0.79, 199/185).
- F4: The side split holds in both coins on their own. At 1 day: BTC excess 0.0012 vs -0.0013 (t 1.89), ETH 0.0020 vs -0.0020 (t 2.38). At 7 days: BTC t 1.64, ETH t 1.99.
- F5: Below 50, a longer run below the midpoint gives a slightly lower 7-day excess return (slope t -1.15, 406 cases). The below-50 bucket's 7-day excess mean is -0.0101 (t -1.90), so the information sits on both sides of the midpoint.
- F6: The market's own rise is a minority of the gain. Per coin, the market part is 0.00043 of BTC's 0.00133 and 0.00030 of ETH's 0.00056; timing is 0.00091 (BTC) and 0.00026 (ETH).
- F7: The book's gain is not one period or a few trades. Its daily mean is 0.00092 with t 2.93 over 2898 days, and 13 of 24 windows are positive. 2022 is the only clearly losing year (-0.00046 a day) and 2020 the strongest (0.00315). Its top 10 of 567 trades hold 40% of the summed trade returns (1408 of 3501), with a 41% win rate.
