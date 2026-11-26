---
line: 7.d confirmed, not profitable
backtest: 031-01.g1.g2.d1_monthly-gain-lifts-saturday_1d
idea tested: 031-01.g1.g2.d1_monthly-gain-lifts-saturday
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4152 USD
---
## Findings
- **F1:** The check failed only on Calmar, 0.715 against the 0.75 it needs (yearly +8.9 %, deepest fall −12.5 %). The deepest fall ran 703 days and bottomed in w17, after w16 lost 7.05 % of book (the book's worst window, fall −11.0 %), while the coins themselves rose about 54 % in w16 and 51 % in w17.
- **F2:** The book's worst Saturdays are big positions on coins that were already stretched. The 20 worst signal Saturdays in w16–w17 had a mean allocation of 0.98 and lost 4.7 % on average (worst −10.75 %). Their coins had risen a mean 12.5 % over 5 days and 34 % over 20 days, and the median coin closed at its 20-day high.
- **F3:** Inside the signal, the 5-day return at Friday's close grades Saturday's excess return cleanly. By 5-day-return quartile the excess is −0.32 %, +0.33 %, +0.85 % and +1.64 % (about 246 cases each). Signal Fridays with a 5-day rise earn +0.95 % (t 5.51, 735 cases); those with a 5-day fall earn −0.16 % (t −1.04, 394 cases).
- **F4:** The 5-day-rise condition is not an effect of its own. Without the 20-day gain, Fridays with a 5-day rise earn only +0.38 % (t 1.78, 380 cases), against +0.95 % when both hold. On other weekdays a 20-day gain with a 5-day rise earns +0.00 % (t 0.03, 4037 cases). So it belongs to the idea's own story, a gain still running into the weekend.
- **F5:** Keeping only the signal Saturdays whose coin rose over the 5 days to Friday changes the failing measure. Calmar goes from 0.715 to 0.834, the deepest fall from −12.5 % to −11.4 %, the yearly return from 8.95 % to 9.51 % and the Sharpe from 0.86 to 0.95. A filter on closing near the 20-day high instead lowers Calmar to 0.535.
- **F6:** The effect sits in the strongest cases of the 20-day gain. The top quartile of the 20-day gain (above 26 %) earns +1.32 % excess, against +0.33 % to +0.43 % in the three lower quartiles. The top forecast quartile (17.6–20) earns +1.42 % against +0.28 % to +0.41 % below it, so the low-forecast trades pay fees for little.
- **F7:** The effect carries over Sunday. Signal cases earn +0.75 % excess over Saturday and Sunday together (t 4.60, 1178 cases), against +0.61 % over Saturday alone (t 4.93). Each trade's 0.19 % cost would then cover a larger move.

## Ideas
- `031-01.g1.g2.d1.d1_weekend-lift-needs-fresh-gain` (from F2, F3, F4, F5): The higher a coin's gain over the past 20 days at Friday's close (UTC), the more it rises over the next day, Saturday, this holding only while that coin has also risen over the past 5 days, and more the larger that 5-day rise.
- `031-01.g1.g2.d1.d2_strongest-monthly-gains-lift-saturday` (from F6, F3): The higher a coin's gain over the past 20 days at Friday's close (UTC), the more it rises over the next day, Saturday, the rise growing sharply in the largest 20-day gains, so that a small 20-day gain says little about Saturday.
- `031-01.g1.g2.d1.d3_monthly-gain-lifts-weekend` (from F7, F1): The higher a coin's gain over the past 20 days at Friday's close (UTC), the more it rises over the next two days, Saturday and Sunday, this holding only when that 20-day return is a gain.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
