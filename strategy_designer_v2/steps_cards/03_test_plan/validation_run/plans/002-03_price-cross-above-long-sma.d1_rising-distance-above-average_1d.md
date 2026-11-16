---
idea: 002-03_price-cross-above-long-sma.d1_rising-distance-above-average
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: close above its long SMA, and the distance from it widening over recent bars -> replaced: no component measures how the distance from the SMA changes over n bars.
- Comparison: widening against narrowing distance, and both against holding the coin -> kept: the narrowing bars are left flat, and the book is judged against holding the coin.
- Outcome: the price drifts upward, more when the distance is larger -> kept: a long position graded by the SMA distance, scored on forward returns.
- Verdict transfer: no: with the widening condition replaced by a proxy, a confirm or reject would not be about widening distance.
Reason: The idea needs the change in (close - SMA)/SMA over the last few bars, and its sign, from the coin's own closes. A regime rule could gate on it, with a graded `MovingAverageDistanceComponent` (sma 200, clipped at 0) sizing the long. No catalogue component outputs that change, and rules cannot compare two components. `PriceEvolutionComponent` minus `MovingAverageSlopeComponent` is distorted once each is standardised on its own past. `MovingAverageDistanceComponent` at period 10 measures distance from a short average, not widening.
