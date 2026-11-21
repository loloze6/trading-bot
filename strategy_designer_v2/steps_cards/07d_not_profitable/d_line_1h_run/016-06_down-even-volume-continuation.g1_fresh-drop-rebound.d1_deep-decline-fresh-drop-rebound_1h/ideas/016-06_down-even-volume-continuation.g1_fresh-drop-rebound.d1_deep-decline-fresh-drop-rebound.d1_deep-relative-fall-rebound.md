---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound
line: 7.d not profitable
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has fallen over the past 3 days, the larger its fall over the last 1 day, the more it rises over the next 3 days, and the deeper its 3-day fall, the larger that rebound, only while that 3-day fall is large against the coin's typical 3-day move over the past 30 days, the rebound growing with that relative depth.
Consequence: Buy the rebound only after falls that are deep for the coin's own recent volatility, and keep it for days, instead of leaning long through every mild 3-day decline.
Why:
- F1: Fees, not a missing effect, are what sink the book: before fees it earns 0.000132 a day, but it pays 0.000878 a day in fees, about 6.6 times its gain, with a turnover of 0.81 of the book a day.
- F3: The book's timing loses: of its 0.000132 a day before fees, 0.000312 comes from the coins' own rise and -0.000180 from timing, even though the book is long on 66% of bars at a mean allocation of 0.32.
- F4: Only the deepest falls rebound, while mild 3-day declines keep underperforming, and the book is long through all of them. On the non-overlapping 72-hour grid of falling bars (550 cases per quintile), the deepest 3-day-fall quintile (mean -14.4%) earns an excess 72-hour return of +0.59%, the middle quintiles earn -0.05% to -0.48%, and the mildest (mean -0.6%) earns -1.13%.
- F5: The fresh 1-day fall pays only at its extreme: in the deepest 1-day-return quintile (mean -8.5%) the excess 72-hour return is +0.98% (excess 24-hour return +0.99%), while the other four quintiles lie between -0.28% and -1.05%.
- F6: The forecast, standardised over the coin's last 60 to 72 hours, does not rank the rebound by its real depth. Next-hour gain per bar is negative in the lowest forecast quintile (-6.3e-6) and also in the highest (-5.6e-5, mean forecast 17.8), while only the middle quintiles are positive (2.7e-5 and 8.0e-5). Fees run from 3.7e-5 to 9.4e-5 per bar, at least as large as any quintile's gain.
