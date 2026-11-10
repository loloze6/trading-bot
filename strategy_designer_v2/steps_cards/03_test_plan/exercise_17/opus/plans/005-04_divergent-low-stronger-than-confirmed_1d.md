---
idea: 005-04_divergent-low-stronger-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: the close makes a new low over a recent window -> adapted: graded as where the close sits in its range (Donchian position).
- Comparison: the RSI low against the RSI at the prior price low, higher or not -> replaced: no component places RSI against its own prior low; only the RSI level exists.
- Outcome: higher returns after divergent lows than after confirmed lows -> kept: forward returns of the position against holding the coin.
- Verdict transfer: no: RSI's level is not the same as RSI's position against its own prior low, and the brief excludes RSI extremes as the question.
Reason: The divergence is RSI not making a new low while price does. That needs RSI's position within its own recent range, set against price's position within its range. No catalogue component computes this. The standardise rule leaves no room for a second history op on an RSI history in strategies, so it cannot be composed there. A regime gate would only switch the position on and off and would not grade the divergence.
