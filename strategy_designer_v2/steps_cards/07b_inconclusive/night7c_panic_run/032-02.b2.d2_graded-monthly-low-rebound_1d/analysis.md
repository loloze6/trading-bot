---
line: 7.b inconclusive
backtest: 032-02.b2.d2_graded-monthly-low-rebound_1d
idea tested: 032-02.b2.d2_graded-monthly-low-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3375 USD
---
## Findings
- **F1:** Step 5's result is on the side the idea predicts but below the bar: the mean next-day excess return is +0.82 % with a pooled t of 1.46 over 197 days. On folds B and C alone it is +1.85 % with a pooled t of 2.10 (209 cases, 89 days), so folds A and D are weaker but not reversed. More coins exist on the same folds than the six tested.
- **F2:** The effect is mixed over time. It is about zero in 2018 (+0.07 %, 102 cases, t 0.08) and 2019 (+0.39 %, 51 cases, t 0.37), and large in 2020 (+6.0 %, 31 cases, t 1.97) and 2021 (+6.9 %, 25 cases, t 2.00). The mean range ratio of the cases also rises across those years, from 0.61 to 1.55.
- **F3:** The effect is graded as the idea says and sits in the strongest cases. By forecast quartile the excess runs -0.41 %, +0.64 %, +2.48 %, +4.75 % (t 3.32 in the top quartile). By range-width tercile it runs -0.86 %, +1.49 %, +4.92 % (pooled t 2.60). Deep breaks with wide ranges earn +6.25 % (pooled t 2.79, 52 cases), while the other three depth-by-width cells earn between -0.34 % and +1.10 %.
- **F4:** The sharpest grading is the fall of the past 5 days. In the steepest 5-day-fall tercile (-20 % to -56 %) the excess is +5.64 % (pooled t 3.07, 67 cases, 33 days), against +0.61 % and -0.87 % in the other two terciles. Its Spearman correlation with the next-day excess return is -0.36, stronger than the forecast's 0.22.
- **F5:** The rebound is a one-day move. On the same cases the mean excess is +1.85 % at 1 day (t 3.65), +0.69 % at 2 days, -0.25 % at 3 days and -2.24 % at 10 days (t -2.07). The comparison is with ordinary declining days without a break, which lose 0.27 % the next day (t -2.78, 2,821 days).

## Ideas
- `032-02.b2.d2.b1_monthly-low-rebound-more-coins` (from F1, F3): In a coin that has fallen over the past 30 days, a close below its lowest low of the prior 30 days is followed by a rise over the next 1 day. The rise is larger the further that close sits below the prior 30-day low, measured in units of the coin's mean daily high-low range over the past 30 days, and larger the wider those ranges are compared with the coin's past year.
- `032-02.b2.d2.b2_plunge-into-monthly-low-rebound` (from F4, F5, F3): In a coin that has fallen over the past 30 days and closes below its lowest low of the prior 30 days, the close is followed by a rise over the next 1 day that is larger the more the coin fell over the past 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
