---
idea: 022-03_combined-extremes-larger-moves
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: af2e424c34f8
---
Fidelity:
- Situation: a coin's combined score, learned from past predictive power, far from its usual value -> kept: the past-weighted composite of the four effects (z-scores weighted by their past correlation with 5-day returns), with the strongest graded dead zone.
- Comparison: the move after equally rare readings of each single signal -> kept: each single effect's own weighted term is recorded at weight 0, and its equally rare readings are compared.
- Outcome: the move over the next 5 days is larger, and grows the further out the score is -> kept: 5-bar move in the score's direction, graded by its size.
- Verdict transfer: yes: the same composite, the same singles and the same 5-day move are measured as the idea states them.
Forecast: The forecast is `PastPredictivePowerWeightedCompositeComponent` with "correlation" weighting at its default settings. These are: momentum over 28 days, a 1-day reversal, nearness to the 90-day high and 30-day volatility. Each signal is z-scored over 365 days, and each is weighted by its correlation with the next 5-day return over the past 365 days, relearned every bar. The composite is standardised over 455 bars, then passed through signed_power with exponent 3 and pivot 20. It is positive when the past-weighted effects point up and negative when they point down. It is near zero at usual readings and grows as the cube of the score's distance out, up to ±20. Four single-effect terms ("single" weighting, one per signal) run at weight 0. They do not move the forecast; they are recorded only for the comparison.
Config: 022-03_combined-extremes-larger-moves_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The measure uses non-overlapping 5-bar grid cells in every coin and window. On each cell, take the unusual move: the 5-day return minus the coin's mean 5-day return over all windows, signed by the reading's sign. Compare its mean on cells where abs(combined `last_history_value`) is in its top 10% (pooled over coins and windows) against its mean on each single signal's own top-10% cells. The comparison is combined minus the best single, by Welch t.
- Supporting check: Among all combined cells, regress the signed unusual move on abs(combined `post_pipeline_value`); the slope is positive.
- Confirm: Combined minus the best single has Welch t ≥ 2, combined beats every single signal, and the check's slope t ≥ 2.
- Reject: Combined minus the best single has Welch t ≤ -2, or the check's slope t ≤ -2.
- Inconclusive: Any other result, including differences near zero, is inconclusive. Each top-10% group needs at least 30 non-overlapping cases, else inconclusive.
