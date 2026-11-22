---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade
line: 7.b inconclusive
backtest: 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin falls far more than its typical hourly move over the past 30 days, the price recovers part of that fall over the next three hours; the deeper that hour's fall in typical hourly moves, the larger the recovery.
Consequence: A trader can expect the sharpest hourly falls on BTC and ETH to be partly given back within three hours, and only the deepest falls give back enough to cover the cost of a trade.
Why:
- F2: The recovery is carried by the depth of the fall. On the 3-hour grid, the deepest fall quintile is followed by +11.9 bp over 3 hours (t 3.83) and +14.5 bp over 6 hours (t 3.56, 4,647 cases). The middle and shallow quintiles give between −1.7 and +3.5 bp. Depth correlates with the 3-hour unusual move (r 0.034, t 5.2, 23,205 cases).
- F4: The move peaks near 3 hours rather than the plan's 6 hours. Over all cases it is +4.05 bp at 3 hours (t 3.52) and +3.96 bp at 6 hours (t 2.48), then fades to +1.6 bp at 24 hours (t 0.51).
- F5: In the two deepest fall quintiles the 3-hour recovery holds on both coins: BTC +9.3 bp (t 3.86, 4,473 cases) and ETH +9.0 bp (t 2.97, 4,820 cases). It is positive in 6 of 8 years, strongest in 2020 (+21.5 bp, t 3.84) and 2024 (+15.9 bp, t 4.24), and negative in 2022 (−3.7 bp) and 2025 (−1.4 bp).
- F6: Size against cost: the deepest-fall cases move +14.5 bp unusual over 6 hours, about 0.17 % in total with the drift. This is above the 0.11 % cost of a trade, while the tested idea's cases moved 0.06 % in total, 0.6 times the cost.
