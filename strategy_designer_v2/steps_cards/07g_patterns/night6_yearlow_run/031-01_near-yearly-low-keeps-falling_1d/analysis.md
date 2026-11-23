---
line: 7.g patterns
backtest: 031-01_near-yearly-low-keeps-falling_1d
idea tested: 031-01_near-yearly-low-keeps-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5106 USD
---
## Findings
- **F1:** The tested short lost mainly because the coins rose: per case the unusual move is -1.41 % (t -0.75 with the cases of one day taken together, 243 days) on top of a normal drift of -3.03 % in the short's direction, a total of -4.44 % per case (23 times the 0.19 % cost of a trade) while in a position on 86 % of the coins' days, so the book's Sharpe is -0.30 and its yearly return -16.4 %.
- **F2:** Nearness to the yearly low does not grade the next 20 days: by proximity quintile the drift-adjusted 20-day return is -2.4 %, +0.3 %, +4.0 %, -0.3 % and -1.7 % (all |t| ≤ 1.24, about 161 cases each), and the 17 cases closing at the low itself average -9.2 % with t -1.69.
- **F3:** Saturday is the one day on which the coins rise clearly: the per-day mean over the coins is +0.47 % (t 3.14, 414 days) against between -0.18 % and +0.32 % on the other weekdays, and Saturday minus the other days has a Welch t of 2.36.
- **F4:** The Saturday rise is broad but uneven: it shows in 7 of 8 years (2023, -0.18 %, is the exception) and in all 6 coins (Saturday minus other days from +0.05 % for BTC to +0.59 % for LTC, per-coin t 0.34 to 2.67), and it is weaker in windows w13 to w24 (excess +0.23 %, t 1.27) than in w1 to w12 (+0.38 %, t 2.05).
- **F5:** Saturday's return grows with the coin's return over the 5 days before it: by quintile of that 5-day return the Saturday mean is -0.29 % (t -0.29), 0.00 % (t 0.85), +0.44 % (t 3.21), +0.97 % (t 3.09) and +1.13 % (t 2.71), about 464 cases each, cases of one day taken together.
- **F6:** Saturday's return does not depend on Friday's return alone: by quintile of Friday's return it is positive in every quintile and not ordered (+0.23 %, +0.60 %, +0.23 %, +0.61 %, +0.45 %).
- **F7:** The always-short book pays for the Saturday rise: its per-day mean is -0.14 % on Saturdays (t -2.26, 414 days), its worst weekday.

## Ideas
- `031-01.g1_weekly-gains-carry-into-saturday` (from F3, F4, F5, F6, F7): Going into the weekend, the higher a coin's return over the past 5 days, the more it rises over the next day (Saturday, UTC), so a week of gains carries on into Saturday.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
