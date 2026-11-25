---
line: 7.g patterns
backtest: 058-01_agitated-decline-rally-giveback_1d
idea tested: 058-01_agitated-decline-rally-giveback
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5441 USD
---
## Findings
- **F1:** The tested idea's grading is absent in the falling, agitated profile: on the 5-day grid, the unusual 5-day move by quintile of the scaled 3-day return runs +3.78 %, +0.41 %, +3.37 %, -2.06 %, -0.76 % (45, 44, 44, 44, 45 cases), with no steady fall as the rise grows; the largest rises are followed by -0.76 % (t -0.53), and the Spearman rho of the scaled 3-day return with the move is -0.107 (p 0.11, 222 cases).
- **F2:** The book lost on its own trades: 394 short trades, mean net -2.77 %, median -0.72 %. The trade cost is 0.19 %, against a total move per case of -0.32 % and an unusual move of +0.33 % (t 0.49).
- **F3:** What the profile does hold is a rebound after the deepest 10-day falls, which the profile map already lists for falling agitated long (035-01, 038-01, 047-01, 051-01 and others): the lowest quintile of the scaled 10-day return is followed by an unusual 5-day move of +8.00 % (plain t 3.81, but t 1.74 with the cases of one day together, 19 days), and the rho is -0.182 (p 0.0066, 222 cases).
- **F4:** Inside the profile, a narrower case of the brief's situation does grade the give-back. Among up days, the larger the one-day rise against the 30-day swing, the lower the unusual move that follows: Spearman rho -0.249 over 3 days (p 0.0005) and -0.254 over 5 days (p 0.034). On the 5-day grid, the top quintile of one-day rises is followed by -3.41 % (plain t -2.47, 45 cases; t -1.71 with the cases of one day together, 26 days). Over 2 days the pattern is absent (rho -0.015).
- **F5:** Outside the falling, agitated profile, past moves continue instead of reversing: on the 5-day grid, the rho of the unusual 5-day move with the scaled 3-day return is +0.106 (p 0.0003) and with the scaled 10-day return +0.115 (p 0.0001), 1,142 cases. The top 3-day quintile is followed by +2.33 % (t 2.06, 96 days), the bottom by -2.09 % (t -1.66, 85 days), and all six coins show a negative bottom 10-day quintile (-0.49 % to -2.54 %) and a positive top one (+0.15 % to +3.56 %).
- **F6:** That continuation is strongest in falling, calm markets: rho +0.244 (p 0.0010, 180 cases), with the bottom 10-day quarter followed by -4.56 % (t -1.57) and the top quarter by +3.39 % (t 1.68). This uses my own approximation of the calm/agitated split (30-day swing against the coin's expanding swing), not the official percentile. The other profiles show weaker rhos: rising calm 0.105 (p 0.14), rising agitated 0.129 (p 0.16).
- **F7:** The continuation is not steady across years. The top 10-day quintile outside the profile is followed by -1.05 % in 2018 (22 cases), -2.88 % in 2019 (41), +3.93 % in 2020 (83) and +3.25 % in 2021 (83). The bottom quintile is followed by -2.85 %, -2.06 %, -4.97 % and +2.39 % over the same years.
- **F8:** No calendar or bar-shape pattern stands out. The unusual 5-day move by weekday ranges from -1.92 % to +1.48 % (about 190 cases each). By close position in the day's range and by range against the swing, every quintile has |t| < 1.9.

## Ideas
- `058-01.g2_agitated-decline-one-day-rise-fades` (from F1, F4): In a falling, agitated market, the larger a coin's one-day rise against the standard deviation of its daily returns over the past 30 days, the larger the fall in its price over the next 3 days.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `058-01.g1_falling-calm-move-continuation` (from F5, F6, F7): In a falling, calm market, the larger a coin's 10-day return against the standard deviation of its daily returns over the past 30 days, the further its price moves the same way over the next 5 days: deep 10-day falls keep falling and strong 10-day rises keep rising.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
