---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e2_breakout-fails-in-downtrend
line: 7.d not profitable
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e2_breakout-fails-in-downtrend_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin's four-hour bar closes above the high of its preceding two days while its 30-day return is negative, the coin falls more than usual over the next 12 days, and the narrower its four-hour ranges over those two days compared with its ranges of the past 30 days, the larger the decline.
Consequence: A trader should fade upward breakouts in a month-long decline mainly when they come out of an unusually tight two-day range, the tighter the more so, where the move per case is several times the cost of a trade.
Why:
- F1: The book loses because its short bets pay the coins' own rise: summed over all coins and windows, position times next-bar return is -3.46, of which -15.01 is the market's drift against a book that is always short (mean position -0.18 to -0.32 on every coin) and +11.55 is timing; per entry the move from the signal's close over 12 days is +2.53 % unusual (t 9.2, 4027 entries) but only +0.37 % total (t 1.33), and 2548 short trades lost 3.9 % each before fees.
- F2: The idea's total move per case, +0.34 %, is only 1.5 times the 0.22 % cost of a round trip, because the coins' normal 12-day drift in the short direction is -2.21 %; the forecast's size does not grade the move: the total move is +0.93 %, +0.12 %, +0.01 % and +0.41 % from the largest to the smallest forecast quartile, and the correlation with the move is only 0.013.
- F5: A narrow range before the breakout carries the decline: in the quarter of entries with the narrowest 2-day range against its 30-day mean, the 12-day short total is +2.08 % (t 2.93, 680), and in the widest quarter it is -1.31 % (t -1.89). Combined with a 30-day fall of -13 % to -24 % and a narrow range, it is +4.71 % (t 5.63, 343), 21 times the cost.
- F6: The narrow-range effect comes from the later windows: in w13 to w24 the narrowest quarter gives +3.15 % (t 3.54, 413) and the widest -2.09 % (t -2.07). In w1 to w12 the narrowest gives only +0.43 % (t 0.37).
