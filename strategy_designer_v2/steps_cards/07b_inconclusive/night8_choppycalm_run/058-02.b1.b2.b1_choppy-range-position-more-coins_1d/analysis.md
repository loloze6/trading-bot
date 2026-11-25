---
line: 7.b inconclusive
backtest: 058-02.b1.b2.b1_choppy-range-position-more-coins_1d
idea tested: 058-02.b1.b2.b1_choppy-range-position-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4060 USD
---
## Findings
- **F1:** Step 5's slope of the excess 5-day return on the forecast is on the predicted side but well short of the bar (t 0.79 clustered by day, 1640 cases on 429 days), and the idea is small: an unusual move of +0.40 % per case (t 1.20 over 1194 days), only 0.019 of a usual 12.35 % move, against a 0.22 % trade cost. The test already used every coin and fold on daily bars, so more data would not rescue it.
- **F2:** The effect lives in calm markets only. On the non-overlapping 5-day grid of folds B and C, the slope of the winsorised excess return on the raw range position was +0.033 (t 2.42, 518 cases, 132 days) in choppy calm markets and +0.001 (t 0.07, 487 cases) in choppy agitated ones. Agitation here was read against each coin's own median 30-day swing, an approximation of the profile's past-year median.
- **F3:** The same split holds over 10 days: choppy calm gave a slope of +0.059 (t 2.38, 253 cases, 66 days) against −0.004 (t −0.11, 251 cases) for choppy agitated. So the test, which pooled calm and agitated choppy bars, diluted a calm-only effect with a null one.
- **F4:** Calm markets of every trend show the same graded continuation, and agitated ones do not. At 5 days, rising calm gave t 3.37 (263 cases) and falling calm t 3.21 (232 cases), while rising agitated gave t 0.57 and falling agitated t −0.28. At 10 days rising calm gave t 6.18 (133 cases).
- **F5:** Inside the tested choppy book the pooled result is fragile. The top quintile of range position holds one case of +385 %, and winsorising at 1 %/99 % cuts the 5-day t from 1.83 to 1.68. Taking the return net of the day's mean across coins leaves t 1.12. The yearly slopes run from −0.97 (2018) to +1.09 (2020), which is the mixing of calm and agitated bars that F2 separates.
- **F6:** Across horizons, the choppy-book slope peaks at 5 to 10 days (t 1.67 and 1.42 on the forecast) and vanishes at 1 day (t 0.32) and at 20 days (t −0.19). The plan's 5-day horizon is the right one; the problem is the profile, not the horizon.

## Ideas
- `058-02.b1.b2.b1.b1_choppy-calm-range-position` (from F1, F2, F3, F5): In a choppy, calm market, the higher a coin's close sits within its 20-day high-low range, the larger its rise over the next 5 days.
- `058-02.b1.b2.b1.b2_calm-market-range-position` (from F2, F4, F6): In a calm market, the higher a coin's close sits within its 20-day high-low range, the larger its rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
