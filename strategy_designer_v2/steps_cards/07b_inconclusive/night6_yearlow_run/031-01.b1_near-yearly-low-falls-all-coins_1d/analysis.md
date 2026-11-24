---
line: 7.b inconclusive
backtest: 031-01.b1_near-yearly-low-falls-all-coins_1d
idea tested: 031-01.b1_near-yearly-low-falls-all-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3720 USD
---
## Findings
- **F1:** The tested slope sits on the side the idea predicts, but it is small at every horizon on the same non-overlapping grid. At 5 days it is 0.00035 (t 0.90, 6,157 cases), at 10 days 0.00102 (t 1.42, 3,049), at 20 days 0.00158 (t 1.07, 1,495) and at 40 days 0.00180 (t 0.50, 718), so no other horizon brings it near t 2. The test already used every coin and every fold available (last year in the record: 2025), so no more data exists to run it on.
- **F2:** Nearness to the low does not grade the 20-day excess return. By raw proximity quintile the mean excess runs -0.93 %, -1.10 %, +2.49 %, +0.05 %, -0.51 % (299 cases each, all |t| < 1.3), and the slope on raw proximity is -0.019 (t -0.30) at 20 days and -0.105 (t -1.45) at 40 days, opposite in sign to the forecast's slope.
- **F3:** Only the deepest forecasts point the idea's way, and the next bin up points the other way. The -20 to -15 bin averages -3.46 % excess over 20 days (t -1.54, 336 cases on 99 days) and -1.83 % over 10 days (t -1.65), while the -15 to -10 bin averages +2.71 % (t 0.85) and +1.77 % (t 1.42). The steps are mixed, not graded.
- **F4:** Closes truly at the yearly low show bounces as often as falls. Within 1 % of the 365-day low, the 10-day excess is +3.18 % (t 1.00, 55 cases) and the 20-day excess is -1.47 % (t -0.26, 37 cases). Within 3 % of the low after a falling 20 days, the 20-day excess is -2.97 % (t -0.64, 49 cases).
- **F5:** The deep-forecast cases (forecast ≤ -10) swing with the year. The mean 20-day excess is -10.7 % in 2018, -6.6 % in 2022 and -7.0 % in 2025, but +11.5 % in 2020, +10.6 % in 2023 and +7.0 % in 2024, each with |t| < 1.9. By year the slope runs from -0.0074 to +0.0037, with no year at |t| ≥ 1.6. The effect is drowned by which market phase the low falls in, not carried by any lasting part of the data.
- **F6:** Across coins the 20-day slope is positive for 13 of 17 coins with a slope, but none reaches |t| 2 (best: INJ 1.75, BTC 1.68, ETH 1.64; AAVE is -1.34, UNI -1.03). No coin subset carries a clear effect.

## Ideas
- No ideas: The slope is on the idea's side but small at every horizon (F1), the test already used all available coins and folds, and the effect is not graded in proximity (F2–F4) and appears in no stable coin, year or horizon subset, only in market-phase swings that flip sign (F5, F6), so no amended idea has a finding to rest on.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
