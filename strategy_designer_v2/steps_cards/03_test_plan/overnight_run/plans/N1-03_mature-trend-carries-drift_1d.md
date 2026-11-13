---
idea: N1-03_mature-trend-carries-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: the close has stayed above its 200-day SMA for more than about 20 consecutive bars, versus the first 5–20 bars after a cross -> replaced: the catalogue has only the distance from the SMA, not how long the episode has lasted.
- Comparison: the coin's average 20-bar return -> kept: judged against holding the coin over all windows.
- Outcome: the coin rises more than its average over the next 20 bars, long side -> adapted: the 20-bar hold is dropped; gains are counted while the position is held.
- Verdict transfer: no: distance above the SMA is not the episode's age, so a large distance can also mark a fresh, steep cross, and the test would not separate mature episodes from new ones.
Reason: The idea's situation is the age of an above-SMA200 episode, which is the number of consecutive bars the close has spent above its 200-day SMA. That count can be computed from the coin's own closes, and the config could use it as a regime rule (age at least 20) or as a graded input. No catalogue component counts bars since a cross or the length of an episode. Combining distance, range-position or trend-fit components does not give it.
