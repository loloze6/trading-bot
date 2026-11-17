---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: daily close near its highest close of the past 20 days, on heavy volume -> kept for closeness (`DistanceFromHighComponent`, period 20); the volume part is not computable (see comparison).
- Comparison: that day's volume against its 30-day average volume -> replaced: no graded component reads volume against its average.
- Outcome: higher return over the next 7 days, upward -> kept: 7 bars on daily bars.
- Verdict transfer: no: without the volume ratio, the test would check closeness to the high alone, not the idea's joint condition.
Reason: Volume and its 30-day average are in each coin's own bars, and a weighted sum of components could hold them. But the only component that reads volume is `VolumeExpansionHedgeComponent`, which is on/off and fires only on low-volume up bars. `volume_filter` is a dead zone that is not allowed in `strategies`. So no graded measure of today's volume against its 30-day average can be built.
