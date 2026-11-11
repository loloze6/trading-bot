---
idea: 005-02_bullish-rsi-divergence-rebound
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low below the previous price low -> replaced: no component finds swing lows; only the close's place in its range exists, which is not a new low against a prior low.
- Comparison: RSI at the new low is higher than RSI at the previous price low -> replaced: no component keeps RSI's value at a past price low; RSI's current level is a different quantity.
- Outcome: price then rebounds and recovers part of the decline into the low -> adapted: a long position sized by the divergence, with the holding period dropped.
- Verdict transfer: no: a proxy built from range position and RSI level tests weak momentum near range lows, not a divergence between two price lows.
Reason: The idea compares RSI at two separate price lows, which needs the last two swing lows located in the coin's own closes and RSI read at each. No catalogue component, alone or combined, computes this. Donchian position minus RSI only measures the current RSI level, not the RSI at the prior low.
