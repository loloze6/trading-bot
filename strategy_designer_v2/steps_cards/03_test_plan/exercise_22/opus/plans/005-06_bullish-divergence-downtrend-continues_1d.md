---
idea: 005-06_bullish-divergence-downtrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price at a new low while RSI makes a higher low -> replaced: no component places RSI against its own earlier low.
- Comparison: the current RSI low against the RSI low at the prior price low -> replaced: nothing in the catalogue computes it.
- Outcome: price keeps falling to further lows -> kept: a short position graded by the divergence, judged on later returns.
- Verdict transfer: no: without the RSI-versus-its-own-low part, the test would measure "price near its range low", which is a different idea.
Reason: The idea needs RSI's position against its own recent low, compared with price's position against its own recent low. That data is in each coin's daily closes, and the config could hold it: a regime rule for price near its range low, plus a graded RSI-range component sized as a short. But no catalogue component gives RSI's rolling low or its place in its own range. `percentile` on the RSI history cannot sit next to `standardise` (V15), and no composition of the existing components rebuilds it.
