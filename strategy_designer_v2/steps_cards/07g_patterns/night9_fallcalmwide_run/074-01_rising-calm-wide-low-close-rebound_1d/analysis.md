---
line: 7.g patterns
backtest: 074-01_rising-calm-wide-low-close-rebound_1d
idea tested: 074-01_rising-calm-wide-low-close-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4207 USD
---
## Findings
- **F1:** In the rising calm profile, wide days (range at least 2 swings) that close in the lower third rise more over the next three days than over one. On the non-overlapping grid of folds B and C, the excess return is +2.05 % over 1 day (t 3.31, 113 cases, 62 days), +2.79 % over 2 days (t 2.43, 63 cases, 35 days) and +3.53 % over 3 days (t 2.80, 46 cases, 23 days, strength 0.38 of a usual 3-day move). Over 5 days it turns to −3.05 % (t −1.29, only 13 days). Every bar's 3-day return gives +3.75 % (t 4.65, 62 days), against +2.20 % for wide high-close days.
- **F2:** Inside the rising calm profile, the grading by the tested score (range in swings times nearness to the low) is weak and not monotonic. Its correlation with the excess return is 0.107 over 1 day and −0.024 over 3 days. The score's 3-day quintiles go +0.97 %, +0.04 %, −0.87 %, +1.45 %, +3.45 % (top quintile t 2.68, 56 days). Only the top fifth stands out.
- **F3:** The rebound is concentrated in one year. The 3-day grid cases give +6.03 % in 2021 (t 3.40, 9 days) against +1.18 % in 2019 (t 1.00, 6 days) and +0.45 % in 2020 (t 0.30, 7 days). No single coin has enough cases to stand alone: the most are ETH with 11 at +2.60 % and XMR with 8 at +2.53 %.
- **F4:** In the rising calm profile, a down day measured in the coin's own 30-day swings is followed by a rise that grows with the size of the fall. This holds whether or not the day is wide.
- **F5:** Outside the rising calm profile, very wide days (above 3 swings) that close near their high fall the next day, by −2.00 % (t −2.73, 126 cases, 79 days). On a falling 60-day trend, wide high-close days fall by −1.62 % (t −2.28, 58 days), while in a rising trend they gain +0.71 %. This is the fade family of brief 060, already held (060-01.g1.d2.d1, falling agitated short), so it is not a discovery.
- **F6:** Other angles showed nothing that stands out once the many angles are counted.

## Ideas
- `074-01.g1_rising-calm-low-close-three-days` (from F1, F2, F3): In a rising, calm market, a day whose high-to-low range is wide against the coin's 30-day swing of daily returns and that closes near its low is followed by a rise over the next three days. The wider the day against that swing, the larger the rise.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `074-01.g2_rising-calm-scaled-dip-rebound` (from F4, F1): In a rising, calm market, a day that falls against the coin's 30-day swing of daily returns is followed by a rise over the next three days. The larger the day's fall measured in those swings, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
