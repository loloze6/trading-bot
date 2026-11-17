---
idea: 010-06_rsi-below-share-reversal
brief: 010_rsi-midline-regime-direction
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: share of the past 30 days that the 14-day RSI spent below 50 -> replaced: no component counts RSI's days below 50 over a 30-bar window; the nearest is today's RSI level.
- Comparison: a larger share against a smaller share -> kept: a share is graded, so a larger share gives a larger long.
- Outcome: the coin's return over the next 14 days is higher -> kept: the horizon is 14 bars on 1d bars.
- Verdict transfer: no: a test on today's RSI level would judge a different situation from the 30-day share below the midpoint.
Reason: The 30-day share of RSI(14) below 50 can be computed from closes alone. No catalogue component outputs a count of RSI's time on one side of 50. A config cannot build one either: averaging over 30 bars needs an `ema` history op, and `standardise` must be the only history op in `transforms`. Even with that average, a mean of 50 - RSI would measure how deep RSI sits below 50, not how much of the time it sits there.
