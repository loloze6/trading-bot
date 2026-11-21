---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_one-day-fall-multi-day-rebound
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_one-day-fall-multi-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The higher a coin's hourly volatility over its last 24 hours relative to its own last 30 days, the more the coin rises over the next 3 days.
Consequence: A trader would buy coins whose last day was unusually turbulent and hold for days, and would refuse to buy coins after an unusually calm day.
Why:
- F1: The higher a coin's hourly volatility over its last 24 hours relative to its last 30 days, the more it rises over the next 72 hours net of its drift. Regressed on the within-coin rank of that ratio, the slope is 0.188 usual moves per unit of rank (t 3.95, 5251 independent cases). The top decile ends +1.33 % above drift (strength 0.153, t 2.97, 529 cases), about 7 times the 0.19 % round trip. The bottom four deciles end -0.17 % to -0.79 %.
- F2: The volatility pattern holds on every coin and in most periods. The rank correlation is positive on all 6 coins (0.020 BTC to 0.105 XRP) and in 19 of 24 windows. The top quintile beats the other four in 7 of 8 years, with 2019 the exception (-0.031 against -0.027). It is strongest on XRP and ZEC, where the top quintile's strength is 0.23 and 0.19 against -0.06 and -0.05 for the rest.
