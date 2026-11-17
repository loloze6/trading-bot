---
line: 7.b inconclusive
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3153 USD
---
## Findings
- **F1:** The test's main measure is on the side the idea predicts, but it is weak: the mean short gain over holding is 0.00194 with t = 1.29 over 2881 independent 3-day cases, and it varies widely across windows, from t = -1.82 in w10 to t = 2.07 in w2. By year it ranges from t = 1.96 in 2018 to t = -1.76 in 2023.
- **F2:** The level of the effect exists but its grading does not. Falling-month cases have a lower excess 3-day return than flat-or-rising cases (-0.0030 vs 0.0031, Welch t = -2.75). But depth within falling months does not order the outcome: the Spearman correlation of forecast with excess return is -0.006, and the deepest forecast quintile has a positive excess (+0.0025, t = 0.79) while q2 to q4 are negative (-0.0069 to -0.0048). This is why the supporting check fails (deep minus shallow = +0.0016).
- **F3:** Raw 30-day return shows the same non-monotonic pattern. The deepest falls (mean -38%) are followed by +0.0050 excess (t = 0.97), while the middle quintiles of falls (mean -22% and -14%) are followed by -0.0065 (t = -1.80) and -0.0077 (t = -2.23). The steepest crashes tend to bounce, which cancels the graded effect.
- **F4:** The graded effect shows clearly only when the coin's 60-day return is still positive, that is, a down month inside a rising two months. There the short gain is 0.00855 (t = 2.99, n = 323), and the excess 3-day return falls with the depth of the forecast: deep tercile -0.0278 (t = -3.19), mid -0.0148 (t = -2.05), shallow -0.0005 (t = -0.07).
- **F5:** When the 60-day return is down, the short gain is 0.0016 (t = 0.52, n = 1038), with deep-half excess -0.0020 against shallow-half +0.0017. The plan's measure is therefore diluted by the majority of cases, where the effect is absent.
- **F6:** Horizon is not the issue. The plan's 3 days is the best horizon tested: t = 0.31 at 1 day, 1.29 at 3 days, 0.62 at 5 days, 0.38 at 10 days and -0.21 at 20 days. The book loses money (Sharpe -0.27).

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.b1_pullback-inside-rising-trend` (from F4, F5, F2): The more negative a coin's 30-day return, the lower its return over the next 3 days, only while its 60-day return is positive.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.b2_falling-month-more-coins` (from F1, F2): The more negative a coin's 30-day return, the lower its return over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
