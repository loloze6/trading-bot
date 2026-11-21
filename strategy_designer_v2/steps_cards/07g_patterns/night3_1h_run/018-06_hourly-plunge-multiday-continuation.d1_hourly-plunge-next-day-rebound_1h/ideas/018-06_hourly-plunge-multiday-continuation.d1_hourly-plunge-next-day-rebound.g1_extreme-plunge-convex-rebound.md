---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound
line: 7.g patterns
backtest: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, is a drop far beyond its usual daily moves, measured in multiples of its 30-day average absolute 24-hour return, the price rises over the next 1 day by more than the coin's normal drift. The rise grows much faster than the multiple, so the most extreme drops are followed by rebounds several times larger than those after moderate ones.
Consequence: A trader should buy only the most extreme hourly-read daily plunges, sized up steeply with the plunge's multiple, because only there is the next-day rebound many times the cost of a trade.
Why:
- F1: When a coin's 24-hour return, read on the 24-hour grid, is a drop of at least 3 times its 30-day mean absolute 24-hour return, the next 24 hours end above the coin's normal drift. Over 376 independent cases on 6 coins the mean strength is 0.378 (t 4.6) and the unusual move is +1.87 %. That is about 10 times this backtest's 0.19 % cost of a buy and a sell.
- F2: Past about 3 multiples the rebound is graded, and its strength climbs much faster than the drop's size:
- F3: The deep-drop rebound is positive on all 6 coins: strength 0.16 on LTC to 0.50 on XMR, t 0.8 to 2.6, about 53 to 72 cases each. It is not stable over time. In the first half of the windows it is 0.069 (t 0.9, 194 cases); in the second half it is 0.706 (t 4.9, 182 cases).
- F4: The tested forecast was fully long from 2 multiples onward, so most of its 8426 cases were mild drops. Drops of 0 to 1 multiple even end below drift: strength -0.039, t -2.8, 4968 cases. This explains the tested idea's measured strength of 0.020 and its unusual move of 0.6 times the cost.
