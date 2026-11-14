---
idea: 003-06_down-move-retrace-by-volume
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: a sharp one-day drop on BTC daily bars -> adapted: the threshold "sharp" becomes graded, using the size of the one-bar fall from `PriceEvolutionComponent` with period 1.
- Comparison: the drop's volume, unusually low versus unusually high, at a similar drop size -> replaced: the only volume tool is `volume_filter` in a veto, which gives just an above/below 20-bar-mean split.
- Outcome: thin drops give back more of the fall and heavy drops hold or continue -> adapted: a long position after thin drops and a short one after heavy drops, held while the situation lasts.
- Verdict transfer: no: a yes/no split at average volume cannot test whether reversion grows as volume gets unusually low, nor match drops of similar size.
Reason: Volume is in each coin's own bars, and the config could carry a graded relative-volume reading as a regime input or a component. But no catalogue component outputs volume relative to its average as a continuous value. `VolumeExpansionHedgeComponent` fires only on up bars and is on/off, and `volume_filter` is a dead-zone op that gives a yes/no split, so the graded volume comparison can only be replaced, never kept.
