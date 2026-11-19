---
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs_1h
idea tested: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3426 USD
---
## Findings
- **F1:** The pooled 336-bar slope's t of 2.18 (576 cases) rests on a few large gains. Dropping the 3, 5 or 10 largest excess returns cuts it to t 1.35, 0.74 and 0.68. Winsorising at 2.5/97.5 % gives t 1.29, and the rank correlation of forecast with excess return is −0.0009 (p 0.98).
- **F2:** In the top forecast bin (above 10, 174 cases) the mean excess return is +0.048 but the median is −0.025, and only 45 % of cases are positive, against 47 % at a zero forecast. The mean is lifted by right tails, mostly in ZEC (mean +0.120, median −0.071) and XRP (mean +0.077, median −0.028).
- **F3:** The effect is mixed across coins and years. The per-coin slope t ranges from −0.16 (ETH) and −0.14 (LTC) to +1.70 (ZEC). The per-year t swings from +2.26 (2019) and +2.40 (2021) to −2.17 (2023).
- **F4:** At other horizons the effect does not show. The slope t is 0.92 at 168 bars (1,218 cases) and 0.64 at 720 bars (271 cases). At 24 bars it reverses to −3.25 (8,740 cases), where positive-forecast grid bars trail zero-forecast ones by Welch t −2.51.
- **F5:** The book's daily gross gain per coin-day (+0.000083) is smaller than its gain from the market's own rise (+0.000214), so its timing part is negative (−0.000131). Its fees (0.001825 per coin-day, with 3.8 trades a day of 4-hour median length) make it lose −0.0017 a day. The book thus trades the 1-day reversal of F4, not the two-week drift.

## Ideas
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs.b1_near-high-momentum-more-coins` (from F1, F2, F3): When a coin closes above its long moving average, the nearer its close sits to the top of its recent range and the stronger its recent rise, the larger its return over the following days to two weeks. The effect fades by about a month.
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs.b2_near-high-one-day-giveback` (from F4, F5): When a coin closes above its 8-day moving average, the larger its 20-hour rise and the nearer its close to its 20-hour high, the lower its return over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
