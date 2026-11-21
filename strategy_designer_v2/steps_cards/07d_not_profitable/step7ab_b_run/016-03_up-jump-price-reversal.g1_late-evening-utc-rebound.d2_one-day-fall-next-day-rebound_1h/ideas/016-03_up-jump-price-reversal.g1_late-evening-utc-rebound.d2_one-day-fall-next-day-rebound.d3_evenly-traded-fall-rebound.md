---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_one-day-fall-next-day-rebound
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_one-day-fall-next-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over its last 24 hours, the more it rises over the next 24 hours, the more so the more evenly that day's volume was spread across its hours.
Consequence: A trader buys one-day falls made on evenly spread volume, and gives less weight to falls carried by a single hour's volume burst.
Why:
- F1: Each case's unusual move is +0.12 % per 24 hours (strength 0.025), but a round trip costs 0.19 %, and the book earns 2.3 bps a day against 6.7 to 15.5 bps for holding the coins; its Sharpe is 0.21 against holding's 0.55, its Calmar is −0.003 and its deepest falls per coin are 39 % to 64 %.
- F7: Falls whose volume was spread evenly over the 24 hours rebound more than falls carried by one hour's volume burst.
