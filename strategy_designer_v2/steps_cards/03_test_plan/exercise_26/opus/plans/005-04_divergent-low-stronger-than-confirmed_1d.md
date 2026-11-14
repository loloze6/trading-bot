---
idea: 005-04_divergent-low-stronger-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low while RSI makes a higher low -> replaced: no component places RSI within its own recent range, so "higher RSI low" cannot be measured.
- Comparison: new price lows where RSI also makes a new low -> replaced: depends on the same missing RSI-low reading.
- Outcome: returns after divergent lows are stronger (upward) -> adapted: "after the low" made "while price sits at its range low with RSI above its own low".
- Verdict transfer: no: substituting the RSI level (RSIPullback) for RSI relative to its earlier low would test oversold RSI, which the brief excludes.
Reason: The divergence needs RSI's position against its own recent low, set against price's position against its recent low (DonchianBreakoutComponent covers the price side). No catalogue component computes RSI's position in its own range, and no combination of RSIPullback, Donchian or the others gives it. The data is in the coin's own closes. A graded difference of the two range positions (weights +1 and -1) would fit the config's logic.
