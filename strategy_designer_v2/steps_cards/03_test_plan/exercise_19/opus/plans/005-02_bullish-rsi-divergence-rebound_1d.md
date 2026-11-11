---
idea: 005-02_bullish-rsi-divergence-rebound
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price at a new low while RSI is above its value at the prior price low -> replaced: the catalogue has only the RSI level and range position, not RSI at the prior low.
- Comparison: current RSI against RSI at the previous swing low in price -> replaced: no component finds the prior price low or stores RSI there.
- Outcome: price rebounds after the new low, recovering part of the decline (long) -> kept: a long position sized by the divergence, judged on later returns.
- Verdict transfer: no: a mix of RSI level and Donchian position does not identify divergences, so neither result would bear on the idea.
Reason: The idea needs RSI compared at two price swing lows. That means finding the previous low in the closes and reading RSI on that bar. No catalogue component does this, and no weighted sum of RSI level and range position can stand in for that two-point comparison. All the inputs are in the coin's own closes, and a stateless component over the bar window could compute it, so the gap is in the components, not in the config's logic.
