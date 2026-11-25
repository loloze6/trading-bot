---
line: 7.g patterns
backtest: 058-02.b1.b2.b1_choppy-range-position-more-coins_1d
idea tested: 058-02.b1.b2.b1_choppy-range-position-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4220 USD
---
## Findings
- **F1:** Within the tested choppy profile, the range-position effect lives only in the calm half. On the five possible 5-day grids, the slope of the excess 5-day return on the 20-day range position averages +7.98 % per unit with t 2.35 (min 1.29, max 3.19; about 142 cases per grid) in choppy calm markets, against −0.68 % with t −0.32 (about 40 cases) in choppy agitated ones. This is the opposite of the brief's reversion and explains why the pooled choppy test got only t 0.79.
- **F2:** In choppy calm markets the effect is graded and shows in medians as well as means. From the bottom to the top fifth of range position (−1 to +1), the median excess 5-day return goes −7.73 %, −1.35 %, −1.45 %, +1.98 %, +1.54 %, and the share of positive outcomes goes 11 %, 33 %, 41 %, 61 %, 59 % (18, 33, 39, 28 and 34 cases). By year the slope is positive in each year measured (t 0.65 in 2019, 0.30 in 2020, 2.45 in 2021), so most of its strength comes from 2021.
- **F3:** The same continuation is as strong in falling calm markets. The slope averages +6.38 % with t 2.58 over the five grids (min 1.54, about 210 cases), and it is positive in every year (t 2.59, 1.15, 2.77, 1.11 for 2018 to 2021). Closes near the 20-day low were followed by −4.88 % excess (t −2.54, 64 cases), closes near the high by +4.98 % (t 3.24, 16 cases).
- **F4:** Agitated markets show no range-position effect in any trend. The mean grid t is 0.11 falling, −0.32 choppy and 0.67 rising, against 2.4 to 2.6 in all three calm trends (rising calm +5.79 %, t 2.40). So calm, not chop, is the condition, and the effect overlaps the held strategy 035-01.b1 (calm market nearness to high).
- **F5:** The book's short legs near the range low lost on the bars where the idea is weakest. Short positions held with range position below −0.6 earned −0.055 % a day (493 coin-days). Long positions above +0.6 earned +0.455 % a day (409 coin-days).
- **F6:** Other angles did not stand out enough to count. A next day after a fall of more than 2 usual daily moves gave +1.69 % (t 1.96, 245 cases), a re-finding of the held agitated-fall rebounds. Neither weekday (|t| ≤ 1.48) nor prior 5-day return fifths (|t| ≤ 1.81) showed anything.

## Ideas
- `058-02.b1.b2.b1.g1_choppy-calm-range-position-continuation` (from F1, F2, F4, F5): In a choppy, calm market, the higher a coin's close sits within its 20-day high-low range, the larger its rise over the next 5 days.
- `058-02.b1.b2.b1.g2_falling-calm-range-low-continuation` (from F3, F4): In a falling, calm market, the lower a coin's close sits within its 20-day high-low range, the larger its fall over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
