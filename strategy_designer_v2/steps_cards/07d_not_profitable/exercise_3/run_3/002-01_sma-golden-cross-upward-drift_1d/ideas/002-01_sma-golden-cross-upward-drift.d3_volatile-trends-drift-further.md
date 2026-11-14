---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 50-day SMA is above its 200-day SMA, the coin's upward drift is larger the higher its recent daily volatility.
Consequence: A trader would not shrink the golden-cross position in volatile stretches, since those stretches carry most of the gain.
Why:
- F6: The volatility sizing puts the smallest positions where the coin gains most: in the highest 20-day volatility quintile the coin earns 0.004961 a day (t 2.89) at a mean allocation of 0.33, while the lowest quintile earns 0.000591 at an allocation of 0.67.
- F2: While long, the coin's own past 20-day return grades what follows: in the top quintile (above +18.9%) the book earns 0.002455 a day (Sharpe 1.52, n=1731) and the coin 0.005509 (t 3.69); in the middle quintile the book earns 0.000157 and in the bottom quintile 0.000102.
