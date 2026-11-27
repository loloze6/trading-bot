---
line: 7.b inconclusive
backtest: 064-01_choppy-large-up-day-continuation_1d
idea tested: 064-01_choppy-large-up-day-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 0
cost: 0.1965 USD
---
## Findings
- **F1:** The test's main measure sits at zero, not short of a bar. Mean strength is -0.024 with t -0.20 over 259 cases on 174 days. In folds B and C the 127 recomputed cases give -0.025 (t -0.27), a negative median of -0.088, and only 43 % of cases ending above the coin's drift. The positive +1.25 % unusual move (t 0.64) comes from a few large winners, not a typical follow-through.
- **F2:** No horizon shows the continuation in B and C. Over 1 day the strength is -0.081 (t -0.82), over 3 days -0.030 (t -0.33), over 5 days -0.025 (t -0.27) and over 10 days +0.088 (t 0.84). The idea's 5 days is not measuring a move that lives elsewhere.
- **F3:** The grading the idea claims is barely present:
- **F4:** The effect is mixed across periods and coins rather than living in one part:
- **F5:** Splitting by agitation does not reveal a home for the effect:
- **F6:** The asymmetry the brief claims does not appear. On the non-overlapping grid of choppy bars, large up days of 2 to 3 swings give -0.04 (n 58). Days of -2 to -3 swings give +0.11 (n 66) and days below -3 swings give -0.09 (n 26). None of these differ from ordinary days (+0.01, n 1295).

## Ideas
- No ideas: The theme's effect is not in the data. The test's result is zero (strength -0.024, t -0.20), and no horizon, jump size, coin, period or agitation level shows the continuation clearly (best t 1.14 on 44 cases). Neither more data nor a narrower idea is warranted (F1–F5).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
