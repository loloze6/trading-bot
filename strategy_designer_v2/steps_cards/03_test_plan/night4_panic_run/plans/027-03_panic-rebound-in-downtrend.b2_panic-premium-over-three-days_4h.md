---
idea: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days
brief: 027_panic-days-are-followed-by-a-premium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: a 24-hour stretch where the coin falls hard while its range is several times its 30-day average -> adapted: "after X" made "while X". A regime is active while the 6-bar return is at most -2 usual 6-bar moves (30-day mean absolute) and the 6-bar mean bar range is at least 3 times its 180-bar mean.
- Comparison: higher than usual returns, growing as the range exceeds its 30-day average -> adapted: the condition is kept as the regime, and the size grows with the range excess (10 x (1 - L/Q), standardised).
- Outcome: the price rises more than usual over the next 3 days -> kept: each bet is held 18 bars and judged against the coin's usual 18-bar return.
- Verdict transfer: yes: the test measures panic bars with the idea's fall, range, 30-day base and 3-day horizon, and its size follows the range excess.
Forecast: The regime detector marks a bar as a panic, using the 4h bars of the last 24 hours (6 bars) and the last 30 days (180 bars). Both conditions must hold: - the 6-bar return is at most -2 times the coin's mean absolute 6-bar return over the last 180 bars; - the mean bar range of the last 6 bars is at least 3 times its 180-bar mean (`MeanBarRangeRatio` long 180, short 6, raw value at most 1/3). Off a panic the forecast is 0. On a panic bar the forecast is the equal-weight mean of two parts: - the 180/6 mean-bar-range ratio, standardised (window 180, min_periods 45) and negated; - the standardised constant +10. That gives about 5 x (1 - L/Q), where Q/L is the range excess: - 3 times the usual range gives about 3.3; - 6 times gives about 4.2; - the limit for an ever larger range is 5. So inside a panic the forecast is long and grows with the range excess. It is never negative.
Config: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: The cases are the bets (forecast rises of at least 2), one per cell of a non-overlapping 18-bar grid in each window. For each case, take the coin's 18-bar return from the signal bar's close minus the coin's mean 18-bar return over all windows. Report the mean of this excess and its t, before costs.
- Supporting check: Split the cases at their median forecast. The mean excess return of the cases above the median minus that of the cases below must be greater than 0.
- Confirm: The mean excess 18-bar return is positive with t ≥ 2, and the supporting check passes.
- Reject: The mean excess 18-bar return is negative with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is t ≥ 2 when the supporting check fails, and any result with fewer than 30 independent cases across all coins and windows.
