---
idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e1_depth-graded-plunge-rebound-uptrend
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 5c26677afd57
---
Fidelity:
- Situation: a coin with a positive 30-day return has a large 24-hour fall in units of its 30-day mean absolute daily return -> adapted: the fall in usual daily moves is kept exactly; "large" and "30-day return positive" are made graded (the forecast is the fall times the positive 30-day return, with a strong dead zone).
- Comparison: the rise is judged against the coin's usual 4-day drift -> kept: the measure subtracts the coin's mean 96-bar return over all windows.
- Outcome: the price rises over the next 4 days, more after a deeper fall -> kept: a long position held 96 bars, sized by the depth of the fall.
- Verdict transfer: yes: the forecast is the idea's own fall measure, gated in graded form by its own 30-day rise, and it is long over the idea's 4-day horizon.
Forecast: One component, MeanAbsScaledFallTimesRiseComponent, at fall_period 24, window 720 and rise_period 720 (24 hours and 30 days on 1h bars). Its raw value is the 24-hour fall measured in the coin's 30-day mean absolute daily return, times the positive 30-day percent return. It is 0 when the last 24 hours did not fall or when the 30-day return is not positive. It is standardised over its past 500 values (min_periods 120). A signed_power with exponent 3 and pivot 10 then gives the strongest graded dead zone, because the situation is a rare extreme. Shallow dips stay near 0, and deep plunges in a rising coin give large long positions. The forecast is never negative (long only by construction). It grows with the depth of the fall and with the size of the 30-day rise, and it is 0 whenever the situation is absent.
Config: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e1_depth-graded-plunge-rebound-uptrend_1h_config.json
Criterion:
- Horizon: 96 bars
- Main measure: Cases are bets, meaning rises of the forecast of at least 2 points, read once per cell of each window's 96-bar grid and pooled over all coins and windows. For each case, take the coin's return over the next 96 bars from the case bar's close, minus that coin's mean 96-bar return over all its windows. The measure is the mean of this unusual move, with its t of the mean.
- Supporting check: Across the cases, the Spearman rank correlation between the forecast at the case bar and its unusual move is above 0 (a deeper plunge is followed by a larger rise).
- Confirm: The mean unusual move is positive with t >= 2 over at least 30 independent cases, and the supporting check passes.
- Reject: The mean unusual move is negative with t <= -2 over at least 30 independent cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t >= 2 with a rank correlation of 0 or below is also inconclusive. So is any result from fewer than 30 independent cases pooled.
