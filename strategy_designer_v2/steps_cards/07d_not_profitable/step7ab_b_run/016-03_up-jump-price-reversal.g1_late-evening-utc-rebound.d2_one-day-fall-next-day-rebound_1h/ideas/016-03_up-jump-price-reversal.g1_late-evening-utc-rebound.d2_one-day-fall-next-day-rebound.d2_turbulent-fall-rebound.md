---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_one-day-fall-next-day-rebound
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_one-day-fall-next-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over its last 24 hours, the more it rises over the next 24 hours, the more so the larger its hourly moves over those 24 hours were compared with its hourly moves over the last 10 days.
Consequence: A trader buys a one-day fall made in unusually turbulent hours, where the rebound is large, and refuses calm falls that keep sliding.
Why:
- F1: Each case's unusual move is +0.12 % per 24 hours (strength 0.025), but a round trip costs 0.19 %, and the book earns 2.3 bps a day against 6.7 to 15.5 bps for holding the coins; its Sharpe is 0.21 against holding's 0.55, its Calmar is −0.003 and its deepest falls per coin are 39 % to 64 %.
- F6: Cases where the last 24 hours' hourly moves were large against the coin's 10-day average rebound more.
- F9: On BTC the book's gain before costs per unit traded (4.8 bps) is below its fee per unit traded (5.1 bps). On the other coins it covers it, but at 11 to 25 bps against 5.5 to 15.7 bps of fees it leaves little.
