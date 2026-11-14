---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new high -> kept: `DonchianBreakoutComponent` grades how close the close is to its recent high.
- Comparison: current RSI lower than the RSI at the previous price high -> replaced: no component stores the RSI at the prior swing high, and current RSI against 50 is a different quantity.
- Outcome: price falls back after the high, retracing part of the run-up -> kept: a short position graded by divergence strength, judged on the following bars.
- Verdict transfer: no: without the RSI at the prior peak, the test would measure overbought momentum at highs, not divergence.
Reason: The idea compares today's RSI with the RSI recorded at the previous price high. Every input for that is in the coin's own closes, but no catalogue component or transform gives a rolling maximum or a value taken at a past swing high. Combining Donchian with `RSIPullbackComponent`, by weighted mean or by a score_product regime, only compares current RSI with 50, so the comparison would be replaced.
