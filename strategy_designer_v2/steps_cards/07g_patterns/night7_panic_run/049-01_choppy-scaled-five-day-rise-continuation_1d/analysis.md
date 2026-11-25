---
line: 7.g patterns
backtest: 049-01_choppy-scaled-five-day-rise-continuation_1d
idea tested: 049-01_choppy-scaled-five-day-rise-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3897 USD
---
## Findings
- **F1:** Outside the choppy profile (60-day trend beyond ±10 %), the top fifth of each coin's 5-day return scaled by its 30-day daily swing is followed by an excess 3-day return of +1.75 % (t 2.24, 375 cases on 149 days) and an excess 5-day return of +2.76 % (t 2.32, 205 cases). This is about 9 times the 0.19 % cost of a trade. Inside the choppy profile the same fifth gives -0.58 % over 3 days (t -0.78, 65 cases) and +0.50 % over 5 days (t 0.23), so the tested idea sat in the one profile where the continuation is absent.
- **F2:** Outside the choppy profile the follow-through grows with the scaled rise. The excess 3-day return climbs from -0.79 % and -1.09 % in the two lowest deciles to +2.28 % (t 2.94, 191 cases) and +1.19 % (t 1.11, 184 cases) in the two highest. The linear slope on positive scaled rises alone is weak (+0.27 % per unit, t 0.85), so the effect sits in the largest rises.
- **F3:** Splitting by the 60-day trend read in-window, the top fifth of scaled 5-day rises carries most strongly in a rising market: +2.51 % over 3 days (t 1.87, 154 cases on 68 days). In a falling market it gives +0.92 % (t 0.55, 92 cases) and in choppy bars -0.38 % (t -0.38, 40 cases). This is the opposite of the brief's claim that rising markets damp the carry-on.
- **F4:** The non-choppy top-fifth continuation is broad. It is positive on all 6 coins, from ZEC +0.71 % (t 0.53) to XRP +3.91 % (t 2.11), and in 9 of the 12 windows. By year it is -0.11 % in 2018 (t -0.06), +0.67 % in 2019, +2.18 % in 2020 (t 1.52) and +2.92 % in 2021 (t 2.19), so it is uneven over time.
- **F5:** Inside the choppy profile, the bottom fifth of scaled 5-day returns (the largest falls) is followed by -4.47 % over 3 days (t -2.03, 52 cases on 39 days) and -9.54 % over 5 days (t -2.34, 29 cases). There are few cases, and this is one cell among dozens examined, so it does not stand out from chance.
- **F6:** The other angles show nothing that stands apart from chance after this many looks:

## Ideas
- `049-01.g1_rising-market-scaled-rise-continuation` (from F1, F2, F3, F4): In a rising market, after a five-day rise, a coin rises further over the next 3 days, more so the larger its 5-day return in units of its 30-day daily-return swing.
- `049-01.g2_rising-scaled-rise-five-day-carry` (from F1, F2, F3): In a rising market, after a five-day rise, a coin rises further over the next 5 days, more so the larger its 5-day return in units of its 30-day daily-return swing.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
