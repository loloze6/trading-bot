---
line: 7.g patterns
backtest: 032-01.b1.b1_flat-range-breaks-more-coins_1d
idea tested: 032-01.b1.b1_flat-range-breaks-more-coins
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4857 USD
---
## Findings
- **F1:** Over the next 10 days, a coin's unusual move rises with where its close sits in the prior 20-day high-low range. By quintile of that position the moves are -0.5 %, -0.3 %, -3.1 %, +1.05 % and +5.7 %. The top quintile has t 2.20 (180 non-overlapping cases on 55 days, day-clustered), and it is positive in both folds shown (B +7.0 %, t 1.52; C +4.5 %, t 1.72).
- **F2:** The same grading holds over 5 days. The top quintile of the 20-day range position is followed by +3.38 % unusual (t 2.00, 364 cases, 117 days) and the bottom by -1.52 %. The top quintile is positive in fold B (+4.0 %) and fold C (+2.7 %). The correlation of range position with the standardised move is positive in 10 of 12 coins at 5 days and 9 of 12 at 10 days.
- **F3:** Over 20 days the grading is gone. The top quintile of the 20-day range position has +0.52 % unusual (t 0.14), and the 60-day range position's top quintile has +7.3 % (t 1.41, 17 days). So the edge of position in the range shows mostly within the first 10 days, not at the idea's 20-day horizon.
- **F4:** Over 10 days, the top tercile of the 60-day range position is followed by a positive unusual move in all three terciles of the 60-day efficiency ratio. The move is largest in the flattest tercile (+9.6 %, t 1.22), then +4.3 % (t 1.55), then +3.4 % (t 1.14). The flattest tercile's middle positions fall -5.6 % (t -1.88). This fits a graded continuation that is stronger in flat coins, but no single cell is sure.
- **F5:** The book's gain rests on few days. It made a summed 0.748 of daily return over 1449 book-days. Its 10 best days sum to 0.533 and its 30 best to 1.159, more than the total, and only 31.9 % of days are positive. Median trade return rises with entry forecast by quartile: +3.6 %, +3.4 %, +5.5 %, +8.8 %. This differs from step 5's failed above-minus-below-median check (-3.4 %).
- **F6:** The other angles gave no pattern that stands out against the more than 30 tables looked at. These were: past 5-, 20- and 60-day return, last day's return, 20-day volatility, the volatility ratio, the 20-day efficiency ratio, day range against its mean, volume against its mean and weekday. Each was non-monotonic or had only a lone quintile with t near ±2 and no grading.

## Ideas
- `032-01.b1.b1.g1_20-day-range-position-continues` (from F1, F2, F3): The higher a coin's daily close sits in its range of highs and lows over the past 20 days, the larger its rise over the next 10 days. A close above the 20-day high is followed by the largest rise.
- `032-01.b1.b1.g2_flat-range-top-continues-briefly` (from F4, F1, F3): In a coin whose price has gone nowhere over the past 60 days, the higher its daily close sits in its 60-day high-low range, the larger its rise over the next 10 days. That rise is larger the flatter the past 60 days were.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
