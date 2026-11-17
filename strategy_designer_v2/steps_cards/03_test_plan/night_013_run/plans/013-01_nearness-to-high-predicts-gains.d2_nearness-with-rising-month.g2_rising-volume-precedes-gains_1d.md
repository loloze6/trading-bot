---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g2_rising-volume-precedes-gains
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: the coin's traded volume over the past 5 days -> replaced: no catalogue component reads volume in graded form.
- Comparison: that volume relative to the coin's volume over the past 30 days -> replaced: no component averages volume over two windows or takes their ratio.
- Outcome: higher return over the next 7 days (7 bars), rising with the ratio -> kept.
- Verdict transfer: no: without a volume measure, any forecast would test a different quantity, not participation.
Reason: The idea needs only the coin's own `volume` column, and a graded ratio fits the config's logic. But only one catalogue component reads volume: `VolumeExpansionHedgeComponent`, which is on/off, fires only on low-volume up bars, and compares against a 24-bar mean. The `volume_filter` op is a dead zone against a 20-bar mean and is refused in `strategies`. Neither can be combined into a 5-day over 30-day volume ratio.
