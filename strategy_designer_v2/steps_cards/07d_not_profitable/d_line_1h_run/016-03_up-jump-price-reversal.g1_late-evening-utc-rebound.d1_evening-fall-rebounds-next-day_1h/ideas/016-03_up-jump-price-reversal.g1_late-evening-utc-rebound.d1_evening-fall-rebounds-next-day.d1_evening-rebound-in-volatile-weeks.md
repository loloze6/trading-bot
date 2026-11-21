---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over the 24 hours up to the 20:00 UTC close, the more it rises over the next 24 hours, only while its hourly volatility over the past 7 days is high, and the more so the higher that volatility.
Consequence: A late-evening long after a deep daily fall should be held through the whole next day and taken mainly when the coin has been volatile all week; in calm weeks it should be refused.
Why:
- F1: The book holds each position for only about one hour while the idea needs a day. There were 7238 trades, all long, with a median duration of 60 minutes. The mean allocation on forecast>0 bars is 0.45, and one bar later it is only 0.001. Each trade loses 0.095% gross (t -7.18) and 0.195% net after a fee of about 0.10% per trade. The book's mean daily return is -0.00041, against the coin's +0.00119.
- F2: The rebound the idea bets on is real and graded but arrives after the first hour. On forecast>0 bars (n 8661) the first-hour return is only +0.000274. The full 24-hour return is +0.001993, of which +0.001698 comes from hour 2 to hour 24. The excess 24-hour return rises across forecast quartiles: -0.000865, -0.000345, +0.001315, +0.002063.
- F3: Holding the same allocation for the full 24 hours instead of one bar, with a 0.1% fee per trade, would earn +0.001048 per case. That is t 3.65 over 8128 non-overlapping daily cases, with a rough annualised Sharpe of 0.77, against the book's actual -2.24.
- F4: The 24-hour rebound is concentrated where the coin's 7-day hourly volatility is high. In the high-volatility tercile the excess return is +0.003269 (t 2.50, n 2709). In the low and middle terciles it is negative: -0.000654 (t -0.97) and -0.000842 (t -1.02).
