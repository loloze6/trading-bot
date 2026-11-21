---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_one-day-fall-multi-day-rebound
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_one-day-fall-multi-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The higher a coin's traded volume over its last 24 hours relative to its average over the last 30 days, the more the coin rises over the next 3 days.
Consequence: A trader would buy after a day of unusually heavy trading and hold for days, and would refuse to buy after a day of unusually thin trading.
Why:
- F4: Volume shows the same pattern. The higher a coin's volume over its last 24 hours relative to its 30-day hourly mean, the more it rises over the next 72 hours: strength -0.075 (t -2.49) in the lowest quintile, +0.112 (t 3.29, +1.04 % above drift) in the highest, about 1050 cases each. The 72-hour volatility ratio gives the same ordering (-0.060 to +0.085, t 2.39), smaller.
- F1: The higher a coin's hourly volatility over its last 24 hours relative to its last 30 days, the more it rises over the next 72 hours net of its drift. Regressed on the within-coin rank of that ratio, the slope is 0.188 usual moves per unit of rank (t 3.95, 5251 independent cases). The top decile ends +1.33 % above drift (strength 0.153, t 2.97, 529 cases), about 7 times the 0.19 % round trip. The bottom four deciles end -0.17 % to -0.79 %.
