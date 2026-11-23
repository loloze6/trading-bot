---
idea: 031-01_up-streak-length-reversal
brief: 031_daily-close-streak-reversal-or-continuation
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 31f1a8c6c7f6
---
Fidelity:
- Situation: the number of days in a row the coin has closed higher -> replaced: no component counts consecutive up closes; the nearest one measures the streak's gain in usual moves, not its length.
- Comparison: that count against the lengths of the coin's own up-close streaks over the past 365 days -> replaced: `standardise` over 365 bars divides by the mean daily value, which includes zero days, so it does not compare against past streak lengths.
- Outcome: the price falls over the next 5 days, more after longer streaks -> kept: a graded short with a 5-bar horizon.
- Verdict transfer: no: a test of streak gain in usual moves, scaled by its daily mean, would judge a different quantity than streak length ranked against past streak lengths.
Reason: The idea needs the count of consecutive higher closes and that count set against the lengths of past up streaks; both come from the coin's own closes and fit the config's graded logic. No catalogue component computes either one. `DownStreakLossInUsualMovesComponent` with `side` "up" gives the streak's gain, not its length. `RsiMidlineAgeComponent` and `MovingAverageAgeComponent` count runs of other conditions. `standardise` cannot rank against past streak lengths.
