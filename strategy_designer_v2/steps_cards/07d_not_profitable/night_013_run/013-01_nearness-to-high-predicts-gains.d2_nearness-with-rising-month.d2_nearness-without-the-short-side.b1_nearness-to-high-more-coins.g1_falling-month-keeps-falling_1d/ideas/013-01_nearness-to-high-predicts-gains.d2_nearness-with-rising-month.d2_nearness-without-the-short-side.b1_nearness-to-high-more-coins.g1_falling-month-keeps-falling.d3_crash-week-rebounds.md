---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins.g1_falling-month-keeps-falling
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins.g1_falling-month-keeps-falling_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is negative, the larger its 7-day loss, the higher its return over the next 7 days relative to its own average.
Consequence: A trader treats a crash week inside a falling month as a candidate for a long rebound, not for adding to a short.
Why:
- F2: The losses sit in the deepest, fastest falls, where the coin bounces the next day:
- F3: On the 7-day grid in the falling month, the depth effect is not monotone, so the linear slope fails (t 0.86):
- F5: The worst 5% of bars came right after sharp drops, with the book more heavily short:
