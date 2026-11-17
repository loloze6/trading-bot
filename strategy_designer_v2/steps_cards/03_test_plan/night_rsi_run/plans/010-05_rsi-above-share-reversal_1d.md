---
idea: 010-05_rsi-above-share-reversal
brief: 010_rsi-midline-regime-direction
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: the share of the past 30 days that the coin's 14-day RSI spent above 50 -> replaced: no component counts the bars with RSI above 50, and the only nearby measure is the current RSI level.
- Comparison: a larger share against a smaller share -> kept: a graded forecast that grows with the share.
- Outcome: a lower return over the next 14 days, so the higher the share, the more short -> kept: a 14-bar horizon on daily bars with the forecast negated.
- Verdict transfer: no: the current RSI level, or a smoothed one, is a different quantity from the share of days above 50, so neither a confirm nor a reject would carry over to the idea.
Reason: The idea needs the fraction of the last 30 daily bars on which RSI(14) was above 50. No catalogue component outputs it. The transforms cannot build it either: there is no sign or indicator op, and `standardise` must be the only history op, which rules out averaging an RSI history. Everything needed is in the coin's own closes, so only the component is missing.
