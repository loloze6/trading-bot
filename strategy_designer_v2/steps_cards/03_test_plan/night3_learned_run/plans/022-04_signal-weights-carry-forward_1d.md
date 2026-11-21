---
idea: 022-04_signal-weights-carry-forward
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: each signal's predictive power for the coin's 5-day returns over the past 365 days -> replaced: no catalogue component measures a signal's past correlation with its own later 5-day returns.
- Comparison: higher past power against lower past power, across signals and periods -> adapted: graded, with the signal weighted by its past power.
- Outcome: the same signal's predictive power for that coin over the following 90 days is higher -> adapted: measured as the gain of the signal weighted by past power, held 5 days, over the next 90 bars.
- Verdict transfer: no: without a past-predictive-power measure, the forecast cannot weight a signal by what worked before, so no result bears on the idea.
Reason: Everything the idea needs is in one coin's daily closes: the signals, and their correlation with 5-day forward returns over the trailing 365 bars. No catalogue component computes that trailing predictive power. The config cannot multiply two components (only a weighted mean, and score_product only in the regime), so it also cannot weight a signal by its past power.
