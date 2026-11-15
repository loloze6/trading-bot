---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 50-day SMA is above its 200-day SMA, the larger the coin's 10-day return, the more it rises over the next 10 days relative to its usual 10-day return.
Consequence: A trader in an uptrend would add to coins with the strongest recent 10-day gains and hold back on those that have just fallen.
Why:
- F5: The coin's own past 10-day return predicts its next 10-day excess return where the spread does not.
- F4: The forecast mostly tracks the market's yearly move rather than predicting the next 10 days.
- F2: The effect is not graded by the spread. The mean 10-day excess return by forecast bucket runs -0.0085 (0–5, n 212), 0.0023 (5–10, n 183), 0.0105 (10–15, n 174) and 0.00004 (15–20, n 263), with a standard deviation of 0.15–0.22 in each bucket. The hit rates in the positive buckets (0.47–0.52) are below the flat bucket's 0.53, which matches the failed supporting check (-0.021).
