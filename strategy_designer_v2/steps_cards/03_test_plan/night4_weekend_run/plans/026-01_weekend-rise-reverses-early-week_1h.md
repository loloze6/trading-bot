---
idea: 026-01_weekend-rise-reverses-early-week
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: the coin's price rises from Saturday 00:00 UTC to Monday 00:00 UTC -> kept: the 48-bar return read at the bar that closes at Monday 00:00, short side only when it is positive.
- Comparison: none -> kept
- Outcome: the price falls over the next two days, Monday and Tuesday, more after a larger gain -> kept: the short is sized by the gain and held 48 bars.
- Verdict transfer: yes: the position is exactly the weekend gain, short from Monday 00:00 for Monday and Tuesday, so its forward fall is the idea's claim.
Forecast: Two calendar measures pick the regime: the weekday and the UTC hour of the coming bar. Only the bar whose coming bar is Monday 00:00 is active. That bar is stamped Sunday 23:00 and closes at the Monday 00:00 price. On that bar the forecast is the 48-bar percent return, which is the move from Saturday 00:00 to Monday 00:00. The return is standardised against the mean absolute size of its last 60 hourly values, negated, and clipped at 0. It is negative, a short, only after a weekend gain, and grows linearly with the gain up to the -20 cap. It is 0 after a weekend fall and on every other bar. The 48-bar holding period keeps the short through Monday and Tuesday.
Config: 026-01_weekend-rise-reverses-early-week_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: A case is a Monday-00:00 bar with a negative forecast that makes a bet. For each case, take the coin's 48-bar return from that bar's close, minus the coin's mean 48-bar return over all windows (its normal drift), signed in the short direction. The measure is the mean of these values over all coins and windows, with its t-statistic. Cases are one per week and do not overlap.
- Supporting check: The slope of that signed unusual move on the case's |forecast| (least squares across cases) is above 0.
- Confirm: The mean signed unusual move is positive with t ≥ 2, and the slope is above 0.
- Reject: The mean signed unusual move has t ≤ -2, meaning weekend gains are followed by rises beyond the coin's drift.
- Inconclusive: Any t between -2 and 2, or t ≥ 2 with a slope at or below 0. At least 100 cases are required; with fewer, the result is inconclusive.
