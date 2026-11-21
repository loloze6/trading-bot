---
idea: 021-03_thin-cloud-upward-breakout.d1_momentum-backed-breakout-longer-hold
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: bf6ee48001bb
---
Fidelity:
- Situation: a daily close crossing up from below the Ichimoku cloud to above it -> kept: a regime on the bar whose cross age is 1, which is the cross bar itself.
- Comparison: the larger the 60-day return before the cross, the larger the rise -> adapted: graded by the 60-day return at the cross, with no position when that return is not positive.
- Outcome: the coin rises over the next 40 days -> kept: each cross bet is held 40 daily bars.
- Verdict transfer: yes: the cross bar, the 60-day sizing and the 40-day hold are all measured as the idea states them.
Forecast: The forecast is zero except on the bar where the close first sits above the cloud after leaving it from below. The cloud uses the standard Ichimoku settings 9, 26, 52 and displacement 26, and that bar is where the cross age is exactly 1. On that bar the forecast is the 60-day percent return, standardised against its own past 60 values, with negative values set to 0. It is positive and grows with the pre-cross rise, up to 20. Each such bet is held 40 bars.
Config: 021-03_thin-cloud-upward-breakout.d1_momentum-backed-breakout-longer-hold_1d_config.json
Criterion:
- Horizon: 40 bars
- Main measure: Per cross case (a bet, counted once per 40-bar grid cell), take the coin's 40-bar return from the cross bar's close minus its normal 40-bar drift. Measure the slope of that unusual move on the case's forecast, before costs.
- Supporting check: The mean unusual 40-bar move over all cases is above zero.
- Confirm: The slope is positive with t >= 2 and the mean unusual move over the cases is above zero.
- Reject: The slope is negative with t <= -2.
- Inconclusive: Any slope t between -2 and 2 is inconclusive. So is a positive slope with a mean unusual move at or below zero. The test needs at least 30 cases across coins and windows; fewer is inconclusive.
