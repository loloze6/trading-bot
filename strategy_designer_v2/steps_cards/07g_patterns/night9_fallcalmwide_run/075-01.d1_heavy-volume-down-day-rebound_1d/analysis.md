---
line: 7.g patterns
backtest: 075-01.d1_heavy-volume-down-day-rebound_1d
idea tested: 075-01.d1_heavy-volume-down-day-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3966 USD
---
## Findings
- **F1:** Over all trends together, up days are followed by a next-day excess return of −0.57 % in a falling market (60-day return below −10 %; 1296 cases, t −3.93) and −0.48 % in a choppy one (503, t −2.26), but +0.19 % in a rising one (1386, t +1.07), so the lower the 60-day trend, the weaker the day after an up day.
- **F2:** The weak day after an up day in a falling market does not depend on the day's own features: by size of the rise its quartiles give −0.53, −0.74, −0.36 and −0.63 % (slope on the scaled rise t −0.32, 314 days); by close position −0.76, −0.47 and −0.47 %; by volume −0.76 (light), −0.21 and −0.74 % (heavy).
- **F3:** The weak day after an up day in a falling market has the same sign every year: 2018 −0.80 % (t −2.53), 2019 −0.91 % (t −4.72), 2020 −0.15 % (t −0.45) and 2021 −0.36 % (t −1.49).
- **F4:** The brief's light-volume side is really this trend effect, not volume. On up days the slope of next-day excess return on lightness has t −0.40 (556 days). Light-volume up days are negative in falling (−0.76 %, t −3.67) and choppy (−0.61 %, t −2.22) markets but flat in rising ones (+0.02 %, t +0.09).
- **F5:** The tested idea's rebound is convex in volume. Down days in the heaviest volume fifth are followed by +1.15 % excess (955, t 4.98), against +0.34 % (t 1.83) in the fourth fifth and +0.15 to +0.19 % in the three lightest fifths. The top-fifth move per case is about five times the 0.22 % trade cost.
- **F6:** Heavy-volume down days rebound more when they come at the end of a 5-day fall. The lowest quartile of the 5-day return gives +1.83 % (450, t 4.18), against +0.19 % and −0.20 % in the middle quartiles.
- **F7:** The rebound after heavy-volume down days also grows with the size of the day's own fall. Days with a scaled fall in the biggest quartile give +0.96 % (866, t 4.23), and days with a low close give +1.04 % (610, t 4.40). The smallest-fall quartile gives −0.36 % (t −0.88), and high-close days give +0.21 % (t 0.65).
- **F8:** Heavy-volume down days rebound in a falling market (+0.58 %, 513, t 2.38) more than in rising (+0.26 %, t 0.73) or choppy (−0.45 %, t −0.80) markets. This falling-market rebound on heavy volume is already held by 064-01 (falling agitated heavy volume fall rebound). The agitation split could not be read: 30-day swings against a year did not compute inside these short windows.

## Ideas
- `075-01.d1.g2_heavy-volume-after-fall-rebound` (from F5, F6, F7): The heavier a coin's volume on a down day, relative to its average over the past 20 days, and the deeper its fall over the past 5 days, the larger its rise over the next day.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `075-01.d1.g1_up-day-fades-in-downtrend` (from F1, F2, F3, F4): The lower a coin's 60-day return, the weaker its next day after a day that closed higher. In a falling market, an up day is followed by a next day below the coin's normal drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
