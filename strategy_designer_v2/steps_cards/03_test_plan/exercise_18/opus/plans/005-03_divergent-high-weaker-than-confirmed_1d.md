---
idea: 005-03_divergent-high-weaker-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price at a new high while RSI's high is below its prior high -> replaced: no component compares RSI with its own earlier peak; RSI level or price-range position alone would replace it.
- Comparison: new highs with a lower RSI high vs new highs with a confirming RSI high -> replaced: the same missing RSI-peak reading is needed to split the two kinds of new high.
- Outcome: weaker returns, a reversal down, after diverging highs -> adapted: a graded short position held while the divergence lasts, judged on the following bars.
- Verdict transfer: no: without a measure of RSI against its prior high, a test would judge RSI level or price position, not divergence.
Reason: The idea needs RSI compared with its own recent peak, set against price compared with its recent peak, all from one coin's closes. The catalogue has price-range position (`DonchianBreakoutComponent`) and RSI level (`RSIPullbackComponent`), but nothing that ranks RSI within its own recent range. Combining RSI level with Donchian, or applying `standardise`, does not yield a rolling RSI maximum, so the divergence cannot be built.
