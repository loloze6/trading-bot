---
brief: 016_grind-versus-jump-moves
source-idea: 016-01_up-grind-price-continuation
line: 7.g patterns
backtest: 016-01_up-grind-price-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The higher a coin's average return in a given UTC hour of day over its past 30 days, the more the coin rises during that same hour over the next day.
Consequence: A trader times long exposure to the hours of the day where the coin's own recent hourly drift has been strongest, such as the 20-21 UTC hours.
Why:
- F2: UTC hours 20 and 21 carry a large share of the coins' rise. Their mean hourly returns are +0.000545 (t 6.75) and +0.000436 (t 5.66), against a range of -0.000356 to +0.000271 for the other 22 hours. The excess of hours 20-21 over the other hours is positive in all 6 coins (+0.00041 to +0.00053, Welch t 2.66 to 4.10) and in 7 of 8 years (Welch t 1.43 to 4.95 in those 7; 2022 is -0.00017, t -1.07).
