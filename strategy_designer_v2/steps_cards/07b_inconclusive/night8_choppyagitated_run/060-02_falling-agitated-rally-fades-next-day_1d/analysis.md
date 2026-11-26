---
line: 7.b inconclusive
backtest: 060-02_falling-agitated-rally-fades-next-day_1d
idea tested: 060-02_falling-agitated-rally-fades-next-day
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4025 USD
---
## Findings
- **F1:** The giveback is real on average but does not grow with the size of the rise. Inside the profile, up days are followed by a next-day excess fall of +0.91 % (t 2.33, 728 cases on 281 days in folds B and C; step 5 found +0.52 %, t 2.35, on all folds). The slope on the scaled rise is flat in this sample, -0.0024 (t -0.33, 590 cases), as it is in step 5's verdict (t 0.40).
- **F2:** The largest rises are what break the grading. By quintile of the scaled rise, the next-day giveback is +0.82 %, +1.09 %, +0.92 % and +1.82 % (t 2.91) for the first four, then only +0.28 % (t 0.33) for the top quintile (mean 1.53 swings). By |forecast| quintile it is the same: the top quintile gives -0.20 % (t -0.25).
- **F3:** A longer horizon does not rescue the effect. The mean short gain is +0.61 % over 2 days (t 1.13), +0.59 % over 3 days (t 1.04) and +0.60 % over 5 days (t 0.81), against +0.91 % (t 2.33) over 1 day. The 3-day slope on the scaled rise is 0.0002 (t 0.02). So the effect is a one-day move, not a giveback that builds over the brief's one to three days.
- **F4:** A graded effect appears only once the largest rises are left out, and only weakly. Without the top quintile, the 3-day slope reaches t 2.03 (463 cases), while the next-day slope is still t 1.19. Keeping that part would need a ceiling on the rise, which is a threshold; on the full set of cases the slopes stay near 0.
- **F5:** No other cut makes the giveback grade. The slope t is 0.37 against the 60-day trend, 0.37 against the prior 10-day return, 0.41 against the upper-wick share and 1.31 against the range in swings. Splitting the top quintile by wick or by prior 10-day return leaves all halves under t 1.1 (59 cases each).
- **F6:** The effect is spread thinly rather than living in one part of the data. The next-day mean is positive in 9 of 10 coins, but only BTC (t 2.51) and ZEC (t 2.03) reach t 2. It is positive in all four years 2018–2021, with only 2019 reaching t 2 (t 2.03) and 2020 at t 0.65. The test already used every coin and fold available, so there is no further data to add.

## Ideas
- No ideas: The theme's effect is not in the data. Up days in a falling agitated market are given back only as a flat average over one day, and the giveback does not grow with the size of the rise, which the brief itself names as the test of its theory (the largest rises fade least, F2, and no other measure grades it, F5). No horizon (F3), part of the data (F6) or condition without a threshold (F4) turns it into a graded effect.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
