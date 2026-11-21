---
idea: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: af2e424c34f8
---
Fidelity:
- Situation: the 1-day return, scored against its past 365 days and weighted by how well it predicted the next 5 days over those 365 days, is far from its usual value -> adapted: "far from usual" becomes a graded size, the single-effect z-score times its correlation, with the strongest graded dead zone.
- Comparison: the term's own 365-day history, and its 365-day correlation with 5-day forward returns -> kept: z_window 365, corr_lookback 365, horizon 5.
- Outcome: the coin moves in the term's direction over the next 20 days, more the further out the term is -> kept: the book holds for 20 bars and the position grows with the term.
- Verdict transfer: yes: the component computes the idea's exact term, and the test reads the 20-day move that follows it, by sign and by size.
Forecast: The forecast is the weighted reversal term of `PastPredictivePowerWeightedCompositeComponent` (weighting "single", signal "reversal", reversal_period 1, z_window 365, corr_lookback 365, horizon 5). The term is the z-score of minus the 1-day return over the last 365 days, times that signal's 365-day correlation with the following 5-day return. The term is standardised over its past 455 values, then damped by signed_power (exponent 3, pivot 20). It is positive when the term points up, negative when it points down, and near zero unless the term is far from its usual size. It grows with the cube of that size. It is active on every bar, with no regime.
Config: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: Cases are bars on the non-overlapping 20-bar grid of each window where abs(forecast) >= 2. For each case, take the coin's 20-bar return minus its normal 20-bar drift (all windows together), multiplied by the sign of the forecast. The measure is the mean over cases and its t-statistic, before costs.
- Supporting check: Split the cases at the median abs(forecast). The larger-forecast half has a higher mean signed excess 20-bar return than the smaller half (difference larger minus smaller, greater than 0).
- Confirm: The main-measure t is 2 or more over at least 30 cases, and the supporting check difference is above 0.
- Reject: The main-measure t is -2 or less over at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t of 2 or more with the supporting check not passing is also inconclusive. Fewer than 30 cases is inconclusive whatever the t.
