---
idea: 005-04_divergent-low-stronger-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: a new price low where RSI holds above its own prior low -> replaced: no component measures RSI against its own recent low.
- Comparison: divergent new lows against new lows that RSI confirms -> replaced: needs the same missing RSI-versus-its-past reading.
- Outcome: price rises more after divergent lows than after confirmed lows -> kept: long position sized by the divergence's strength, judged on later returns.
- Verdict transfer: no: without a reading of RSI against its own prior low, no config can tell a divergent low from a confirmed one.
Reason: The new price low can be read from the bars with `DonchianBreakoutComponent` (close at the bottom of its range), and the rest could be held as a regime (price at a new low) plus a graded long component. But no component compares RSI with its own recent low. `RSIPullbackComponent` gives only the RSI level, and `standardise` must be the only history op, so the RSI history cannot be ranked or differenced to find its range position or its change.
