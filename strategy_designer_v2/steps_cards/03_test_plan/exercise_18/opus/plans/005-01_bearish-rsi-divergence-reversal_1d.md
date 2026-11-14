---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new high over its recent range -> adapted: graded by where the close sits in its range (Donchian position), not a yes/no new-high event.
- Comparison: RSI now is lower than RSI at the previous price high -> replaced: the catalogue gives only the current RSI level, not RSI at the previous price peak.
- Outcome: price then falls and gives back part of the run-up -> adapted: a graded short held while the signal lasts, with no fixed holding period.
- Verdict transfer: no: a test of current RSI level at a range high does not test RSI falling short of its value at the prior peak, so neither result would settle the idea.
Reason: The idea compares RSI at two price peaks, which needs RSI's value at the previous swing high. No catalogue component stores or looks up RSI at a past price peak, alone or combined. Using the current RSI level, or a range position minus RSI, would replace the comparison. All the data is in the coin's own closes, and a graded per-bar value could hold it.
