---
idea: 005-06_bullish-divergence-downtrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low while RSI makes a higher low -> replaced: no component places RSI against its own earlier low.
- Comparison: the RSI low against the earlier RSI low, at a new price low -> replaced: only the RSI level (RSIPullback) exists, not RSI against its prior trough.
- Outcome: price keeps falling to further lows -> kept: a graded short sized by the divergence, judged on later returns.
- Verdict transfer: no: RSI level is a different quantity from a higher RSI low, so a result would not judge the divergence.
Reason: Price's place in its range is available (DonchianBreakoutComponent on closes), but no catalogued component measures where RSI sits relative to its own recent low. Weighted sums of the existing components cannot rebuild it, because RSI level is not RSI against its prior trough. Built from one coin's closes, such a component could feed a regime rule (price at the bottom of its range) with a graded short sized by how far RSI sits above its own low.
