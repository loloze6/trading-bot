---
idea: 005-06_bullish-divergence-downtrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1h
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price at a new low while RSI makes a higher low -> replaced: no component gives RSI's position against its own earlier low; Donchian gives only the price half.
- Comparison: the RSI low against its earlier low, beside the price low -> replaced: RSI level against 50 is the only RSI reading, not RSI against its own past low.
- Outcome: price keeps falling to further lows -> adapted: a graded short that grows with the divergence, held while it lasts, judged on forward returns.
- Verdict transfer: no: a test built on RSI's level would test something else, so neither result would carry over to the divergence idea.
Reason: The divergence needs RSI's position against its own recent low, set beside the close's position in its range. The catalogue has the price half (`DonchianBreakoutComponent`) but no component tracks RSI's rolling minimum or range. Weighted sums of Donchian with `RSIPullbackComponent` compare RSI to 50, not to its earlier low, so they replace the comparison. The config could hold the difference of two range positions as a graded short signal, but no component computes the RSI half.
