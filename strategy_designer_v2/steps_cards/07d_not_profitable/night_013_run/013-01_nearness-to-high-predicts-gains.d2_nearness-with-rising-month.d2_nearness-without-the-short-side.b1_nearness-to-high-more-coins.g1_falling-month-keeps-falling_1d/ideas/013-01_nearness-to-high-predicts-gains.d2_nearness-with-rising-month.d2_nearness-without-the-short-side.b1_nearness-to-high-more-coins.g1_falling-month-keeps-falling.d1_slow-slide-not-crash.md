---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins.g1_falling-month-keeps-falling
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins.g1_falling-month-keeps-falling_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is negative, the further its close sits below its 60-day high, the lower its return over the next 7 days relative to its own average, through the range of ordinary declines, except that the larger its 7-day loss, the more this weakness turns into a rebound over the next 7 days.
Consequence: A trader keeps the short on a coin sliding slowly below its high, but cuts it in step with the size of the last week's crash, which is when the coin bounces.
Why:
- F2: The losses sit in the deepest, fastest falls, where the coin bounces the next day:
- F3: On the 7-day grid in the falling month, the depth effect is not monotone, so the linear slope fails (t 0.86):
- F5: The worst 5% of bars came right after sharp drops, with the book more heavily short:
- F1: The book loses because its shorts pay the coins' own rise: the active short averaged -0.32 of the book (mean over all bars), which cost -0.000453 per bar from the coins' mean daily rise, while timing earned only +0.000415 per bar and fees took 0.000078, leaving a gain of -0.000042 per bar.
