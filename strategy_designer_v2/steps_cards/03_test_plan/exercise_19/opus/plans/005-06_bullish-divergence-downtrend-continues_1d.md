---
idea: 005-06_bullish-divergence-downtrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low while RSI makes a higher low -> replaced: no catalogue component compares RSI now with RSI at the prior price low.
- Comparison: RSI's current low against its own earlier low at the prior price low -> replaced: catalogue RSI is a level against 50, not against its own past low.
- Outcome: price keeps falling to further lows (short, continuation) -> kept: a short forecast on the divergence, judged on later returns.
- Verdict transfer: no: without the divergence measure, a test would judge new lows or RSI levels, not divergence.
Reason: The divergence needs RSI's position against its own recent low, set beside price's position in its range. `DonchianBreakoutComponent` covers the price side, but no component places RSI within its own recent range. A weighted mean of Donchian and `RSIPullbackComponent` would only compare RSI to 50. A regime rule could only compare RSI to a fixed level. Neither can express "higher low than before".
