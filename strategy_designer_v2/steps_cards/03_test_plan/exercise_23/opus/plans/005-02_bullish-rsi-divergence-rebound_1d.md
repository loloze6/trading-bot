---
idea: 005-02_bullish-rsi-divergence-rebound
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low -> kept: the close's position at the bottom of its recent range (`DonchianBreakoutComponent`, negated) measures it.
- Comparison: RSI makes a higher low than at the previous price low -> replaced: no component reads RSI at the previous price low, so only the current RSI level could stand in for it.
- Outcome: price then rebounds and recovers part of the decline -> kept: a long position, graded, gains when price rises after the low.
- Verdict transfer: no: an RSI-level stand-in tests "new low while RSI is not oversold", not "RSI higher low than at the previous price low".
Reason: The divergence compares RSI now with RSI at the previous price swing low. That needs swing-low detection and a look-up of past RSI values from the coin's own closes, which no catalogue component computes. Sums of Donchian position and RSI level give a level, not a comparison, so they cannot rebuild it.
