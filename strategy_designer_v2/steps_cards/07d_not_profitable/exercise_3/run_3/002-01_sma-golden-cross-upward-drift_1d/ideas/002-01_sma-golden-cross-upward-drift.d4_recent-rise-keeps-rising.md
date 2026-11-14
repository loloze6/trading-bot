---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin has risen strongly over its recent weeks, it keeps rising over the following days, and the larger the past rise, the larger the next rise.
Consequence: A trader would go long in proportion to the coin's recent return, including while its averages have not yet crossed, which takes in the drift the cross book misses when flat.
Why:
- F2: While long, the coin's own past 20-day return grades what follows: in the top quintile (above +18.9%) the book earns 0.002455 a day (Sharpe 1.52, n=1731) and the coin 0.005509 (t 3.69); in the middle quintile the book earns 0.000157 and in the bottom quintile 0.000102.
- F5: Holding beats the book because the flat bars still carry the coin's drift: on the 8454 bars with forecast 0 the coin averages 0.001295 a day (t 2.79) while the book earns 0.000018. Every coin's book mean (0.000108–0.000868) is below its coin mean (0.000670–0.001879).
