---
line: 7.g patterns
backtest: 059-01.b1.b1.d1.b1_choppy-calm-rise-three-weeks_1d
idea tested: 059-01.b1.b1.d1.b1_choppy-calm-rise-three-weeks
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4412 USD
---
## Findings
- **F1:** Inside the choppy calm profile, a large one-day rise is followed by a fall the next day. Days rising 2 to 3 times the coin's usual 30-day daily swing return -1.98 % against the coin's normal drift (t -2.24, cases of a day together, 31 cases on 25 days). Days rising more than 3 times return -1.35 % (t -2.44, 9 cases on 9 days). Days rising 0 to 2 times return between -0.15 % and +0.06 % (t -0.60 and +0.11).
- **F2:** This giveback after large in-profile up days (rise above 1.5 usual daily swings, next day) points the same way in every year and every coin with cases. Every year 2018 to 2021 is negative (-2.75 %, -3.02 %, -0.58 %, -0.65 %; t -1.85, -1.98, -0.43, -0.62). All 8 coins with cases are negative (for example ADA -4.9 % with t -2.59, XMR -2.1 % with t -1.73). Over 3 days, 2019 to 2021 are negative too (-1.4 %, -1.8 %, -2.5 %).
- **F3:** The giveback after up days in the choppy calm profile is graded. On up days, the excess return over the next 3 days falls by 1.23 % per usual daily swing of the day's rise (slope t -2.67, day-clustered, 160 cases). Outside the profile the same slope is opposite in rising markets (+1.91 %, t +2.00, 355 cases), so the reversal belongs to the trendless quiet market.
- **F4:** The tested idea's own grading is not visible in folds B and C. In-profile cases split into forecast quartiles return -10.9 %, +22.3 % and -6.5 % over 21 days, with only 5, 5 and 9 cases. The 21-day returns binned by scaled weekly rise in the profile do not rise with the rise (+28.9 % at -1.5 to -0.5 swings, -6.7 % at -0.5 to 0.5, +0.8 % above 1.5, all with |t| under 2). This matches step 5's unusual move of -0.88 % (t -0.59).
- **F5:** The book's entries at low forecast lose and those at higher forecast gain. Trades in the lowest forecast third lose 2.04 % on average after fees (97 trades); the rest gain 6.74 % on average with a median of 1.57 % (195 trades). The book is in the profile only 12 % of the coin-days in these folds.
- **F6:** Outside the profile, large down days rebound the next day: below -2 usual swings, +1.88 % (t 1.94, 67 days). This is what the map already holds in the agitated and falling-agitated cells. It is left out as not new.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `059-01.b1.b1.d1.b1.g1_choppy-calm-spike-reverses` (from F1, F2, F3): In a choppy, calm market, the larger a coin's one-day rise measured in multiples of its usual daily swing over the past 30 days, the larger its fall over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
