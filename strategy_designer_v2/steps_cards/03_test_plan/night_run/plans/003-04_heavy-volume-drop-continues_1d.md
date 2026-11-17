---
idea: 003-04_heavy-volume-drop-continues
brief: 003_volume-separates-reversal-from-continuation
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a sharp one-day fall on volume well above its 30-day average -> replaced: no catalogue component grades a bar's volume against its own 30-day average.
- Comparison: the day's volume against its own 30-day average daily volume, the heavier the stronger -> replaced: volume_filter and VolumeExpansionHedgeComponent are only on/off, and the latter fires only on low-volume up bars.
- Outcome: the coin keeps falling over the next 5 days, more after larger, heavier falls -> adapted: "after the fall" made "while the fall's reading holds", with the 5-day hold dropped.
- Verdict transfer: no: without a graded volume ratio, the test cannot weigh the position by how heavy the volume was, so its result would not bear on the idea.
Reason: The idea needs the day's volume divided by its 30-day average, as a graded value that sets the position's size, and it sits in each coin's own volume column. No catalogue component computes it, alone or in a combination. The only volume tools are on/off: a dead-zone transform that is barred from strategies, and a component that reads only low-volume up bars.
