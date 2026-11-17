---
idea: 003-03_heavy-volume-rise-continues
brief: 003_volume-separates-reversal-from-continuation
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a sharp one-day rise on volume well above its 30-day average -> replaced: the rise can be measured, but the volume can only be an on/off above-average gate (`volume_filter` in a veto), not a graded measure.
- Comparison: the day's volume against its own 30-day average daily volume, heavier meaning larger gain -> replaced: no catalogue component outputs a graded volume-to-average ratio.
- Outcome: price keeps rising over the next 5 days, more after larger, heavier-volume rises -> adapted: "after" becomes "while" and the 5-day hold is dropped.
- Verdict transfer: no: without a graded volume ratio, the test cannot check that heavier volume brings a larger further gain.
Reason: The idea needs the day's volume against its own 30-day average, graded, so that heavier volume gives a larger position. The volume column is in the coin's own bars, but no catalogue component computes this ratio. `volume_filter` only tests "volume at or above its mean" (on/off, and refused in `strategies`), and `VolumeExpansionHedgeComponent` is on/off and fires only on low-volume up bars.
