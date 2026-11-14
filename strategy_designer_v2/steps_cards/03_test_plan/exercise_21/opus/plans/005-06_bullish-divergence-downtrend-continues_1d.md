---
idea: 005-06_bullish-divergence-downtrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price at a new low while RSI makes a higher low -> replaced: the catalogue measures the price low (Donchian) but not RSI's prior low, so the divergence itself cannot be built.
- Comparison: new lows with divergence against new lows without it -> kept: a zero forecast on non-divergent lows would give that contrast.
- Outcome: price keeps falling to further lows -> kept: a short position, graded by divergence strength, gains when price falls.
- Verdict transfer: no: without an RSI higher-low measure, a substitute like RSI's level or rank against its history tests RSI extremes, which the brief excludes.
Reason: A bullish divergence compares RSI at the current price low with RSI at the earlier low in the same window. No component outputs RSI's own rolling low or its position in its recent range, and no combination supplies it. Weighted sums cannot form the needed interaction, and `percentile` on RSI ranks it against its whole history, not against the prior swing low.
