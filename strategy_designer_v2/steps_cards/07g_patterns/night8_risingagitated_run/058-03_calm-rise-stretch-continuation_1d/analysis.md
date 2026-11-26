---
line: 7.g patterns
backtest: 058-03_calm-rise-stretch-continuation_1d
idea tested: 058-03_calm-rise-stretch-continuation
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 3
cost: 0.6073 USD
---
## Findings
- **F1:** In agitated markets the place of the close inside the day's range predicts the next day against itself. With the profile read as a 30-day trend and a 10-day swing above the coin's median, the day-clustered slope of the next-day return beyond drift on (close position − 0.5) is −0.0258 (t −2.75, 1,392 cases, 537 days) in choppy agitated, −0.0286 (t −2.61, 1,226 cases, 383 days) in falling agitated and −0.0156 (t −1.97, 1,206 cases, 510 days) in rising agitated. The three calm profiles sit between −0.006 and +0.003 (t −1.06 to +0.40).
- **F2:** Read with the workflow's own profile elements (60-day trend, 30-day swing above the coin's median), the same next-day slope holds in falling agitated (−0.0274, t −2.43, 1,165 cases, 338 days) and choppy agitated (−0.0345, t −2.05, 167 cases, 126 days). It vanishes in rising agitated (+0.005, t 0.53) and in all calm profiles (|t| ≤ 0.75), so it is a falling or choppy agitated effect.
- **F3:** Over two days in choppy agitated, the slope is negative in all six coins (t −0.37 to −2.05) and in 3 of 4 years (2019 t −2.34, 2020 t −2.31, 2021 t −0.99, 2018 t −0.01). Closes in the top fifth of the range are followed by a two-day move beyond drift with t −2.83. Weighting the close position by the day's range keeps the slope at t −2.06 (714 cases, 288 days).
- **F4:** The tested rising-calm stretch is mostly a level effect, not a graded one. Rising-calm grid bars gain +2.83 % beyond drift over 5 days (t 2.54, 221 cases, 79 days), but the slope on the distance is only t 1.43 (h5) and t 1.40 (h10). The rising-agitated slope is negative at both horizons (t −0.95, −1.29), which leans the brief's way without reaching significance.
- **F5:** Next-day returns after the coin's own lowest decile of daily returns are +0.97 % beyond drift (t 2.22, 831 cases, 271 days). This is a fall rebound that the profile map already holds many times in the agitated profiles, so it is not a discovery.
- **F6:** The book's gain rests on a few days. Its top 2 % of days (mean +5.0 %) sum to 154 % of its total gain, and its bottom 2 % (mean −3.4 %) to −105 %. Trades win only 46 % of the time, with a mean net of +4.04 % (613 trades, median 6 days).
- **F7:** The other angles did not stand out against the number of looks taken: weekday (largest |t| 1.52), recent-volatility ratio (|t| ≤ 1.31), 3-day return quintiles (|t| ≤ 1.82), and the distance slope in falling calm (t 2.84 at 1 day on 176 cases, but t 0.75 with the 60-day profile).

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `058-03.g1_falling-agitated-high-close-fade` (from F1, F2, F3): In a falling, agitated market, the nearer a coin's daily close stands to the top of that day's high-low range, the more the coin falls over the next day.
- `058-03.g2_choppy-agitated-strong-close-fade` (from F1, F2, F3): In a choppy, agitated market, the nearer a coin's daily close stands to the top of that day's high-low range, the more the coin falls over the next two days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
