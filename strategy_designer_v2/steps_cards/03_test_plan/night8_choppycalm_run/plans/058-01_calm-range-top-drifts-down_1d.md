---
idea: 058-01_calm-range-top-drifts-down
brief: 058_choppy-calm-range-edge-reversion
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 088be9d08c17
---
Fidelity:
- Situation: in a choppy calm market, how near the close sits to the top of its 20-day high-low range -> replaced: the catalogue's listed params give only the position inside the 20-day closing range, not the high-low range.
- Comparison: none -> kept
- Outcome: a larger fall over the next 5 days, the nearer the top -> kept
- Verdict transfer: no: the closing range has a different top and bottom from the high-low range, so a result on it does not confirm or reject the idea as stated.
Reason: The idea measures where the close sits inside the 20-day high-low range. The only catalogue component that reads it is `DonchianBreakoutComponent` with `source` "high_low", and `source` is not among the params its row lists, so the config cannot use it. No combination of listed components gives the close's position between the 20-day max high and min low. `FlatnessWeightedRangePositionComponent` "high_low" multiplies that position by a flatness factor. `DistanceFromHighComponent` gives the distance from the high only, not the position within the range.
