---
idea: 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the coin's Saturday-to-Sunday close-to-close move, sized against its usual daily move -> kept: the Sunday bar's one-bar return over the 20-bar std of daily returns, read only at the Sunday close (the coming bar is Monday).
- Comparison: the weekend move relative to the coin's usual daily move -> kept: the volatility-scaled return divides by the usual daily move.
- Outcome: price moves against the weekend move over the next 2 days (Monday and Tuesday), more so for larger moves -> adapted: holding period dropped, so the config holds only from Sunday close to Monday close, and the criterion reads the 2-bar return from the record's prices.
- Verdict transfer: yes: the forecast set at each Sunday close is judged against the Sunday-to-Tuesday close return, which is exactly the idea's claim.
Forecast: At each Sunday bar's close (the WeekdayComponent says the coming bar is Monday), the forecast is minus the standardised volatility-scaled return of that bar. That return is the Saturday-to-Sunday close return divided by the standard deviation of the last 20 daily returns. Standardise uses a window of 60 and min_periods of 20. The forecast is short after a weekend rise and long after a weekend fall. Its size grows with the weekend move measured in usual moves, at about 10 for an average move and capped at 20. On all other bars the regime is null and the forecast is 0.
Config: 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways_1d_config.json
Criterion:
- Horizon: 2 bars
- Main measure: On each Sunday bar (regime mean_reversion) where 2 more bars exist inside the same window: - excess = (close[t+2]/close[t] - 1) minus the coin's mean 2-bar return over all its windows (holding the coin), before costs; - each case's value = (forecast/10) x excess; - the ordinary t of the mean of these values is taken over all cases, pooled across coins and windows. Sundays are 7 bars apart, so the cases do not overlap.
- Supporting check: Among the same cases, the top third by |forecast| has a higher mean of sign(forecast) x excess than the bottom third (the difference is above 0).
- Confirm: The mean value is positive with t >= 2, and the supporting check passes.
- Reject: The mean value is negative with t <= -2, meaning weekend moves continue into Monday and Tuesday.
- Inconclusive: Any t between -2 and 2, or t >= 2 with the supporting check failing. At least 200 Sunday cases with a full 2-bar outcome are required; fewer is inconclusive.
