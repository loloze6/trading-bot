---
idea: 013-04_heavy-volume-below-high-breakout
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: the coin closes above its prior 52-week high -> kept: a regime rule on `DistanceFromHighComponent` (365 bars) at 0, or `BarsSinceHighComponent` (lookback 365).
- Comparison: volume over the preceding 10 days, relative to its own 90-day average -> replaced: no catalogue component computes a 10-day versus 90-day volume ratio.
- Outcome: return over the next 30 days is larger, upward -> adapted: the 30-bar hold becomes "while" the break holds, and the return is judged over a 30-bar horizon.
- Verdict transfer: no: without the volume ratio, the graded strength the idea ranks breaks by cannot be measured.
Reason: The 52-week-high break can be built as a regime from closes. The idea's graded strength cannot: heavier 10-day volume against the 90-day average needs the volume column, which only on/off parts read. `VolumeExpansionHedgeComponent` is on/off, and the `volume_filter` op only compares one bar's volume with its own average. No composition of the components yields a graded volume ratio.
