---
line: 7.g patterns
backtest: 059-01.b1.b1.d1.b1.b1.d2_choppy-calm-rise-four-weeks_1d
idea tested: 059-01.b1.b1.d1.b1.b1.d2_choppy-calm-rise-four-weeks
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5597 USD
---
## Findings
- **F1:** In a falling, agitated market, a large up day is followed by a fall rather than a further rise, and the fall grows with the size of the day. A day in the top fifth of rises (the day's return over its 30-day daily standard deviation) has a next-day excess return of -1.18 % (t -2.06, day-clustered, 216 cases on 87 days) and a 3-day excess return of -4.04 % (t -2.20, 76 cases on 29 days). Within that profile's rise days, the 3-day excess goes from +1.16 % to -0.54 % to -4.12 % across terciles of the day's scaled size (top tercile t -2.19, 74 cases on 29 days). The next-day excess also falls step by step, -0.44 %, -0.71 %, -1.19 %. The profile map has no strategy in the falling agitated short cell. The 2-day grid is weaker (-0.34 %, t -0.37), and I looked at many angles, so this rests on t near 2.2.
- **F2:** The tested continuation is not graded inside the choppy calm profile. Over 7 days, the excess return by quintile of the scaled weekly rise is +1.73 %, -0.17 %, -3.24 % (t -2.10), +0.41 % and +5.11 % (t 2.29, 33 cases). Over 28 days the in-profile quintiles hold only 4 to 9 cases each. This matches step 5's unusual move of +0.93 % with t 0.42 over 267 days.
- **F3:** The book's trades do not grow with the entry forecast. The mean net trade return by forecast tercile is +0.92 %, +9.18 % and +4.62 %, with win rates of 53 %, 56 % and 50 % (89 to 90 trades each).
- **F4:** The book mostly moves with the coin, and one window carries its fall.
- **F5:** The largest daily falls rebound the next day, and the rebound is graded. By decile of the scaled one-day move:
- **F6:** Weekday next-day excess returns are not distinguishable from chance once days are clustered. The largest is Saturday, +0.37 % with t 1.44. A large up day in a choppy market leads to +6.8 % over 7 days, but with t 1.26 on 22 cases.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `059-01.b1.b1.d1.b1.b1.d2.g1_falling-agitated-rally-fades` (from F1): In a falling, agitated market, the larger a coin's one-day rise in multiples of its usual daily swing over the past 30 days, the larger its fall over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
