---
idea: 005-04_divergent-low-stronger-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: close makes a new N-bar low -> adapted: graded by the close's position in its range (DonchianBreakoutComponent, negated).
- Comparison: RSI at that low is higher than at the prior low, versus RSI also at a new low -> replaced: no component places RSI against its own recent low, only against the fixed 50 (RSIPullbackComponent).
- Outcome: price rises more after divergent lows than after confirming lows -> kept: forward returns follow a long forecast, judged against holding the coin.
- Verdict transfer: no: measuring RSI against 50 instead of against its own prior low tests RSI level, not divergence, so neither a confirm nor a reject would carry over to the idea.
Reason: The divergence needs RSI measured against its own recent extremes, so that "price at its range low while RSI sits above its range low" can be scored. The config could hold this as a weighted difference (price range position minus RSI range position), but no catalogue component computes where RSI sits in its own recent range. RSIPullbackComponent only compares RSI with 50, which is the RSI-extremes question the brief excludes.
