---
idea: 005-02_bullish-rsi-divergence-rebound
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: close makes a new 30-day low while 14-day RSI is above its reading at the previous low in that window -> adapted: the new low is made graded as the close's position in its 30-bar range (Donchian, period 30); the RSI condition is in the comparison line.
- Comparison: current 14-day RSI against the RSI at the window's previous low, a larger gap meaning a stronger signal -> replaced: no component records the RSI at an earlier swing low, and current RSI alone is the level the brief excludes.
- Outcome: price rebounds over the next 10 days, more when the RSI gap is larger -> kept: the 10-bar forward return, long, measured on 1d bars.
- Verdict transfer: no: without the RSI-at-previous-low reading, the test would measure RSI level near a low, not divergence.
Reason: The divergence needs the 14-day RSI at the bar of the earlier 30-day low compared with the current RSI. That comes from the coin's own closes, but no catalogue component stores or looks up a past swing point's RSI. Combining the Donchian range position with the RSI pullback only gives the current RSI level, which the brief rules out.
