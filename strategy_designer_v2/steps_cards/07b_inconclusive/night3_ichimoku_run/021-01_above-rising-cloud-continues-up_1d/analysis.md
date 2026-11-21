---
line: 7.b inconclusive
backtest: 021-01_above-rising-cloud-continues-up_1d
idea tested: 021-01_above-rising-cloud-continues-up
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3068 USD
---
## Findings
- **F1:** The positive mean rests on a handful of very large gains rather than a broad effect. Among the 149 non-overlapping 26-day cases with a forecast above 0, the mean excess return is +4.8 % (t 1.30). The skew is 3.6, the median case is -3.0 % and only 46 % of cases are positive. Clipping the top and bottom 5 % cuts the mean to +1.3 % (t 0.56), and dropping the 5 largest cases turns it negative, at -1.2 % (t -0.54).
- **F2:** The grading the idea predicts is absent, so a faster-rising cloud is not followed by a larger rise. The excess return regressed on the recorded raw 26-day cloud slope gives t -0.40 (149 cases). The forecast terciles are not ordered: low +9.5 % (t 1.27), mid -3.8 % (t -1.03), high +8.5 % (t 1.18).
- **F3:** Changing the horizon does not show the effect more clearly. With a forecast above 0, the mean excess return is +0.4 % over 5 days (t 0.99, 852 cases), +0.9 % over 10 days (t 1.08, 421 cases) and -2.6 % over 40 days (t -0.84, 109 cases).
- **F4:** The effect depends on the period and the coin. The first half of the windows (w1–w12) gives +10.2 % (t 2.12, 62 cases), while w13–w24 gives +1.0 % (t 0.18, 87 cases). The years alternate in sign, for example 2020 -7.1 % (t -1.17) against 2024 +9.4 % (t 1.73). By coin the mean runs from -1.6 % on LTC (19 cases) to +21.3 % on ZEC (17 cases), and no coin reaches t 1.1.
- **F5:** The cloud situation separates the coin's future only weakly from the bars outside it. Bars above a rising cloud minus all other bars gives +6.5 % over 26 days (Welch t 1.66). The other bars average -1.7 % (t -1.39, 427 cases).
- **F6:** Cost is not what keeps the result unclear. The total move per case, +6.36 %, is 33 times the 0.19 % round trip, and the unusual move, +2.48 %, is 12.9 times it. The strength is 0.056, the usual value for real ideas, so the open question is whether the effect is real and graded, not whether it is large enough.

## Ideas
- `021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins` (from F1, F4, F6): When a coin closes above its Ichimoku cloud and the cloud is rising, its return over the next 26 days is positive, and larger the faster the cloud has risen over the past 26 days. The cloud is the band between the average of the 9-day and 26-day high-low midpoints and the 52-day high-low midpoint, plotted 26 days ahead.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
