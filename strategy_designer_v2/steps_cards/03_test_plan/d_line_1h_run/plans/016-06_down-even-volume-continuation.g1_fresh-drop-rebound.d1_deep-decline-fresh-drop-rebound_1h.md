---
idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the coin has fallen over the past 3 days and has a fresh fall over the last 1 day -> kept: a regime keeps the 72-bar fall as the condition, and the 24-bar fall is measured as a size.
- Comparison: the larger the 1-day fall and the deeper the 3-day fall, the larger the rebound -> kept: the forecast grows with both falls, as a weighted mean of the two graded measures.
- Outcome: the coin rises over the next 3 days -> kept: the 72-bar forward return is measured against the coin's average.
- Verdict transfer: yes: the test measures the same falls, condition and horizon, so its confirm or reject applies to the idea.
Forecast: The forecast is active only on bars whose 72-bar return is at or below 0 (regime `mean_reversion`); on every other bar it is 0. On active bars it is the equal-weight mean of two parts. The first part is the 72-bar fall: the 72-bar return, standardised over 72 bars and negated, so it is positive and grows with the depth of the 3-day decline. The second part is the 24-bar fall: the 24-bar return, standardised over 60 bars, negated and clipped at 0, so it is positive and grows with the size of the fresh 1-day drop, and is 0 when the last day rose. The forecast is never negative (long only). It is near 0 just after the coin starts falling over 3 days with no fresh drop, and it grows as either fall deepens.
Config: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: On the non-overlapping 72-bar grid of each window, take the active bars (regime `mean_reversion`, forecast above 0). On those bars, regress the coin's 72-bar forward return minus the coin's mean 72-bar return over all windows on the forecast, pooled over coins and windows. The measure is the slope's t-statistic.
- Supporting check: On the same cases, the mean excess 72-bar return of the cases above the median forecast minus that of the cases below it must be above 0.
- Confirm: The slope's t is 2 or more and the supporting check is above 0, with at least 200 cases.
- Reject: The slope's t is -2 or less, with at least 200 cases.
- Inconclusive: A t between -2 and 2, or a t of 2 or more with the check failing, or fewer than 200 active grid cases.
