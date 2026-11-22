---
line: 7.b inconclusive
backtest: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days_4h
idea tested: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3637 USD
---
## Findings
- **F1:** The test's result is on the side the idea predicts and far past the bar. The mean excess 18-bar return is +3.65 % with t 5.04 over 135 cases. My recomputation gives +3.09 % with t 4.64 on 156 cases and 60 % of cases positive. The result is inconclusive only because the grading runs the wrong way: cases above the median forecast earn 2.77 % less than those below.
- **F2:** The range excess grades the move the opposite way to the idea. By quartile of the 6-bar to 180-bar range ratio (medians 2.7, 3.2, 3.7, 4.8), the mean excess 18-bar return falls from +5.87 % (t 4.05) to +3.73 % (t 2.60), +1.52 % (t 1.40) and +0.98 % (t 0.81). Alone, the ratio's slope is -0.019 with t -2.92.
- **F3:** The depth of the fall shows the same reversal. The deepest quartile of the 24-hour fall (median -7.8 usual moves) earns +1.32 % (t 1.06), while the mildest (median -2.2) earns +5.92 % (t 3.72).
- **F4:** The coin's 30-day return before the panic is what grades the rebound. By quartile of that return (medians -29 %, -11 %, +13 %, +42 %), the mean excess 18-bar return is +0.12 % (t 0.08), -0.12 % (t -0.12), +3.46 % (t 3.13) and +6.98 % (t 4.01).
- **F5:** In a joint regression on standardised range ratio, fall depth and 30-day return (120 cases), only the 30-day return stays significant: coefficient +2.90 % with t 3.22. The range ratio is at t -0.95 and the fall depth at t -0.85. Their reversed grading comes from their correlation with the prior trend (Spearman: range ratio with 30-day return -0.66, fall depth with 30-day return +0.73).
- **F6:** The premium holds in five of six coins when the coin was up over 30 days, and is near zero when it was down:
- **F7:** The premium is paid within the 3 days and does not last to the brief's one to two weeks. The mean excess return is +1.73 % (t 3.12) over 1 day, +3.09 % (t 4.64) over 3 days, +1.10 % (t 0.90) over 7 days and +0.44 % (t 0.29) over 14 days.
- **F8:** The move is large against the cost of a trade, so cost is not the problem. The total move of +4.07 % per case is 21 times the 0.19 % cost. The book fails on its mean daily return (6.9e-05) and its Calmar (0.34), because panics are rare (0.012 trades per day) and the years 2018 (-1.05 %, 24 cases) and 2022 (-0.55 %, 17 cases) are flat or negative.

## Ideas
- `027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend` (from F1, F2, F3, F4, F5, F6, F7): A 24-hour stretch in which the coin falls hard while its range is several times its 30-day average is followed by higher than usual returns over the next 3 days. The higher the coin's 30-day return before the stretch, the higher the return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
