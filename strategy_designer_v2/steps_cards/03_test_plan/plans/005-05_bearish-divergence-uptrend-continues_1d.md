---
idea: 005-05_bearish-divergence-uptrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price at a new high while RSI makes a lower high -> kept: price's new high is `DonchianBreakoutComponent`, but no component computes RSI's lower high.
- Comparison: current RSI peak against RSI's prior peak, at the earlier price high -> replaced: only RSI's absolute level is available, not its prior peak.
- Outcome: price keeps rising to further highs (long) -> kept: a graded long position sized by divergence strength, judged on forward returns.
- Verdict transfer: no: RSI's level is not the same as RSI's distance below its own prior peak, so neither a confirm nor a reject would transfer.
Reason: A lower RSI high at a new price high needs RSI compared with its own recent maximum. The catalogue has RSI only as a level, and no component computes it against its own rolling high. Combining Donchian with RSI's level, or a percentile of RSI in a veto or score, measures "RSI not high", not "RSI below its prior peak", and `standardise` must be the only history op in a strategy pipeline.
