---
idea: 005-02_bullish-rsi-divergence-rebound
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price closes at a new low -> kept: DonchianBreakoutComponent gives the close's place in its range, lowest at a new low.
- Comparison: RSI at this low is higher than RSI at the previous price low -> replaced: the catalogue has only the current RSI level, with nothing that recalls RSI at an earlier price low.
- Outcome: price rebounds and recovers part of the decline -> adapted: a long position graded by divergence strength, judged on returns over a fixed horizon.
- Verdict transfer: no: with RSI level in place of RSI at the prior low, the test would measure RSI extremes at new lows, which the brief rules out as a different question.
Reason: The divergence compares RSI now with RSI at the previous price low. That needs the RSI value at an earlier pivot, and no component or combination provides it. The data is all in the coin's own closes, and a per-bar graded value could carry it, but no catalogue component computes it.
