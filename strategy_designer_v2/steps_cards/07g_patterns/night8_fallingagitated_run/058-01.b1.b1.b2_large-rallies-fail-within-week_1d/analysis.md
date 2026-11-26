---
line: 7.g patterns
backtest: 058-01.b1.b1.b2_large-rallies-fail-within-week_1d
idea tested: 058-01.b1.b1.b2_large-rallies-fail-within-week
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4778 USD
---
## Findings
- **F1:** Inside the falling, agitated profile, large rises were not given back over 5 days: the top quintile of the scaled 3-day rise (mean 1.06) was followed by a 5-day excess return of only -0.87 % (t -0.68, 53 cases). Among rises, the slope of the 5-day excess return on the scaled rise was -0.0089 (t -0.76, 108 cases on 43 days). The book's trades lost in 3 of 4 years (2018 -3.63 %, 2020 -5.07 %, 2021 -2.90 %; only 2019 +1.56 %). The total move per case, +0.12 %, is about half the 0.22 % cost of a trade.
- **F2:** At a 3-day horizon inside the profile, the give-back is graded. On 3-day rises, the slope of the next 3 days' excess return on the scaled rise is -0.0319 (clustered t -2.20, 180 cases on 75 days): larger rises are followed by lower returns. The mean is -0.96 % (t -0.86). At 2 days the slope weakens to -0.0165 (t -1.12), and at 5 days to -0.0089 (t -0.76). This is one of about 24 cells tested, so it is a lead, not proof.
- **F3:** Inside the profile, an up day is followed by a lower next day: mean excess -0.85 % (t -1.98 clustered by day, 639 cases on 235 days). This holds in every year (2018 -1.56 %, 2019 -0.77 %, 2020 -0.39 %, 2021 -0.79 %). It is not graded by the up day's size: slope +0.0057, t 0.88; the two top quintiles give -0.96 % (t -2.78) and -0.73 % (t -1.78).
- **F4:** Inside the profile, the strongest pattern is the rebound after falls. The bottom quintile of the scaled 1-day return gives +2.22 % the next day (t 5.42, 260 cases). On down days the slope is -0.0219 (t -2.52) and the mean +1.25 % (t 2.74, 248 days). The bottom quintile of the scaled 10-day return gives +9.02 % over 5 days (t 4.62, 53 cases). The map already holds this (falling agitated long, 12 strategies), so it is not a discovery.
- **F5:** Outside the profile, scaled 3-day moves continue over 5 days. By quintile of the scaled 3-day return, the 5-day excess returns are -1.50 % (t -2.18), -1.96 % (t -2.90), +0.73 %, +0.34 % and +2.45 % (t 3.15), with 272 cases each.
- **F6:** The continuation of F5 is clearest in a falling, calm market, a cell the map holds short with only one strategy. There, the slope of the 5-day excess return on the scaled 3-day return is +0.0265 (clustered t 2.52, 265 cases on 81 days), and on the scaled 10-day return +0.0235 (t 2.43). After 3-day falls the mean is -2.78 % (t -1.75) and the slope +0.0364 (t 1.95). After 10-day falls the mean is -2.90 % (t -2.03, 57 days).

## Ideas
- `058-01.b1.b1.b2.g1_large-rallies-fail-within-days` (from F2, F1, F3): In a falling, agitated market, the larger a coin's 3-day rise against the standard deviation of its daily returns over the past 30 days, the lower its return over the next 3 days.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `058-01.b1.b1.b2.g2_calm-decline-falls-continue` (from F6, F5): In a falling, calm market, the larger a coin's 3-day fall against the standard deviation of its daily returns over the past 30 days, the further its price falls over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
