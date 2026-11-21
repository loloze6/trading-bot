---
idea: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades.b1_post-selloff-surge-fades-more-coins
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 1efb53e47d25
---
Fidelity:
- Situation: the 24h return first reaches several times the 30-day mean absolute daily return, on the upside, after a fall in the 7 days before that day -> adapted: "first reaches" becomes "while the 24h return is at or above 3 usual daily moves", and the prior 7-day return is negative; the fall's depth is measured in 30-day usual moves.
- Comparison: the coin's usual 5-day return -> kept: each case's 5-day return minus the coin's mean 5-day return over all windows.
- Outcome: over the next 5 days the price rises less than usual, by more after a deeper fall -> kept: a short sized by the fall's depth, held 120 bars.
- Verdict transfer: yes: a confirm or a reject on the drift-removed 5-day move after these surges, graded by fall depth, is a confirm or a reject of the idea itself.
Forecast: The regime is active only while two conditions hold. The first is the 24h return in usual daily moves (MeanAbsScaledReturn, period 24, window 720) at or above 3. The second is the 7-day return ending 24 bars ago (VolatilityScaledReturn, period 168, lag 24, vol_period 720) below 0. On all other bars the forecast is flat. In the regime, the forecast is that lagged 7-day return, standardised over its own past (window 500, min_periods 120) and clipped at 0 from above. It is therefore always zero or negative (short), and its size grows continuously with the depth of the prior fall. A shallow fall gives near 0, and a fall about twice its usual size gives about -20.
Config: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades.b1_post-selloff-surge-fades-more-coins_1h_config.json
Criterion:
- Horizon: 120 bars
- Main measure: The cases are bets (short rises of the forecast of at least 2 points), read once per 120-bar grid cell in each window. For each case, take the coin's 120-bar return from the signal bar's close and subtract the coin's mean 120-bar return over all its windows (non-overlapping). Then flip the sign into the short direction. The measure is the mean of this value over all cases, with its t-statistic.
- Supporting check: The half of the cases with the larger |forecast| at the signal bar (deeper prior fall) has a larger mean drift-removed short-side move than the other half. The difference must be deeper half minus shallower half, and greater than 0.
- Confirm: The main mean is above 0 with t ≥ 2, and the supporting check passes.
- Reject: The main mean is below 0 with t ≤ -2, meaning the price rose more than usual after these surges.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a main t ≥ 2 when the depth check fails. So is any count below 30 independent cases.
