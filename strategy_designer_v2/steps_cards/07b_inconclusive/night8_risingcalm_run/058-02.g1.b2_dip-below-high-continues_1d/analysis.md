---
line: 7.b inconclusive
backtest: 058-02.g1.b2_dip-below-high-continues_1d
idea tested: 058-02.g1.b2_dip-below-high-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3185 USD
---
## Findings
- **F1:** The tested result points the way the idea predicts but falls short of the bar: the slope over all folds is +0.00044 with t 1.08 (3,419 cases, 617 days). On folds B and C alone the same slope is +0.00152 with day-clustered t 2.21 (1,710 cases, 305 days), so the effect is on the predicted side in the part shown, and the full test is too thin to show it clearly.
- **F2:** The slope is positive on all six coins but clears 2 on only two of them: XRP (t 2.54) and XMR (t 2.17). BTC, ETH and LTC have t of 0.86 to 0.97 and ZEC 1.57, with 285 cases each. It is also positive in all four years of folds B and C (t 1.04 to 2.58). The effect is weak and spread across coins rather than concentrated in a few, so the remedy is more cases.
- **F3:** Only the deepest dips are followed by falls. In the fifth of cases with the most negative forecast (mean −19.9), the mean excess 5-day return is −2.50 % (day-clustered t −2.13, 112 days). The three middle fifths sit between −0.4 % and +0.7 % (t from −0.64 to +1.15), and the cases at the 5-day high (forecast 0) gain +2.07 % (t 1.86). Restricted to dips only, the slope weakens to t 1.36 (1,317 cases).
- **F4:** The plan's 5-day horizon is where the effect shows best. The day-clustered slope t is −0.10 at 1 day, 0.59 at 3 days, 2.21 at 5 days and 1.17 at 10 days. A change of horizon would not sharpen the answer.
- **F5:** By profile, the slope is strongest in rising calm markets (t 3.10, 190 cases) and weaker in rising agitated (0.72), falling calm (1.92) and choppy calm (1.52). However, 864 of 1,710 cases have no 60-day trend within the recorded window, so the sample is too partial to locate the effect in one profile.
- **F6:** The idea's size is far below what a trade costs. The unusual move per case is −0.18 % (t −0.52, 1,163 days), a strength of −0.015, against a trade cost of 0.19 %. As a result the book lost 35.1 % a year (Sharpe −0.67), whatever the verdict on reality.

## Ideas
- `058-02.g1.b2.b1_dip-continuation-more-coins` (from F1, F2, F4): The further a coin's close sits below its highest close of the past 5 days, measured against its usual daily swing over the past 30 days, the larger its fall over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
