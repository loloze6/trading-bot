---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 50-day SMA has stayed above its 200-day SMA for more than about 20 bars, the price keeps rising over the next 10 bars more than it does in the first 20 bars after the up-cross.
Consequence: A trader would skip the first weeks after a golden cross and take the long only once the trend has lasted about a month.
Why:
- F2: The drift does not start at the cross. In the first 20 bars after the 50-day SMA rises above the 200-day, the forward 10-bar return is -1.03%; at 20 to 60 bars of age it is +2.97%. In the first 20 bars after a down-cross, while the book is flat, it is +2.09%. Moves right after a cross reverse.
- F6: Fees are not the cause; whipsaws are. The 1091 trades have a mean gross gain of +0.87% against about 0.1% commission each. Trades held 40 days or less (635 of them) lose -10.1% gross each, while those held longer than 40 days gain +16.1%. The per-window book drawdown reaches -96% (XRP) and -93% (ZEC), which makes the Calmar ratio 0.001.
