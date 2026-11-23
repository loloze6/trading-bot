---
line: 7.d confirmed, not profitable
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g2_low-close-rebound-in-volatility_1d
idea tested: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g2_low-close-rebound-in-volatility
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5389 USD
---
## Findings
- **F1:** The book is mostly a half-sized long on the coins, and the market's falls carry its deepest fall: it was in a position on 99 % of coin-days with a mean allocation of 0.50, its daily returns correlate 0.86 with holding (beta 0.45, alpha 0.028 % a day), and its deepest fall of −51 % ran 342 days across w12 to w14 while holding fell −78 %, which leaves Calmar at 0.46 against the 0.75 rule.
- **F2:** All of the gain comes from the strongest forecasts. By forecast quintile, the position's gain per bar is 0.000 %, +0.007 %, −0.029 %, +0.094 % and +0.502 %, and the next-day move is −0.03 %, +0.03 %, −0.08 %, +0.13 % and +0.60 %. The three lower quintiles still hold allocations of 0.10 to 0.47.
- **F3:** Inside the deepest fall (w12–w14), the weak forecasts are what lose. Quintiles 1 and 2 lose −0.113 % and −0.236 % per bar on next-day moves of −0.56 % and −0.55 %, while the top quintile still gains +0.250 % (next-day move +0.53 %).
- **F4:** Trading only the strong readings, with costs of 0.095 % per side included, fixes the failing measure.
- **F5:** The idea's own joint situation (top-half 20-day volatility and a lower-half close) gives a deepest fall of only −20 %, Calmar 1.01, Sharpe 0.96 and yearly +20.1 %, while in a position 19 % of the time, and it gained +20.9 % through w12–w14.
- **F6:** Neither condition earns alone, so the joint situation is the idea itself and not a separate effect.
- **F7:** The strong case holds in both 20-day trend states, so a trend filter is not the repair. High-volatility low closes are followed by +0.42 % (t 3.16, n 1865) after a falling 20 days and +0.62 % (t 4.60, n 1501) after a rising 20 days. Adding a rising-trend filter to forecast ≥ 15 lowers Calmar to 0.48.
- **F8:** The strong case pays in every window group. Forecast ≥ 15 days are followed by a next-day move of:

## Ideas
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g2_low-close-rebound-in-volatility.d1_strong-low-close-volatility-only` (from F1, F2, F3, F4, F8): The higher a coin's 20-day daily volatility, the more a day that closed near its low is followed by a rise over the next day. The rise is concentrated where both the low close and the volatility are at their strongest, and the bet is held only on those days, out of the market when the reading is weak.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g2_low-close-rebound-in-volatility.d2_joint-low-close-high-volatility-rebound` (from F5, F6, F7, F3): The higher a coin's 20-day daily volatility, the more a day that closed near its low is followed by a rise over the next day. The rise appears only when the close sits in the lower part of the day's range and the volatility is high together, and it grows with how low the close sits and how high the volatility is.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
