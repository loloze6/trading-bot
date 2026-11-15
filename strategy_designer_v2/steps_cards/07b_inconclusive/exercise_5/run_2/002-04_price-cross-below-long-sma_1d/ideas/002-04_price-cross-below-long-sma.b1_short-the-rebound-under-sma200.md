---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.b inconclusive
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is below its 200-day simple moving average, it falls further than its usual drift over the next 10 days, and the more its 60-day return has recovered toward the average, the larger that fall.
Consequence: A trader would short coins below their 200-day average when they rally back toward it, and would refuse shorts after deep, recent sell-offs, where a bounce is more likely.
Why:
- F4: Among bars below the SMA200, the 10-day short excess gain rises with the coin's own 60-day return, and this is the only significant result in the pooled data. It is -0.013 (t -1.00, n 135) after the largest 60-day falls (mean -39 %), +0.014 (t 1.42) in the middle tercile, and +0.027 (t 2.27, n 135) in the top tercile (mean +6 %, a rebound toward the falling average).
- F5: The top-60-day-return effect is positive in every coin, from ETH +0.008 to BTC +0.043 (t 0.25 to 1.39, 20 to 26 blocks each), so a few coins do not carry it.
- F6: The plan's grading by depth below the SMA does not hold. The deepest quintile of distance (mean -46 %) earns +0.0001 (t 0.00), and the shallow quintiles earn +0.007 to +0.011. The correlation of the short gain with distance is only 0.05, and the plan's regression slope is -0.013. Grading by depth adds the most size where the coin is already most sold-off, which is where it tends to bounce (F4).
- F1: The short gain beyond holding is close to zero at every horizon while the close is below the 200-day SMA (non-overlapping blocks: 1 day t -0.10 on 8674 cases, 5 days t -0.39 on 1709, 10 days t -0.70 on 841, 20 days t -0.01 on 412, 40 days t +0.26 on 197), so the test did not miss the effect by using the wrong horizon.
