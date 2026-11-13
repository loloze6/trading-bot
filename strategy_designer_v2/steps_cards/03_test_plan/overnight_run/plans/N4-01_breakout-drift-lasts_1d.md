---
idea: N4-01_breakout-drift-lasts
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: untestable
---
Fidelity:
- Situation: a close at the highest close of the prior 20 days, on an up day -> adapted: graded as where the close sits in its 20-day range.
- Comparison: the rise persists on later days that close back below the new high -> replaced: only days still near the high could carry a position.
- Outcome: price keeps rising over the next ten or more days -> adapted: holding period dropped, measured only while near the high.
- Verdict transfer: no: the idea is about holding through the days after the high, which a per-bar forecast cannot do.
Reason: The idea says the rise continues on the days after the new high, even when those days close below it. Testing that needs a position held for one to two weeks after the event. The config cannot express time-based holds or bars since an event: the position exists only while the bar's own forecast shows the situation.
