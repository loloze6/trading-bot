---
line: 7.g patterns
backtest: 031-03.g1.b1.d2.e2.g1.g2_fade-during-volatility-bursts_1d
idea tested: 031-03.g1.b1.d2.e2.g1.g2_fade-during-volatility-bursts
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4971 USD
---
## Findings
- **F1:** XMR's next-day reversal comes almost entirely after down days. After days with z < -1 (the one-day return over the 30-day daily volatility), the next day beat the coin's mean daily return by +1.10 % (t 3.91, 304 cases). After days with z > 1, the fade earned +0.36 % (t 1.45, 333 cases). Regressing the next-day return on z gives a slope t of -3.37 on down days (1133 cases) against -0.94 on up days (1282 cases).
- **F2:** The level of the 30-day volatility scales the reversal more than the 5-day-to-30-day ratio the idea uses. In one joint regression of the next-day return, z × standardised 30-day volatility has t -5.04 and z × the 5-day/30-day ratio has t -2.60, while z alone has t -0.41.
- **F3:** The fade gain after |z| > 1 days rises across the 30-day volatility terciles: +0.05 % (t 0.21, 225 cases), +0.86 % (t 3.07, 231), +1.34 % (t 2.85, 181). On down days, the slope of the next-day return on z steepens in the same order: -0.0034 (t -1.45), -0.0065 (t -2.18), -0.0116 (t -2.44), about 377 cases each.
- **F4:** The rebound after down days is graded by the size of the fall. The next day's excess return is +0.03 % after z in (-0.5, 0] (509 cases) and +0.22 % after (-1, -0.5] (320). It is +1.14 % after (-1.5, -1] (t 2.96, 147), +0.97 % after (-2.5, -1.5] (t 2.38, 123) and +1.36 % after z ≤ -2.5 (34 cases). The matching up-day bins stay between -0.23 % and -0.36 % until z > 2.5 (-1.21 %, t -1.32, 33 cases).
- **F5:** The reversal lasts about three days and then fades. On non-overlapping grids, the slope of the forward return on z has t -4.91 at 1 day (2417 cases), -2.25 at 2 days (1202) and -2.46 at 3 days (786), then turns to +1.39 at 5 days (474). Down days alone keep t -1.97 at 2 days and -2.01 at 3 days.
- **F6:** The brief's own two-to-three-month situation shows no lean in this data. The 60-day return predicts the forward return with t -0.22 at 1 day (1457 cases), +0.13 at 2 days and +0.35 at 5 days. The 20-day return is not significant at any horizon tested (t between -0.94 and -0.36).
- **F7:** The book's gain is concentrated and uneven over time. Its top 5 % of bars carry 180 % of the summed bar gains. Its best 2 % of bars follow a mean z of -0.55 with a mean position of +0.10, which makes them rebounds after falls. The down-day rebound after z < -1 was absent in 2019 (+0.07 %, t 0.08) and 2025 (-0.07 %, t -0.12) and strong in 2020 (+2.26 %, t 3.38) and 2023 (+0.77 %, t 3.16). Weekday effects (book on Sundays +0.40 %, t 2.96) do not stand out from the many angles examined.

## Ideas
- `031-03.g1.b1.d2.e2.g1.g2.g1_xmr-rebound-after-volatile-falls` (from F1, F3, F4, F5, F7): The larger XMR's one-day fall measured against its 30-day daily volatility, the more it rises back over the next one to three days. This rebound is larger the higher its 30-day daily volatility stands.
- `031-03.g1.b1.d2.e2.g1.g2.g2_fade-scaled-by-monthly-volatility` (from F2, F3, F5): The larger XMR's one-day move against its 30-day daily volatility, the more it moves back the other way over the next one to three days. This reversal grows with the level of its 30-day daily volatility.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
