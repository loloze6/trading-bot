---
idea: 003-04_high-volume-down-move-continues
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: a sharp one-bar drop on unusually high volume -> replaced: the catalogue can only test volume above its plain mean (the `volume_filter` op in a veto), not volume that is unusually high.
- Comparison: volume judged against its own recent normal -> replaced: only an on/off "at or above the 20-bar mean" exists, with no measure of how far above.
- Outcome: price keeps falling over the next bars -> kept: a short position graded by the drop's size, judged on later returns.
- Verdict transfer: no: about half of all bars sit above mean volume, so a result would be about ordinary-volume drops, not unusual ones.
Reason: Relative volume, meaning the bar's volume compared with its recent average, can be computed from the coin's own bars. A regime rule on it ("relative volume >= 2") could hold the idea's condition, with a graded short sized by the one-bar drop inside that regime. But no component outputs volume in any graded form: `VolumeExpansionHedgeComponent` is on/off and fires on low-volume up bars, and `volume_filter` only gives above or below the mean. No combination can tell unusually high volume from ordinary above-average volume.
