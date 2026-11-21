---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over the 24 hours up to the 01:00 UTC close, the more it rises over the next 24 hours.
Consequence: A daily rebound long reads its signal more profitably just after midnight UTC than in the late evening.
Why:
- F2: The reversal depends on when the 24-hour move is read: per-hour slopes of next-24h excess return on the fall are largest at the 00:00–05:00 UTC closes (25–35 bp per z, t 6.1–8.9) and vanish at 13:00–15:00 UTC (t −1.5 to −0.2), while the tested 19:00-stamped bar sits in between (12.4 bp, t 3.2); at the 01:00 bar the slope is significant on every coin (t −2.3 for XRP to −6.4 for XMR) and in 6 of 8 years.
- F5: The book fails mainly because it holds too little of the market's rise rather than because the signal is wrong: Sharpe 0.50 sits 0.057 below holding, and its mean daily return of 0.000368 is under the 0.0005 bar, while the reversal it trades is only a mid-strength slice (F2) of a broader effect that is strongest in high-volatility stretches (F1).
