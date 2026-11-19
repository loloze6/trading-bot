---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over the 24 hours up to the 20:00 UTC close, the more it rises over the next 24 hours, except when its 7-day return before that fall is also negative.
Consequence: A trader buying the evening dip should hold it for the following day when the dip interrupts a rising week, and refuse it when the dip extends a falling week.
Why:
- F2: The rebound the idea bets on is real and graded but arrives after the first hour. On forecast>0 bars (n 8661) the first-hour return is only +0.000274. The full 24-hour return is +0.001993, of which +0.001698 comes from hour 2 to hour 24. The excess 24-hour return rises across forecast quartiles: -0.000865, -0.000345, +0.001315, +0.002063.
- F3: Holding the same allocation for the full 24 hours instead of one bar, with a 0.1% fee per trade, would earn +0.001048 per case. That is t 3.65 over 8128 non-overlapping daily cases, with a rough annualised Sharpe of 0.77, against the book's actual -2.24.
- F5: The rebound also appears mostly when the preceding week was up. After an up week the excess 24-hour return is +0.001264 (t 1.78, n 4193). After a down week it is -0.000126 (t -0.14, n 3935).
