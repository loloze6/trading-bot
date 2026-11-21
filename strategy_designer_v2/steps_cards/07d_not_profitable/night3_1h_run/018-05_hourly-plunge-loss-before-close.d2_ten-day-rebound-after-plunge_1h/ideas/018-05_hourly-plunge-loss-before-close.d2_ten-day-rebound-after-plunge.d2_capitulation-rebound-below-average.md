---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-05_hourly-plunge-loss-before-close.d2_ten-day-rebound-after-plunge
line: 7.d not profitable
backtest: 018-05_hourly-plunge-loss-before-close.d2_ten-day-rebound-after-plunge_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, falls by several times its 30-day average absolute daily return while its price is below its 60-day average price, the coin rises over the next 10 days more than its normal drift, and the further below that average, the larger the rise.
Consequence: A trader sizes a drop-rebound bet by how far the coin is already below its 60-day average, and refuses the bet in coins near or above it, where no unusual rebound follows.
Why:
- F5: The depth of the drop does not grade the rebound. Trades by quintile of the 24-hour fall in usual daily moves net 6.3, 4.3, 2.3, 7.2 and 7.8 % from the deepest to the mildest. The step 5 slope of the unusual move on the forecast has a t of only 0.71.
- F6: The unusual rebound shows only after drops in coins already below their 60-day average. There it is +1.63 % per case (t 0.96, 120 cases). Above that average it is -0.05 % (137 cases). By quintile of distance from the average, the strength is 0.12 and 0.11 in the two furthest below, and -0.01, -0.07 and 0.07 in the others.
