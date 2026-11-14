---
idea: 005-03_divergent-high-weaker-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1h
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new high over a lookback window -> kept: DonchianBreakoutComponent gives where the close sits in its range, at +sf on a new high.
- Comparison: the RSI high at the new price high is below, or above, RSI's own prior high -> replaced: no component places RSI against its own recent high; only the RSI level (RSIPullbackComponent) exists.
- Outcome: returns after divergent highs are weaker (lower) than after confirmed highs -> kept: the forward return of a short position scaled by the divergence.
- Verdict transfer: no: using the RSI level in place of the RSI-versus-its-prior-high would test overbought RSI, which the brief says is not the question.
Reason: The divergence needs the position of RSI within its own recent range at the bar where price reaches its range high. All of this comes from one coin's closes and a graded config could hold it. But no catalogue component computes RSI against its own past high, and no composition can build it: the transforms work on a component's own history and cannot take a rolling max of RSI.
