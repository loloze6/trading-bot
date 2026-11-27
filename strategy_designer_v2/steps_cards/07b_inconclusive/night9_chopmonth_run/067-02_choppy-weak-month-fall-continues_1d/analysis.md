---
line: 7.b inconclusive
backtest: 067-02_choppy-weak-month-fall-continues_1d
idea tested: 067-02_choppy-weak-month-fall-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3963 USD
---
## Findings
- **F1:** The test traded a different situation from the idea's: the forecast is the 30-day return standardised against its own past 60 values, so it is below 0 whenever the month is weaker than usual, and 48 of the 159 cases in folds B and C (30 %) had a 30-day return at or above zero; on those cases the short-side unusual 7-day move is −2.73 % (22 days, t −0.77, weighted −5.64 %), against the idea.
- **F2:** On the cases the idea describes, a 30-day return below zero, the short-side unusual 7-day move is +5.14 % (111 cases on 54 days, t 2.67 with one day's cases taken together, weighted +6.96 %), compared with +2.76 % and t 1.57 on 76 days for all the test's cases; the non-falls pull the test's main measure under the bar.
- **F3:** Among the true falls the move is graded by depth as the idea predicts: shallow third +1.14 % (t_day 0.61), middle third +4.04 % (t_day 1.78), deepest third +10.23 % (t_day 2.84), Spearman 0.36 between depth and the move (p 0.0001, 111 cases); the plan's own supporting check also passed (+2.42 %).
- **F4:** The effect is stronger when the coin is agitated: among the true falls, with the 30-day swing above the coin's median, the unusual move is +8.73 % (40 cases, 25 days, t_day 2.65), and when calm it is +3.11 % (71 cases, 36 days, t_day 1.67); per unit of the coin's 7-day swing the strength is 0.53 against 0.19.
- **F5:** The effect belongs to the 7-day horizon and does not last: the mean short-side unusual move over all cases is +1.65 % at 3 days (t 2.19) and +2.76 % at 7 days (t 2.63), then falls to +1.75 % at 14 days (t 0.90) and +1.39 % at 21 days (t 0.52).
- **F6:** The effect varies across periods: most windows are positive, for example w9 at +6.8 % (t 3.16) and w16 at +24.4 % (t 4.59), but w11 is −12.4 % (t −2.27) and w10 is −1.4 %; by year it is positive in each of 2018 to 2021, from +1.3 % to +5.2 %.

## Ideas
- `067-02.b1_choppy-plain-month-fall-continues` (from F1, F2, F3, F5): In a choppy market, the larger a coin's plain 30-day fall below zero (its close under its close of 30 days earlier), the more it falls over the next 7 days.
- `067-02.b2_agitated-choppy-month-fall-continues` (from F2, F3, F4): In a choppy, agitated market, the larger a coin's plain 30-day fall below zero (its close under its close of 30 days earlier), the more it falls over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
