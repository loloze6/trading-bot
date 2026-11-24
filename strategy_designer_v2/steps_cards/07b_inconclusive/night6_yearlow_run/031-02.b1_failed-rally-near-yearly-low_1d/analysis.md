---
line: 7.b inconclusive
backtest: 031-02.b1_failed-rally-near-yearly-low_1d
idea tested: 031-02.b1_failed-rally-near-yearly-low
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4917 USD
---
## Findings
- **F1:** The test's main correlation is on the predicted side but nowhere near the bar: r 0.025, t 0.50 over 410 cases; its Spearman version gives rho 0.023, t 0.47. Clipping the excess returns at 2 % and 98 % raises it only to r 0.054, t 1.09. One case in the -1..0 forecast bin returned +454 % above the coin's mean, and it lifts that bin's mean to +11.1 % while the bin's median is -0.7 %.
- **F2:** The far-from-low (long) side, which the plan's forecast added to the idea, carries nothing and makes up two thirds of the cases. On its 276 cases r is 0.014 (t 0.24) and the mean excess return is +1.2 % (t 0.78); the 152 cases at forecast above 4 average +0.6 % (t 0.28).
- **F3:** The near-low (short) side carries the idea's direction, graded but weak. Cases at forecast -4 or below average -4.6 % (n 25, t -1.37), cases between -4 and -2 average -1.6 % (n 38), and all 63 cases at -2 or below average -2.8 % (median -3.3 %). Its unusual move toward the short is +5.3 % per case, but with a day-clustered t of only 1.28 on 34 days.
- **F4:** Inside the near-low cases, the effect grows with the 60-day rally, which the test used only as an on/off condition.
- **F5:** The near-low cases with an above-median 60-day return fall in 6 of 7 years and on all 6 coins: in 2020 -29.9 %, 2021 -14.6 % and 2022 -16.9 %; on XRP -19.2 % and on ZEC -19.2 %. 2019 is the exception at +15.8 % (5 cases), and 2019 also gives the only negative yearly correlation (t -2.40).
- **F6:** The test also used a horizon that dilutes the near-low effect slightly. The same forecast reaches t 2.34 at 5 days (1681 cases) and t 1.54 at 10 days, against 0.50 at 20 days. The near-low side's mean excess return deepens with the horizon (-1.2 % at 5 days, -8.6 % at 40 days) but on ever fewer cases (267 down to 27).

## Ideas
- `031-02.b1.b1_strong-failed-rally-near-low` (from F2, F3, F4, F5): The more a coin has risen over the past 60 days while its daily close sits nearer its lowest close of the past 365 days than it usually has over that year, the more it falls over the next 20 days.
- `031-02.b1.b2_failed-rally-more-coins` (from F1, F3): The closer a coin's daily close is to its lowest close of the past 365 days, compared with how close it has usually been over that year, the more it falls over the next 20 days, while its 60-day return is positive.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
