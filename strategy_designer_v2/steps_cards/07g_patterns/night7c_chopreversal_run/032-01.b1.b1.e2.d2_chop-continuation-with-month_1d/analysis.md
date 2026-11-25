---
line: 7.g patterns
backtest: 032-01.b1.b1.e2.d2_chop-continuation-with-month_1d
idea tested: 032-01.b1.b1.e2.d2_chop-continuation-with-month
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3551 USD
---
## Findings
- **F1:** In choppy months (30-day efficiency ratio at most 0.3, 612 non-overlapping 7-day cases), the 30-day move scaled by 30-day daily swings predicts the next 7 days' move beyond drift the same way (slope t 4.24, signed mean +2.03 %, t 3.49). Outside chop (ER above 0.3, 247 cases) it predicts nothing (slope t -0.34, mean -0.09 %). In the top ER quintile the sign even turns against continuation (mean -2.57 %, t -1.97, 172 cases).
- **F2:** Inside chop, the continuation is far stronger when the coin's 30-day daily swings are low against its 90-day swings. In the lowest third of that ratio the slope t is 4.85 (signed mean +4.25 %, t 2.99, 132 cases), against slope t 1.46 and 1.38 in the middle and upper thirds (131 and 132 cases).
- **F3:** In a joint regression on chop cases (612), the scaled last-7-day move and the scaled move of the 23 days before it both point to continuation (t 5.28 and t 3.30). The older 23 days alone give slope t only 1.43. So the month's older part adds to the week rather than standing on its own.
- **F4:** When the 7-day and 30-day moves disagree in chop (268 cases), the next week is flat (signed mean +0.18 %, slope t 0.07). When they agree (344 cases) it continues (signed mean +3.74 %, t 4.89, slope t 5.14). Long and short regime cases pay alike (+3.54 % t 3.40 vs +3.94 % t 3.52).
- **F5:** The pattern is not confined to the most trendless months. Inside chop the slope t rises with the efficiency ratio: 1.16 for ER 0–0.1 (232 cases), 2.02 for 0.1–0.2 (185) and 3.56 for 0.2–0.3 (195).
- **F6:** The book's daily returns barely track holding the coins (correlation 0.045). On its best 2 % of days (29) it gains +6.46 % while holding gains +0.26 %. On its worst 2 % it loses -4.98 % while holding loses -1.78 %. The gains come from timing, not from the market's rise.

## Ideas
- `032-01.b1.b1.e2.d2.g1_contracted-swings-monthly-continuation` (from F2, F1, F6): When a coin's daily swings over the past 30 days are smaller than over the past 90 days, its 30-day move counted in its 30-day daily swings tends to be followed by a move the same way over the next 7 days. The larger the scaled 30-day move and the more the swings have shrunk, the larger the following move.
- `032-01.b1.b1.e2.d2.g2_chop-week-plus-month-continuation` (from F3, F4, F1, F5): When a coin's past 30 days have gone back and forth with little net progress, its last 7-day move and the move of the 23 days before it, each counted in 30-day daily swings, add up to predict a move the same way over the next 7 days. The larger their sum, the larger the following move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
