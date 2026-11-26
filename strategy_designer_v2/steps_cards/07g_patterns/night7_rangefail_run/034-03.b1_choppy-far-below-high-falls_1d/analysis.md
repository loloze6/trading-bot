---
line: 7.g patterns
backtest: 034-03.b1_choppy-far-below-high-falls_1d
idea tested: 034-03.b1_choppy-far-below-high-falls
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4213 USD
---
## Findings
- **F1:** A sharp one-day fall, counted in the coin's own 20-day daily swings, is followed by a graded rebound the next day. After a fall of 2 or more swings the next day's drift-adjusted return is +1.48 % (t 2.04 by day, 305 cases on 95 days). After a fall of 1 to 2 swings it is +1.06 % (t 1.68, 924 cases), against −0.27 % after a flat day (t −1.47). On down days the slope of the next day's return on the fall's size is negative in all three trend groups: chop t −2.26, fall t −1.24, rise t −0.75. It is negative in 10 of the 12 windows w7–w18.
- **F2:** In a rising market (60-day return above +10 %), the next 5 days' drift-adjusted return grows steadily with the close's nearness to its prior 20-day high in swings. Slope t 2.05 (484 grid cases, 84 days, Spearman 0.15). By quintile of depth the means rise monotonically: −2.64 % at a median depth of −3.6 swings, −2.03 %, +1.34 %, +1.58 %, and +4.28 % at +0.6 swings above the high. In round 1, closes at or above the high in rising markets gained +6.36 % (t 2.92, 74 cases).
- **F3:** In the choppy profile, the tested depth-below-high reading points the idea's way but is not sure. Its slope t is 1.93 (189 cases, 76 days), and its sign moves between windows (w10 −0.40, w15 −0.01, w17 +0.05, w8 +1.65). This matches step 5's inconclusive t 0.11. The book's own position gain was positive in 2018–2019 (+1.45, +0.79 summed) and negative in 2020–2021 (−1.35, −1.83).
- **F4:** In a choppy market the 5-day prior return, scaled by swings, continues over the next 5 days. Slope t 2.30 (189 cases, Spearman 0.26). The weakest prior-5-day quintile is followed by −9.35 % (t −2.77, 23 cases) and the next by −5.28 % (t −3.18, 41 cases). The slope is weaker in rising (t 1.31) and falling (t 1.02) markets.
- **F5:** Weekday and volatility level show no stable pattern. Drift-adjusted next-day means by weekday all have day-clustered |t| < 1.5 and change sign from year to year. The volatility-rank quartiles show no monotone ordering: −0.41 %, +0.72 %, −1.82 %, −0.31 %.

## Ideas
- `034-03.b1.g1_rising-nearness-to-high-drift` (from F2): In a rising market, a coin rises over the next 5 days more the nearer its daily close stands to its prior 20-day closing high, counted in its own daily swings over the last 20 days, and more still the further it closes above that high.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `034-03.b1.g2_one-day-shock-rebound` (from F1): A coin that falls sharply in one day, measured in its own daily swings over the last 20 days, rises over the next day, more the more swings the day's fall spans.
- `034-03.b1.g3_choppy-weekly-fall-continues` (from F4, F3): In a choppy market, a coin whose 5-day return is negative falls further over the next 5 days, more the more of its own daily swings (20-day) the 5-day fall spans.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
