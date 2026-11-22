---
line: 7.b inconclusive
backtest: 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade_1h
idea tested: 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3513 USD
---
## Findings
- **F1:** The idea's grading by volume runs the opposite way to the idea. Among the long cases on the 6-hour grid, the thinnest volume quintile (mean volume ratio 0.24) is followed by a 3-hour unusual move of −0.9 bp (t −0.50, 3,419 cases), while the heaviest (ratio 3.28) is followed by +9.6 bp (t 2.79, 3,419 cases). On the 3-hour grid the volume ratio correlates positively with the 3-hour unusual move (r 0.028, t 4.2, 23,205 cases). This is why the thin-minus-heavy check failed (−0.022 %) although the main mean had t 2.09.
- **F2:** The recovery is carried by the depth of the fall. On the 3-hour grid, the deepest fall quintile is followed by +11.9 bp over 3 hours (t 3.83) and +14.5 bp over 6 hours (t 3.56, 4,647 cases). The middle and shallow quintiles give between −1.7 and +3.5 bp. Depth correlates with the 3-hour unusual move (r 0.034, t 5.2, 23,205 cases).
- **F3:** Inside the deepest fall quintile, the heavier-volume half carries the effect: +13.8 bp over 3 hours (t 4.10, 4,190 cases), against −5.3 bp for the thinner half (t −0.75, 457 cases). Sharp falls on thin volume are rare and show no recovery.
- **F4:** The move peaks near 3 hours rather than the plan's 6 hours. Over all cases it is +4.05 bp at 3 hours (t 3.52) and +3.96 bp at 6 hours (t 2.48), then fades to +1.6 bp at 24 hours (t 0.51).
- **F5:** In the two deepest fall quintiles the 3-hour recovery holds on both coins: BTC +9.3 bp (t 3.86, 4,473 cases) and ETH +9.0 bp (t 2.97, 4,820 cases). It is positive in 6 of 8 years, strongest in 2020 (+21.5 bp, t 3.84) and 2024 (+15.9 bp, t 4.24), and negative in 2022 (−3.7 bp) and 2025 (−1.4 bp).
- **F6:** Size against cost: the deepest-fall cases move +14.5 bp unusual over 6 hours, about 0.17 % in total with the drift. This is above the 0.11 % cost of a trade, while the tested idea's cases moved 0.06 % in total, 0.6 times the cost.

## Ideas
- `028-04_low-volume-down-fade.d2_thinner-volume-larger-fade.b1_deep-hourly-falls-rebound` (from F2, F4, F5, F6): After an hour in which the coin falls far more than its typical hourly move over the past 30 days, the price recovers part of that fall over the next three hours; the deeper that hour's fall in typical hourly moves, the larger the recovery.
- `028-04_low-volume-down-fade.d2_thinner-volume-larger-fade.b2_heavy-volume-falls-rebound-harder` (from F1, F3, F4): After an hour in which the coin falls far more than its typical hourly move over the past 30 days, the price recovers part of that fall over the next three hours; the further that hour's volume lies above its 30-day hourly average, the larger the recovery.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
