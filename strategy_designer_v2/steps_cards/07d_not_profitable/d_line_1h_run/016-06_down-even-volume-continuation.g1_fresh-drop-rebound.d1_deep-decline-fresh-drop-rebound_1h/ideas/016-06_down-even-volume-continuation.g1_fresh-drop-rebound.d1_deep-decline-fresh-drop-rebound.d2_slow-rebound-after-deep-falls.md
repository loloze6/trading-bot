---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound
line: 7.d not profitable
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's fall over the past 3 days against its typical 3-day move over the past 30 days, the more it rises over the following 3 days, and this rebound shows across the whole 3 days after the fall, not only in its first hours.
Consequence: A rebound position sized by the relative depth of the fall can be held for days, and so turned over slowly, which keeps fees small against the rebound.
Why:
- F1: Fees, not a missing effect, are what sink the book: before fees it earns 0.000132 a day, but it pays 0.000878 a day in fees, about 6.6 times its gain, with a turnover of 0.81 of the book a day.
- F2: The position flickers rather than holding through the 3-day rebound it bets on: the forecast's active runs last a median of 3 hours (mean 17, a quarter of them 1 hour, 11770 runs), so trades open and close as the 72-hour return crosses 0 and the 1-day fall is clipped back to 0.
- F4: Only the deepest falls rebound, while mild 3-day declines keep underperforming, and the book is long through all of them. On the non-overlapping 72-hour grid of falling bars (550 cases per quintile), the deepest 3-day-fall quintile (mean -14.4%) earns an excess 72-hour return of +0.59%, the middle quintiles earn -0.05% to -0.48%, and the mildest (mean -0.6%) earns -1.13%.
- F5: The fresh 1-day fall pays only at its extreme: in the deepest 1-day-return quintile (mean -8.5%) the excess 72-hour return is +0.98% (excess 24-hour return +0.99%), while the other four quintiles lie between -0.28% and -1.05%.
