---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new high -> adapted: graded as where the close sits in its recent range (DonchianBreakoutComponent), not a swing-high event.
- Comparison: RSI's peak now is lower than RSI at the previous price high -> replaced: no component stores RSI at a prior price peak, only the current RSI level.
- Outcome: price falls back and retraces part of the run-up -> adapted: a short forecast, graded by divergence size, held while the situation lasts; no fixed retracement target.
- Verdict transfer: no: RSI level next to a range high is not RSI's peak against its own previous peak, so neither result would settle the divergence idea.
Reason: The comparison needs RSI's value at the previous price swing high, set against RSI now while price exceeds that high. No catalogue component, alone or combined through weights, regimes or transforms, finds a prior price peak or recalls RSI there. Pairing RSI level with range position measures overbought-at-high, which the brief explicitly excludes.
