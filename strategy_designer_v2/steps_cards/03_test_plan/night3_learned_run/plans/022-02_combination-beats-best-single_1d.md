---
idea: 022-02_combination-beats-best-single
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the coin's relearned combined score of its 28-day return, 1-day return, closeness to its 90-day high and 30-day volatility -> replaced: config weights are fixed numbers, and no component relearns them from past predictive success.
- Comparison: the score of whichever single signal has predicted best -> replaced: no component picks the past best signal, and one config gives one forecast, not two side by side.
- Outcome: the 5-day return lines up more closely with the combined score than with the best single score -> kept: 5 bars of the forecast against the next 5-day return.
- Verdict transfer: no: a fixed-weight blend tested alone says nothing about a relearned combination beating the past-best single signal.
Reason: The four single signals exist in the catalogue (`PriceEvolutionComponent` 28 and 1, `DistanceFromHighComponent` 90 proximity, `VolatilityFromStdDevComponent` 30). Weights learned from each signal's past link to 5-day returns, and the pick of the past-best signal, can be computed from one coin's own closes. No component or composition computes them: weights are fixed constants and no transform measures a signal's past predictive success.
