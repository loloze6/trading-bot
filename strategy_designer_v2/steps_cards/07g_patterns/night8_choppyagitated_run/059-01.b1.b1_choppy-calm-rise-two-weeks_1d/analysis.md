---
line: 7.g patterns
backtest: 059-01.b1.b1_choppy-calm-rise-two-weeks_1d
idea tested: 059-01.b1.b1_choppy-calm-rise-two-weeks
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4760 USD
---
## Findings
- **F1:** The tested idea's book earns the coin's drift, not the idea's move. Per case over 14 days the unusual move is -0.04 % (t -0.04, 589 cases on 377 days) against a normal drift of +2.21 %. The book's Sharpe of 0.483 is 0.07 below holding the coins. In every year from 2018 to 2021 the book's mean daily return is below the coins' (2020: 0.19 % against 0.45 %; 2021: 0.05 % against 0.37 %).
- **F2:** After a large one-day fall scaled by the coin's 30-day daily swing, the coin rebounds in rising calm markets. On the 100 days with a scaled fall below -1.09 (54 distinct days), the next day's excess return is +1.85 % (t 2.88, days clustered) and the next 3 days' is +3.35 % (t 2.78).
- **F3:** The same rebound is absent in the other calm profiles. In choppy calm the next-day excess is -0.70 % (t -0.75, 44 cases). In falling calm it is -0.01 % next day (t -0.02) and -1.83 % over 3 days (t -1.73, 151 cases).
- **F4:** Over all profiles, the next-day excess after a scaled fall grows with the fall's size: slope 0.0084 per unit (t 2.35, 4,035 falling days). The largest-fall decile gains +1.11 % next day (t 2.51 clustered, 822 cases on 238 days). The yearly means are +0.84 %, -0.02 %, +1.57 % and +1.64 % for 2018 to 2021.
- **F5:** Inside the choppy calm profile, the tested scaled weekly rise is not graded across its range. Only the top quintile gains: +27.8 % over 14 days (t 2.32), on 14 cases only. The two quintiles below it lose -8.3 % (t -2.50) and -1.9 %.
- **F6:** Some patterns did not survive a check and support no idea:

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `059-01.b1.b1.g1_rising-calm-scaled-dip-rebound` (from F2, F3, F4): In a rising, calm market, the larger a coin's one-day fall against its usual daily swing over the past 30 days, the larger its rebound over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
