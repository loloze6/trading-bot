---
idea: 005-02_bullish-rsi-divergence-rebound
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low while RSI makes a higher low -> replaced: no component finds the previous price low and the RSI reading there; Donchian position plus RSI level would measure a different thing.
- Comparison: RSI at the current low against RSI at the previous price low -> replaced: no component stores RSI at a past swing low; using the current RSI level instead is the RSI-extreme question the brief excludes.
- Outcome: price rebounds and recovers part of the decline (long) -> kept: the portfolio gains against holding over the following bars.
- Verdict transfer: no: a proxy built from range position and RSI level tests "price low but RSI not oversold", not the divergence between two lows.
Reason: The divergence needs the RSI value at the previous price low, compared with RSI at the new low. That is computable from one coin's closes, and a graded score fits the config's logic, but no catalogue component, alone or combined, locates a prior swing low or returns RSI's reading there. Combining DonchianBreakoutComponent with RSIPullbackComponent only gives the current RSI level, which replaces the comparison.
