---
line: 7.b inconclusive
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g2_falling-month-weekly-reversal_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g2_falling-month-weekly-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3144 USD
---
## Findings
- **F1:** The test's main measure is essentially zero: the forecast's slope on the demeaned 7-day forward return over the 1226 falling-month grid cases has t = 0.18. It stays near zero or below at other horizons (t −0.60 at 3 days, −1.76 at 14 days, 0.14 at 30 days). It is also flat in every coin (t from −1.09 to 1.14) and every year (t from −1.00 to 0.89), so the zero is not a coin or period averaging out.
- **F2:** The effect is mixed by how deep the month's fall is. Within falling months, the reversal slope of −r7 on the 7-day excess return has t = 3.34 in the deepest third (mean 30-day return −33%, n 276). It has t = −1.32 in the middle third (−14%) and t = −1.63 in the shallowest third (−4%). The graded interaction r7 × r30 has slope 0.47 with t = 3.84 (n 829). The test's sign rule therefore pools a reversal zone with a continuation zone.
- **F3:** Inside the deepest-fall third, the reversal is on the side the idea predicts in all six coins (t of −r7 from 0.65 to 1.86) and in every year with enough cases (2018 t 2.19, 2021 t 2.39, 2025 t 1.31, n 27 to 102). The 7-day excess return falls steadily across 7-day-return quartiles: +2.4%, +1.7%, −1.3%, −4.2%, and the top quartile has t = −2.55 (n 69 each).
- **F4:** Most of that deep-fall slope comes from the falling side. Among weeks that fell, the slope has t = 3.05 (n 185, mean excess +0.9%). Among weeks that bounced, the slope has t = −0.29 (n 91), although those bounces are followed by a mean excess of −2.9%.
- **F5:** Outside falling months the 7-day return continues rather than reverses. The slope of −r7 on the 7-day excess return has t = −3.26 (n 1156) at 7 days and t = −2.30 to −3.01 at 3, 14 and 30 days. Across all bars it has t from −2.07 to −3.90 in every 30-day-return quintile except the lowest (mean −30%), where t = +3.26.

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g2_falling-month-weekly-reversal.b1_deep-fall-weekly-reversal` (from F1, F2, F3, F4): While a coin's 30-day return is negative, the larger its 7-day return, the lower its return over the next 7 days, and this reversal grows stronger the deeper the coin's 30-day fall.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g2_falling-month-weekly-reversal.b2_weekly-continuation-outside-crashes` (from F2, F5): While a coin's 30-day return is above its deepest-fall levels, the larger its 7-day return, the higher its return over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
