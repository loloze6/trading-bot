---
idea: 022-01_learned-combined-signal-score
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: af2e424c34f8
---
Fidelity:
- Situation: the four signals combined into one score, each weighted by its past 365-day predictive power, relearned daily -> kept
- Comparison: a higher score against a lower one -> kept
- Outcome: the coin's return over the next 5 days is higher the higher the score -> kept
- Verdict transfer: yes: the catalogue's composite computes exactly these four signals, these weights and this daily relearning, and the test measures the stated graded 5-day relation.
Forecast: The forecast uses one component, PastPredictivePowerWeightedCompositeComponent with weighting "correlation" and the brief's settings (28-day return, 1-day reversal, 90-day high, 30-day volatility, 365-day z-score and training window, 5-day horizon). Each bar, each signal's z-score is weighted by its correlation with the coin's own 5-day returns over the past 365 days. The weighted sum is divided by the sum of the absolute weights. The score is standardised against its own past 365 values, with no dead zone and no regime. The forecast is positive (long) when the composite score is positive, negative (short) when it is negative, and its size grows in proportion to the score.
Config: 022-01_learned-combined-signal-score_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are the non-overlapping 5-bar grid within each window (positions 0, 5, 10, ...), on bars where the forecast is not zero. For each case, compute the forecast / 10 × (the coin's 5-day return − the coin's mean 5-day return over all its windows). The measure is the mean of this across cases, with its t-statistic. This is the gain beyond holding the coin, and it grows with the size of the position.
- Supporting check: none
- Confirm: The mean is above 0 with t ≥ 2, before costs.
- Reject: The mean is below 0 with t ≤ -2, before costs.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is any result with fewer than 100 cases with a non-zero forecast.
