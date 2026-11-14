---
idea: 005-04_divergent-low-stronger-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: the close makes a new N-bar low -> adapted: a regime rule on the Donchian position at the bottom of its range, "after" made "while".
- Comparison: the RSI low against the RSI at the prior low (higher low vs new low) -> kept in principle, but no component computes where RSI sits in its own recent range.
- Outcome: the price rises next, more after a divergent low than a confirming one -> kept: a graded long that grows as RSI sits further above its own range low.
- Verdict transfer: no: without the RSI-versus-its-prior-low measure, the divergent and confirming lows cannot be told apart.
Reason: The regime "close at its N-bar low" can be built from `DonchianBreakoutComponent`. No catalogue component, alone or combined, compares the current RSI with its own recent lows. `RSIPullbackComponent` gives only the RSI level, not whether RSI made a new low. A history op such as `percentile` on RSI cannot sit next to `standardise` (V15), and in `history_transforms` it sees a single value.
