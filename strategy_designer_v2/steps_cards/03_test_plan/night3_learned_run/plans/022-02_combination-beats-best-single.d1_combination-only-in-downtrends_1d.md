---
idea: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: the coin's 90-day return is negative, and more negative is a stronger case -> adapted: the negative 90-day return selects the regime, and the depth grading is checked in the criterion rather than sized.
- Comparison: the relearned combined score against the best single signal's score -> kept: the combined score is traded and the best-single score is rebuilt from prices with the same component's "best" weighting.
- Outcome: the next 5-day return lines up more closely with the combined score -> kept: forward 5-bar returns are compared with both scores on the decline bars.
- Verdict transfer: yes: both the combined-versus-best fit and its growth with the decline's depth are measured directly on the decline bars.
Forecast: A regime rule selects bars where the 90-day price change is below 0. On those bars the forecast is the relearned combined score, standardised. That score is `PastPredictivePowerWeightedCompositeComponent` with "correlation" weighting over four signals: the 28-day return, the reversed 1-day return, the closeness to the 90-day high and the negated 30-day volatility. Each signal's z-score is weighted by its correlation with the 5-day forward return over the past 365 days. The forecast is positive when the weighted signals point up and negative when they point down. Its size grows with the score's strength, and it is capped at ±20. On all other bars the forecast is 0 (flat).
Config: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The sample is the regime "mean_reversion" bars on a non-overlapping 5-bar grid per window. For each case, take r = the 5-bar forward return minus the coin's mean 5-bar return over all windows (holding the coin). Divide zc = combo's post_pipeline_value by its standard deviation across the cases. Divide zb = the "best"-weighting composite, recomputed from prices with the same settings, by its standard deviation the same way. The per-case value is (zc − zb) × r. Measure the t of its mean, pooled over coins and windows, before costs.
- Supporting check: Split the decline cases at the median of their 90-day return. The mean of (zc − zb) × r in the deeper half must exceed the mean in the shallower half (deeper minus shallower > 0).
- Confirm: The main measure's t is 2 or more, and the supporting check passes.
- Reject: The main measure's t is −2 or less.
- Inconclusive: A t between −2 and 2 is inconclusive. A t of 2 or more is also inconclusive when the deeper half does not exceed the shallower half. Fewer than 100 grid cases on decline bars is inconclusive whatever the t.
