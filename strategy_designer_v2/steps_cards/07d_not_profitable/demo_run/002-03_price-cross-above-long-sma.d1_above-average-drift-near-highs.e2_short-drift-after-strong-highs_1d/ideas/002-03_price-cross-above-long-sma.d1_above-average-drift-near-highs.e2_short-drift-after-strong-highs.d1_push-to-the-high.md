---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average, the stronger its rise toward its 20-day high, the larger its rise over the next 5 days. The effect concentrates on closes pressed against the 20-day high after a large 5-day gain, with the rise growing with that 5-day gain.
Consequence: A trader would carry little or no long on closes merely in the upper half of the range, and concentrate exposure on strong recent pushes right at the 20-day high, lifting the mean return per day held.
Why:
- F1: The book's mean daily return is 0.000479, against 0.00118 for holding the coins. The book is in a position on only 33.8 % of bars, at a mean allocation of 0.53 when in. Its gain before fees is 0.000546 per bar, against fees of 0.000067 per bar, so fees are not what keeps the mean daily return below 0.0005.
- F2: Nearly all the gain comes from closes at the very top of the 20-day range. In the top forecast quintile (forecast 17.1) the next-day return is 0.00506 and the gain 0.00529, from 1043 bars. Quintiles 2 to 3 (forecast 7.9 to 11.6) earn only 0.00034 to 0.00070 at allocations of 0.41 to 0.63, and the next-day return there (0.0013 and 0.0006) is below the coin's all-window mean of 0.00119.
- F4: Active bars that move further toward the high over 5 days are followed by larger rises. The 5-day return quintiles from -4.6 % to +24 % carry next-day returns rising from 0.00063 to 0.00450 and gains from 0.00052 to 0.00355, about 1000 bars each.
