---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a coin's day volume, heavier relative to its own average -> replaced: no catalogue component reads volume as a graded level.
- Comparison: the coin's own 30-day average volume -> replaced: no component divides volume by its 30-bar mean, and `volume_filter` is an on/off dead zone that is refused in `strategies`.
- Outcome: a higher return over the next 3 days, long side -> kept: 3 bars on 1d bars.
- Verdict transfer: no: no catalogue quantity measures relative volume, so any config would test a different quantity.
Reason: The idea needs a graded ratio of the day's volume to its 30-day average, taken from the coin's own volume column. The only volume tools in the catalogue cannot supply it. `VolumeExpansionHedgeComponent` is on/off, fires only on low-volume up bars and is never positive. `volume_filter` is an on/off dead zone. No combination of components or transforms yields that ratio.
