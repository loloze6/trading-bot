---
idea: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: the 14-day RSI above 50, graded by how far above -> kept
- Comparison: a rise above the coin's usual move, strongest while the 60-day return is positive -> kept: the excess over the coin's mean move, split by 60-day return sign recomputed from closes
- Outcome: the price rises over the next 10 days -> kept: 10 bars on 1d
- Verdict transfer: yes: the forecast is RSI's distance above 50, and the record tests both the 10-day excess rise and its uptrend strengthening.
Forecast: The forecast uses RSI(14) on daily closes as momentum, through RSIPullbackComponent's (50 - RSI) flipped in sign. That value is standardised against its own past 60 values (target 10, cap 20) and clipped at 0. The forecast is 0 when RSI is at or below 50 and positive when RSI is above 50. It grows steadily with RSI's distance above 50 and never goes negative.
Config: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The cases are non-overlapping 10-bar grid bars (positions 0, 10, 20, ... of each coin-window). On those cases, fit a pooled OLS slope of y on the forecast at bar t, where y is close[t+10]/close[t] - 1 minus that coin's mean 10-bar return over all windows. Report the slope's t.
- Supporting check: Recompute the 60-day return close[t]/close[t-60] - 1 from closes, leaving out cases without 60 prior bars in the window. The same slope must be larger on cases with a positive 60-day return than on the other cases.
- Confirm: The main slope's t is 2 or more, and the slope on positive-60-day cases exceeds the slope on the other cases.
- Reject: The main slope's t is -2 or less.
- Inconclusive: These results are inconclusive: a t between -2 and 2, or a t of 2 or more with a failed check. At least 100 cases with forecast > 0 are needed, and at least 30 in each 60-day-return group; with fewer, the test is inconclusive.
