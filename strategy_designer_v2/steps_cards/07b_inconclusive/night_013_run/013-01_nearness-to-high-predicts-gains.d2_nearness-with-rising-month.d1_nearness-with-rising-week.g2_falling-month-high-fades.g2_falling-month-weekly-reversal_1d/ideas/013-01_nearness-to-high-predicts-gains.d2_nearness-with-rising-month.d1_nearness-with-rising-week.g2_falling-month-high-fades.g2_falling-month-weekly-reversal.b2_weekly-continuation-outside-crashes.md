---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g2_falling-month-weekly-reversal
line: 7.b inconclusive
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g2_falling-month-weekly-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is above its deepest-fall levels, the larger its 7-day return, the higher its return over the next 7 days.
Consequence: Outside deep monthly falls, a trader can follow a coin's one-week move instead of fading it.
Why:
- F2: The effect is mixed by how deep the month's fall is. Within falling months, the reversal slope of −r7 on the 7-day excess return has t = 3.34 in the deepest third (mean 30-day return −33%, n 276). It has t = −1.32 in the middle third (−14%) and t = −1.63 in the shallowest third (−4%). The graded interaction r7 × r30 has slope 0.47 with t = 3.84 (n 829). The test's sign rule therefore pools a reversal zone with a continuation zone.
- F5: Outside falling months the 7-day return continues rather than reverses. The slope of −r7 on the 7-day excess return has t = −3.26 (n 1156) at 7 days and t = −2.30 to −3.01 at 3, 14 and 30 days. Across all bars it has t from −2.07 to −3.90 in every 30-day-return quintile except the lowest (mean −30%), where t = +3.26.
