---
idea: 029-05_failed-breakout-multiday-drift
brief: 029_failed-breakout-traps-late-buyers
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 1063cd22d7e7
---
Fidelity:
- Situation: a close back below the old 20-day high, within 3 days of a close above it -> replaced: no component reads the 20-day high from before the breakout; the available prior highs include the breakout bars.
- Comparison: the deeper the re-entry close sits below the old high, the larger the fall -> replaced: the depth below the old high needs that same pre-breakout high, which no component gives.
- Outcome: the price falls from day 2 to day 10 after the failure -> adapted: a lagged reading of the failure, held 8 bars from day 2, would fit, but no component lags this reading.
- Verdict transfer: no: a depth measured against the breakout bar's high, or read on the failure day, tests a different situation and a different window of the fall.
Reason: The idea needs the 20-day closing high that stood before a breakout 1 to 3 days earlier, and the failure close's depth below it, read 2 bars later. The data is in the coin's own closes and a graded component fits the config. But no catalogue component, alone or combined, gives a lagged pre-breakout high: DistanceFromHigh, BreakoutInMeanRanges and VolatilityScaledDistanceFromHigh leave out only the current bar, and BarsSinceHigh gives only the timing.
