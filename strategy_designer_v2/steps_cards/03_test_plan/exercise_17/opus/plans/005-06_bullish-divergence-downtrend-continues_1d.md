---
idea: 005-06_bullish-divergence-downtrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price closes at a new N-bar low while RSI holds above its earlier low -> replaced: the catalogue has no measure of RSI's prior low or its range position, so only "price at range low" (Donchian) is buildable.
- Comparison: the current RSI low against RSI at the earlier price low -> replaced: no component stores or compares RSI swing lows.
- Outcome: price keeps falling to further lows (short, continuation) -> kept: a graded short position, judged on the next bars' returns.
- Verdict transfer: no: without the RSI higher-low part, the test would measure new lows alone, not divergence.
Reason: The divergence needs RSI compared with its own earlier low while the close sits at a new low. All of this is in each coin's own closes, and the config could hold it as a regime condition plus a graded short. But no catalogue component, alone or combined, gives RSI's past minimum or RSI's position in its own range. Weighted sums of Donchian and RSIPullback cannot express "RSI above its earlier low". A percentile of RSI in the detector would replace the higher-low comparison, not measure it.
