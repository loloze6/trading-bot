---
idea: 036-02_fall-vs-range-next-day-rebound
brief: 036_outsized-daily-fall-rebounds
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 00d5d6f5c07b
---
Fidelity:
- Situation: a one-day close-to-close fall that exceeds the coin's average daily high-to-low range over the past 30 days -> replaced: no catalogue component divides the close-to-close fall by the 30-day mean bar range.
- Comparison: the fall against the mean daily high-to-low range of the past 30 days -> replaced: the catalogue's nearest forms use another divisor (return std, mean absolute return) or another reference price (yesterday's high).
- Outcome: the coin rises over the next day, more the larger the excess -> kept: a long position held 1 bar, graded by the excess.
- Verdict transfer: no: with the fall or its yardstick replaced, a result would not speak for the idea as stated.
Reason: The idea needs the close-to-close fall measured in multiples of the coin's 30-day mean daily high-to-low range, both for the graded size and for the "exceeds" condition. No catalogue component gives that ratio. The weighted mean cannot divide one component by another. `BreakoutInMeanRangesComponent` "below" measures from yesterday's high, not yesterday's close. `VolatilityScaledReturnComponent` and `MeanAbsScaledReturnComponent` divide by return volatility, not by the bar range.
