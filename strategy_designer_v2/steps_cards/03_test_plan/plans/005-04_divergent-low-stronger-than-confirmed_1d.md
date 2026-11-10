---
idea: 005-04_divergent-low-stronger-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price closes at a new N-bar low -> kept: a regime rule on `DonchianBreakoutComponent` at the bottom of its range.
- Comparison: RSI at this low above RSI's own prior low (divergent) versus at a new RSI low (confirming) -> replaced: the catalogue has only the RSI level, not RSI's position against its own recent lows.
- Outcome: returns after divergent lows beat returns after confirming lows, upward -> adapted: "after the low" becomes "while the low holds", with no fixed holding period.
- Verdict transfer: no: an RSI level is not the same as RSI failing to make a new low, so neither result would carry over to the idea.
Reason: Detecting the divergence needs to know whether RSI made a new low over the same window in which price made one. No component measures where RSI sits inside its own recent range. Combining `RSIPullbackComponent` with `DonchianBreakoutComponent` through weights or `standardise` only rescales the RSI level and cannot recover its range position. Everything needed comes from the coin's own closes, and the config could hold the test: a regime for "close at its N-bar low", plus a graded forecast that is the RSI range position minus the price range position.
