---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In the first 20 days after a coin's 50-day SMA crosses above its 200-day SMA, the coin falls relative to its usual move over the next 10 days, and the fall is larger the more recent the cross.
Consequence: A trader should not buy the golden cross on its day but wait for the early give-back before following the trend.
Why:
- F6: The cross itself does not start a drift. Bars within 20 days after the spread turned positive have mean excess 10-day return -0.018 (107 cases) and 40-day return -0.123 (17 cases). Bars 20–60 days after have +0.004 and +0.082. Early post-cross moves tend to give back first.
