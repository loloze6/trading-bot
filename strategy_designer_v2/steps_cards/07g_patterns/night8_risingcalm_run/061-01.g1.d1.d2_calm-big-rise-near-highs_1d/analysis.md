---
line: 7.g patterns
backtest: 061-01.g1.d1.d2_calm-big-rise-near-highs_1d
idea tested: 061-01.g1.d1.d2_calm-big-rise-near-highs
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5025 USD
---
## Findings
- **F1:** Across all profiles, the 5-day excess return falls steadily as the close sits further below its 20-day closing high, on the non-overlapping 5-day grid. At a new high (0 to 1 % below) it is +4.89 % (t 3.72, 144 cases). From 0 to 5 % below it is +0.90 % (t 1.82, 334). From 5 to 10 % below it is +0.14 % (t 0.25, 306). From 10 to 20 % below it is -1.84 % (t -2.74, 359). More than 20 % below it is -1.17 % (t -1.66, 359).
- **F2:** The same gradient is steepest in a choppy market (60-day return between -10 % and +10 %), and its lower end is negative. The 5-day excess return is +11.7 % at a new high (t 2.41, 12 cases). It is +0.23 % at 0 to 5 % below (40), -1.64 % at 5 to 10 % below (t -1.17, 31), -4.44 % at 10 to 20 % below (t -3.02, 27) and -10.95 % more than 20 % below (t -2.48, 15). In falling markets the 10 to 20 % band is also -2.96 % (t -3.13, 93).
- **F3:** The upper end of F1, continuation near the high, is mostly a rising-market effect: +7.65 % at a new high in rising markets (t 2.76, 51 cases). The profile map already holds this in nearness-to-high and range-top-continuation books (034-01.b1, 033-03.b2, 035-01.b1), so it is not new. The lower end, falls far below the high in a choppy market, is short-side, and the map's choppy agitated short cell is empty.
- **F4:** In a choppy market, the 5-day move measured in 30-day-swing units continues over the next 5 days, in both directions, but on few cases. Moves below -1.5 units are followed by -18.4 % (t -2.53, 7 cases). Moves from -1.5 to -0.5 units are followed by -5.8 % (t -2.05, 15). Moves from -0.5 to +0.5 are followed by -0.56 % (67). Moves above +1.5 are followed by +9.8 % (t 2.25, 4). The pooled slope of 5-day excess return on the day's z in a choppy market is 0.032 (t 2.55, 125 cases).
- **F5:** The tested idea's effect sits only at the top of the forecast, not across it. In choppy calm, rise days with z from 0 to 1 are followed by -1.52 % (t -1.44, 67 cases), z from 1 to 2 by +7.96 % (t 1.85, 14) and z above 2 by +3.51 % (t 1.62, 9). By forecast quartile, only the top quartile pays (+6.75 %, t 2.44, 24 cases); the other three are -0.64 %, -3.21 % and -0.77 %.
- **F6:** The brief's claim that the effect lives in calm markets only is not supported. Outside choppy calm, the slope of 5-day excess return on the day's z is 0.0102 (t 2.77, 1,186 cases), and days with z above 2 are followed by +7.73 % (t 2.19, 27).
- **F7:** The choppy-calm grid is dominated by one year. Its 5-day excess return is -5.23 % in 2018 (t -4.36, 49 cases) against +0.89 % in 2020 and +2.96 % in 2021. Down and flat days in choppy calm, where the forecast is 0, are followed by -1.84 % (t -2.45, 104 cases).
- **F8:** Next-day excess return differs by weekday, though only moderately against the seven weekdays tested. It is -0.50 % after Wednesday bars (t -2.78), +0.41 % after Thursday (t 2.80) and +0.38 % after Friday (t 2.74), about 1,190 days each. A late-week gain is already held for rising markets (045-01).
- **F9:** The book's trades pay most on mid and high entry forecasts. Mean net P&L is +2.01 % in the middle tercile (t 2.56, 134 trades) and +1.50 % in the high tercile (t 1.70), against +0.43 % in the low tercile (t 0.45). XMR loses (-1.46 %, t -1.47, 83 trades) while ETH (+3.28 %) and ZEC (+3.21 %) carry it.

## Ideas
- `061-01.g1.d1.d2.g1_choppy-far-below-high-decline` (from F1, F2, F3): In a choppy market, the further a coin's close sits below its highest close of the past 20 days, the further it keeps falling over the next 5 days.
- `061-01.g1.d1.d2.g2_choppy-swing-scaled-move-continues` (from F4, F6): In a choppy market, the larger a coin's 5-day move against the standard deviation of its daily returns over the past 30 days, the further it keeps moving the same way over the next 5 days.
- `061-01.g1.d1.d2.g3_calm-only-large-rises-continue` (from F5): In a calm market, the larger a coin's one-day rise against the standard deviation of its daily returns over the past 30 days, the further it keeps rising over the next 5 days, beginning only from rises of more than one usual daily swing.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
