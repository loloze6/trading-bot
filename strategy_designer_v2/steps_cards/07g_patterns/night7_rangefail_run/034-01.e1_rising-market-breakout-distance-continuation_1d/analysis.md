---
line: 7.g patterns
backtest: 034-01.e1_rising-market-breakout-distance-continuation_1d
idea tested: 034-01.e1_rising-market-breakout-distance-continuation
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4762 USD
---
## Findings
- **F1:** In rising markets the edge of a close above the prior 20-day high grows with the horizon, while closes below the high give nothing. Above-high cases return, in excess of drift: +3.08 % over 3 days (151 cases, 63 days, pooled t 1.14), +6.36 % over 5 days (74 cases, 32 days, pooled t 2.54, strength 0.98) and +12.25 % over 10 days (38 cases, 15 days, pooled t 2.21, strength 1.11). Below-high cases return +0.41 %, −0.55 % and −1.39 % over the same horizons, with every t under 1 in absolute value. Removing DOGE leaves the effect intact: +6.82 % at 5 days, t 2.87.
- **F2:** Within the above-high cases, the distance above the high does not rank the outcome. The Spearman correlation of distance with the scaled excess return is 0.03 at 3 days (p 0.73), −0.04 at 5 days (p 0.72) and 0.31 at 10 days (p 0.056). Entry-forecast quartiles of the book's trades are not monotone either: 6.8 %, 7.1 %, 22.4 % and 12.3 % per trade.
- **F3:** Outside rising markets, the further a close sits below its 20-day high in swings, the lower the next 3 days. The Spearman correlation is 0.112 (p 0.0002, 1103 cases). Pooled-by-day excess returns by distance in swings are:
- **F4:** This downward drift far below the high is strongest in choppy markets. Choppy cases 4 to 8 swings below the high return −3.68 % over 3 days (69 cases, t −3.16 unpooled), and those 2 to 4 swings below return −1.29 % (104 cases, t −2.10). Choppy cases at least 4 swings below give −3.49 % pooled (41 days, t −1.94); the same cases in falling markets give −1.44 % (99 days, t −1.42). The deep cases outside rising markets are negative in 9 of the 12 windows, including all six windows with 44 or more cases (w7, w9, w12–w15).
- **F5:** In rising markets, coins far below their high do not fall. Cases 4 to 8 swings below return −0.74 % over 3 days (t −0.59), and cases 2 to 4 below return +0.58 % (t 0.78). The weakness far below the high therefore belongs to non-rising markets, not to the brief's rising one.
- **F6:** The book's gain is concentrated in a few days. The top 1 % of its 1449 days carry 88 % of the total summed daily gain, and the top 5 % carry 181 %. The mean daily return ranges from −0.017 % to +0.243 % across windows w7–w18, and 4 of the 12 windows are negative.

## Ideas
- `034-01.e1.g1_rising-breakout-ten-day-drift` (from F1, F2): In a rising market, the nearer a coin's daily close comes to its 20-day high, and the further it stands above it, measured in units of its daily swing over the last 20 days, the more it rises over the next 10 days.
- `034-01.e1.g2_choppy-far-below-high-decline` (from F3, F4, F5): In a choppy market, the further a coin's daily close sits below its 20-day high, measured in units of its daily swing over the last 20 days, the more it falls over the next 5 days.
- `034-01.e1.g3_falling-far-below-high-decline` (from F3, F4): In a falling market, the further a coin's daily close sits below its 20-day high, measured in units of its daily swing over the last 20 days, the more it falls over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
