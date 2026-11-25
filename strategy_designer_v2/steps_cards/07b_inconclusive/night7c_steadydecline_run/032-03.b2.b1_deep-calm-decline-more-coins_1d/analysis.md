---
line: 7.b inconclusive
backtest: 032-03.b2.b1_deep-calm-decline-more-coins_1d
idea tested: 032-03.b2.b1_deep-calm-decline-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3777 USD
---
## Findings
- **F1:** In folds B and C, the plan's forecast (the 28-day fall standardised over its own past 60 values) predicts the drift-adjusted 10-day return only weakly: slope 0.0036, t 2.14 by OLS but 1.39 with cases of one day pooled (335 cases, 93 days). The raw 28-day percentage fall over the same thin-volume falls predicts it more clearly: slope 0.31, t 3.76 by OLS and 2.47 with days pooled (261 cases, 70 days). The two measures correlate only 0.66, so the standardisation blurs the depth that the idea names.
- **F2:** The effect is graded but sits in the deep falls. In thin-volume falls cut into quintiles of the raw 28-day fall, the two deepest quintiles (mean falls −34.7 % and −21.0 %) are followed by short-side unusual moves of +6.7 % (t 3.84) and +8.2 % (t 3.93) over 10 days. The middle quintile gives +0.3 % (t 0.15), and the two shallowest give −1.1 % and −2.9 % (t −1.30).
- **F3:** The grading is carried by steady declines. In thin-volume falls, take steadiness as the 28-day log move over the sum of the absolute daily moves. In the steady half, the slope on the raw fall is 0.68 with day-pooled t 2.59 (130 cases, 55 days). In the choppy half, it is 0.14 with t 0.77 (131 cases, 46 days).
- **F4:** Thin volume is part of the effect. In falls outside the thin-volume regime, the slope on the raw fall is −0.11 (t −1.27, 164 cases), and the deepest tercile (mean −41.7 %) gives only +0.6 % (t 0.27). Inside the regime, the slope is +0.31 (t 3.76, 261 cases).
- **F5:** The effect is mixed across periods but not across coins:
- **F6:** The idea's 10-day horizon is the right one. On the forecast, the slope's OLS t is 1.50 at 5 days, 2.14 at 10 days and 1.75 at 20 days. The test already used every coin and every fold, so no further data is available.

## Ideas
- `032-03.b2.b1.b1_steady-thin-volume-deep-decline` (from F1, F2, F3, F4, F5, F6): Among coins whose volume over the past 28 days is below their own usual volume, the larger the fall over those 28 days, the larger the further fall over the next 10 days. This holds only while the fall came in steady steps, with the 28-day move large against the sum of its daily moves, and the steadier the decline, the stronger the further fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
