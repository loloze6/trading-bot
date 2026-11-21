---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e1_breakout-continues-rising-week
line: 7.b inconclusive
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e1_breakout-continues-rising-week_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin's four-hour bar closes above the high of its preceding two days, the coin rises more than usual over the next 6 days, and the larger its 7-day return before that bar, the larger the rise.
Consequence: A trader should expect an upward breakout after a strong week to pay mostly in its first six days and not count on the second week.
Why:
- F1: The tested result is on the predicted side but small: +0.44 % unusual move per case over 12 days (t 0.85, 2249 cases, strength 0.017). That is 2.0 times the 0.22 % cost of a trade. The test already used all 19 coins and all four folds, so no more 4h data is available.
- F2: The effect is graded by the forecast and sits only in its upper part. By forecast quintile, the 12-day unusual move is −0.9 %, −1.4 %, −1.4 %, +1.9 % and +3.7 % (t −1.0 to +2.1). The top two quintiles together have a strength of 0.129 (t 3.13, 901 cases), and the slope check passes (t 3.96).
- F6: The plan's 12-day horizon is not where the move per case is clearest. Over 6 days the unusual move is +0.73 % (t 2.20, 2369 cases, strength 0.046), against +0.44 % (t 0.85) over 12 days. Over 6 days the top forecast quintile gains +2.1 % and the lowest +0.2 %.
