---
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close_1d
idea tested: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4268 USD
---
## Findings
- **F1:** The day's own fall carries the next-day rise. Next-day excess return is +0.48 % (t 4.88, n 3448) on the bottom fifth of same-day returns, against −0.07 % to −0.23 % on the other four fifths. Measured in units of the coin's 20-day daily volatility, it grows with the size of the fall: +0.54 % (t 3.93, n 1495) after a fall of 1 to 2 units and +0.76 % (t 2.36, n 422) after more than 2 units. Gains of the same size show nothing (−0.09 %, t −0.71 and −0.04 %, t −0.15).
- **F2:** The close-location effect exists only when the coin is volatile. The slope of next-day excess return on the close's distance from the high is −0.25 % (t −1.35) in the calmest third of 20-day volatility, +0.30 % (t 1.37) in the middle third and +1.77 % (t 5.69) in the wildest third, about 5 070 days each.
- **F3:** Volume surge plays the same role as volatility. That slope is +0.02 % (t 0.09) on the lightest-volume third of days, +0.49 % (t 2.21) on the middle third and +1.12 % (t 4.05) on the heaviest third. In the heaviest third, the fifth of days closing nearest the low is followed by +0.88 % next day.
- **F4:** The book sizes up where the idea is weakest. Its largest positions (top fifth of allocation) sit on days with a mean 20-day volatility of 3.05 %, against 4.36 % over all days, so vol targeting puts most capital in the calm regime where F2 finds no effect. Both its best and worst 2 % of next-bar results follow the same kind of day: allocation about 1.0, close location about 0.70, volume about 2× its 20-day mean, a same-day return of −2.8 % to −3.9 %.
- **F5:** The effect lasts one day. The top forecast fifth earns +0.44 % excess over one day (t 4.78), +0.57 % over three days (t 2.08, n about 1 160) and +0.11 % over five days (t 0.31).
- **F6:** The effect is fading over time. The close-location slope is t 2.98, 3.03 and 5.16 in 2018 to 2020, and t 1.02, −0.17, 2.00, 0.01 and −1.24 in 2021 to 2025. Across the 24 windows the median t is 1.17 and the lowest is −2.56.
- **F7:** Range expansion and weekday show marginal patterns that do not stand out enough to build on.

## Ideas
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g1_volatility-scaled-fall-next-day-rebound` (from F1, F4): The larger a coin's fall on a day, measured in units of its own 20-day daily volatility, the more the coin rises over the next day.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g2_low-close-rebound-in-volatility` (from F2, F3, F4, F5): The higher a coin's 20-day daily volatility, the more a day that closed near its low is followed by a rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
