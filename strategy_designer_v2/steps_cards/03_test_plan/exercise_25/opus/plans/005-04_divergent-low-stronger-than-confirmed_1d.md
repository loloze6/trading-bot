---
idea: 005-04_divergent-low-stronger-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: a new price low, with RSI making a higher low (versus RSI also making a new low) -> replaced: no component measures RSI against its own earlier low.
- Comparison: divergent new lows against new lows that RSI confirms -> replaced: needs RSI's position in its own range, which no component gives.
- Outcome: stronger (upward) returns after divergent lows than after confirmed lows -> kept: forward returns of the long position on 1d bars.
- Verdict transfer: no: RSI's level (`RSIPullbackComponent`) only measures RSI extremes, which the brief excludes, so it would not test the divergence.
Reason: The divergence compares RSI at the current price low with RSI at the earlier low, which needs the low of RSI over a window. The catalogue gives RSI only as a level, and `percentile` cannot be combined with `standardise` in a strategy component (V15), so no component or composition measures it. Everything needed is in each coin's own closes, and the config could hold it as a graded signal: price range position (`DonchianBreakoutComponent`) combined with an RSI range position.
