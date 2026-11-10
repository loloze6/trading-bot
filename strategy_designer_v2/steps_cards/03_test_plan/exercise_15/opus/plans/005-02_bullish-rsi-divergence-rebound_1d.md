---
idea: 005-02_bullish-rsi-divergence-rebound
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low -> adapted: graded as where the close sits in its recent range (DonchianBreakoutComponent, flipped).
- Comparison: RSI now vs RSI at the previous price low (higher low) -> replaced: the catalogue only gives the current RSI level, not its value at the prior swing low.
- Outcome: price rebounds and recovers part of the decline -> adapted: long while the divergence holds, with no holding period.
- Verdict transfer: no: without RSI at the prior low there is no divergence, only "price low while RSI is not low", which is a different signal.
Reason: The divergence compares RSI at the current price low with RSI at the previous swing low, which can be computed from the coin's own closes. No catalogue component, alone or combined, finds the prior swing low or reads RSI there. Pairing Donchian position with the RSI level against 50 replaces that comparison instead of measuring it.
