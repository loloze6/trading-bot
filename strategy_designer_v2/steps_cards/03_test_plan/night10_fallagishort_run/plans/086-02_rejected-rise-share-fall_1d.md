---
idea: 086-02_rejected-rise-share-fall
brief: 086_falling-agitated-rejected-rally-wick
data-instruments: BCH, AVAX, XMR, INJ, GRT, DOGE, FIL, LTC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: bd33e939b067
---
Fidelity:
- Situation: in a falling, agitated market, a day's rise above its open, and the share of it given back by the close -> replaced: no component measures (high − close) / (high − open); only shares of the high-to-low range or distances from the high exist.
- Comparison: none (graded: the larger the share given back, the larger the fall) -> kept
- Outcome: the coin falls over the next 3 days (3 bars) -> kept
- Verdict transfer: no: a close-location or distance-from-high measure judges where the day closed, which the idea says is not its information.
Reason: The idea's measure is the share of the intraday rise above the open that the close gives back, (high − close) / (high − open). No catalogue component reads the open against the high this way. `CloseLocationInRangeComponent` and `VolatilityScaledDistanceFromHighComponent` measure from the low or in usual moves, and a weighted mean of components cannot form this ratio.
