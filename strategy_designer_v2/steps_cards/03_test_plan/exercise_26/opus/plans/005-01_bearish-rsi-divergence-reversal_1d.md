---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new high while RSI makes a lower high -> replaced: no component reads RSI at a past price high, so only RSI level or range position is available.
- Comparison: current RSI peak against RSI at the previous price high -> replaced: no component or op gives a lagged or pivot-referenced RSI value.
- Outcome: price then falls back, retracing part of the run-up -> kept: a short forecast judged on the following returns.
- Verdict transfer: no: a test of RSI level or range position would not measure divergence, so neither its confirm nor its reject would carry over to the idea.
Reason: The divergence needs the coin's closes only, and a graded forecast could hold it. No catalogue component, alone or composed by weights, negate, clip or signed_power, gives RSI at the previous price high or the gap between that RSI and the current one. `RSIPullbackComponent` gives only the current RSI level, and the transforms have no lag or difference op.
