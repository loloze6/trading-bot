---
idea: 010-07_rsi-above-streak-reversal
brief: 010_rsi-midline-regime-direction
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: the 14-day RSI has stayed above 50 without a break, counted in days up to the current close -> replaced: no component counts RSI's days above 50, and `MovingAverageAgeComponent` counts days above an SMA, not RSI.
- Comparison: longer streaks against shorter ones, graded by the streak's length -> kept: a forecast that grows with the streak's length would express it.
- Outcome: lower return over the next 14 days (a short, growing with the streak) -> kept: a horizon of 14 bars on 1d bars.
- Verdict transfer: no: without a count of RSI's days above 50, any substitute measures a different situation.
Reason: The streak can be computed from each coin's own closes, and a graded forecast could hold it as a negated, standardised value. But no catalogue component counts consecutive bars of RSI on one side of 50. `RSIPullbackComponent` gives only RSI's current level. `MovingAverageAgeComponent` and `BarsSinceHighComponent` count runs of other conditions. No weighted combination of levels turns into a run length.
