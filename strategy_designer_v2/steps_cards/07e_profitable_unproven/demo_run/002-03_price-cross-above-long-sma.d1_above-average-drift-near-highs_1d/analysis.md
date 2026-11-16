---
line: 7.e profitable but not proven
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs_1d
idea tested: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs
step 5: not observable
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3595 USD
---
## Findings
- **F1:** The book's mean daily return of 0.000565 splits into 0.000224 from the market's own rise and 0.000340 of timing, and days held in the coin saw a mean coin return of 0.001824 against 0.000712 on days out of it (7468 vs 9912 coin-days), so most of the gain is timing, not drift.
- **F2:** The forecast grades the move over short horizons but not over the plan's 20 days: the pooled slope t is 2.94 at 1 day (n=17380), 3.21 at 3 days (n=5723), 2.91 at 5 days (n=3419) and 3.32 at 10 days (n=1691), against 1.22 at 20 days (n=827) and 0.98 at 40 days (n=395).
- **F3:** The grading also holds among the active cases alone: the slope t within forecast > 0 is 2.29 at 1 day, 2.74 at 3 days, 1.89 at 5 days and 2.70 at 10 days (598 cases), but only 0.85 at 20 days (284 cases).
- **F4:** At 10 days the top forecast tercile earns a de-meaned +0.0346 (200 cases), against -0.0061 for the low tercile, -0.0010 for the mid tercile and -0.0050 when flat; at 5 days the terciles rise from -0.0033 to 0.0084 to 0.0107.
- **F5:** Within the active cases at 10 days, the 20-day range position carries the grading (raw t 1.96) more than the 20-day rise does (t 0.61); at 5 days the two are similar (t 1.60 and 1.53), and at 20 days both are about 0 (t -0.16 and -0.11).
- **F6:** The gain is concentrated in time: windows w11, w17 and w21 (years 2021, 2020 and 2024) hold 68% of the summed daily book returns, and without them the book's mean falls to 0.000208 with a Sharpe of 0.41; the 10-day slope t drops from 3.32 to 1.85 (n=1481) and the 5-day one from 2.91 to 1.24.
- **F7:** Three coins carry the timing, at about 0.00066 to 0.00079 a day each (BTC 0.000658, ETH 0.000681, XRP 0.000792), while LTC (-0.000099) and XMR (-0.000182) lose on timing; LTC's 10-day slope t is -0.69 and XMR's is 0.40.
- **F8:** The book wins on few trades: 2888 trades with 44% winners and a median of -0.88%, and the top 10 trades give 8591 of the 26139 summed percent (33%).

## Ideas
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days` (from F2, F3, F4, F5): While a coin's close is above its 200-day average, the higher its close sits in its 20-day close range, the larger its rise over the next 10 days.
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs` (from F2, F3, F4, F6): While a coin's close is above its 200-day average, the stronger its rise toward its 20-day high, the larger its rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
