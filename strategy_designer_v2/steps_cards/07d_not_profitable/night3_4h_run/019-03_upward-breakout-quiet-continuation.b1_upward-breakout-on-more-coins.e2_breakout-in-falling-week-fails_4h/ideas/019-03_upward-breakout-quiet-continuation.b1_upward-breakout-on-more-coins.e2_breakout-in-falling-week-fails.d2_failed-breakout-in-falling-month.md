---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e2_breakout-in-falling-week-fails
line: 7.d not profitable
backtest: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e2_breakout-in-falling-week-fails_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes above the highest high of the preceding two days after the coin has fallen over the past 7 days, the coin falls over the next three days, and the deeper the past week's fall, the larger the decline, only while the coin's 30-day return is negative.
Consequence: A trader should refuse an upside breakout in a falling week mainly when the past month is also down, and should not fade it while the month is rising.
Why:
- F5: A falling month carries the effect.
- F6: The result rests on falling windows, which fails the leave-one-out check.
- F1: Only breakouts after a deep week pay. Grouped by the 7-day fall measured in the coin's usual 7-day move, the deepest fifth (beyond -0.69 of a usual move) returns +0.91 % total per case on the short (t 2.1, 427 cases), with strength 0.16; the shallowest fifth (fall under 0.09 of a usual move) loses -1.07 % (t -3.0, 427 cases), so the coin rises after those breakouts.
