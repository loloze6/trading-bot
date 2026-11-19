---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is negative, its return over the next 7 days is below its usual 7-day return, and more so the higher its 7-day return.
Consequence: In a falling month, a one-week bounce is a reason to refuse a long and to lean short.
Why:
- F3: While the 30-day return is negative, the coin's 168-bar forward return is below its own average. The regression constant is -0.0120 (t = -3.98, n ≈ 1590), 16 of 19 coins are negative, and 7 of 8 years are negative. Inside that state, a higher 7-day return predicts a lower next 7 days (slope -0.0070 per standard deviation, t = -2.24). The deepest 30-day falls are the exception (+0.0135, t = 1.75).
