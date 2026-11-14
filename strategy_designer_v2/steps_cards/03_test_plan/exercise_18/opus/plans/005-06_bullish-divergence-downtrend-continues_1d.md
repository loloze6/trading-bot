---
idea: 005-06_bullish-divergence-downtrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price at a new low while RSI makes a higher low -> replaced: no component places RSI against its own earlier low, and RSI level or price momentum would be a different quantity.
- Comparison: today's RSI against RSI at the previous price low -> replaced: needs a rolling RSI trough, which no component or composition gives.
- Outcome: price keeps falling to further lows after the divergence -> kept: a short forecast, graded by divergence strength, is judged on later returns.
- Verdict transfer: no: a test built on RSI level or momentum near a price low would measure oversold continuation, not divergence.
Reason: The divergence needs RSI compared with its own recent low, alongside the close's position in its range. The catalogue has the price-range position (`DonchianBreakoutComponent`) and the RSI level (`RSIPullbackComponent`), but nothing for RSI's position against its own past trough. No weighted mix, negation or regime rule of the existing components yields it.
