---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 50-day SMA is above its 200-day SMA, the price keeps rising over the next 10 bars when the coin's own 60-day return is not among its weakest, and it falls when the 60-day return is among its weakest.
Consequence: A trader would refuse longs inside an up-trend whose price has stalled over the last 60 days.
Why:
- F4: Inside an up-trend, 60-bar momentum separates winners from losers. In the lowest 60-bar-return tercile the forward 10-bar return is -0.55%; in the middle tercile it is +3.72% and in the top tercile +1.49%.
- F3: A larger forecast does not earn more. Forward 10-bar return by forecast bucket is 1.46% (0-5), 1.67% (5-10), 0.81% (10-15) and 0.49% (15-20), then 2.38% at the cap. Over non-overlapping blocks the slope has t = 0.37.
