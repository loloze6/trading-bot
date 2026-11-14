---
idea: 005-06_bullish-divergence-downtrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low while RSI makes a higher low (a bullish price-RSI divergence) -> replaced: the catalogue has the RSI level (`RSIPullbackComponent`, 50 - RSI) and the close's place in its range (`DonchianBreakoutComponent`), but nothing compares the current RSI low with RSI's earlier low. Any combination of the two would measure "price low while RSI is below or above 50", not the divergence.
- Comparison: the new price low is judged against the earlier price low, and the RSI low against the earlier RSI low -> replaced: the price half can be kept with Donchian's range position on closes. The RSI half has no counterpart, since no component places RSI within its own recent range or against its own prior trough.
- Outcome: price keeps falling to further lows after the divergence -> kept: this is a short position whose size grows with the divergence's strength, judged on the next bars' returns.
- Verdict transfer: no: a test built on RSI's level or price's range position alone would confirm or reject a statement about oversold lows, not about a higher RSI low under a lower price low.
Reason: The divergence uses only the coin's own closes, and the config could hold it as one graded short signal. No catalogue component, alone or combined, measures RSI against its own earlier low, so the "higher RSI low" half of the situation cannot be built. RSI level, the Donchian range position and RSI pullback measure different things.
