---
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.g1_volatility-scaled-momentum-above-average_1d
idea tested: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.g1_volatility-scaled-momentum-above-average
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4865 USD
---
## Findings
- **F1:** Below the 200-day average (the 'unknown' regime), the next day's excess return falls as the day's own fall, measured against 20-day volatility, gets smaller: the slope on down days is -0.0041 (t -5.39, 3810 cases), while above the average it is -0.0008 (t -0.58, 3246 cases) and on up days it is -0.0001 (t -0.19, 7286 cases).
- **F2:** The rebound below the average is graded. On those down days, the next-day excess return by quintile of the vol-scaled fall runs +0.72% (t 3.35), +0.37% (t 2.38), +0.07%, -0.21%, -0.14%, with 762 cases in each quintile.
- **F3:** The rebound holds beyond one day and beyond one year. On a non-overlapping 2-day grid the slope is -0.0035 (t -2.52, 1823 cases), and without 2020 it is -0.0019 (t -2.43, 3552 cases). Even so, 2020 alone is the strongest year (slope -0.0198, t -6.07, 258 cases).
- **F4:** The slope below the average is negative in all 6 coins and all 8 years. The coins are strongest in XMR (t -3.64) and XRP (t -3.66), and BTC is weakest (t -1.67).
- **F5:** Above the average, the tested momentum effect sits mostly in the top vol-scaled quintile, with excess 10-day return +5.5% (t 3.09, 140 cases). The middle quintiles lie between -2.1% and +1.1% and none is significant, so the gain comes from the largest vol-scaled moves rather than from a steady gradient.
- **F6:** The book's gain depends on a few days. Its best 2% of days carry 175% of its total gain, its worst 2% take away 149%, and daily skew is 0.91. This is consistent with the failed Calmar of 0.73.
- **F7:** I looked at many angles, and two did not count as patterns. Next-day excess returns by weekday look significant for Friday (+0.30%, t 3.76, 2479 cases) and are positive in all 6 coins. But weekday is a condition, not a graded situation. The 20-day volatility level does not sort forward 10-day returns in either regime (slope t -0.11 above the average, 1.06 below).

## Ideas
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.g1_volatility-scaled-momentum-above-average.g1_below-average-oversold-day-rebound` (from F1, F2, F3, F4): While a coin's close is below its 200-day average, the larger its one-day fall measured against its 20-day daily volatility, the larger its rise over the next 1 to 2 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
