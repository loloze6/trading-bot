---
idea: 022-01_learned-combined-signal-score
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the coin's 28-day return, minus its 1-day return, its closeness to its 90-day high, and minus its 30-day volatility -> kept: PriceEvolutionComponent 28, PriceEvolutionComponent 1 negated, DistanceFromHighComponent 90 proximity, VolatilityFromStdDevComponent 30 negated.
- Comparison: each signal weighted by how well it predicted the coin's own 5-day returns over the past 365 days, relearned each day -> replaced: config weights are fixed numbers, and no component learns a weight from past predictive power.
- Outcome: the 5-day return is higher the higher the combined score -> kept: 5 bars on daily bars.
- Verdict transfer: no: with fixed weights the test measures a static blend, not the relearned weighting the idea is about.
Reason: Everything the idea needs comes from one coin's own closes: the four signals, and each signal's past relation to the coin's own later 5-day returns. But no catalogue component computes a weight from past predictive power, and a weighted mean with fixed weights cannot relearn it. Splitting it into four separately standardised components would also cancel the relative sizes of their weights, so it has to be one composite component.
