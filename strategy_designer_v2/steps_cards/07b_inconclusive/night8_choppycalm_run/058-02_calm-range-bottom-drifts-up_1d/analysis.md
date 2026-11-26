---
line: 7.b inconclusive
backtest: 058-02_calm-range-bottom-drifts-up_1d
idea tested: 058-02_calm-range-bottom-drifts-up
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3404 USD
---
## Findings
- **F1:** The tested result is zero, not short of the bar. Step 5's slope of the excess 5-day return on the forecast was -0.000195 with t -0.34, and the forecast>0 cases had a mean excess 5-day return of -0.96 %. The idea's size is on the opposite side and is sure: an unusual move of -1.20 % per case (t -2.78 over 322 days, strength -0.132; total move -0.58 %, about 3 times the 0.19 % cost of a trade).
- **F2:** In the choppy calm profile, closes near the range bottom fall further rather than rebound. On the 5-day grid in folds B and C, the lower half of the 20-day range had a mean excess return of -2.49 % (t -3.02, 90 cases) and the bottom fifth -3.07 % (t -1.98, 18 cases). The upper half had +1.26 % (t 1.17, 88 cases) and the top fifth +2.38 %.
- **F3:** Across the whole range the effect is graded continuation, not reversion. In the profile, the slope of the excess 5-day return on the range position (-1 at the low, +1 at the high) was +0.0385 with t 2.81 over 178 cases, and t 2.00 with cases clustered by day (92 days). Its sign holds at 10 days (+0.052, t 1.60) and 20 days (+0.077, t 1.64).
- **F4:** The continuation is broad across coins but uneven across years. The slope on the range position is positive or near zero on every coin: XRP +0.135 (t 3.03), ZEC +0.092 (t 1.98), XMR +0.039 (t 1.23), BTC +0.020 (t 0.96), ETH -0.001. By year it is concentrated in 2021 (+0.138, t 2.95), with 2018 and 2019 slightly negative (t -0.76, -0.97). The lower-half fall is strongest in 2018 (-6.10 %, t -3.44) and 2021 (-5.96 %, t -2.03).
- **F5:** The same graded continuation exists outside the profile (slope +0.0268, t 4.33, 1186 cases; top fifth +3.34 %, t 3.45). So the brief's claim that the pull back is stronger in a calm choppy market is not seen. The plan's standardised forecast also blurred the raw range position: in the profile its slope was -0.0022 with t -1.80, against t 2.81 for the raw position.

## Ideas
- `058-02.b1_calm-range-bottom-keeps-falling` (from F1, F2, F3): In a choppy, calm market, the nearer a coin's close sits to the bottom of its 20-day high-low range, the larger its fall over the next 5 days.
- `058-02.b2_calm-range-position-continues` (from F2, F3, F4): In a choppy, calm market, the higher a coin's close sits within its 20-day high-low range, the larger its rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
