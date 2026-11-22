---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-04_downrun-volume-fade-depth-rebound
line: 7.g patterns
backtest: 024-04_downrun-volume-fade-depth-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin's volume over the past day is high relative to its 30-day average, the larger its 1-day fall relative to its usual daily move, the larger its rise over the next three days.
Consequence: A sharp fall on heavy volume is a reason to buy for a three-day rebound, more so the deeper the fall.
Why:
- F3: The direction of the past day's move changes what heavy volume means. In the top volume tercile, a 6-bar fall (lowest tercile of the vol-scaled 6-bar return) is followed by +1.07 % excess (691 cases), against -1.13 % for a flat day (310 cases). In the bottom volume tercile, a 6-bar rise is followed by -1.06 % (436 cases). Pooled, the lowest 6-bar-return quintile gives +0.84 % (t 3.07) and the Spearman is -0.052.
- F2: Recent volume grades the next three days. On non-overlapping 18-bar cells, the past day's volume against its 30-day average sorts the excess return from -0.55 % (t -2.27, 1032 cases, bottom quintile) to +0.80 % (t 2.56, 1032 cases, top quintile). Its Spearman with the excess return is +0.056 pooled and positive in all six coins (0.041 to 0.099, 858 cases each) and in 7 of 8 years (2022: -0.003). The top quintile's total move, about +1.2 %, is about six times the 0.19 % cost of a trade.
- F1: The tested idea's own grading runs the wrong way. Among down-streaks with a loss of more than 3 usual moves, the 18-bar excess return by volume-fade tercile is +0.99 %, +2.10 % and +1.16 % (144–145 cases each), so it does not rise with the fade. Step 5's above-minus-below-median fade difference is -0.58 %. Up-streaks of the same size give +0.96 %, +0.70 % and +0.78 %, so large streaks in either direction are followed by a rise, not a give-back.
