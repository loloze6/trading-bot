---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold
line: 7.d not profitable
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has fallen over the past 3 days, the larger its fall over the last 1 day, the more it rises over the next 3 days, only among falls that are large against the coin's usual daily moves, and the rise grows steeply with the fall's size there, with most of it within the first day.
Consequence: Commit capital only on the deepest drops and let the small drops pass, since buying the small ones is where the book loses, both before and after fees.
Why:
- F4: The rebound sits only in the deepest 1-day falls: in the fall regime, forecasts of 15–20 are followed by a 72-hour excess of +0.0099 (n 739), while forecasts of 0–15 are followed by -0.0091 (n 1152; Welch t 4.98), and the 0–5, 5–10 and 10–15 buckets are all negative (-0.0088, -0.0054, -0.0142).
- F5: Most of the deep-fall rebound comes in the first day: for forecasts of 15–20 the excess is +0.0081 over the first 24 hours and only +0.0022 over hours 24–72, which is why the idea's supporting check failed (late slope 6.0e-05).
- F1: Fees, not the forecast, sink the book: the positions earn 0.000107 a day before fees but pay 0.001195 a day in fees, on a turnover of 1.10 of the book a day, which leaves a mean daily book return of -0.001114 and a Sharpe of -1.44.
