---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 50-day SMA is above its 200-day SMA, the coin keeps rising, further the larger the spread, only while its own recent return is strongly positive and its price stands near its recent high; the stronger the recent rise, the larger the gain that follows.
Consequence: A trader would hold the golden-cross long in proportion to the coin's recent momentum and refuse it when price stalls or drops away from its high inside the cross.
Why:
- F2: While long, the coin's own past 20-day return grades what follows: in the top quintile (above +18.9%) the book earns 0.002455 a day (Sharpe 1.52, n=1731) and the coin 0.005509 (t 3.69); in the middle quintile the book earns 0.000157 and in the bottom quintile 0.000102.
- F3: While long, bars near the coin's 60-day high (within 3.4%) earn the book 0.001762 a day (Sharpe 1.11, n=1881); the other drawdown quintiles earn between -0.000125 and 0.001094.
- F4: The deepest falls happen while the book is long: BTC fell -45.6% in 88 days while fully long (share long 1.00, mean forecast 15.2, coin -63%). ZEC fell -84.8%, XRP -59.6% and ETH -69.1%, with the book long 61–75% of those stretches and the coin falling 71–92%. This is what keeps Calmar at 0.20.
