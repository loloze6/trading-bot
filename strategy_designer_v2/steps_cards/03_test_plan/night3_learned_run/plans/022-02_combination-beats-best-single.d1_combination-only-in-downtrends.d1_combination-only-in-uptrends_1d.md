---
idea: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: the coin's 90-day return is positive, and the more positive the stronger -> kept: a regime rule on the 90-day return above 0, with that return recorded as a graded value for the criterion.
- Comparison: the relearned combined score of the four signals against the score of whichever single signal predicted best -> kept: the same composite component computed both ways ("correlation" and "best"), both recorded on every bar.
- Outcome: the 5-day return lines up more closely with the combined score -> kept: each score's fit with the next 5-day return, compared on the same cases.
- Verdict transfer: yes: the test measures both scores, the 90-day condition, its size and the 5-day fit as the idea states them.
Forecast: The forecast is active only while the coin's 90-day price change is above 0. On other bars it is flat. When active, it is the relearned combined score: the four signals are each z-scored over 365 days and weighted by their 365-day correlation with past 5-day returns. The signals are the 28-day return, the reversed 1-day return, the closeness to the 90-day closing high and the negated 30-day volatility. The score is standardised over its past 365 values. It is positive when the weighted signals point up and negative when they point down, and its size grows with their agreement and strength. Two more components carry weight 0, so they do not change the forecast; they only record values for the measure. One is the best-single-signal score ("best"). The other is the 90-day return.
Config: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are the trending-regime bars on each window's non-overlapping 5-bar grid. For each case, take the next 5-day return minus the coin's mean 5-day return over all windows, which removes the gain from simply holding the coin. Divide each score's post_pipeline_value by its pooled standard deviation. Then d = (scaled combined − scaled best) × excess return. The measure is the mean of d and its t across the cases.
- Supporting check: Split the cases at the median of ret90's last_history_value. The mean of d in the upper half minus the mean of d in the lower half must be above 0.
- Confirm: The idea is confirmed when the mean d has t ≥ 2 and the supporting check is above 0.
- Reject: The idea is rejected when the mean d has t ≤ −2.
- Inconclusive: The result is inconclusive when t is between −2 and 2. It is also inconclusive when t ≥ 2 but the check is at or below 0. At least 200 independent cases in the regime are required; with fewer, the result is inconclusive.
