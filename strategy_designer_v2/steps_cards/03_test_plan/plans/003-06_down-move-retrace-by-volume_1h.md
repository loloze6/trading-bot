---
idea: 003-06_down-move-retrace-by-volume
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: a sharp downward move of a given size -> kept: a graded drop size from PriceEvolutionComponent, with a `clip` so only drops count.
- Comparison: the same move on low volume against high volume -> replaced: no component grades the volume of the move against its usual level, and `volume_filter` only gives an on/off reading of the current bar.
- Outcome: thin drops give back more of the drop than heavy drops, which hold -> kept: a graded long position after a drop, judged on the following bars.
- Verdict transfer: no: without a graded volume reading over the move's bars, the test cannot split drops by volume, so neither result would speak to the idea.
Reason: The idea needs the move's volume relative to its usual level, graded, over the same bars as the drop, to size a contrarian long; the data is in the coin's own bars, but no catalogue component computes it. A detector veto using `volume_filter` reads only the current bar's volume, on or off, so it misses the volume of multi-bar moves and loses the regime once the move ends.
