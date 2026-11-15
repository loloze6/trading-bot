---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 50-day SMA is above its 200-day SMA, the longer it has stayed above over the past 20 to 60 days, the larger the coin's return over the next 10 days, relative to the days right after the cross.
Consequence: A trader should not buy the fresh golden cross itself but add exposure once the uptrend has persisted for a few weeks.
Why:
- F6: Uptrend age matters mildly. In the first 20 days of the on state the 10-day excess return is -0.0058 (304 cases), against +0.0066 at 20 to 60 days (328) and +0.0002 at 60 to 150 days (200), so fresh crosses do not drift upward.
- F1: The 50/200 spread forecast predicts almost nothing at any horizon: the pooled slope's t is 0.20 at 5 days (3349 cases), 0.37 at 10 days (1657), 0.55 at 20 days (811) and -0.06 at 40 days (388), and forward 10-day excess returns are 0.0005 with the forecast on against -0.0005 with it off (Welch t 0.14, 832 vs 825 cases).
