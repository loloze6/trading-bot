---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs
line: 7.e profitable but not proven
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average, the stronger its rise toward its 20-day high, the larger its rise over the next 5 days.
Consequence: A trader would treat a strong push to recent highs above the long average as a short-lived long, taken for days and not weeks.
Why:
- F2: The forecast grades the move over short horizons but not over the plan's 20 days: the pooled slope t is 2.94 at 1 day (n=17380), 3.21 at 3 days (n=5723), 2.91 at 5 days (n=3419) and 3.32 at 10 days (n=1691), against 1.22 at 20 days (n=827) and 0.98 at 40 days (n=395).
- F3: The grading also holds among the active cases alone: the slope t within forecast > 0 is 2.29 at 1 day, 2.74 at 3 days, 1.89 at 5 days and 2.70 at 10 days (598 cases), but only 0.85 at 20 days (284 cases).
- F4: At 10 days the top forecast tercile earns a de-meaned +0.0346 (200 cases), against -0.0061 for the low tercile, -0.0010 for the mid tercile and -0.0050 when flat; at 5 days the terciles rise from -0.0033 to 0.0084 to 0.0107.
- F6: The gain is concentrated in time: windows w11, w17 and w21 (years 2021, 2020 and 2024) hold 68% of the summed daily book returns, and without them the book's mean falls to 0.000208 with a Sharpe of 0.41; the 10-day slope t drops from 3.32 to 1.85 (n=1481) and the 5-day one from 2.91 to 1.24.
