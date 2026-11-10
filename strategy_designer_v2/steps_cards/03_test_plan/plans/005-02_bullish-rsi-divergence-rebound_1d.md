---
idea: 005-02_bullish-rsi-divergence-rebound
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low below its previous swing low -> adapted: graded as how far the close sits below the prior swing low's close.
- Comparison: RSI at this low against RSI at the previous price low -> replaced: no catalogue component gives RSI's value at a prior swing low, or RSI's change between two lows.
- Outcome: price rebounds and recovers part of the decline -> kept: a long position's gain over the next bars, measured against holding the coin.
- Verdict transfer: no: without the RSI-at-prior-low comparison, any catalogue proxy would test "price at range lows with RSI not oversold", not divergence.
Reason: The idea needs RSI compared between the current price low and the previous swing low. That comparison uses only the coin's closes, and a per-bar graded component could compute it. No catalogue component, alone or combined, does: RSIPullback gives only the current RSI, and no transform can look up or difference a past value of a component's history at a pivot.
