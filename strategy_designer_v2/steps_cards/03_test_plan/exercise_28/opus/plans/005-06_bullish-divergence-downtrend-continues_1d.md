---
idea: 005-06_bullish-divergence-downtrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low while RSI makes a higher low -> replaced: no component measures RSI against its own earlier low, so only RSI's level could stand in for it.
- Comparison: the new price low against the earlier price low, and the RSI low against the earlier RSI low -> replaced: the catalogue has a price-range position (Donchian) but no RSI-range position.
- Outcome: price keeps falling to further lows -> kept: a short position that grows with the divergence, judged on later returns.
- Verdict transfer: no: a mix of "close near its range low" and "RSI level" is not a divergence, so neither result would carry over to the idea.
Reason: The divergence needs RSI compared with its own earlier low, which can be computed from the coin's closes alone. No component does this, and none can be combined to do it: `DonchianBreakoutComponent` ranks closes only, `RSIPullbackComponent` gives the RSI level, and `standardise` must be the only history op in a pipeline, so the stored RSI history cannot be ranked by percentile.
