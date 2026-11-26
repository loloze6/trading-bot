---
line: 7.g patterns
backtest: 058-01_rising-calm-dip-rebound_1d
idea tested: 058-01_rising-calm-dip-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3920 USD
---
## Findings
- **F1:** In the rising calm bars (folds B, C, 5-day grid), the brief's dip side is not there: the deepest fifth of 3-day returns scaled by the 30-day swing (z3 from -3.17 to -0.74, 57 cases) was followed by a 5-day excess return of -1.37 % (t -1.06). The slope of excess return on z3 is positive (+0.0117 per unit, day-clustered t 2.12, 284 cases), so a larger dip goes with a smaller rise, not a larger one.
- **F2:** In rising calm the gain sits on the rise side. The top fifth of z3 (1.34 to 5.98) earned +4.40 % excess (t 2.33, 57 cases), and all rising calm cases with z3 > 0 earned +2.60 % excess (t 2.33 on 76 days, strength 0.21, 163 cases). This is continuation, which the map already holds in rising calm long (034-01.e1, 034-02, 033-03.b2).
- **F3:** The continuation slope of excess 5-day return on the swing-scaled recent return is positive in all three calm profiles:
- **F4:** In falling calm, the two lowest quarters of the 10-day return scaled by swing (z10 below -0.42) were followed by further 5-day excess falls of -5.40 % (t -2.80, 37 cases) and -3.63 % (t -3.15, 37 cases). The top quarter was followed by +1.75 % (t 1.38). This is the short side of the calm continuation, a cell the map holds with only one strategy (035-01.b1).
- **F5:** Over all bars, a 20-day return from -18 % to -4 % was followed by a 5-day excess of -2.65 % (t -4.23, 273 cases), and one from +4.7 % to +20 % by +2.28 % (t 3.15, 273 cases). Medium-sized 20-day moves continue across all profiles.
- **F6:** The tested idea's size is small and not sure: unusual move +0.36 % per case (t 0.54, 307 days, strength 0.033), against a trade cost of 0.19 %. The book's yearly return is +5.5 % with a Calmar of 0.39.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `058-01.g1_calm-market-decline-continues` (from F3, F4, F5, F1): In a calm market, the further a coin's 10-day return has fallen below zero, measured against its usual daily swing over the past 30 days, the larger its further fall over the next 5 days.
- `058-01.g2_falling-calm-decline-extends` (from F4, F3): In a falling, calm market, the further a coin's 10-day return has fallen below zero, measured against its usual daily swing over the past 30 days, the larger its fall over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
