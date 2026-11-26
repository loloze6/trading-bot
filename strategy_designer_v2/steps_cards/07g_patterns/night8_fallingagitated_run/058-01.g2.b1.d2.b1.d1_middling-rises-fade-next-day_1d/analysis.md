---
line: 7.g patterns
backtest: 058-01.g2.b1.d2.b1.d1_middling-rises-fade-next-day_1d
idea tested: 058-01.g2.b1.d2.b1.d1_middling-rises-fade-next-day
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4355 USD
---
## Findings
- **F1:** Inside the falling agitated profile (folds B and C), one-day rises of up to one 30-day standard deviation were followed by a next-day unusual move of -0.97 % (z 0 to 0.5: 354 cases, 166 days, t -1.88) and -1.18 % (z 0.5 to 1: 163 cases, 97 days, t -1.76), and this was negative in every year (2018 -2.2 % t -2.51, 2019 -0.9 % t -2.14, 2020 -0.1 %, 2021 -1.2 %); rises above one deviation were not given back (z 1 to 2: -0.17 %, t -0.24, 101 cases; z > 2: +0.21 %, 21 cases), so on these folds the hump has the idea's shape, but each bin's t is under 2.
- **F2:** Inside the profile, the rise over the last 3 days against the 30-day swing is given back over the next 3 days, and more so for larger rises: on the 3-day grid, z3 0.8 to 1.3 gave -3.66 % unusual (31 cases, 20 days, t -2.02), z3 > 1.3 gave -2.67 % (23 cases, t -1.14), z3 0.3 to 0.8 gave -0.37 %, and the correlation of the rise's size with the next-3-day unusual move over the up cases is -0.22 (180 cases); per case this move is more than ten times the 0.22 % cost of a trade, against 0.47 % total per case for the tested one-day book.
- **F3:** Outside the profile, 3-day rises keep going instead of being given back: z3 0.5 to 1.5 gave +1.0 % over the next 3 days (465 cases, 190 days, t 1.89) and z3 > 1.5 gave +1.9 % (169 cases, t 1.49), so the give-back in F2 belongs to the falling agitated profile.
- **F4:** Inside the profile, large down days rebound the next day, graded by their size: z1 below -2 gave +6.2 % (29 cases, 11 days, t 1.63), -2 to -1 gave +2.1 % (t 1.77), and -1 to -0.5 gave +1.1 % (t 1.91); this was positive in all four years (2020 +9.1 %, t 2.64), and days whose range is in the widest quarter against their 30-day median gave +1.58 % (t 1.94). This is the falling agitated long rebound the map already holds 12 times, so it is not a discovery.
- **F5:** Outside the profile, in rising markets with a coin's swing at or below its median (approximated by its rank over the whole sample, not over the past year), one-day falls beyond one 30-day deviation were followed by a next-day unusual rise of +1.59 % (t 3.01). It is the only cell among about 100 inspected with a t above 3. The same falls in rising agitated markets gave +1.2 % (t 1.43). Weekday (all |t| < 1.7), the up day's close position and the day's range showed nothing else.

## Ideas
- `058-01.g2.b1.d2.b1.d1.g1_three-day-rallies-fade-three-days` (from F2, F3, F1): In a falling, agitated market, a coin's rise over the last 3 days, measured against the standard deviation of its daily returns over the past 30 days, is given back over the next 3 days, and the larger that rise, the larger the share given back.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `058-01.g2.b1.d2.b1.d1.g2_calm-uptrend-dip-next-day-rebound` (from F5): In a rising, calm market, a coin's one-day fall, measured against the standard deviation of its daily returns over the past 30 days, is followed by a rise over the next day, and the larger the fall, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
