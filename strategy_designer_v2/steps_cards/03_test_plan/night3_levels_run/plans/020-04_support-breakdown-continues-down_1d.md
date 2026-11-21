---
idea: 020-04_support-breakdown-continues-down
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a daily close below a price where the coin turned up several times in the past 90 days -> replaced: no component finds repeated turning-up prices; the nearest is the break below the 90-day low, which ignores turns.
- Comparison: the more times the level held before, the larger the fall -> replaced: no component counts the past turns at a level; StallUnderHighCount counts bars near highs only.
- Outcome: keeps falling over the next 5 days -> kept: a short over 5 bars.
- Verdict transfer: no: a test of a break of the 90-day low, unweighted by the count of held turns, would neither confirm nor reject an idea about repeatedly defended levels.
Reason: The idea's level is a price where the coin turned up several times in the past 90 days, and its strength is how many times the level held. Both come from the coin's own high, low and close, and a graded component could hold them. No catalogue component, alone or combined, locates turning-up prices or counts the turns at a level. DistanceFromHigh (low) gives only the single lowest low, and StallUnderHighCount works only on the high side and counts bars, not turns.
