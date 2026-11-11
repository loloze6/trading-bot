---
idea: 005-02_bullish-rsi-divergence-rebound
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low while RSI makes a higher low -> replaced: no component measures it; the nearest, Donchian range position, drops the RSI condition.
- Comparison: RSI at this low versus RSI at the previous price low -> replaced: no component recalls RSI at an earlier swing low or ranks RSI within its own range.
- Outcome: price rebounds and recovers part of the decline into the low (up) -> kept
- Verdict transfer: no: a test on new lows or on RSI level alone measures RSI extremes or plain range position, which the brief excludes, so its result says nothing about divergence.
Reason: The divergence needs RSI at the current price low compared with RSI at the previous price low. Both come from the coin's own closes, and a graded value fits the config's logic. No catalogue component, alone or combined, measures RSI against its own past lows: Donchian ranks price only, and RSIPullback gives the RSI level only.
