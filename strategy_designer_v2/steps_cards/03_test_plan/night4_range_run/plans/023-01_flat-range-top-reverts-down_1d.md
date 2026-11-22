---
idea: 023-01_flat-range-top-reverts-down
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: 30-day net move small relative to the 30-day high-low range -> replaced: no component divides the net move by the high-low range (the efficiency ratio divides by the path length instead)
- Comparison: how far the close sits above the middle of that 30-day high-low range -> replaced: `DonchianBreakoutComponent` measures position in the closing range, not the high-low range
- Outcome: the further above the middle, the more it falls over the next 5 days -> kept: a graded short held 5 bars
- Verdict transfer: no: with the flat-market condition and the range middle both measured by other quantities, neither result would speak for the idea.
Reason: The condition "small 30-day net move relative to the 30-day high-low range" needs a ratio of two quantities. No catalogue component computes it, and the config cannot divide one component by another (score_product only divides by constants). The close's position against the middle of the 30-day high-low range is not computed either: Donchian reads only closes. Both come from one coin's own bars, and a regime rule plus a graded component could hold them.
