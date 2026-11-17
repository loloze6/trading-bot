---
idea: 010-01_rsi-above-share-continuation
brief: 010_rsi-midline-regime-direction
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: the share of the past 30 days that the coin's 14-day RSI spent above 50 -> replaced: no component counts the bars RSI spent above 50; only the current RSI level exists.
- Comparison: a larger share against a smaller share of time above the midpoint -> kept
- Outcome: a higher return over the next 14 days, upward with the share -> kept
- Verdict transfer: no: a test on the current RSI level, or on any smoothing of it, measures a different quantity from time spent above 50.
Reason: The situation needs a 30-bar count of the days on which the 14-day RSI closed above 50, computed from the coin's own closes. The catalogue has only the current RSI (`RSIPullbackComponent`), and no combination of components or transforms can count its past side; `standardise` must be the only history op, so not even an average of RSI can be built.
