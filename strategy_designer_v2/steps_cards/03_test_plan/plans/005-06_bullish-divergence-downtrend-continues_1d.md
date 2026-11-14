---
idea: 005-06_bullish-divergence-downtrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low while RSI makes a higher low -> replaced: no component compares RSI with its own earlier low; only RSI's level is available.
- Comparison: current RSI low against the RSI low at the prior price low -> replaced: this would become an RSI level, not a comparison of two RSI lows.
- Outcome: price keeps falling to further lows -> kept: a short position gains when price falls over the next bars.
- Verdict transfer: no: a test on RSI level at a price low would test oversold readings, which the brief excludes, not divergence.
Reason: The divergence needs RSI now compared with RSI at the earlier price low, while price sits at a new low. No catalogue component gives RSI's position against its own recent low. `standardise` must be the only history op in a strategy's transforms, and regime rules compare raw values only, so no graded combination can build that comparison from the closes.
