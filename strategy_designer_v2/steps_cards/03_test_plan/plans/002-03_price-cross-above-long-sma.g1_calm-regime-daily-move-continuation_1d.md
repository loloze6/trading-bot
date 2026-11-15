---
idea: 002-03_price-cross-above-long-sma.g1_calm-regime-daily-move-continuation
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a day's return large relative to the coin's 20-day volatility, in a low-volatility coin -> adapted: "large" is made graded (the vol-scaled one-day return with a graded dead zone), and "low 20-day volatility" is a regime condition (20-day volatility percentile at or below the median).
- Comparison: the effect weakens or reverses as 20-day volatility rises -> kept: the same scaled-move relation is measured on high-volatility bars, recomputed from prices.
- Outcome: price moves the same way as the day's move over the next 5 days, more after larger scaled moves -> adapted: the position is held only while the signal lasts, so the 5-day holding is dropped and the 5-bar forward return is measured instead.
- Verdict transfer: yes: the test measures follow-through of the same vol-scaled daily move in calm markets over the same 5 days, and contrasts it with volatile markets.
Forecast: One indicator: the day's return divided by the standard deviation of the last 20 daily returns (VolatilityScaledReturnComponent, period 1, vol_period 20). It is standardised over its past 60 values (min 20), then damped with signed_power (exponent 2, pivot 10), so ordinary days give a near-zero position and large days a large one, in the direction of the day's move. The forecast is active only when the regime is trending. That regime holds when the 20-day volatility percentile within the last 100 bars (unsmoothed) is at or below 0.5. On other bars the forecast is 0. It is positive after a strong up day, negative after a strong down day, and grows with the square of the scaled move.
Config: 002-03_price-cross-above-long-sma.g1_calm-regime-daily-move-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Use the non-overlapping 5-bar grid of each window (positions 0, 5, 10, ...) and keep the bars where the forecast is non-zero. On each, take forecast × (5-bar forward return minus the coin's mean 5-bar return over all windows). Pool across coins and report the t of the mean of these products, with the count of cases.
- Supporting check: Recompute the same scaled move and standardised forecast from prices on the grid bars where the volatility percentile is above 0.5. Compute the same mean product there. The check passes if the low-volatility mean minus the high-volatility mean is above 0.
- Confirm: The main measure's mean product is positive with t ≥ 2, on at least 30 cases, and the supporting check passes.
- Reject: The main measure's mean product is negative with t ≤ -2, on at least 30 cases: calm-market strong days reverse.
- Inconclusive: Any result with t between -2 and 2 is inconclusive. So is a confirm-level main measure whose supporting check fails, or any result on fewer than 30 non-zero-forecast grid cases pooled across coins.
