---
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs_1h
idea tested: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4125 USD
---
## Findings
- **F1:** Fees, not a missing effect, sink the book. Before costs the positions earn +0.000084 per coin-day. Fees cost 0.001842 per coin-day on a turnover of 1.70 per day. That nearly matches the book's mean daily return of -0.001761 over 17381 coin-days, with a Sharpe of -3.21.
- **F2:** The forecast switches far too often for a two-week effect. It turns on or off 1.75 times a day across 15227 on-runs, with a median run of 3 hours and 52.9% of runs lasting 3 hours or less, so the book keeps paying to enter and leave.
- **F3:** The forecast's information sits only at the slow horizon. At 336 hours the top forecast tercile gains +0.0784 (n=140) against +0.0252 when the forecast is zero (n=215). At 24 hours the top tercile loses -0.0011 (n=1995) against +0.0038 for zero (n=2944). The hourly moves the book trades on carry no edge.
- **F4:** The book loses on timing. The timing part is -0.001975 per day against a market-rise part of +0.000214, with a mean allocation of 0.18. The frequent hourly entries buy short-lived highs that do not follow through within the day.
- **F5:** A slower measure keeps the two-week effect and needs far fewer switches. Rise times nearness to the high, over 168 bars (7 days), has a 336-bar excess-return slope t of 3.21 over 522 non-overlapping cases, with terciles of -0.0276, -0.0087 and +0.0284, and switches 0.81 times a day. Over 480 bars (20 days) the slope t is 2.91 over 432 cases, the top tercile is +0.0424, and it switches 0.55 times a day.

## Ideas
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs.d1_weekly-proximity-momentum-uptrend` (from F1, F2, F3, F4, F5): When a coin closes above its long moving average, the nearer its close sits to the top of its 7-day range and the stronger its 7-day rise, the larger its return over the following 14 days, with the situation read from the week's range and rise rather than the last day's.
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs.d2_twenty-day-high-proximity-momentum` (from F1, F2, F3, F5): When a coin closes above its long moving average, the nearer its close sits to the top of its 20-day range and the stronger its 20-day rise, the larger its return over the following 14 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
