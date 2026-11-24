---
line: 7.g patterns
backtest: 031-01.g1_weekly-gains-carry-into-saturday_1d
idea tested: 031-01.g1_weekly-gains-carry-into-saturday
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4259 USD
---
## Findings
- **F1:** The Saturday effect comes from the four days before Friday, not from Friday itself: the product of the coin's prior 4-day return (Monday close to Thursday close, scaled by volatility) and Saturday's excess return averages 0.00764 with t 3.73 over 345 days, against 0.00134 with t 0.74 for Friday's own move; for the same 4-day return before any other weekday, t ranges from −0.99 to 1.68.
- **F2:** Friday's own move does not grade Saturday: Saturday's excess return across Friday's own-move quintiles is +0.05 %, +0.43 %, +0.24 %, +0.23 % and +0.30 % (all t ≤ 1.83, about 414 cases each), with no rising order.
- **F3:** The weekly-return slope exists only into Saturday: the correlation of the volatility-scaled 5-day return with the next day's excess return is 0.18 (t 3.45, 345 days) into Saturday, against −0.07 to 0.05 (t −1.54 to 0.98) into every other weekday.
- **F4:** Into Saturday the effect rises steadily across the 5-day-return quintiles: Saturday's excess return goes from −0.58 % (t −1.49), −0.30 %, +0.35 %, +0.75 % (t 2.99) to +1.03 % (t 2.78) in the top quintile, about 418 cases each; Sunday gives back only −0.23 % to −0.25 % (t −0.70 to −0.95) in the top two quintiles.
- **F5:** The Saturday cases are positive on all six coins (mean +0.30 % for BTC with t 1.91, up to +1.39 % for XRP with t 2.80; LTC +0.97 % with t 3.37) and in 7 of 8 years; the exception is 2023 at −0.15 % (t −0.65).
- **F6:** A longer run also carries into Saturday: the 20-day volatility-scaled return times the next day's excess return averages 0.00554 with t 2.56 into Saturday and 0.00369 with t 1.76 into Friday, against |t| ≤ 0.98 into the other five weekdays.
- **F7:** The book earns entirely on Saturdays (summed daily returns 0.911 on Saturdays against −0.098 on Fridays and 0 on other days), and its 29 best days (top 1 %) carry 135 % of its total gain, on days when its coins rose 5.4 % on average.
- **F8:** Unconditionally, Saturday is the only weekday with a measurable excess return (+0.30 %, t 2.09, 414 days; the other days range from t −1.30 to 1.28), so part of the Saturday gain is a weekday effect apart from the weekly return.

## Ideas
- `031-01.g1.g1_midweek-run-carries-into-saturday` (from F1, F2, F3, F5): The higher a coin's return over the four days from Monday's close to Thursday's close, the more it rises over Saturday (UTC), and this grading does not come from Friday's own move.
- `031-01.g1.g2_monthly-trend-carries-into-saturday` (from F6, F3, F4): The higher a coin's return over the past 20 days at Friday's close (UTC), the more it rises over the next day, Saturday.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
