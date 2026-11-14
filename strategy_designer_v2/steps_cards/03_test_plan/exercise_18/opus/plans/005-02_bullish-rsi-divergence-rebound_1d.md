---
idea: 005-02_bullish-rsi-divergence-rebound
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low below its previous swing low -> replaced: no component finds swing lows; the Donchian range position only shows nearness to the window low.
- Comparison: RSI at the new low against RSI at the previous price low (a higher low) -> replaced: no component keeps RSI at a past pivot; the current RSI level is a different quantity.
- Outcome: price rebounds and recovers part of the decline (long) -> kept: a long forecast scored on the forward return.
- Verdict transfer: no: a mix of range position and current RSI level is not a two-pivot divergence, so neither result would carry over to the idea.
Reason: The idea compares RSI at two price swing lows, and those lows have to be found and remembered. Only the coin's own closes are needed, and a per-bar graded value could carry it. No catalogue component finds pivots or keeps an indicator's value at a past pivot. Combining DonchianBreakoutComponent with RSIPullbackComponent only weighs how deep price sits in its range against today's RSI, which replaces the comparison rather than building it.
