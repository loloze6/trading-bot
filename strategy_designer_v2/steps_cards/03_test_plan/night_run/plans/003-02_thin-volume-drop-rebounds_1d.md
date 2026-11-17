---
idea: 003-02_thin-volume-drop-rebounds
brief: 003_volume-separates-reversal-from-continuation
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a sharp one-day fall on a coin -> adapted: graded by the size of the one-day fall, measured against the coin's usual daily move, instead of a "sharp" threshold.
- Comparison: that day's volume well below the coin's own 30-day average daily volume, and the thinner the volume the larger the rebound -> kept in principle, but no catalogue component grades volume against its 30-day average.
- Outcome: the price wins back part of the fall over the next 5 days (up) -> adapted: the long position is held while the situation lasts, and the 5-day holding period is dropped.
- Verdict transfer: no: without a graded measure of volume against its 30-day average, the thin-volume condition and its size cannot be built, so no test of this idea can be read as its verdict.
Reason: Volume is in the coin's own bars, and a graded volume-thinness measure could be weighted against the one-day fall. But the only volume components are refused or unfit. `VolumeExpansionHedgeComponent` is on/off and fires only on up bars, and `volume_filter` is an on/off gate at the average, so neither can make the rebound grow with how thin the volume is, as the idea requires.
