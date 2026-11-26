---
line: 7.g patterns
backtest: 062-02_rising-volume-growth-stalls_1d
idea tested: 062-02_rising-volume-growth-stalls
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6039 USD
---
## Findings
- **F1:** In rising markets (60-day return above +10 %), on the 5-day grid of folds B and C, the lowest quarter of the 30-day against prior 30-day volume ratio (mean log ratio −0.55) was followed by a 5-day return +3.46 % above the coin's drift (t 1.99, 80 cases), and the highest quarter (mean +0.82) by −0.21 % (80 cases); the quarters fall in order: +3.46 %, +1.29 %, +0.34 %, −0.21 %.
- **F2:** The rising-market slope of the drift-removed 5-day return on the raw volume ratio, scaled per coin, is negative on all 6 coins (XMR t −2.34, XRP −1.67, ETH −1.01, the others near 0); pooled it is −0.147 with t −1.66 clustered by day (318 cases, 84 days), and by year its t is −2.56 in 2021, −1.14 in 2019 and −0.59 in 2020; so in these folds a shrinking volume comes before a larger rise, the brief's direction.
- **F3:** The effect sits in rising agitated markets: there the slope is −0.228 with t −1.91 (140 cases, 58 days); in rising calm markets it is −0.021 with t −0.18 (178 cases, 65 days).
- **F4:** The tested forecast (the ratio standardised over its own past 60 values) catches less of it than the raw ratio: its slope t is +1.52 in these folds against the raw ratio's −1.66 (the sign of the forecast is flipped, so both point the same way); its correlation with the raw ratio in rising markets is 0.60; and over all folds its size is +0.20 % per case (t 0.43), equal to the 0.19 % cost of a trade.
- **F5:** The book lost on its shorts on every coin (mean net trade −2.97 % to −14.14 %; LTC −14.14 % over 125 trades) and gained on its longs on every coin (+2.84 % to +18.49 %); its losses come from the short side, the growing-volume side, which the brief's own reading treats only as a weaker rise, not a fall.
- **F6:** The next day's return after a Thursday or a Friday close beats the other days on all 6 coins (by coin +0.34 % to +1.04 % a day above the rest, t 1.41 to 3.33) and in 10 of 12 windows; it is strongest in 2019 (t 4.71) and 2020 (t 3.22), and absent in falling agitated markets (−0.47 %, t −0.68). It is a fixed weekday condition, not a graded one, and the map already holds it in rising markets (045-01), so I write no idea from it.
- **F7:** In choppy calm markets the past 5-day return predicts the next 5 days (slope t 2.81, 99 cases, 53 days; lowest quarter −8.67 % against drift, t −3.55, 32 cases). It comes from 2020 alone (t 3.87; 2019 t −0.75) and is one of about 45 slices looked at, so it does not stand out from chance.

## Ideas
- `062-02.g1_agitated-uptrend-volume-dry-up` (from F1, F2, F3, F4, F5): In a rising, agitated market, the more a coin's trading volume over the past 30 days has shrunk against the 30 days before, the larger its rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
