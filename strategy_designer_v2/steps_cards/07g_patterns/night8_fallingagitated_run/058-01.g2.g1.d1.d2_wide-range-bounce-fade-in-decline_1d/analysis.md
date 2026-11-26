---
line: 7.g patterns
backtest: 058-01.g2.g1.d1.d2_wide-range-bounce-fade-in-decline_1d
idea tested: 058-01.g2.g1.d1.d2_wide-range-bounce-fade-in-decline
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4244 USD
---
## Findings
- **F1:** In the falling agitated profile, the largest up days are given back over the next three days in a clean gradient: on non-overlapping 3-day cases, the mean unusual move after FA up days rises from +2.50 % (t 1.47, 47 cases) in the smallest quartile of the day's return against its 30-day swing to +0.14 %, then −0.52 %, then −4.01 % (t −1.77, 46 cases, 25 days) in the largest quartile, while over one day the same quartiles show no gradient (slope of next-day move on that ratio +0.0048, day-clustered t 0.79, 542 cases).
- **F2:** In the falling agitated profile, an up day that extends an already positive 3-day move is followed by a next-day fall of −0.95 % against drift (t −2.14, 371 cases, 167 days), but its day-range terciles do not grade it (−0.71 %, −1.41 %, −0.79 %), and in the short side of every profile the map holds only one strategy.
- **F3:** Outside the falling agitated profile, the tested situation (an up day with a negative 3-day return) is also followed by a next-day fall of −0.66 % against drift (t −2.50, 1,125 cases, 474 days), larger for wider days (range terciles −0.10 % t −0.31, −0.61 % t −1.97, −0.69 % t −1.65), while the other three day types outside the profile stay near zero (t 0.24 to 0.62).
- **F4:** Inside the profile, the tested idea's grading shows on folds B and C: by day-range tercile the next-day move is +0.83 %, −0.54 %, −2.30 % (t −1.82, 70 cases), but the book's active cases carry it unevenly, with BTC −1.77 % (t −2.22, 48 cases) and ZEC −1.83 % (t −2.17, 52) against ETH −0.04 %, XRP −0.08 % and XMR +0.18 %, and the per-year top-half up days falling in 2018, 2019 and 2020 (−1.86 %, −1.40 %, −1.04 %) but rising in 2021 (+0.81 %).
- **F5:** In the falling agitated profile, down days with a negative 3-day return rebound the next day by +1.27 % (t 2.59, 500 cases, 226 days), +3.04 % in the widest-range tercile (t 2.64), and the lowest quintile of the day's return against its swing rebounds +2.24 % (t 2.73); this is the falling agitated long rebound that the map already holds in 12 strategies, so it is not a discovery.
- **F6:** Neither the weekday nor where an up day closes inside its range sorts the next-day move in the falling agitated profile: the largest weekday |t| is 1.69 over 7 days, and the low, mid and high close thirds give −0.96 %, −1.20 % and −0.87 % with no order.

## Ideas
- `058-01.g2.g1.d1.d2.g1_large-bounce-three-day-giveback` (from F1, F2): In a falling, agitated market, an up day is partly given back over the next 3 days, and the larger that day's return against the standard deviation of the coin's daily returns over the past 30 days, the larger the fall over those 3 days.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `058-01.g2.g1.d1.d2.g2_wide-bounce-fade-everywhere` (from F3, F4): An up day that comes while the coin's 3-day return is still negative is followed by a fall over the next day, and the wider that day's high-to-low range against the standard deviation of its daily returns over the past 30 days, the larger the next-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
