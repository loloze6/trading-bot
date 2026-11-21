---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation
line: 7.b inconclusive
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin whose 30-day return is positive keeps rising over the next 7 days by more than its usual 7-day drift, and the larger its 30-day return, the larger that rise.
Consequence: A coin's month-long rise is a reason to hold it long for the following week, more strongly as the rise is larger.
Why:
- F5: The effect is clearest at a shorter horizon than the plan's: over 168 bars (7 days) the weighted mean excess is +1.19 % at t 2.19 over 1,196 independent cells. Over 336 bars it is +2.41 % at t 1.77 over 568 cells, and over 672 bars +2.23 % at t 0.62 over 276 cells.
- F6: The grading shows on the standardised rise but not on the raw one. The slope of excess on forecast has t 2.62, and forecast quartiles go from −4.07 % (q1) to +4.18 % (q4). But raw 30-day-return quintiles over all cells are flat, from −0.14 % (lowest) to −0.17 % (highest, mean 30-day return +53 %). Cells with zero forecast average −0.77 % (t −1.01, 580 cells).
- F8: The size is above the cost but small next to the noise. The unusual move is +0.75 % per case (strength 0.029, about half the 0.05 of F10 in the prior findings), 3.9 times the 0.19 % round trip; the total move is +2.77 %, 14.4 times the cost. The book beat holding (Sharpe 1.07, 0.52 above holding's) with 0.13 trades a day.
