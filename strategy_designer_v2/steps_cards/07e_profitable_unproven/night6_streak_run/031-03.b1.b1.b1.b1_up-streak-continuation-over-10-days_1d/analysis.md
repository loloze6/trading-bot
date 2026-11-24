---
line: 7.e profitable but not proven
backtest: 031-03.b1.b1.b1.b1_up-streak-continuation-over-10-days_1d
idea tested: 031-03.b1.b1.b1.b1_up-streak-continuation-over-10-days
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4904 USD
---
## Findings
- **F1:** The tested streak adds nothing on its own: among 10-day non-overlapping cases with a positive 30-day return, those with no up streak have a larger unusual move (+1.44 %, t 0.97, 533 cases) than those with a streak (+0.78 %, t 0.60, 628 cases), and the same holds at 20 days (+1.30 % against +0.28 %).
- **F2:** What the book earns grows with the strength of the coin's 30-day return relative to its own 30-day volatility. Over 10 days the unusual move by quintile of that ratio is −0.94 %, −1.91 %, −1.48 %, +1.25 %, +3.08 % (top quintile t 1.72, 299 cases on 74 days), which is about 0.20 of the coin's usual 10-day move of 15.76 %. The slope of the unusual move on the ratio is +1.29 % per unit (t 1.75, 1495 cases).
- **F3:** Inside the book's positions, the gain sits in the highest 30-day returns. On held days split by 30-day return quartile (medians −7 %, +5 %, +17 %, +45 %), the timing gain is −0.074 %, −0.015 %, +0.245 % and +0.278 % a day.
- **F4:** On raw 30-day return terciles among positive months, the 10-day unusual move is −1.04 %, +1.32 % and +2.97 % (top tercile t 1.74), and over 5 days −0.45 %, +1.01 % and +1.50 % (t 1.78).
- **F5:** The market's own rise carries most of the book. Of the book's mean daily return of 0.130 % (Sharpe 0.96, 2898 days), 0.080 % (61 %) is the position times the coin's mean daily return, and the timing rest is 0.051 % a day with t 1.05 (timing Sharpe 0.37).
- **F6:** The book earns mostly after the streak signal has ended. Days held after a zero forecast contribute 0.073 % a day to the book (0.029 % timing), against 0.059 % (0.023 % timing) for days with a live streak forecast; trades last 28.9 days on average against the plan's 10-day horizon.
- **F7:** The gain rests on a few trades and some periods:
- **F8:** The momentum grading holds in both halves of the period. The top quintile of the 30-day return over volatility beats the bottom quintile over 10 days in 2018–21 (+4.81 % against −1.51 %) and in 2022–25 (+2.36 % against −0.78 %).

## Ideas
- `031-03.b1.b1.b1.b1.e1_volatility-scaled-monthly-momentum-continuation` (from F1, F2, F3, F5, F8): The larger a coin's 30-day return relative to the volatility of its daily returns over those same 30 days, the more it rises over the next 10 days, above its normal drift.
- `031-03.b1.b1.b1.b1.e2_30-day-return-short-continuation` (from F3, F4, F6): The higher a coin's 30-day return, the more it rises over the next 5 days, above its normal drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
