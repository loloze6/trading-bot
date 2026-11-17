---
idea: 013-03_breakout-above-high-continues
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a close above the prior 52-week (365-bar) high, graded by how far above it closes -> replaced: no catalogue component measures distance above the prior high; `DistanceFromHighComponent` includes the current bar and so reads 0 at any new high, and `DonchianBreakoutComponent` sits at +sf on every new high.
- Comparison: further above the high versus only just above it -> kept: a graded size would carry it, if the situation could be measured.
- Outcome: a larger return over the next 30 days (30 bars), upward -> adapted: the 30-day hold is dropped, and the outcome is measured on 30-bar forward returns.
- Verdict transfer: no: a substitute such as the one-day return or the Donchian position does not measure distance above the prior high, so its result would not confirm or reject the idea.
Reason: The idea needs the close's distance above the highest of the prior 365 closes, with the current bar excluded. This is computable from the coin's own closes, and a graded component in a regime gated by `BarsSinceHighComponent` could hold it. No catalogue component outputs it, alone or combined: no component excludes the current bar, `DistanceFromHigh` is never positive, and `Donchian` saturates at a new high.
