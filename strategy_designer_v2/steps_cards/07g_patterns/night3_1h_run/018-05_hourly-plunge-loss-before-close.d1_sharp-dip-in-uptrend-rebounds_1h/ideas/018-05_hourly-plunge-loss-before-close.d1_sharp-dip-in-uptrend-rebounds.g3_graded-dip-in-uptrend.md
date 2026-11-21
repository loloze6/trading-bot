---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds
line: 7.g patterns
backtest: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, is a fall measured in multiples of its 30-day mean absolute 24-hour return, the coin rises over the next 3 days more than its normal drift, and the rise is larger the larger the fall multiplied by the coin's 30-day return measured in multiples of its usual 30-day move, with a continuous scale whose values stay distinct up to the deepest falls.
Consequence: The deeper the dip and the stronger the month's rise, the larger the rebound long a trader should hold.
Why:
- F4: Among falls, a deeper 24-hour fall is followed by a larger 72-hour move. The Spearman rho is 0.083 (p 0.00015, 2054 cases). Inside a positive 30-day return, the deepest quartile of falls gives +2.17 % (t 3.78, 238 cases, strength 0.26). Inside a negative 30-day return, the same quartile gives only +0.62 % (t 1.33, 276 cases).
- F6: The tested forecast is barely graded in practice, which explains why the supporting check could not be run. On bars with a positive forecast, 53 % sit at the +20 cap and the median is 20. As a result, all 2803 cases tied at or below the median entry forecast.
- F5: The rebound after sharp falls is uneven over time, so it depends on the regime. By year, the deepest-fall cases give:
