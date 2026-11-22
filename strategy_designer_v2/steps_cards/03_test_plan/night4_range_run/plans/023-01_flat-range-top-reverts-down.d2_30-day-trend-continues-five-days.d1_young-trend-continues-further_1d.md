---
idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.d1_young-trend-continues-further
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: be08f97ea86e
---
Fidelity:
- Situation: 30-day net move large relative to the 30-day high-low range -> kept: `NetMoveToRangeRatioComponent` (period 30) in a regime rule.
- Comparison: young trend against one in place more than about a week -> replaced: it needs the same missing age count.
- Outcome: price continues in the 30-day direction over the next 5 days -> kept: a 5-bar horizon on daily bars.
- Verdict transfer: no: without the age of the condition, the test cannot check the claim that fresh trends continue more than old ones.
Reason: The idea sizes the bet by how many days have passed since the 30-day net-move-to-range ratio became large. That is computable from the coin's own closes, highs and lows, and a graded component could hold it. But no catalogue component counts bars since this condition began. `MovingAverageAgeComponent`, `RsiMidlineAgeComponent` and `IchimokuCloudCrossAgeComponent` time other events, and no combination of components gives a lagged ratio or the time since a threshold was crossed.
