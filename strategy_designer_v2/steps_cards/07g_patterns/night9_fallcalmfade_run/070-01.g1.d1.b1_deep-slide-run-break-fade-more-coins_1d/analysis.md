---
line: 7.g patterns
backtest: 070-01.g1.d1.b1_deep-slide-run-break-fade-more-coins_1d
idea tested: 070-01.g1.d1.b1_deep-slide-run-break-fade-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4584 USD
---
## Findings
- **F1:** Across all 10 coins in folds B and C, with no regime filter, an up close that ends a run of two or more down closes is followed by a next-day unusual move of -1.09 % (t -3.45, 1183 cases on 432 days) and a three-day unusual move of -1.32 % (t -2.69, 1168 cases); all other bars are followed by +0.15 % (t 1.10, 8721 cases).
- **F2:** The next-day fall after a run break grows with how far the run itself fell, measured in the coin's 20-day daily swing. By quartile of that fall, deepest to shallowest, the next-day moves are -1.65 % (t -2.92, 256 cases, 111 days), -0.86 %, -0.17 % and -0.48 %. In a regression of the next-day move on the run's scaled fall and the up day's scaled size, the run's fall has t 4.40 and the up day's size t 1.43 (1015 cases).
- **F3:** Over three days the deepest quartile of run falls is followed by -3.08 % (t -3.53, 248 cases, 109 days), while the other three quartiles give +0.04 %, +0.00 % and -0.58 %. That is more than ten times the 0.23 % cost of a trade.
- **F4:** The fade is absent in rising markets and present elsewhere. By the 60-day return, run breaks are followed next day by -1.35 % in falling markets (t -2.94, 299 cases), -1.36 % in choppy markets (t -2.09, 96 cases) and +0.35 % in rising markets (t 0.58, 205 cases). Over three days the same groups give -2.48 % (t -2.74), -2.13 % (t -2.37) and +0.41 % (t 0.43).
- **F5:** Breaks outside the tested profile fade as strongly as those inside it. In the "chop" regime (outside falling calm) the next-day move is -1.14 % (t -2.94, 889 cases). In "trending" (falling calm with the 20-day return at -10 % or below) it is -1.32 % (t -2.45, 162 cases). In "unknown" (falling calm with a shallower 20-day fall) it is only -0.47 % (t -1.25, 132 cases).
- **F6:** Inside the tested regime the fade is largest after the longest runs. Breaks of runs of five or more down days are followed by -3.49 % next day (t -3.16, 21 cases on 20 days), against -0.98 % after two-day runs (t -1.33, 83 cases). Over three days the trending breaks fall -2.62 % (t -3.00, 158 cases).
- **F7:** The fade does not depend on the up day itself. By the size of the up day the next-day moves are -1.06 %, -0.71 % and -0.61 % (small to big). By where it closes in its range they are -1.20 % (low), -0.86 % (mid) and -1.30 % (high), so neither grading is monotonic.
- **F8:** The tested book's cases earned most of their gain in one year. The short-direction move per case was +2.37 % in 2018 (t 2.52, 71 cases) against +0.63 % in 2019 and +0.21 % in 2021. The raw run-break fade, however, is negative in every year: 2018 -2.03 % (t -3.77), 2019 -0.85 % (t -2.17), 2020 -0.58 %, 2021 -1.03 %.
- **F9:** Neither weekday nor the level of volatility explains anything. The next-day move by weekday ranges from -0.44 % to +0.37 % with |t| at most 1.44. By volatility tercile it is +0.03 %, -0.12 % and +0.16 %, all with |t| under 0.7.

## Ideas
- `070-01.g1.d1.b1.g1_calm-decline-deep-run-fade` (from F2, F3, F6, F7): In a falling, calm market, an up day that ends a run of down days is followed by a fall over the next three days, and the fall is larger the further the run of down days had fallen, measured in the coin's usual daily swing over the past 20 days.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `070-01.g1.d1.b1.g2_choppy-market-deep-run-fade` (from F1, F2, F3, F4): In a choppy market, an up day that ends a run of down days is followed by a fall over the next three days, and the fall is larger the further the run of down days had fallen, measured in the coin's usual daily swing over the past 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
