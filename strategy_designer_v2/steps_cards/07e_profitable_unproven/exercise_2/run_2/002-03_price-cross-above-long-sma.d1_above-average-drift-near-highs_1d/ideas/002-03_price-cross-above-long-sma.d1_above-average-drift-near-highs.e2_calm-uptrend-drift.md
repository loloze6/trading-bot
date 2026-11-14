---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs
line: 7.e profitable but not proven
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin above its long moving average whose recent daily volatility is low relative to its own history drifts upward over the following weeks by more than its usual drift. The quieter the advance, the larger the drift.
Consequence: Favour holding trend longs through calm, orderly advances and cut exposure when the uptrend turns volatile.
Why:
- F7: The only 20-bar pocket inside the trending regime is the calm one. In the coin's lowest third of 30-day volatility, the excess 20-bar return is +0.041 (t 2.17, n 96). The middle third shows −0.023 (t −1.04, n 76) and the highest third −0.010 (t −0.32, n 96).
- F4: Nearly all the gain came in moderate uptrends. Bars whose past 60-day rise lies in (0, 0.2] carry 49% of the summed gain and those in (0.2, 0.5] carry 48%. In the (0, 0.2] state, the next-bar return while in the market is 49.6 bps against 14.7 bps on all bars of that state. Bars after 60-day falls contribute −1.3% of the gain.
