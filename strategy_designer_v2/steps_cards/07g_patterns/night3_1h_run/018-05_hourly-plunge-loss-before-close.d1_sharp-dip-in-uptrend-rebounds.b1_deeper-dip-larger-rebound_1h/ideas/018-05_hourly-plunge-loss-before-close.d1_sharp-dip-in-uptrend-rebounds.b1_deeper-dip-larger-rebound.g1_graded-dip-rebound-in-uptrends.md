---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.b1_deeper-dip-larger-rebound
line: 7.g patterns
backtest: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.b1_deeper-dip-larger-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is positive, it rises over the next 3 days by more than its normal drift after any 24-hour fall, and the rise grows steadily with the depth of that fall measured in multiples of its 30-day average absolute 24-hour return, from ordinary falls to deep ones.
Consequence: Inside a month-long rise, a trader buys for 3 days after every 24-hour fall, scaling the position smoothly with the fall's depth in usual daily moves rather than waiting for only the most extreme drops.
Why:
- F1: Inside a 30-day rise, the 72-hour rebound grows with the depth of the 24-hour fall across all falls, not only the deepest. On 950 non-overlapping 72-hour cases with a 24-hour fall and a positive 30-day return, the Spearman correlation between the fall's depth (in 30-day average absolute 24-hour returns) and the unusual 72-hour move is 0.165, about t 5. The deepest tenth of 24-hour moves (median -1.89 usual moves) is followed by +0.237 usual moves (+210 bps, t 3.46, 218 cases), and the tenth at a median of -0.27 by -0.133 (t -2.09).
- F2: The tested forecast bets only on the deepest falls. Its mean is 13.5 in that deepest tenth, 3.3 in the next and about 0 beyond, so the depth barely varies among the bets. That fits the failed supporting check (larger half minus smaller half -0.23 %) while F1's grading across all falls holds.
- F3: The rebound is confined to rising months. The deepest 15 % of 24-hour falls inside a 30-day decline are followed by +0.037 usual moves (t 0.76, 360 cases), against +0.15 to +0.18 in each tercile of 30-day rise strength (t 1.49 to 2.43, about 145 cases each).
- F4: The rebound after the deepest tenth of falls in a rise is positive on all six coins and in both halves of the record, but uneven over years.
- F5: The rebound after the deepest falls is large next to the cost of a trade: +210 bps unusual over 72 hours, about 11 times the 19 bps a buy and a sell cost this backtest.
