---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g2_break-of-30-day-high
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: close standing above the highest high of the previous 30 days, by how far -> adapted: the config could hold it as a graded distance that is zero at or below the high, but no catalogue component computes it.
- Comparison: the highest high of the previous 30 days, excluding today -> kept in principle, but no component reads the `high` column for a prior-window maximum.
- Outcome: higher return over the next 7 days, rising with the distance -> kept: 7 bars on daily bars, long side.
- Verdict transfer: no: no catalogue component, alone or combined, measures how far the close stands above the prior 30-day high, so no test can carry the idea's verdict.
Reason: The data (`high` and `close`) is in the coin's own bars, and a graded long-only forecast could hold the idea, but no component measures a positive distance of the close above a prior high. `DistanceFromHighComponent` includes the current close, so it is never positive. `DonchianBreakoutComponent` includes the current close and reads no highs, so it sits at +sf on every break whatever its size. Weighted sums, differences, negation or clipping of the existing components cannot produce this distance.
