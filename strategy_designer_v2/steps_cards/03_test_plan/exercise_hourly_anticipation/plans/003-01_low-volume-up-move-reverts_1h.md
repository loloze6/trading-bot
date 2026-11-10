---
idea: 003-01_low-volume-up-move-reverts
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: sharp up move on unusually low volume -> replaced: the only volume test available is volume_filter, which checks "latest volume below its 20-bar mean" (most bars) and cannot measure "unusually" low.
- Comparison: the size of the rise, set against how much of it is given back -> kept: the forecast can be sized by the move's size.
- Outcome: price falls back, giving up part of the rise -> kept: a graded short after the up bar, scored on the returns that follow.
- Verdict transfer: no: a test on "below-average volume" covers most bars, so its result would not speak to unusually thin moves.
Reason: The idea needs to know how low the move's volume is relative to normal. The catalogue reads volume only through two things. VolumeExpansionHedgeComponent is on/off and refused as a forecast source. volume_filter is a fixed at-the-mean dead zone, allowed only in vetoes, and it cannot express "unusually" low or grade it. Combining these with the price components cannot give a graded or selectable relative-volume reading.
