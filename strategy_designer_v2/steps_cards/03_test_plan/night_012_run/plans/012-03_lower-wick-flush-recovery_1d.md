---
idea: 012-03_lower-wick-flush-recovery
brief: 012_liquidation-flush-partial-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: bars that fall sharply on a volume burst -> adapted: the fall in usual moves and volume at or above its 20-bar mean, as an on/off regime condition (veto with `volume_filter`).
- Comparison: the longer the lower wick below the close, as a share of the high-to-low range -> replaced: no component reads a bar's low against its range, so only a different quantity could stand in.
- Outcome: a larger price rise over the next 3 days -> kept: the 3-bar forward return on daily bars.
- Verdict transfer: no: without the wick share, the test could only show a rebound after sharp high-volume falls, not that it grows with the wick.
Reason: The idea's graded quantity is (close - low) / (high - low), the lower wick as a share of the bar's range, and no catalogue component computes it. Only ADX and Keltner read high and low, and they output a smoothed DI ratio and a distance from the EMA in ATR units, which no combination turns into one bar's wick share. The "extreme" size of the volume burst also has no graded measure: `volume_filter` only tests whether volume is at or above its mean.
