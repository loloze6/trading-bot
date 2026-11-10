---
idea: 005-03_divergent-high-weaker-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: a new price high reached with RSI below its own prior high -> replaced: no component compares RSI with its own recent high.
- Comparison: divergent new highs set against new highs where RSI also makes a new high -> kept: a rule on Donchian at its top selects new highs, and the RSI gap would separate the two groups.
- Outcome: weaker (more downward) returns after divergent highs -> kept: the forecast's sign and size, set against the next bars' returns.
- Verdict transfer: no: RSI level is the only stand-in, and it tests RSI extremes, which the brief rules out.
Reason: The idea needs today's RSI measured against RSI's own peak over the same window where price sets its new high. No catalogue component computes this. RSIPullbackComponent gives only the RSI level, and `standardise` must be the only history op in a forecast pipeline, so no rolling-max or rank of RSI can be built from the existing ops.
