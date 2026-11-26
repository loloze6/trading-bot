---
line: 7.g patterns
backtest: 059-01.b1.b1.d1.b1.b1_choppy-calm-rise-two-weeks_1d
idea tested: 059-01.b1.b1.d1.b1.b1_choppy-calm-rise-two-weeks
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4148 USD
---
## Findings
- **F1:** Drift, not timing, carries the tested idea. Its unusual move per case is -0.14 % over 14 days (t -0.14, 375 days, 581 cases) against a normal drift of +2.21 %, and the book trails holding the coins (Sharpe 0.47, 0.087 below holding's). In folds B and C its daily mean ranges from -0.30 % (w14) to +0.36 % (w17), and its yearly sums run from -54 % (2018) to +69 % (2020).
- **F2:** Inside the choppy-calm profile (12 % of bars), the 14-day unusual move after the 7-day scaled return does not rise with it. By quintile it reads +2.4 %, -9.9 %, -6.7 %, +5.8 %, +21.5 %, only about 14 cases each, with no |t| above 2.1. Over 3 days the same quintiles give -0.8 % to +0.8 % (t_day ≤ 1.0, about 43 cases each).
- **F3:** Outside the profile, the largest scaled weekly rises are followed by +1.4 % over 3 days (t 2.93, 437 cases, not day-clustered) but by -2.3 % over 14 days (t -0.99). Only the fourth quintile shows +6.9 % over 14 days (t 2.58), so the effect is not graded. In the rising profile the top quintile's 3-day +2.6 % has a day-clustered t of only 1.60 (46 days). That continuation in rising markets is already held (034-01.e1, 033-03.b2).
- **F4:** Across all coins, the next day rebounds after the most scaled one-day fall (bottom z1 quintile +0.69 %, t 4.80, 1,637 cases, 11 of 12 windows positive) and after a close near the low (bottom close-location quintile +0.49 %, t 3.82, 9 of 12 windows). These t's are not day-clustered. By profile, with day clustering, neither clears 2: falling +0.74 % (t_day 1.38) and +0.97 % (t_day 1.71); choppy calm +0.42 % (t_day 0.65) and -0.25 % (t_day -0.43). This is the low-close and fall rebound family that the map already holds 13 times in falling agitated and 5 times in choppy agitated.
- **F5:** Weekday next-day unusual moves are negative on Wednesday (-0.44 %, t -2.60) and positive on Thursday (+0.32 %, t 2.25) and Friday (+0.37 %, t 2.85). These are 7 groups of about 1,410 coin-days with t's not clustered by day, and they repeat the held "late week gain" idea (045-01).
- **F6:** In the choppy-agitated profile (130 bars) every bucket of every signal is negative. The next-day mean runs from -1.4 % to -3.8 % across the z1 quintiles, with about 25 cases per bucket. This is the profile's own fall, not a graded pattern.

## Ideas
- No ideas: Across the forecast, the profiles, the scaled one-day and weekly moves, the close location, the weekday and the windows, the only patterns that stand out are the next-day rebounds and late-week gains the map already holds. Nothing new stands out from chance in the choppy-calm profile (F2, F4), and the choppy-agitated signal is the profile's drift on 130 bars (F6).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
