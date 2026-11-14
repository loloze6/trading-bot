---
idea: N1-02_above-rising-long-average
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: close above its 200-day SMA, and that SMA has risen over the last 20 bars -> replaced: the close-vs-SMA part is kept, but no component gives the SMA's 20-bar change.
- Comparison: trades above a rising SMA against those refused when the SMA is falling -> replaced: the rising/falling SMA split needs the same missing slope measure.
- Outcome: price keeps rising over the next weeks -> kept
- Verdict transfer: no: a proxy for the SMA slope, such as an SMA-pair spread, would test a different condition from "the 200-day SMA rose over 20 bars".
Reason: The 20-bar change of the 200-day SMA is computable from the coin's own closes. A regime rule (slope > 0) or a graded component could hold it. No catalogue component outputs it, and no combination recovers it. The exact identity mixes SMA20, SMA200 and SMA220 levels linearly, but the catalogue only gives normalised SMA distances or spreads, and `standardise` rescales each component separately, which breaks fixed linear weights.
