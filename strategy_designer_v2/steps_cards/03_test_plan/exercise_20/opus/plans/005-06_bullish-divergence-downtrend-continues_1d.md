---
idea: 005-06_bullish-divergence-downtrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low while RSI makes a higher low -> replaced: no catalogue component measures RSI against its own earlier low; only the price half (Donchian range position) exists.
- Comparison: new lows without RSI divergence, and simply holding the coin -> kept: the criterion can set divergence bars against plain new-low bars and against holding.
- Outcome: price keeps falling to further lows -> kept: a short position that grows with the divergence's strength.
- Verdict transfer: no: without RSI's own trough, any proxy (such as a raw RSI level at a price low) tests a different situation.
Reason: The price half is computable: DonchianBreakoutComponent shows the close at its range low. Nothing gives RSI's position relative to its own recent low, and no transform can supply it, because only one history op (`standardise`) is allowed. The data is all in the coin's closes, and a regime rule or score_product could hold "price at its low × RSI above its low", so only the component is missing.
