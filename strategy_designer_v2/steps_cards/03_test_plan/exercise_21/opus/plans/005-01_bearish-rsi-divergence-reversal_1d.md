---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price closes at a new high -> kept: Donchian range position is +sf when the close is the highest of its window.
- Comparison: RSI's high now is lower than at the previous price high -> replaced: no component compares RSI with its own earlier peak; only the RSI level exists.
- Outcome: price falls back from the new high -> kept: a short forecast scored on the next bars' return.
- Verdict transfer: no: a "high price, low RSI" level proxy is not a lower RSI high than at the prior price peak, so neither verdict would carry over.
Reason: A divergence compares RSI at the current price high with RSI at the previous price high. That needs RSI's position within its own recent range, set against price's position within the same window. No catalogue component, alone or combined, gives RSI's range position or its value at the prior swing high. Weighting Donchian against RSIPullback measures "price high while RSI is low", which is a different quantity.
