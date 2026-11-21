---
idea: 021-03_thin-cloud-upward-breakout.d2_calm-breakout-lasts-longer
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: bf6ee48001bb
---
Fidelity:
- Situation: a daily close crossing up from below the cloud to above it -> kept: a regime is active only on the first close above the cloud after the last outside side was below.
- Comparison: the lower the 20-day realised volatility at the cross, the larger the rise -> kept: the long bet on the cross bar grows with the inverse of the 20-day volatility on that bar.
- Outcome: the coin rises over the next 40 days -> kept: each cross-bar bet is held 40 daily bars.
- Verdict transfer: yes: the cross bar, the volatility at the cross, the upward 40-day outcome and its grading are all measured as stated.
Forecast: The detector reads `IchimokuCloudCrossAgeComponent` (9/26/52, displacement 26). On a bar where it equals +1 (the first close above the cloud after coming from below), the regime is `trending`. Every other bar is flat. On that bar the forecast is `HighProximityVolatilityRatioComponent` (period 2, vol_period 20, vol_lookback 365), standardised. With period 2, its proximity factor is about 100 on a cross bar. Its ratio is the 365-day mean of the 20-day volatility over today's 20-day volatility. So the forecast is always positive (long only), about +10 at usual volatility, larger when the 20-day volatility at the cross is lower, smaller when it is higher, and capped at 20. The bet is held 40 bars.
Config: 021-03_thin-cloud-upward-breakout.d2_calm-breakout-lasts-longer_1d_config.json
Criterion:
- Horizon: 40 bars
- Main measure: The cases are the cross-bar bets, keeping only those with 40 bars left in the window. For each case, take the coin's 40-bar return from the cross close minus its normal 40-bar drift, divided by its usual 40-bar move. The main measure is the mean of this value weighted by the bet's forecast, with its t.
- Supporting check: Split the cases at the median forecast. Compare the mean drift-adjusted 40-bar return of the high-forecast half (calm crosses) minus that of the low-forecast half (violent crosses), using Welch's t.
- Confirm: The weighted mean is above 0 with t >= 2, and the calm-minus-violent difference is above 0 with Welch t >= 2.
- Reject: The weighted mean has t <= -2, or the calm-minus-violent difference has Welch t <= -2.
- Inconclusive: Any other result, or fewer than 30 cases in total over the coins and windows.
