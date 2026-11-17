---
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g2_falling-month-weekly-reversal_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g2_falling-month-weekly-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3138 USD
---
## Findings
- **F1:** The book is flat on the bars where coins rise most and active where they barely move. Flat bars (n=8112) had a mean next-bar coin return of +0.216%, against +0.016% on long bars (n=5896) and +0.071% on short bars (n=3516), so the book leaves the market's rise behind (Sharpe -0.16, Sharpe minus holding's -0.71).
- **F2:** In a rising month (30-day return > 0, non-overlapping 7-day grid), the 7-day return grades the next 7 days in the trend's direction. The mean forward return goes from -0.27% in the lowest 7-day-return quintile to +1.08%, +0.89%, +2.86% and +5.12% in the highest (179 cases per quintile). The book holds about 0 position there (mean position about 0.00).
- **F3:** In a falling month the reversal the book bets on is not graded. The mean 7-day forward return by 7-day-return quintile, lowest to highest, is +0.91%, +0.12%, -0.47%, -0.73% and +0.39% (166 cases each). Mean positions run from +0.75 to -0.53, so the largest shorts sit on the quintile that then rose (+0.39%).
- **F4:** Inside falling months, reversal appears only when the month fell hard. Correlation of 7-day return with the next 7 days by 30-day-return tercile:
- **F5:** The book's shorts lose and its longs lose too, before fees:
- **F6:** Losses are spread across periods, not concentrated in one. Twelve of 24 windows have a negative mean daily book return. The book lost even in rising windows, for example w11 (book -0.043% a day against coins +1.26%) and w16 (-0.044% against +0.45%). This matches F1 and F3: it sat out rises and shorted bounces that kept going.

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g2_falling-month-weekly-reversal.d1_deep-fall-bounce-reversal` (from F3, F4, F5): While a coin's 30-day return is negative, the larger its 7-day return, the lower its return over the next 7 days, only while that 30-day fall is deep, and the more strongly so the deeper the 30-day fall.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g2_falling-month-weekly-reversal.d2_rising-month-weekly-momentum` (from F1, F2, F6): While a coin's 30-day return is positive, the larger its 7-day return, the higher its return over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
