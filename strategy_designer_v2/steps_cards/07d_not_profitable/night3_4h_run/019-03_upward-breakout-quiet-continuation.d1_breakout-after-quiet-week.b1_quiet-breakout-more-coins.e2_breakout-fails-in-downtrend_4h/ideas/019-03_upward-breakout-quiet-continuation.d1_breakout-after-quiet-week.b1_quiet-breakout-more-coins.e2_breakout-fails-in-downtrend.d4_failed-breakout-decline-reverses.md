---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e2_breakout-fails-in-downtrend
line: 7.d not profitable
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e2_breakout-fails-in-downtrend_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: After a coin's four-hour bar closes above the high of its preceding two days while its 30-day return is negative, the coin rises more than usual from 12 to 24 days later, and the larger its decline over the first 12 days, the larger that later rise.
Consequence: A trader fading such breakouts should treat the 12-day decline as finished and expect the coin to recover it, the more so the larger the decline.
Why:
- F7: The decline is spent within 12 days and then reverses, while the book keeps holding. Summed position-times-return is +1.12 in a position's first 12 days, -2.19 in days 12 to 24 and -2.33 in days 24 to 36. The mean trade lasts 490 hours (about 20 days). From the signal's close, the 24-day short total is -0.97 % (t -2.08, 3715).
- F1: The book loses because its short bets pay the coins' own rise: summed over all coins and windows, position times next-bar return is -3.46, of which -15.01 is the market's drift against a book that is always short (mean position -0.18 to -0.32 on every coin) and +11.55 is timing; per entry the move from the signal's close over 12 days is +2.53 % unusual (t 9.2, 4027 entries) but only +0.37 % total (t 1.33), and 2548 short trades lost 3.9 % each before fees.
