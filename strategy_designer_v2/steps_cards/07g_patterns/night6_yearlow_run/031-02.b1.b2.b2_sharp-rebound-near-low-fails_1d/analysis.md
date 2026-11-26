---
line: 7.g patterns
backtest: 031-02.b1.b2.b2_sharp-rebound-near-low-fails_1d
idea tested: 031-02.b1.b2.b2_sharp-rebound-near-low-fails
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4325 USD
---
## Findings
- **F1:** Inside the regime (close nearer its 365-day closing low than usual), coins did no worse than outside it. On the 20-day grid the mean unusual move was -0.39 % (t -0.18, 872 cases, day-clustered) against +0.50 % outside it (t 0.25, 684 cases). On the 5-day grid it was -0.32 % (t -0.69, 3578 cases) against +0.40 % (t 0.79, 2838 cases). Being near the yearly low carries no measurable drift in either direction.
- **F2:** Among about 36 slope tests across two horizons, no past-return grading inside the regime stands out from chance. At the 20-day horizon the best were the 40-day return (slope -0.035, t -2.29, 573 cases on 89 days) and the 1-day return (slope -1.20, t -2.26, 713 cases on 114 days). At the 5-day horizon the same gradings fall to t -1.41 and t -1.05.
- **F3:** The time spent in the regime looked graded but is not reliable. By quartile of consecutive regime days, the 20-day unusual move went from +1.40 % (median 1 day) to -3.40 % (median 81 days). The slope is t -1.26 (872 cases, 137 days). The pattern reverses in 2023, when late was +9.8 % and early +3.0 %.
- **F4:** The raw weekday effect does not hold up. Raw per-coin daily deviations gave weekday t values from -2.90 to +3.79 over about 4650 coin-days each. Taken one value per day, the largest falls to t 1.92 (Saturday, +0.30 %, 414 days), and the sign changes from year to year.
- **F5:** The book's small gain rests on a handful of days and the typical trade loses. Over 2898 days the daily returns sum to +1.00, while the 10 best days alone sum to +2.45. The 1400 shorts have a median net result of -1.6 %. Their mean of -19.7 % is driven by one trade at -5837 %. No entry-forecast quartile has a positive median (-0.28 % to -2.65 %).

## Ideas
- No ideas: Across the regime, past returns at 1 to 60 days, volatility, time in the regime, time since the low, weekday, year and the trades, nothing passed day-clustered t-statistics given how many angles were examined (F1–F5), so no finding supports an idea.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
