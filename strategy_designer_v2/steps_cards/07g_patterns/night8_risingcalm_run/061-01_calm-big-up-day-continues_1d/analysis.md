---
line: 7.g patterns
backtest: 061-01_calm-big-up-day-continues_1d
idea tested: 061-01_calm-big-up-day-continues
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3704 USD
---
## Findings
- **F1:** In calm markets the 5-day return scaled by the 30-day daily swing predicts the next 5 days' excess return about as well as the single day does: day-clustered slope t is 2.83 for the 5-day return, 2.97 for the 3-day, 3.10 for the 10-day, 2.81 for the 20-day and 2.52 for the 1-day (718 cases, 178 days); in agitated markets every one is flat (t from -0.02 to 0.86, 508 cases, 153 days).
- **F2:** In calm markets, when the 1-day, 5-day and 20-day scaled returns are put in one regression, none keeps a t above 2 (z1 t 1.24, z5 t 1.41, z20 t 1.18; 718 cases). The single large day carries no effect of its own beyond the coin's recent scaled run.
- **F3:** In calm markets the scaled prior 5-day return sorts the next 5 days at both ends. The lowest quintile has a mean excess return of -3.20 % (t -3.90, 130 cases) and the highest +2.90 % (t 2.89, 154 cases). In agitated markets the same quintiles give -0.52 % and +1.22 % (t -0.36 and 0.97).
- **F4:** Inside calm markets the scaled 5-day slope is strongest in a choppy 60-day trend (slope 0.048, t 3.09, 101 cases, 55 days). It is weaker in a falling trend (t 2.21, 219 cases) and in a rising trend (t 1.47, 178 cases).
- **F5:** In calm markets the follow-through grows with the size of the 5-day run on both sides, measured as mean directional excess return by |z5| tercile:
- **F6:** The book's gain comes from its longs. Long bars sum to +6.63 (mean +0.27 % per bar, 2466 bars) and short bars to -0.96 (mean -0.04 %, 2459 bars). The 1259 short trades average -2.53 % net against +4.41 % for the 906 long trades.
- **F7:** Coins rise on Fridays (+0.53 % a day, t 3.66, 1187 days) and Saturdays (+0.57 %, t 4.09, 1185 days). This repeats the late-week gain the map already holds (045-01, rising), so no idea is written from it.

## Ideas
- `061-01.g1_choppy-calm-day-follow-through` (from F1, F4): In a choppy, calm market, the larger a coin's one-day move against the standard deviation of its daily returns over the past 30 days, the further it keeps moving in that day's direction over the next 5 days.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `061-01.g2_calm-market-scaled-run-continues` (from F1, F2, F3, F5): In a calm market, the larger a coin's 5-day return against the standard deviation of its daily returns over the past 30 days, the larger its move in the same direction over the next 5 days, both after rises and after falls.
- `061-01.g3_choppy-calm-fall-continues` (from F3, F4, F5, F6): In a choppy, calm market, the larger a coin's 5-day fall against the standard deviation of its daily returns over the past 30 days, the larger its further fall over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
