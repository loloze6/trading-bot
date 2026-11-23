---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b2_percent-weekend-fall-rebound
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b2_percent-weekend-fall-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Sunday close-to-close fall is followed by a rise over the next 3 days. That rise is larger the deeper the fall and the lower Sunday's volume is against the coin's own 30-day average volume.
Consequence: Weight a Monday-to-Wednesday long after a Sunday fall by depth times volume thinness, and take little or no long after a Sunday fall made on heavy volume.
Why:
- F1: Thin volume, not depth alone, carries the Sunday-fall rebound. Among Sunday falls, the slope of the drift-adjusted 3-day return on Sunday's return is -0.917 (t -5.02, n 616) in the lowest tercile of Sunday volume relative to its 30-day mean, -0.216 (t -1.30) in the middle tercile and +0.073 (t +0.64) in the highest. In a regression on depth, thinness and their product, depth alone is 0.066 (t 0.82) and depth × thinness is 0.386 (t 3.38), over 1830 cases.
- F2: This volume grading belongs to the weekend. Tuesday-to-Thursday falls show no such ordering: their slope is -0.141 (t -1.67) in the low-volume tercile and -0.153 (t -3.29) in the high-volume tercile, over about 1966 cases each.
- F4: Across all Sundays, both signs together, the reversal slope of the 3-day drift-adjusted return on Sunday's return falls steadily as Sunday's relative volume rises: -0.688 (t -7.92), -0.282 (t -3.95) and -0.120 (t -2.82), over about 1260 cases per tercile.
