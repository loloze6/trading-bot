---
line: 7.c no effect
backtest: 047-03_falling-agitated-scaled-rise-giveback_1d
idea tested: 047-03_falling-agitated-scaled-rise-giveback
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4735 USD
---
## Findings
- **F1:** The tested grading is absent, but the fall after up days is real. In the falling agitated profile, up days (177 cases, 104 days) were followed by a next-day return 1.06 % below the coin's drift (t -1.88, day-clustered), with the same sign in every year (2018 -1.14 %, 2019 -1.09 %, 2020 -0.94 %, 2021 -1.17 %) and every window. Yet the slope of that return on the scaled rise is flat (t 0.13 at 1 day, 0.67 at 2 days, -0.46 at 3 days). The smallest up days fell the most (z sextiles 0.11 and 0.40: -1.19 % and -1.30 %), and the largest the least (z 1.12: -0.66 %).
- **F2:** What grades the fall is how close the up day's close sits to the coin's highest close of the past 30 days, and it shows over 2 to 3 days. The day-clustered slope of the excess return on that distance is t -2.82 over 2 days and t -2.70 over 3 days (176 cases, 103 days). Up days closing nearest the 30-day high (mean 7 % below it) lost 4.36 % over the next 3 days. Those furthest below it (mean 50 % below) gained 1.22 %.
- **F3:** The width of the up day's high-low range, measured in 30-day standard deviations, also grades the next-day fall, though weakly. Its slope is t -1.54 pooled and t -2.53 on BCH (38 cases), and the widest quarter of up days (range 2.38 sd) fell 1.72 % the next day and 2.01 % over 3 days, against -1.07 % and -0.29 % in the narrowest quarter.
- **F4:** The two-way fade of the brief exists only on the down side, which this short-only research cannot take. Profile days in the lowest z sextile (z -1.36) rose 3.20 % the next day (t 3.32), and the second sextile rose 1.80 % (t 3.13). Days closing in the bottom quarter of their range rose 2.43 % against -0.73 % for the top quarter.
- **F5:** The fade belongs to the profile. Outside it, the largest up days (z 1.62) were followed by -0.05 % and the next sextile by +0.05 %, against -0.66 % to -1.30 % inside the profile.
- **F6:** On the full record, the size per short bar is too small for the cost. The total move is +0.31 % per case against a 0.35 % round-trip cost (0.9 times), so a one-day short on the scaled rise cannot pay. Only a longer horizon or a sharper situation (F2: -4.36 % over 3 days) could.

## Ideas
- `047-03.c1_rally-near-30-day-high-fades` (from F2, F1, F5, F6): In a falling, agitated market, the closer a coin's close on an up day is to its highest close of the past 30 days, the larger its fall over the next three days.
- `047-03.c2_wide-up-day-range-fades` (from F3, F1, F5): In a falling, agitated market, the wider a coin's up day's high-low range relative to the standard deviation of its daily returns over the past 30 days, the larger its fall over the next three days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
