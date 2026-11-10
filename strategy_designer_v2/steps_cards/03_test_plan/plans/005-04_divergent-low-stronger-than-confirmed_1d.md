---
idea: 005-04_divergent-low-stronger-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price closes at a new N-bar low -> adapted: graded as the close's position in its 14-bar close range (`DonchianBreakoutComponent`), near -sf at a new low.
- Comparison: RSI at this low is above its prior low, versus RSI also at a new low -> replaced: no component gives where RSI sits relative to its own recent low; RSI level alone is a different quantity.
- Outcome: price rises more after divergent lows than after confirming lows -> adapted: "after the low" becomes "while price sits at its low", with no holding period.
- Verdict transfer: no: without RSI's own recent low, the test cannot separate divergent lows from confirming lows, which is the idea's comparison.
Reason: The config could hold the idea from one coin's closes alone. The forecast would be RSI's position in its own recent range minus price's position in its own range, gated to new price lows. No catalogue component gives RSI's position in its own range. `percentile` on the RSI history is a second history op, which V15 refuses next to `standardise`, and in the detector it only gives an on/off gate. RSI level (`RSIPullbackComponent`) measures oversold depth, not whether RSI made a higher low.
