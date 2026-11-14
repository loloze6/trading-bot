---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-01_breakout-drift-lasts
line: 7.d not profitable
backtest: N4-01_breakout-drift-lasts_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A close at a new 20-day high is followed by a further rise over the next one to two weeks when the coin has already risen strongly over the prior 20 days, rather than when it reaches the top of a flat range.
Consequence: Take new-high longs only after a strong prior 20-day rise, and refuse those that come out of a flat or falling month.
Why:
- F5: The edge sits in strong prior uptrends. On active bars, the mean daily P&L is +0.0065 in the top quartile of the 20-day return (above +17%) and +0.0026 in the next quartile. It is only +0.0003 and +0.0004 in the two quartiles where the 20-day return is below +3.8%. Bars whose 60-day return lies between -20% and 0 lose -0.0022 per day over 1561 bars.
- F2: The gains are lopsided by holding time. The 1705 trades held more than 15 days earn +12.0% gross each (sum of net +20336%). The 1563 trades held 15 days or less all lose on average: -9.1% for 1 day or less, -4.6% for 1.5 to 3.5 days, -4.4% for 3.5 to 7.5 days and -3.3% for 7.5 to 15 days (sum of net -6374%). Overall the median trade is -2.4% and only 41.7% of trades win.
