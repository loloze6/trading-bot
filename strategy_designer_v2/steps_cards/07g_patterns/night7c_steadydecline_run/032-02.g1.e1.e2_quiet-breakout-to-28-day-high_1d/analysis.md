---
line: 7.g patterns
backtest: 032-02.g1.e1.e2_quiet-breakout-to-28-day-high_1d
idea tested: 032-02.g1.e1.e2_quiet-breakout-to-28-day-high
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3823 USD
---
## Findings
- **F1:** A coin's position inside its own 28-day close range predicts its next 5 days. On the non-overlapping 5-day grid, the excess 5-day return rises across the quintiles of that position: −1.55 %, −1.91 %, −0.91 %, +1.14 %, +2.32 %. The slope t is 4.86 over about 1,494 cases. The slope is positive on every coin, with t from 1.69 (ZEC) to 2.59 (XRP). It is positive in 8 of the 12 windows.
- **F2:** Grid cases that close at their 28-day closing high have an excess 5-day return of +4.30 % (t 2.96, 122 cases). The other cases have −0.33 % (t −1.09, 1,588 cases). The largest windows are positive (w11 +11.5 % over 21 cases, w17 +5.6 % over 21, w10 +5.4 % over 16).
- **F3:** Distance below the 28-day high says the same thing. Its top quintile, the cases nearest the high, has +2.40 % excess (t 3.29) and its second quintile −2.87 % (t −4.24). It reads the same over 14 and 56 days, with top quintiles of +2.91 % and +2.67 %.
- **F4:** The tested forecast, volatility compression, adds nothing beyond being at the high. The 20-to-60-day volatility ratio has a quintile slope t of −0.62, and its quintile means all lie within ±0.44 %. The book's losses come from its shorts at the high, where recent volatility had expanded: 241 shorts lost a mean of −6.04 % net, while 354 longs earned +5.68 %.
- **F5:** The brief's calm decline is not visible in these folds. The 28-day return has a quintile slope t of 0.37. In the steepest-fall third, cases with calm ranges (−1.90 %, t −1.90) did not fall more than cases with wide ranges (−2.19 %, t −1.99).
- **F6:** Weekday is at the level of chance once I count how many angles I looked at. Monday is +1.70 % (t 2.42) and Thursday −1.85 % (t −2.50) across 7 groups, so I propose no idea from it.

## Ideas
- `032-02.g1.e1.e2.g1_high-in-28-day-range-rises` (from F1, F2, F3, F4): The higher a coin's close sits within its range of closes over the last 28 days, the larger its rise over the next 5 days. The rise is largest on closes at the top of that range.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
