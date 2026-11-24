---
line: 7.b inconclusive
backtest: 031-01.b1.b2_wide-day-extends-strong-run_1d
idea tested: 031-01.b1.b2_wide-day-extends-strong-run
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3426 USD
---
## Findings
- **F1:** The test's result is on the side the idea predicts but short of the bar: a mean unusual 3-day move of +0.17 % with t 0.76 over 1164 case days. My own reading on every 3-day grid bar with a positive forecast gives the same picture, +0.30 % with t 1.13 (2907 cases, 781 days).
- **F2:** The effect is spread thinly but mostly the right way across coins: 5 of 6 coins are positive at 3 days (XRP +0.80 % t 1.54, ZEC +0.48 % t 0.98, LTC +0.28 %, ETH +0.25 %, BTC +0.11 %), and only XMR is negative (−0.06 % t −0.19). No single coin's t reaches 2, so this data is too small to show the effect, not opposed to it.
- **F3:** The effect swings with the period, which drowns it: it is positive in 2020 (+1.23 %, t 1.54) and 2021 (+1.52 %, t 1.77), negative in 2022 (−1.19 %, t −1.66), and near 0 in 2018, 2019 and 2025 (each 89–106 days).
- **F4:** The 5-day rise carries the effect more than the range does. On rising bars, the top half of 5-day rises gains +0.87 % (t 1.58) on narrower days and +0.72 % (t 1.39) on wider days, against −0.05 % and −0.55 % for the bottom half. The range-multiple quartiles do not rise in order (+0.09 %, +0.56 %, −0.63 %, +1.05 %).
- **F5:** The graded effect shows only while the coin's 60-day return is positive. There, the top quarter of rise × range multiple gains +2.15 % over 3 days (t 2.07, 120 days), and the rank correlation of the product with the unusual move is 0.045. When the 60-day return is not positive, the top quarter gains −0.49 % (t −0.42) and the rank correlation is −0.001.
- **F6:** Per case, the unusual move (+0.17 %) is 0.9 times the 0.19 % cost of a trade, so the plain idea cannot beat holding after costs. The top quarter in F5 (+2.15 %) is about 11 times the cost.

## Ideas
- `031-01.b1.b2.b1_wide-day-strong-run-more-coins` (from F1, F2, F3): After a coin has risen over the past 5 days, the larger that 5-day rise and the wider that day's high-low range compared with its average daily range over the past 20 days, the more the coin rises over the next 3 days.
- `031-01.b1.b2.b2_wide-strong-run-in-uptrend` (from F4, F5, F6): After a coin has risen over the past 5 days, only while its 60-day return is positive, the larger that 5-day rise and the wider that day's high-low range compared with its average daily range over the past 20 days, the more the coin rises over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
