---
line: 7.b inconclusive
backtest: 058-02.b1.b2.b1.b2.b1_calm-rising-range-position_1d
idea tested: 058-02.b1.b2.b1.b2.b1_calm-rising-range-position
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3542 USD
---
## Findings
- **F1:** The tested measure is on the side the idea predicts but short of the bar (mean 0.0798, t 1.59, 552 grid cases on 143 days); on folds B and C the same 10-day measure gives 0.151 with t 2.17 (196 cases, 64 days), and the test already used every coin and every fold available on daily bars, so no more data can be added.
- **F2:** All of the effect sits in the strongest forecasts. With |forecast| above 10, the signed excess 10-day return is +0.137 per day's cases (t 2.75, 108 cases, 46 days); with |forecast| of 10 or less it is −0.001 (t −0.02, 88 cases, 44 days). At 5 days the same split gives +0.070 (t 2.29) against −0.000 (t −0.02).
- **F3:** Read on the raw 20-day range position, the 10-day excess return is +6.4 % for closes in the top fifth of the range (62 cases) and −5.1 % for the bottom fifth (11 cases). The three middle fifths are flat by comparison (−5.2 % for 0.2–0.4, +1.7 % for 0.4–0.6, +1.4 % for 0.6–0.8; 23, 21 and 47 cases), so the move appears at the edges and not in a straight line across the range.
- **F4:** The 10-day measure is positive on both sides but stronger on the long side (0.156, t 1.80, 145 cases, against short 0.069, t 1.44, 51 cases). It is uneven across periods (2018 −0.062 with t −1.11, 2020 +0.273 with t 1.76; windows w12 −0.033 and w14 −0.100), which adds noise that dilutes the overall t.
- **F5:** The effect holds at 5 and 10 days (measure t 2.18 and 2.17) and fades by 20 days (t 0.61, long side −0.003). The plan's 10-day horizon is therefore not the problem.

## Ideas
- `058-02.b1.b2.b1.b2.b1.b1_convex-range-edge-continuation` (from F1, F2, F3, F5): In a calm, rising market, the higher a coin's close sits within its 20-day high-low range, the larger its rise over the next 10 days, with the move growing faster and faster as the close nears the range's high or low, so that closes at the edges of the range carry most of it.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
