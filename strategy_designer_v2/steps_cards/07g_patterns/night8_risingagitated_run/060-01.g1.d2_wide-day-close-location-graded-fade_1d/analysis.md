---
line: 7.g patterns
backtest: 060-01.g1.d2_wide-day-close-location-graded-fade_1d
idea tested: 060-01.g1.d2_wide-day-close-location-graded-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4145 USD
---
## Findings
- **F1:** Inside the falling agitated profile, the day's own return explains the next-day move and the close's place in the range does not: regressing the next-day excess return on the day's return in units of its 20-day swing and on the close location gives a slope of −0.0104 (t −4.24) for the day's return and −0.0040 (t −0.89) for the close location, over 1,298 in-profile bars.
- **F2:** The tested cases, wide in-profile days closing in the upper half of the range, fall next day only when the day itself closed up: such up days are followed by −2.03 % excess (t −2.76, 113 cases on 66 days), while the same high closes on down days are followed by +1.08 % (t 0.64, 20 cases on 13 days).
- **F3:** In-profile up days are followed by a next-day fall in every year (2018 −1.42 %, 2019 −0.92 %, 2020 −0.37 %, 2021 −0.82 %) and on every coin (−0.40 % to −1.24 %; BTC t −2.30, LTC t −2.21). This holds whether the close is high (−0.79 %, t −1.68, 384 cases) or low or middle in the range (−1.07 %, t −1.41, 171 cases).
- **F4:** The fall after in-profile up days is not graded by the size of the rise. By quartile of the rise in units of the 20-day swing (mean 0.09, 0.31, 0.64, 1.65), the next-day excess is −0.89 %, −0.89 %, −1.79 % (t −3.49) and +0.06 % (t 0.08); the Spearman rho is 0.011 (p 0.80, n 555).
- **F5:** The opposite tail is the large in-profile down day, followed by +2.14 % (t 2.81, 227 cases) in the lowest quintile of the day's return and +1.36 % (t 2.52) in the next. The profile map already holds this rebound in falling agitated long (035-01, 047-01, 051-01 and others), so it is not a discovery.
- **F6:** Outside the profile the effect is absent. Wide days closing at the top are followed by −0.24 % (t −0.74, 620 cases), and no quintile of the day's return reaches |t| 1.3. By weekday, no in-profile day reaches |t| 1.8 across seven groups.

## Ideas
- `060-01.g1.d2.g1_up-day-high-close-fade` (from F1, F2, F3, F6): In a falling, agitated market, a coin that closes in the upper part of its day's high-low range on a day it closed higher than the day before falls over the next day. The higher that close sits in the day's range, the larger the next-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
