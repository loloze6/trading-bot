---
line: 7.b inconclusive
backtest: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins.b1_resistance-breakout-three-day-rise_1d
idea tested: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins.b1_resistance-breakout-three-day-rise
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4329 USD
---
## Findings
- **F1:** The pooled result is carried by a few large outcomes. The mean excess 3-day return is +0.19 % (t 1.33, 4748 cases), but the median case is −0.47 % and only 46.8 % of cases are positive. Clipping the top and bottom 1 % cuts the mean to +0.05 % (t 0.47), so the typical break is not followed by a rise.
- **F2:** The effect shows only when the coin was already rising. Sorted by the 30-day return at the break, the excess 3-day return is −0.72 % (t −2.68, 860 cases) in the weakest quarter (30-day return −18 %). It is −0.05 % (t −0.18) in the flat quarter. It is +0.64 % (t 2.62, 875) in the third quarter (+12 %) and +1.15 % (t 2.43, 864) in the strongest (+48 %). Over 10 days the same gradient runs from −2.6 % to about +2.5 %.
- **F3:** Breaks close to the 90-day high carry the rise. In the quarter of cases whose close is within about 1 % of the 90-day high, the excess 3-day return is +1.17 % (t 2.78, 990 cases), +1.56 % over 5 days and +2.87 % over 10 days. In the three lower quarters it is −0.36 %, −0.33 % and 0.00 % (t −1.25 to 0.01).
- **F4:** The test's forecast cannot grade the cases. Its standardised value is capped at 20 for at least half of the cases (quarters 3 and 4 both read 20.0), and its rank correlation with the 3-day outcome is 0.014 (p 0.34). The unstandardised count times margin does grade at the top: its highest quarter gains +0.97 % (t 2.44), while the other three quarters sit between −0.15 % and −0.05 %.
- **F5:** The move shows on the signal's own bar. Breaks close +5.3 % on their own day (t 48.6). The next day's excess is −0.01 % (t −0.12), and across the size quarters of the signal-bar move the 3-day excess shows no pattern (+0.17 %, +0.02 %, +0.02 %, +0.43 %).
- **F6:** The effect is not stable over time and is spread unevenly across coins.
- **F7:** Overall the unusual move is 0.8 times the cost of a round trip (+0.19 % against 0.22 %). In the conditions of F2 (the two upper quarters of 30-day return) and F3 (near the high) it is +0.64 % to +1.17 %, roughly 3 to 5 times the cost.

## Ideas
- `020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins.b1_resistance-breakout-three-day-rise.b1_resistance-break-in-uptrend` (from F1, F2, F6, F7): When a coin closes above a price where it turned down several times in the past 90 days, having closed below it the day before, it tends to rise over the next 3 days, only while its 30-day return is positive, and the higher its 30-day return, the larger the rise.
- `020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins.b1_resistance-breakout-three-day-rise.b2_resistance-break-near-highs` (from F3, F4, F5, F7): When a coin closes above a price where it turned down several times in the past 90 days, having closed below it the day before, it tends to rise over the next 10 days, and the closer that close is to its 90-day high, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
