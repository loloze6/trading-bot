---
idea: 031-04_fading-volume-after-fall-rebounds
brief: 031_medium-term-overreaction-reversal
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 31f1a8c6c7f6
---
Fidelity:
- Situation: after an unusually large 90-day fall -> adapted: "after" made "while"; the condition holds while the 90-day return is 2 or more usual moves down (daily volatility over 365 days x sqrt(90), by convention), as a regime.
- Comparison: 14-day volume against the average daily volume during the 90-day fall -> kept: the log of the mean 14-day volume over the mean 90-day volume, graded by the size of the drop.
- Outcome: price rebounds over the next 30 days, more for a deeper volume drop -> kept: long, held 30 bars, size grows with the volume drop.
- Verdict transfer: yes: the test measures whether, inside large falls, the 30-day rebound grows with the drop in volume, which is the idea's claim.
Forecast: The detector reads the 90-day return divided by the daily return standard deviation over 365 days times sqrt(90). When that is -2 or lower, the bar is in the `mean_reversion` regime. On all other bars the forecast is 0. In the regime, the forecast comes from ln(mean volume of the last 14 days / mean daily volume of the last 90 days). This value is standardised over its past 90 values, then negated and clipped at 0. The forecast is long and grows as the recent volume sinks further below its average during the fall. It is 0 when the volume has not dropped below that average. It is never short.
Config: 031-04_fading-volume-after-fall-rebounds_1d_config.json
Criterion:
- Horizon: 30 bars
- Main measure: Use the bars in the `mean_reversion` regime that sit on the 30-bar grid of each window. On those bars, take the slope of the coin's 30-day forward return minus its normal drift (its mean 30-day return over all windows) on the forecast. The t uses standard errors clustered by day.
- Supporting check: Take the grid cases in the regime with a forecast above 0. Their mean 30-day return minus the coin's normal drift is above 0.
- Confirm: The slope's t is 2 or more, and the supporting check passes.
- Reject: The slope's t is -2 or less.
- Inconclusive: A t between -2 and 2 is inconclusive. A slope t of 2 or more with the supporting check failing is also inconclusive. So is a count below 20 grid cases in the regime, or below 10 with a forecast above 0.
