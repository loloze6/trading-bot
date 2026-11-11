---
idea: 005-05_bearish-divergence-uptrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price at a new high while RSI makes a lower high -> replaced: price at its high is Donchian position, but no component measures the RSI shortfall from its own recent high.
- Comparison: current RSI against its high at the earlier price high -> replaced: no component or transform keeps RSI's rolling maximum or its earlier peak.
- Outcome: price keeps rising to further highs -> adapted: long while the divergence holds, judged on forward returns, with the holding period dropped.
- Verdict transfer: no: without the RSI lower-high measure, the test would not isolate divergent new highs from ordinary new highs.
Reason: The idea needs RSI to be measured against its own recent high, at the same time as price is at its recent high. Both come from one coin's closes, and a regime plus a graded component could hold the idea. No catalogue component computes RSI's rolling maximum or how far RSI sits below it. The available transforms cannot build it either: the `percentile` in a detector veto ranks against a history of uncontrolled length and cannot grade the shortfall, and `standardise` must be the only history op in a strategy pipeline.
