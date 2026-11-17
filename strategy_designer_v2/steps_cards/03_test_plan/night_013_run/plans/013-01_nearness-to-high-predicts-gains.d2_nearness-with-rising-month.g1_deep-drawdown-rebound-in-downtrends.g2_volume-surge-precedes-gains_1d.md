---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: the coin's traded volume over the past day -> replaced: no graded component reads volume; only on/off volume gates exist (`VolumeExpansionHedgeComponent`, `volume_filter`).
- Comparison: that volume against its own average over the past 20 days -> replaced: no component or transform grades volume against its mean; `volume_filter` only gives at-or-above versus below.
- Outcome: a higher return over the next 7 days, rising with relative volume -> kept: the 7-day return is 7 daily bars of the coin's own closes.
- Verdict transfer: no: a volume gate would test a yes-or-no condition, not "the higher the volume ratio, the higher the return," so neither result would carry over to the idea.
Reason: The idea uses only the coin's own volume column, and a graded forecast could hold it. But no component in the catalogue computes a graded ratio of volume to its 20-day mean, and no composition of components or transforms can build one: none of them read volume except two refused on/off gates.
