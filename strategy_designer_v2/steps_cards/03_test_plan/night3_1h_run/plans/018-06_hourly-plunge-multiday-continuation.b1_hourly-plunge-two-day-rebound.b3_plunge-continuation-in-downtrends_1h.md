---
idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b3_plunge-continuation-in-downtrends
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: afc0f50f6fe7
---
Fidelity:
- Situation: a 24-hour fall that is a large multiple of the 30-day average absolute daily return, while the 30-day return is negative -> adapted: "large multiple" becomes a graded size with a cubic dead zone, and "30-day return negative" is a regime rule.
- Comparison: the coin's usual 4-day drift -> kept: measured in the criterion as the 96-bar return minus the coin's normal drift.
- Outcome: the price falls further over the next 4 days, and falls more the deeper the 30-day fall -> kept: 96-bar short-side move, with the depth relation as the supporting check.
- Verdict transfer: yes: every condition of the idea is measured as stated, with only the threshold made graded.
Forecast: The 24-bar percent return is divided by the mean absolute 24-bar return over the 720 bars before it (30 days), then multiplied by 10. So a fall of one usual daily move reads -10 and two usual moves read -20 (the cap). A cubic graded dead zone (exponent 3, pivot 20) keeps ordinary moves near 0. One usual move gives -2.5, 1.5 moves give -8.4, and 2 moves give -20. Clipping at 0 keeps only falls, so the forecast is never positive and its short size grows with the plunge. The forecast is active only while the 30-day (720-bar) return is below 0. On every other bar the regime is null and the forecast is 0.
Config: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b3_plunge-continuation-in-downtrends_1h_config.json
Criterion:
- Horizon: 96 bars
- Main measure: Cases are short bets: the forecast falls at least 2 points below its highest level since the last bet, read once per cell of the non-overlapping 96-bar grid in each window. For each case, take the coin's 96-bar return, minus its normal 96-bar drift over all windows, in the short direction. The measure is the mean of these per-case values, with its t, pooled over coins.
- Supporting check: Over the cases, regress the short-direction unusual move on the 30-day return at the signal bar, recomputed from the closes. The check passes when the slope is below 0, meaning a deeper fall is followed by a larger further decline.
- Confirm: The mean unusual short-direction move is above 0 with t ≥ 2, and the supporting slope is below 0.
- Reject: The mean unusual short-direction move has t ≤ -2, or the main measure confirms but the depth slope is above 0 with t ≥ 2.
- Inconclusive: Any other result is inconclusive, including a t between -2 and 2. Fewer than 30 independent cases pooled over coins is also inconclusive.
