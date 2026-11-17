---
idea: 012-04_flush-depth-retracement-size
brief: 012_liquidation-flush-partial-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a bar that falls sharply, on a volume burst, with a long lower wick -> adapted: the three on/off conditions would become a regime gate on graded measures, but no catalogue component computes the volume burst or the wick.
- Comparison: the larger the bar's drop from its open to its low -> kept: it would be a graded forecast, but no catalogue component reads the open and the low.
- Outcome: a larger price rise over the next 3 days (3 bars) -> kept: a long position, measured over 3 bars.
- Verdict transfer: no: no config can be built from the catalogue, so nothing would be tested.
Reason: Every part lives in the coin's own bars (open, high, low, close, volume), and the config could hold it as a regime gate plus a graded forecast. But no catalogue component measures a volume burst, a lower wick or an open-to-low drop. The only volume reader, VolumeExpansionHedgeComponent, is on/off and fires on low-volume up bars. No component reads the open, and none measures a bar's own low against its close. No combination of the existing components rebuilds these from the bar columns.
