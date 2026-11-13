---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-02_sma-death-cross-downward-drift
line: 7.g patterns
backtest: 002-02_sma-death-cross-downward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When the 50-day SMA stands extremely far above the 200-day SMA, the coin's next 10-day return falls below its usual drift and rises less than half the time.
Consequence: A trader would refuse new longs, or cut them, when the short average is stretched far above the long one.
Why:
- F3: The furthest-above deciles show the weakest drift. With the short SMA very far above the long (raw spread >206), the forward 10-bar return is −0.18% with 46% up. In the flat state with spread above 150, the mean is −0.36% / +0.18% (falling / rising) against about +2% for spreads between 0 and 150, which points to exhaustion at extreme stretch above the long average.
