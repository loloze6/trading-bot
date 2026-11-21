---
idea: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 1efb53e47d25
---
Fidelity:
- Situation: the 24-hour return at an hourly close first reaches several times (3) its 30-day average absolute daily return, upward, after a 7-day fall before that day -> adapted: "first reaches" becomes "while at or above", a regime rule on the 24h move in usual daily moves, AND on the sign of the 7-day return ending 24 bars earlier.
- Comparison: the coin's usual 5-day return -> kept: each case's 120-bar return is set against the coin's normal 120-bar drift.
- Outcome: the price rises less than usual over the next 5 days, and the deeper the 7-day fall, the larger the shortfall -> kept: a short position that grows with the depth of the lagged 7-day fall, held 120 bars.
- Verdict transfer: yes: the test measures the conditioned shortfall against the normal drift, graded by fall depth, so a confirm or reject carries to the idea.
Forecast: The forecast is computed only while two conditions hold at once: - the 24h return is at least 3 times the 30-day mean absolute 24h return (MeanAbsScaledReturnComponent, period 24, window 720, at or above 3); - the 7-day return ending 24 bars ago is negative (VolatilityScaledReturnComponent, period 168, lag 24, vol_period 720, below 0). On those bars the forecast is that same lagged 7-day fall, scaled by a 30-day volatility that is nearly constant over weeks. It is standardised over its past 500 values and clipped at 0. It is therefore negative (short), and it grows in size the deeper the prior 7-day fall. On every other bar it is 0 (flat). It is never positive.
Config: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades_1h_config.json
Criterion:
- Horizon: 120 bars
- Main measure: Per case (a short bet: the forecast falls by at least 2 points, read once per 120-bar grid cell), take the coin's 120-bar return from the signal close minus its normal 120-bar drift over all windows. Read it in the short direction, before costs, and take its mean over all cases with the t of the mean.
- Supporting check: Across cases, the slope of that shortfall on the case's absolute forecast (the depth of the prior fall) is positive.
- Confirm: The mean shortfall is above 0 with t ≥ 2 over at least 30 cases, and the depth slope is above 0.
- Reject: The mean shortfall has t ≤ -2 over at least 30 cases: after such surges the price rises more than its usual 5-day drift.
- Inconclusive: Any t between -2 and 2, a confirming mean with a slope of 0 or below, or fewer than 30 cases in total.
