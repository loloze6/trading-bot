---
line: 7.g patterns
backtest: 032-02.g1.e1.e1.e2_breakout-margin-over-28-day-high_1d
idea tested: 032-02.g1.e1.e1.e2_breakout-margin-over-28-day-high
step 5: mismatch
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3786 USD
---
## Findings
- **F1:** The book never traded: the config gives the `trending` regime no strategy (null). Step 6 shows 0 % of days in a position, 0 trades per day and a Sharpe of 0, so the idea was never tested by this backtest.
- **F2:** Measured from the prices on folds B–C, fresh 28-day closing highs were followed by a mean 5-day return above the coin's normal drift of +4.5 % (t 2.48, 110 cases on 52 days), about 24 times the 0.19 % cost of a trade. The effect was positive in 2020 (+5.3 %, t 2.07) and 2021 (+7.6 %, t 2.07), and negative in 2018 on only 5 cases (−4.9 %).
- **F3:** Among those breakouts, a larger margin over the prior high was not followed by a larger rise: the slope of the 5-day excess return on the margin was −0.11 usual moves per standard deviation (t −0.77, 110 cases, 52 days). The graded part of the tested idea is not seen.
- **F4:** Where the close sits within its prior 28-day closing range grades the next 5 days across all bars (slope 0.12 usual moves per standard deviation, t 2.25, 1278 cases on 230 days). The 5-day excess return was −1.9 % in the 0.1–0.3 band (t −1.81), −1.9 % in the 0.3–0.5 band (t −1.93), +2.0 % in 0.5–0.7 (t 1.83), +1.5 % in 0.9–1.0 and +4.5 % above the range (t 2.48).
- **F5:** Measured as distance below the prior 28-day high, closes 15–25 % below it were followed by a 5-day excess return of −2.7 % (t −2.96, 255 cases, 116 days). Closes within 3 % of it were followed by +2.2 % (t 2.09, 130 cases, 76 days).
- **F6:** The brief's calm-decline effect does not show. In calm declines (20-day range and volatility below their 90-day levels, negative 28-day return), the slope of the 5-day excess return on the 28-day return was −0.19 (t −1.12, 89 cases, 31 days). Its sign means larger falls were followed by smaller further falls, the opposite of the brief, and it cannot be told from 0.
- **F7:** Patterns that did not hold up once cases on the same day were counted together, so they are not findings:

## Ideas
- `032-02.g1.e1.e1.e2.g1_position-in-28-day-range` (from F4, F5, F2, F3): The higher a coin's close sits within the range of its closes over the previous 28 days (from its lowest to its highest close, and beyond the highest), the larger its rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
