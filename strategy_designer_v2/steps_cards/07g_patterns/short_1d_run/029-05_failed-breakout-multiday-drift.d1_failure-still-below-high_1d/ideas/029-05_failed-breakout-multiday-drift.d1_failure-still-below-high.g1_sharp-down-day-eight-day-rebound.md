---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-05_failed-breakout-multiday-drift.d1_failure-still-below-high
line: 7.g patterns
backtest: 029-05_failed-breakout-multiday-drift.d1_failure-still-below-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall measured against its own 20-day volatility of daily returns, the more the coin rises over the next 8 days.
Consequence: A trader would lean long a coin after an unusually sharp down day for its volatility, more so the sharper the fall, and would refuse to short into such a day.
Why:
- F1: The coin's own day return, scaled by its prior 20-day volatility, predicts the next 8 days the opposite way. The slope of the unusual 8-day move on that scaled return is -0.0152, t -4.58, over 1691 non-overlapping cases. Bars in the lowest quintile of the scaled return go on to an unusual move of +2.87 % (t 3.21, 342 cases), against -2.21 % in the fourth quintile (t -3.46) and -1.19 % in the top quintile (t -1.57).
- F2: This reversal is not one coin's or one period's. Its slope is negative in all six coins (t from -0.73 in XRP to -3.06 in ZEC) and in all eight years (strongest in 2022 at t -4.23 and 2018 at t -2.68). It is also negative in every volatility tercile (t -2.63, -3.49, -2.09).
- F3: The reversal shows at every horizon tried. On the raw day return, the slope's t is -2.45 at 2 days (8506 cases), -3.34 at 4 days, -5.07 at 8 days and -3.18 at 12 days, so it builds to about 8 days.
- F4: The reversal is carried by down days. On days that closed down, the slope on the scaled return is -0.0151 (t -2.16, 820 cases) and the mean unusual move is +1.44 %. On up days the slope is -0.0036 (t -0.57, 870 cases).
- F9: A larger move is available than the tested idea's. The lowest-quintile reversal moves +2.87 % beyond the drift over 8 days; on the long side the drift of about +0.5 % to +1.7 % per 8 days adds to it. That is about 15 times the 0.19 % cost of a trade, against the tested idea's total move of -0.21 %.
