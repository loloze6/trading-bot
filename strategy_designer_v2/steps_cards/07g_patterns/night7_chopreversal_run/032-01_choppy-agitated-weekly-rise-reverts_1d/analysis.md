---
line: 7.g patterns
backtest: 032-01_choppy-agitated-weekly-rise-reverts_1d
idea tested: 032-01_choppy-agitated-weekly-rise-reverts
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3941 USD
---
## Findings
- **F1:** Over all regimes, the coin's 7-day move does not reverse over the next 7 days: on the non-overlapping 7-day grid, the correlation of the past 7-day return with the next 7-day return minus drift is 0.012 (t 0.40, 1101 cases). The tested profile itself shows nothing either: in-profile cases have r -0.018 (t -0.13, 60 cases). This matches the verdict's unusual move of -0.69 % (t -0.83). The total move of -1.67 % per case is 8.7 times a trade's 0.19 % cost, on the losing side.
- **F2:** The weekly reversal shows only when the coin's 60-day return is between -10 % and +10 % (choppy). There r = 0.34 (t 3.34, 89 cases), against -0.002 (t -0.04, 241 cases) in falling and 0.06 (t 0.92, 219 cases) in rising markets.
- **F3:** Inside the choppy cases, agitation adds nothing. Calm-choppy has r 0.26 (day-clustered t 1.85, 56 cases on 30 days) and agitated-choppy has r 0.28 (t 1.15, 33 cases on 24 days). The brief's own test, "stronger in agitated than in calm choppy", fails. The choppy reversal's day-clustered t stays under 2.
- **F4:** The choppy reversal has the same strength after rises and after falls: r 0.29 (t 1.96, 45 cases) after a rising week and 0.27 (t 1.85, 44 cases) after a falling week. Across windows it is mixed: 5 of the 9 windows with at least 4 cases are positive, with r from -0.39 to 0.92.
- **F5:** By the coin's 30-day swing, the weekly reversal lives in its calmest third: r 0.20 (t 3.40, 276 cases), against 0.07 (t 1.21) in the middle third and -0.03 (t -0.55) in the most agitated third. Windows are inconsistent here too: 6 of 11 are positive, with r from -0.59 to 0.54.
- **F6:** A coin's largest daily falls (bottom decile of the day's return over its 30-day swing) are followed by a next-day rise beyond drift. That rise is +0.92 % (day-clustered t 2.10, 675 cases on 217 days), and +0.39 % (t 1.37) for the next decile.
- **F7:** That rebound is positive in all 6 coins (+0.28 % to +0.96 %) and in 9 of 12 windows. It is graded only loosely: the size of the fall against the next day's move gives corr 0.09 (t 1.86, 3287 cases). It is largest when the 60-day trend is falling: +0.76 % (t 1.54, 453 cases), against +0.12 % in choppy markets.
- **F8:** A day that closes near its low is followed by a next-day rise beyond drift (+0.53 %, t 1.68, bottom fifth of the range). A day that closes near its high is followed by a next-day fall (-0.35 %, t -1.64). Among moderate-return days the step remains but is weaker (-0.48 %, t -1.61, at the top).
- **F9:** No weekday effect beyond drift stands out: every weekday's day-clustered t is between -1.17 and 1.12.

## Ideas
- `032-01.g1_choppy-market-weekly-reversal` (from F2, F3, F4): In a choppy market, the larger a coin's 7-day move, the larger its move the opposite way over the next 7 days, giving back part of that move, after rises and after falls alike.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `032-01.g2_large-daily-fall-rebounds` (from F6, F7, F8): The larger a coin's one-day fall relative to its usual daily swing over the past 30 days, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
