---
line: 7.e profitable but not proven
backtest: 031-01.g1.g2.d2_outsized-monthly-gain-into-saturday_1d
idea tested: 031-01.g1.g2.d2_outsized-monthly-gain-into-saturday
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3797 USD
---
## Findings
- **F1:** The book's gain rests on a handful of days and trades: the 10 best of 2898 book days sum to 0.646 of the 0.686 total of daily book returns, and the other days average +0.0014 % a day (t 0.24); the 10 best of 796 trades carry 247 of 503 net % and the 30 best carry 487, with a win rate of 49 % and a median trade of −0.02 %.
- **F2:** The market's own rise explains little of the book: the position held times the coin's mean return sums to 0.70 of the book's 5.12 summed position gain (about 14 %), and every unit of gain falls on Saturday bars.
- **F3:** One year carries much of it: 2020 gives 2.02 of the 5.12 summed gain. Saturday's excess return after a 20-day gain is +1.73 % in 2020 (t 4.30, 168 cases), against −0.79 % in 2018 (t −1.79) and −0.27 % in 2023 (t −2.14).
- **F4:** Saturday is the strongest day on its own: its next-day excess is +0.31 % (t 3.84, 2399 cases), against −0.32 % for Thursday (t −2.90) and −0.23 % for Tuesday (t −2.40). On Saturday the excess after a 20-day gain is +0.64 % (t 4.64, 964 cases) and after a 20-day loss −0.08 % (t −0.70); winsorised at 1 %, it stays +0.57 % (t 4.73), with a median of only +0.04 %.
- **F5:** Saturday's excess rises with the 20-day return but is not convex: by per-coin quintile it is −0.50 % (t −1.99), +0.22 %, +0.16 %, +0.54 % (t 3.54) and +0.91 % (t 3.28). Step 5 found the top fifth of the forecast 0.10 % below the rest of the positive cases.
- **F6:** The 5-day return at Friday's close grades Saturday on both sides and more cleanly than the 20-day: by quintile −0.63 % (t −3.07), −0.31 % (t −2.20), +0.50 % (t 4.23), +0.74 % (t 3.57) and +1.03 % (t 3.73).
- **F7:** Over Friday to Sunday (2 days), the 20-day quintiles go from −0.77 % (t −2.20) to +0.81 % (t 3.96) and +1.01 % (t 3.16). Sunday on its own is flat (top quintile +0.18 %, t 0.80), and so is Monday (all quintiles under 0.12 % in size).
- **F8:** The same continuation holds on the day into Friday: after a 20-day gain, the excess over that day is +0.41 % (t 2.79, 990 cases), and the top 20-day quintile gives +0.90 % (t 3.45).
- **F9:** Inside 20-day gains, Saturday's excess is larger when recent volatility is high: +0.86 % (t 2.94) in the top tercile of 20-day volatility, against +0.49 % (t 2.32) in the bottom tercile.

## Ideas
- `031-01.g1.g2.d2.e1_weekly-momentum-into-saturday` (from F4, F5, F6): The higher a coin's 5-day return at Friday's close (UTC), the more it rises over the next day, Saturday; the larger its 5-day fall, the more it falls that Saturday.
- `031-01.g1.g2.d2.e2_late-week-momentum-continuation` (from F4, F8, F2): The higher a coin's 20-day return at the close of Thursday or Friday (UTC), the more it rises over the next day.
- `031-01.g1.g2.d2.e3_monthly-gain-into-weekend` (from F7, F5): The higher a coin's 20-day return at Friday's close (UTC), the more it rises over the next two days, Saturday and Sunday together.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
