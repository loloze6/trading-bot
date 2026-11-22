---
idea: 023-03_flatter-range-stronger-reversion
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: the close's distance from the middle of its 30-day range -> kept: `DonchianBreakoutComponent` (period 30) gives the position of the close in its 30-bar range.
- Comparison: the 30-day net move relative to the 30-day range, smaller meaning stronger reversion -> replaced: no component gives net move over range, and the weighted sum cannot multiply it into the distance.
- Outcome: a move back toward the middle over the next 5 days -> kept: a contrarian forecast held 5 bars.
- Verdict transfer: no: efficiency ratio (net move over path length) or a threshold regime would test a different quantity from net move over range, graded.
Reason: The idea is an interaction: the contrarian range-position bet must grow as the 30-bar net move shrinks relative to the 30-bar range. The forecast is only a weighted sum of components, so it cannot form this product. No catalogue component measures net move over range, alone or combined.
