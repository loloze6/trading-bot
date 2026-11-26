---
line: 7.b inconclusive
backtest: 058-01.g2.b1.d2.b1.d2.d3_multi-day-rally-fades-next-day_1d
idea tested: 058-01.g2.b1.d2.b1.d2.d3_multi-day-rally-fades-next-day
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3739 USD
---
## Findings
- **F1:** The test's result points the way the idea predicts but falls short of the bar. The mean short-direction unusual next-day move is +0.45 % with a day-pooled t of 1.74 over 494 case days and 1,291 cases. The size check passed (+0.42 % larger half minus smaller half). The data the test used was every coin with daily bars in all four folds, so there is no more daily data to add.
- **F2:** On folds B and C (342 cases with a 30-day swing), the whole effect sits in the largest rallies. The top quartile of the 5-day rise against the 30-day swing gives +1.61 % (t 1.94, 54 days, strength 0.21 of a usual move). The other three quartiles give -0.35 %, +0.24 % and +0.06 %, all with |t| under 0.5. The day-pooled slope of the next-day move on the scaled 5-day rise is 0.0080 (t 2.14). The test's flat mean averages a real graded effect with a large share of cases that carry none.
- **F3:** The grading comes from the rise before the last day, not from the last day itself. The four days before the last up day, against the 30-day swing, give a slope of 0.0107 (t 2.68). Their top quartile gives +2.02 % (t 2.28, 52 days) and their bottom quartile -0.87 % (t -1.08). Sorting by the last day's own rise runs the other way: +0.86 % (t 1.26) for its smallest quartile and +0.03 % (t 0.05) for its largest. Large 5-day rises with a small last day give +0.79 % (t 0.84, 44 days), against -1.21 % (t -1.17, 45 days) for small 5-day rises with a large last day.
- **F4:** The effect does not depend on a single period, but it varies across coins:
- **F5:** The test measured the idea at its right horizon, since the effect shows over one day only. Over all cases the mean unusual move is +0.40 % at 1 day (t 1.02). It is -0.11 % at 2 days (t -0.18) and +0.07 % at 3 days (t 0.10), and in the top quartile it falls from +1.61 % at 1 day to +0.30 % at 3 days (t 0.24). A longer horizon would dilute the idea rather than reveal it.

## Ideas
- `058-01.g2.b1.d2.b1.d2.d3.b1_prior-rally-fades-next-day` (from F1, F2, F3, F4, F5): In a falling, agitated market, when a coin closes an up day, the larger its rise over the four days before that day against the standard deviation of its daily returns over the past 30 days, the larger its fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
