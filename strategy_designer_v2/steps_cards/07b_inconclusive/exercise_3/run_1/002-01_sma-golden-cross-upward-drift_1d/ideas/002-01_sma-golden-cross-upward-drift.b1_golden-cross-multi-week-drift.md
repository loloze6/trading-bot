---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While the 50-day SMA of the close is above the 200-day SMA, the coin's return over the following several weeks is higher than its usual return, by more the wider the spread between the two averages.
Consequence: A trader would use the golden-cross state for a position held for weeks rather than for a ten-day trade.
Why:
- F2: The gap between up-state (forecast > 0) and flat bars widens with the horizon but stays below significance: on minus off is 0.0011 at 10 bars (Welch t 0.14), 0.0179 at 20 bars (0.0089 − (−0.0090), t 0.93) and 0.0379 at 40 bars (0.0194 − (−0.0185), t 0.84), so the plan's 10-bar horizon sits where the gap is smallest.
- F1: The effect is too small to separate from noise at any horizon: the forecast slope's t is 0.20, 0.37, 0.55 and −0.06 at 5, 10, 20 and 40 bars (3349, 1657, 811 and 388 non-overlapping cases), while the 10-bar excess return has a standard deviation of 0.14–0.22 against a mean shift of under 0.011.
