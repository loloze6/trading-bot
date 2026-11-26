---
line: 7.g patterns
backtest: 032-01.b1_agitated-trend-weekly-reversal_1d
idea tested: 032-01.b1_agitated-trend-weekly-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3476 USD
---
## Findings
- **F1:** Weekly moves continued instead of reversing. On the non-overlapping 7-day grid of folds B and C, the slope of the next 7-day unusual move on the 7-day return scaled by 30-day swings is +0.0186 (t 2.33, 283 cases). The two highest quintiles of the scaled 7-day return are followed by +5.2 % (t 2.06) and +4.3 % (t 1.94) unusual moves. The lowest quintile is followed by −1.7 % (t −0.97).
- **F2:** The tested situation (agitated and trending) shows no relation between the weekly move and the next week. Its slope is −0.0042 (t −0.26, 53 cases). The book's short cases there lost −1.17 % unusual per case (t −1.03, 298 cases), with a negative grading slope (−0.0027). The rises kept going.
- **F3:** The continuation is concentrated in calm, choppy markets (30-day volatility below its 60-day mean, 30-day efficiency ratio under 0.3). There the slope is +0.063 (t 3.54, 74 cases). Its day-clustered t stays between 1.9 and 3.9 on all 7 offsets of the 7-day grid. In the other three regimes the t lies between −1.1 and 1.1.
- **F4:** In calm chop the top two quintiles of the scaled 7-day return are followed by +14.8 % (t 3.19, 18 cases) and +13.9 % (t 3.19, 16 cases) unusual 7-day moves. Up-weeks there average +8.7 % (48 cases); down-weeks average −2.8 % (26 cases), also continuing.
- **F5:** The continuation grades smoothly with chop and calm. By efficiency-ratio quartile the slope falls from 0.048 to 0.035, 0.014 and 0.003 (t 1.42, 2.00, 0.71, 0.16). By volatility-ratio quartile it falls from 0.026 and 0.030 to 0.012 and −0.014.
- **F6:** The calm-chop continuation is fragile. It is positive with day-clustered t above 2 on ETH, LTC, XMR and XRP (2.36, 2.81, 2.39, 2.11), but negative on BTC (t −1.39). It is very strong in 2018 (t 5.72, 18 cases), slightly negative in 2019 (t −1.80, 20 cases), and flat in 2020 to 2021. Across all regimes, the slope is positive in 7 of 12 windows.
- **F7:** The other angles showed nothing that stands out after this many looks.

## Ideas
- `032-01.b1.g1_calm-chop-weekly-continuation` (from F1, F3, F4, F5, F6): When a coin's daily swings over the past 30 days are small compared with its own recent history and its price has chopped back and forth rather than made steady net progress over those 30 days, its 7-day move tends to continue in the same direction over the next 7 days. The larger that 7-day move is relative to the coin's typical daily swing over the past 30 days, the larger the continuation.
- `032-01.b1.g2_weekly-move-continuation-graded` (from F1, F2, F5): A coin's 7-day move, measured against its typical daily swing over the past 30 days, tends to continue in the same direction over the next 7 days, and the continuation is larger the choppier the coin's price path has been over those 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
