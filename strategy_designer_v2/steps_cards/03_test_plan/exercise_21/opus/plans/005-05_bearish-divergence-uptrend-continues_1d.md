---
idea: 005-05_bearish-divergence-uptrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new high -> kept: the close at the top of its recent range (DonchianBreakoutComponent, rule on its raw value).
- Comparison: RSI's current high is below its own prior high -> replaced: no component places RSI against its own recent peak.
- Outcome: price keeps rising to further highs, long -> kept: long position, judged on forward returns against holding.
- Verdict transfer: no: RSI's level against 50 is not a lower high against its prior peak, so neither result would settle the idea.
Reason: The idea needs RSI compared with its own earlier peak. That uses only the coin's closes and could feed a regime plus a graded component. But the catalogue has only RSI's level (RSIPullbackComponent), and no op takes a rolling max, difference or range of another component's output, so no combination builds it.
