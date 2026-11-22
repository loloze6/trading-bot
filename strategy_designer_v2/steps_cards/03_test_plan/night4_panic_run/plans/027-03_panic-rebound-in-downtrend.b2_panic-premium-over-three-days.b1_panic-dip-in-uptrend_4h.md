---
idea: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend
brief: 027_panic-days-are-followed-by-a-premium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: a 24-hour stretch where the coin falls hard while its range is several times its 30-day average -> adapted: the regime requires the mean bar range of the last 6 bars to be at least 3 times its 180-bar mean and the 6-bar return to be below 0; "hard" is graded by the fall's depth in usual 24h moves.
- Comparison: the higher the 30-day return before the stretch, the higher the return; refuse panics in a 30-day fall -> kept: the 180-bar return ending 6 bars ago must be above 0 in the regime, and it adds to the forecast in proportion to its size.
- Outcome: higher than usual returns over the next 3 days (18 bars), long -> kept.
- Verdict transfer: yes: the forecast is long only in the stated panics after a prior rise, it grows with the fall and the prior rise, and it is judged on the 18-bar excess return.
Forecast: The regime detector selects mean_reversion only when three conditions hold on the bar: - MeanBarRangeRatioComponent (long 180, short 6) is at most 0.3333, that is the last 24 hours' bars are at least 3 times as wide as the 30-day average; - the 24h return (MeanAbsScaledReturnComponent, period 6, window 180) is negative; - the 30-day return before the stretch (VolatilityScaledReturnComponent, period 180, lag 6) is positive. On all other bars the forecast is 0 (flat). Inside the regime the forecast is the equal-weight mean of two parts: - the 24h fall in usual daily moves: standardised, negated, clipped at 0, then damped by signed_power (exponent 3, pivot 20) so that only deep falls carry size; - the prior 30-day return: standardised and clipped at 0. The forecast is never negative. It grows with the depth of the panic and with the strength of the rise before it.
Config: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: The excess return per case. A case is a bet (a forecast rise of at least 2 points), read once per 18-bar grid cell. Its excess return is the 18-bar return from the signal bar's close minus the coin's normal 18-bar drift over all windows. The test is the t of the mean over the cases.
- Supporting check: Across cases, regress the excess return on the `rise` component's post_pipeline_value at the signal bar; the slope must be positive.
- Confirm: The mean excess return has t ≥ 2 and the slope is above 0.
- Reject: The mean excess return has t ≤ -2, or the slope has t ≤ -2.
- Inconclusive: Any other result is inconclusive, including a mean excess return with t between -2 and 2. The test also counts as inconclusive with fewer than 30 cases across all coins and windows.
