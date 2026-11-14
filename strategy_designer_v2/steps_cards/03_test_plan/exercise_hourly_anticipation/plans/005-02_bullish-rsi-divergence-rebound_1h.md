---
idea: 005-02_bullish-rsi-divergence-rebound
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1h
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low while RSI makes a higher low -> replaced: no component compares RSI at two price lows, only price range position or RSI level.
- Comparison: RSI now vs RSI at the previous price low; divergence vs no divergence -> replaced: the closest available is RSI distance from 50, not RSI against its own earlier low.
- Outcome: price rebounds, recovering part of the decline, long side -> kept: a graded long forecast judged on later returns.
- Verdict transfer: no: a test of "price at range low with RSI not oversold" neither confirms nor rejects RSI divergence at successive lows.
Reason: The divergence uses only the coin's own closes, and the config could hold it as one graded long signal. But no catalogue component tracks RSI at the previous price low or compares it with RSI at the new low. Combining DonchianBreakoutComponent with RSIPullbackComponent compares RSI with 50, not with its prior low, so it replaces the idea rather than building it.
