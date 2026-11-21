---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold
line: 7.d not profitable
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has fallen over the past 3 days, the larger its fall over the last 1 day, the more it rises over the next 3 days, with that rebound set by the day's fall as it stands once the day is done, so that the expected rise stays the same through the hours that follow instead of changing from hour to hour.
Consequence: Size the rebound once from the completed day's fall and keep it for about 3 days, so the fees no longer exceed the gross gain of a signal that is real at the 3-day scale.
Why:
- F1: Fees, not the forecast, sink the book: the positions earn 0.000107 a day before fees but pay 0.001195 a day in fees, on a turnover of 1.10 of the book a day, which leaves a mean daily book return of -0.001114 and a Sharpe of -1.44.
- F2: The book trades its signal hour by hour, not over the 3 days the idea is about: the forecast's on-runs last a median 3 hours (mean 8.5, 15930 runs), there are 0.91 new entries a day, and the 58401 trades last a median 5 hours with a mean of -0.386 % before fees and -0.486 % after.
- F3: Holding the position set at each non-overlapping 72-hour grid bar for the full 72 hours would have earned a mean allocation × 72-hour return of +0.0034 per case (t 3.48, n 1891 independent cases), so the rebound is real at the 3-day scale but is lost to hourly re-sizing.
