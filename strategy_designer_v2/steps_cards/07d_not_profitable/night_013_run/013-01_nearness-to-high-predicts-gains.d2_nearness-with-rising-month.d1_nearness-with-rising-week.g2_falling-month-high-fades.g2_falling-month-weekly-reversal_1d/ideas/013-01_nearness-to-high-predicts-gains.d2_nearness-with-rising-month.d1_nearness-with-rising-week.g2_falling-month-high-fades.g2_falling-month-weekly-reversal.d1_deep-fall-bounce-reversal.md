---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g2_falling-month-weekly-reversal
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g2_falling-month-weekly-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is negative, the larger its 7-day return, the lower its return over the next 7 days, only while that 30-day fall is deep, and the more strongly so the deeper the 30-day fall.
Consequence: Fade a one-week bounce only inside a steep monthly decline, and size the fade by how far the month has fallen; in a mild decline, refuse to short the bounce.
Why:
- F3: In a falling month the reversal the book bets on is not graded. The mean 7-day forward return by 7-day-return quintile, lowest to highest, is +0.91%, +0.12%, -0.47%, -0.73% and +0.39% (166 cases each). Mean positions run from +0.75 to -0.53, so the largest shorts sit on the quintile that then rose (+0.39%).
- F4: Inside falling months, reversal appears only when the month fell hard. Correlation of 7-day return with the next 7 days by 30-day-return tercile:
- F5: The book's shorts lose and its longs lose too, before fees:
