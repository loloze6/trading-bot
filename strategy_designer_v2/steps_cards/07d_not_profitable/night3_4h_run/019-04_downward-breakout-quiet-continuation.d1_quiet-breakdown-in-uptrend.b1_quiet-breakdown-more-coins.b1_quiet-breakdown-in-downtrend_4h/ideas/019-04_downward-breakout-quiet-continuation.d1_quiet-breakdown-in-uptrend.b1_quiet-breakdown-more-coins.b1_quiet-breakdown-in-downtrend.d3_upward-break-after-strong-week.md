---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins.b1_quiet-breakdown-in-downtrend
line: 7.d not profitable
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins.b1_quiet-breakdown-in-downtrend_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes above the highest high of a coin's preceding two days, the coin rises over the next three days, and the stronger its 7-day return before the break, the larger the rise.
Consequence: Buy upward breaks of the two-day high in coins that have risen over the past week, sized by that rise, and refuse them after a falling week.
Why:
- F8: Upward breaks of the prior two-day high are graded by the 7-day return. After the strongest fifth of 7-day rises they gained 1.79 % over 18 bars (t 3.39) and 5.71 % over 72 bars (t 6.50). After the weakest fifth they lost 0.64 % (t −2.60).
- F9: The book loses most in windows where the coins rose: w4 −20.4 bps a day against +42.8 for holding, w21 −13.3 against +69.9, w11 −8.1 against +192.8. It gains only in falling windows (w14 +29.5 against −43.1, w7 +17.6 against −47.3), so it fails with one window left out and falls short of holding.
