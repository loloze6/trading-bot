---
line: 7.b inconclusive
backtest: 020-01_resistance-retest-turns-down_1d
idea tested: 020-01_resistance-retest-turns-down
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3460 USD
---
## Findings
- **F1:** The tested claim shows no effect at all: the slope t is -0.17 on 3,226 grid bars, the unusual move per case is -0.05 % (strength 0.002 against a usual 5-day move of 10.6 %), and the strongest forecasts, the (-20,-15] bin with 582 bars, are followed by +0.07 % against drift (t 0.16), not by a fall.
- **F2:** Recomputed from prices, closes within 2 % below a 90-day swing-high level show no ordering by the number of turns: 5-day unusual moves are -0.36 % for 1 turn (330), +0.31 % for 2 (202), +0.89 % for 3 (116), -1.57 % for 4 (41) and +1.49 % for 5 or more (24), all with |t| at or below 1.25. Near and far closes do not differ either (year-adjusted Welch t -0.39, 713 against 2,418).
- **F3:** What the forecast's bars do follow is the market's own year, not the level. Their 5-day unusual move is -2.3 % in 2018 (t -3.4) and -1.3 % in 2022 (t -2.8), but +1.0 % in 2020 and +1.5 % in 2021 (t 2.1). Inside a trend the slope stays null: t -0.94 above the 90-day mean and -0.17 below it.
- **F4:** No other horizon rescues the claim: the slope's t is -2.38 over 1 day (the wrong side, 3,356 bars), 0.26 over 10 days and 1.01 over 20 days.
- **F5:** The brief's other half shows instead: closes that cross above a 90-day swing-high cluster from below are followed by unusual moves larger than other closes (-0.22 % over 5 days, 2,889):
- **F6:** The breakout's 5-day move of about +2 % per case is about 10 times the 0.19 % a round trip cost this backtest. The resistance case's total move is -0.64 % in its direction, mostly the coins' own drift (-0.59 %).

## Ideas
- `020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance` (from F5, F6, F1): When a coin closes above a price where it turned down several times in the past 90 days, having closed below it the day before, it tends to rise over the next 10 days, and the more times it turned down there before, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
