---
line: 7.g patterns
backtest: 032-02.b1_flat-range-upside-break-continues_1d
idea tested: 032-02.b1_flat-range-upside-break-continues
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 3
cost: 0.5128 USD
---
## Findings
- **F1:** Where the close sits in its prior 60-day high-low range forecasts the next 5 days on every coin's non-overlapping 5-day grid (correlation of range position with the unusual 5-day move: 0.147 over about 846 cases). The top quintile gains +3.03 % above drift (t 2.32, 169 cases, 61 days), and the middle quintile loses −1.90 % (t −1.95, 93 days).
- **F2:** F1's top-of-range effect holds inside the tested idea's own chop regime (60-day efficiency ratio ≤ 0.3), so it is not limited to breaks: the top quintile there gains +2.72 % (t 2.10, 133 cases, 55 days), and the two lowest quintiles lose −1.19 % and −1.50 %.
- **F3:** The top-of-range quintile is positive on all six coins: BTC +1.25 % (t 1.06), ETH +2.49 % (t 2.17), LTC +3.00 %, XMR +3.32 % (t 1.89), XRP +9.99 %, ZEC +2.78 %. It is also positive in 2019 (+4.46 %), 2020 (+4.76 %, t 2.32) and 2021 (+1.50 %). Only 2018 is negative, on 3 cases.
- **F4:** The break size does not grade the upside-break move. In thirds of the break's distance above the old high, in mean daily ranges, the moves are +4.77 % (t 2.30), −1.48 % (t −0.84) and +9.12 % (t 2.16). This matches step 5's negative slope of −0.0038 on the forecast, while the per-case total move (+2.44 %) is 12.6 times the 0.19 % trade cost.
- **F5:** The past 20-day return points the same way as range position, but not monotonically. The second-lowest quintile loses −3.54 % (t −2.67, 70 days), and the fourth gains +3.09 % (t 2.51, 76 days). The extreme quintiles are weaker: −0.94 % and +1.72 %.
- **F6:** Closes below the 60-day low in trending coins (efficiency ratio > 0.3) are followed by a further fall of −10.6 % (t −3.46). This rests on only 13 cases on 9 days, and 15 of the 16 cases with a falling 60-day trend fall in 2018 (−9.6 %, t −3.17), so it cannot be told from one year's bear market.
- **F7:** The book's gain is uneven across coins. BTC's 45 trades lose −2.29 % each before fees on average, while XRP (+13.1 %, 16 trades) and ZEC (+6.4 %, 35 trades) carry most of the summed profit. The weekday pattern (Wednesday −1.25 %, Thursday −1.85 %, t −2.50) is concentrated in 2018 (t −2.89) and absent in 2019–2021, so I read it as chance.

## Ideas
- `032-02.b1.g1_range-position-predicts-continuation` (from F1, F2, F3, F4): In a coin whose price has gone nowhere over the past 60 days, the higher its daily close sits within its 60-day high-low range, the larger its rise over the next 5 days.
- `032-02.b1.g2_top-of-range-keeps-rising` (from F1, F3, F5): The higher a coin's daily close sits within its prior 60-day high-low range, the larger its rise over the next 5 days, in any market regime.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
