---
line: 7.g patterns
backtest: 061-01.d2_rising-calm-up-day-continuation_1d
idea tested: 061-01.d2_rising-calm-up-day-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4509 USD
---
## Findings
- **F1:** In the rising calm profile (the book's own regime, folds B and C), the larger a down day against the coin's 30-day swing, the lower the coin's excess return over the next 5 days. On the 5-bar grid, the slope of the excess 5-day return on the scaled day's move is +0.041 per usual move among down days (t 2.77 with one day's cases together, 137 cases). It is +0.021 among up days (t 1.06, 147 cases). By bin, down days of 1 to 2 usual moves are followed by −3.2 % excess (t −2.30, 34 cases) and those beyond 2 usual moves by −7.8 % (3 cases).
- **F2:** The rising-calm down-day continuation holds every year with enough cases. The slope is +0.032 in 2019 (28 cases), +0.030 in 2020 (64) and +0.031 in 2021 (38). The same slope appears with the profile rebuilt from prices: rising and calm, down days, +0.051 (t 2.86, 82 cases). It points the same way over 10 days (+0.081, t 1.82, 37 cases).
- **F3:** The rising-calm down-day continuation follows a one-day bounce. Over the next single day, the slope on down days is −0.010 (t −2.63, 634 bars), so the larger the down day, the higher the next day. The fall shows over the 5 days, not the first one.
- **F4:** In a choppy calm market (60-day return between −10 % and +10 %, swing at or below the coin's median), larger up days are followed by larger 5-day excess returns: slope +0.052 per usual move (t 2.98, 50 cases).
- **F5:** The tested idea's effect, larger up days in rising calm, is not clear in folds B and C. The slope is +0.021 (t 1.06, 147 cases) over 5 days and −0.001 (t −0.36, 811 bars) over 1 day. Its 5-day size per case, +1.59 % total and +0.96 % unusual, is still 8.3 and 5.0 times the 0.19 % cost of a trade.
- **F6:** Outside calm profiles, large days show no graded follow-through over 5 days. The slopes are −0.012 (t −0.26, 63 cases) for up days in rising agitated and −0.025 (t −1.48, 79 cases) in falling agitated. Across all non-rising-calm bars, the up-day slope is +0.010 (t 1.01, 463 cases) and the down-day slope −0.008 (t −0.65, 615 cases).
- **F7:** The book's gain rests on a few days. Its 20 best days sum to 1.48 against a total of 1.13 over 1,449 days, and its 20 worst days sum to −0.97. In 2021 it earned 0.015 % a day while holding the coins earned 0.41 % a day.
- **F8:** Other angles looked at gave nothing new to propose:

## Ideas
- `061-01.d2.g1_rising-calm-down-day-continuation` (from F1, F2, F3, F6): In a rising, calm market, the larger a coin's one-day fall against the standard deviation of its daily returns over the past 30 days, the larger its fall over the next 5 days.
- `061-01.d2.g2_choppy-calm-up-day-continuation` (from F4, F6): In a choppy, calm market, the larger a coin's one-day rise against the standard deviation of its daily returns over the past 30 days, the larger its rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
