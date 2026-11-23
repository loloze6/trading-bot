---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g2_low-close-rebound-in-volatility
line: 7.d confirmed, not profitable
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g2_low-close-rebound-in-volatility_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 20-day daily volatility, the more a day that closed near its low is followed by a rise over the next day. The rise is concentrated where both the low close and the volatility are at their strongest, and the bet is held only on those days, out of the market when the reading is weak.
Consequence: A trader holds the long only on the strongest low-close-in-volatility days and stays out on the rest, where the position only carries the coin's falls.
Why:
- F1: The book is mostly a half-sized long on the coins, and the market's falls carry its deepest fall: it was in a position on 99 % of coin-days with a mean allocation of 0.50, its daily returns correlate 0.86 with holding (beta 0.45, alpha 0.028 % a day), and its deepest fall of −51 % ran 342 days across w12 to w14 while holding fell −78 %, which leaves Calmar at 0.46 against the 0.75 rule.
- F2: All of the gain comes from the strongest forecasts. By forecast quintile, the position's gain per bar is 0.000 %, +0.007 %, −0.029 %, +0.094 % and +0.502 %, and the next-day move is −0.03 %, +0.03 %, −0.08 %, +0.13 % and +0.60 %. The three lower quintiles still hold allocations of 0.10 to 0.47.
- F3: Inside the deepest fall (w12–w14), the weak forecasts are what lose. Quintiles 1 and 2 lose −0.113 % and −0.236 % per bar on next-day moves of −0.56 % and −0.55 %, while the top quintile still gains +0.250 % (next-day move +0.53 %).
- F4: Trading only the strong readings, with costs of 0.095 % per side included, fixes the failing measure.
- F8: The strong case pays in every window group. Forecast ≥ 15 days are followed by a next-day move of:
