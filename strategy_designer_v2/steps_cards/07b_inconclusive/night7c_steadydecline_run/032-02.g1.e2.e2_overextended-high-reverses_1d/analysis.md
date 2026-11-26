---
line: 7.b inconclusive
backtest: 032-02.g1.e2.e2_overextended-high-reverses_1d
idea tested: 032-02.g1.e2.e2_overextended-high-reverses
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3628 USD
---
## Findings
- **F1:** The test's main measure, the slope t of -1.27 over 323 cases, points the way the idea predicts but falls short of the bar, and the supporting check fails: across all of a coin's 28-day closing highs the next 5 days run above drift (step 5: -1.67 % in the short direction, t -3.05 on 491 days; folds B and C: +3.80 %, t 2.82, 147 cases), so on average the coin keeps rising rather than falling.
- **F2:** The run-up predicts a larger fall clearly when measured as the raw scaled 28-day rise (rise over mean absolute 28-day return), and more clearly at longer horizons: slope t -2.73 over 5 days, -2.75 over 10 days and -3.28 over 20 days (133–147 cases); the plan's pipeline strength gives a weaker t of -1.89 because its standardise-and-clip caps 37 % of cases at the maximum of 20.
- **F3:** The effect sits only in the largest run-ups. Above the median scaled rise the 5-day slope has t -2.72 (73 cases), while below it the slope is flat (t -0.02, 74 cases).
- **F4:** The excess move changes sign with run-up size. Run-ups of up to 1 usual move are followed by +6.2 % over 5 days (t 2.71, 61 cases) and +14.0 % over 20 days (t 3.02); run-ups of 1 to 2 usual moves by +8.3 % (t 2.77, 34 cases); run-ups of 2.5–3 and of more than 3 usual moves by -4.8 % (t -1.66, 15 cases) and -2.1 % (t -0.70, 16 cases).
- **F5:** The top quartile of run-ups (mean scaled rise 3.18) falls -3.7 % beyond drift over 5 days (t -1.93, 37 cases), strongest in LTC (-9.1 %, t -3.47) and ZEC (-11.0 %, t -2.57), and negative in 2019 (t -2.57) and 2021 (t -1.74) but not in 2020 (+2.4 %, t 0.87). It is real in part of the data, but thin.

## Ideas
- `032-02.g1.e2.e2.b1_extreme-run-up-high-reverses` (from F1, F2, F3, F4, F5): In a coin that closes at its 28-day highest close, the larger its 28-day rise against its own usual 28-day move, the larger its fall over the next 5 days, only while that rise is at least twice its usual 28-day move.
- `032-02.g1.e2.e2.b2_modest-run-up-high-continues` (from F1, F4): In a coin that closes at its 28-day highest close, the smaller its 28-day rise against its own usual 28-day move, the larger its rise over the next 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
