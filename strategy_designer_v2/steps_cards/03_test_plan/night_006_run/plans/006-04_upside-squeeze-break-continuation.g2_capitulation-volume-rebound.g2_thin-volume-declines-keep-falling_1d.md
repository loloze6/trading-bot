---
idea: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g2_thin-volume-declines-keep-falling
brief: 006_range-compression-precedes-expansion
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: the coin has fallen over the last 5 days -> adapted: "after" made "while", as a regime gate on the 5-day return being below 0.
- Comparison: 5-day average volume against its 30-day average, the lower the stronger -> kept: log of the 5-bar mean volume over the 30-bar mean volume, graded.
- Outcome: a larger further decline over the next 3 days -> adapted: horizon kept at 3 bars, holding period dropped.
- Verdict transfer: yes: the test bets, only on 5-day falls, that the coin's 3-day return falls as the volume ratio falls, which is the idea's relation.
Forecast: The forecast is active only on bars where the 5-bar price change (PriceEvolutionComponent, period 5) is below 0; on every other bar it is flat. On active bars, the forecast is the log of the 5-bar mean volume over the 30-bar mean volume (VolumeRatioComponent, short_period 5, period 30, form "log"). It is standardised over its past 60 values (min_periods 20). It is negative (short) when recent volume is thinner than the 30-bar average, and larger in size the thinner it is. It is near 0 at average volume and positive when volume is heavy. It is continuous, and capped at ±20.
Config: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g2_thin-volume-declines-keep-falling_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: The sample is the mean_reversion bars on each window's non-overlapping 3-bar grid. On those bars, regress the coin's 3-bar forward return minus its mean 3-bar return over all windows on the forecast, and take the t of the slope.
- Supporting check: On the same grid bars with forecast < 0 (thin-volume falls), the mean excess 3-bar return must be below 0.
- Confirm: The slope's t is ≥ 2 and the supporting check passes.
- Reject: The slope's t is ≤ -2.
- Inconclusive: A slope t between -2 and 2 is inconclusive. A t ≥ 2 with a failed supporting check is also inconclusive. So is any result from fewer than 100 grid cases in the regime.
