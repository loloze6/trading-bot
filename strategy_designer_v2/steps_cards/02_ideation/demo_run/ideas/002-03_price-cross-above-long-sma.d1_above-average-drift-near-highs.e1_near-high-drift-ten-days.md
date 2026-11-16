---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs
line: 7.e profitable but not proven
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average, the higher its close sits in its 20-day close range, the larger its rise over the next 10 days.
Consequence: A trader would scale a long by how near the close is to its 20-day high when above the long average, and would expect the reward to show within about 10 days rather than over a month.
Why:
- F2: The forecast grades the move over short horizons but not over the plan's 20 days: the pooled slope t is 2.94 at 1 day (n=17380), 3.21 at 3 days (n=5723), 2.91 at 5 days (n=3419) and 3.32 at 10 days (n=1691), against 1.22 at 20 days (n=827) and 0.98 at 40 days (n=395).
- F3: The grading also holds among the active cases alone: the slope t within forecast > 0 is 2.29 at 1 day, 2.74 at 3 days, 1.89 at 5 days and 2.70 at 10 days (598 cases), but only 0.85 at 20 days (284 cases).
- F4: At 10 days the top forecast tercile earns a de-meaned +0.0346 (200 cases), against -0.0061 for the low tercile, -0.0010 for the mid tercile and -0.0050 when flat; at 5 days the terciles rise from -0.0033 to 0.0084 to 0.0107.
- F5: Within the active cases at 10 days, the 20-day range position carries the grading (raw t 1.96) more than the 20-day rise does (t 0.61); at 5 days the two are similar (t 1.60 and 1.53), and at 20 days both are about 0 (t -0.16 and -0.11).
