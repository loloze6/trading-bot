---
idea: 005-03_divergent-high-weaker-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: new price high whose RSI high is lower than the prior RSI high -> replaced: no catalogue component compares RSI with its own prior high.
- Comparison: returns after confirming highs, where RSI also makes a new high -> replaced: the RSI-new-high split needs the same missing measure.
- Outcome: weaker returns after divergent highs than after confirming highs -> kept: measurable as later returns grouped by the divergence size.
- Verdict transfer: no: without an RSI-versus-prior-RSI-high measure, any test would only check RSI level at highs, which is a different question.
Reason: Divergence needs RSI measured against its own recent high, beside the close's position in its recent range. The catalogue has the close's range position (`DonchianBreakoutComponent`) and the RSI level (`RSIPullbackComponent`), but nothing gives RSI's position in its own range. `standardise` is the only history op allowed in `strategies`, so `percentile` cannot rank RSI there. Detector rules compare raw values only, so they cannot express "RSI below its prior high" in graded form.
