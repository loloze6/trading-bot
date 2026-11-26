---
line: 7.g patterns
backtest: 072-01_choppy-deep-close-continuation_1d
idea tested: 072-01_choppy-deep-close-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5895 USD
---
## Findings
- **F1:** The tested effect is not in these folds. In choppy markets the next-day excess return does not fall with depth below the 20-day high. The slope is +0.13 % per unit of depth on down days (t 0.67, 621 cases, 386 days) and +0.20 % on up days (t 1.40, 629 cases, 378 days). By quintile, the middle three choppy depth quintiles sit between −0.03 % and −0.11 % (|t| ≤ 0.41).
- **F2:** The choppy result rests on one quintile and is not graded. Only the deepest choppy quintile is negative (−0.95 %, t −2.15, 250 cases), and that comes from down days (−1.50 %, t_day −2.03, 88 cases) and not from up days (−0.65 %, t_day −0.78). It does not hold by year: 2021 shows +0.01 %, and 2020 shows −3.40 % with t −0.89 on 38 cases.
- **F3:** In falling markets (60-day return below −10 %), the wider an up day's range against its own 20-day mean range, the lower the next day's excess return. The slope is −1.37 % per unit of relative range (t_day −2.86, 969 cases, 277 days). The same slope is −0.44 % in choppy markets (t −0.86) and +0.24 % in rising markets (t 0.73).
- **F4:** The F3 effect is graded across quintiles of relative range on falling-market up days. The next-day excess return runs +0.43 %, −0.21 %, −0.92 % (t −2.27), −0.55 % and −1.58 % (t_day −2.63, 195 cases, 86 days) from narrowest to widest. The widest quintile's move is about 8 times the 0.19 % cost of a trade.
- **F5:** The F3 slope is negative on all six coins: BTC −1.68 % (t −2.61), ETH −2.07 % (t −3.17), LTC −1.49 % (t −2.10), ZEC −1.39 % (t −2.28), XMR −1.13 % (t −1.43) and XRP −0.73 % (t −0.90). It is also negative in 3 of 4 years: 2018 −1.72 % (t −1.97), 2019 −0.40 %, 2020 −2.38 % (t −3.23), against 2021 +0.79 % (t 0.97).
- **F6:** The F3 fade is stronger when the coin's 20-day swing is in its upper half (slope −1.73 %, t −2.83, 578 cases) than in its lower half (−0.75 %, t −1.63, 391 cases). It is a one-day effect: the two-day slope is −0.57 % (t −0.90).
- **F7:** The opposite case is already held. Wide down days are followed by relative rises, with a slope of +0.76 % per unit of relative range (t_day 2.04, 3627 cases). The profile map already holds several wide-range-fall rebound strategies, so this is not a discovery.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `072-01.g1_falling-wide-up-day-fade` (from F3, F4, F5, F6): In a falling market, the wider a day that closed up is against the coin's average daily range of the last 20 days, the larger the coin's fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
