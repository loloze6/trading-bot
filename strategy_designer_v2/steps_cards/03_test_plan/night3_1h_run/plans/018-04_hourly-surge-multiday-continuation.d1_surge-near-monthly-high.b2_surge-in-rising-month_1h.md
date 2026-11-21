---
idea: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b2_surge-in-rising-month
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 1efb53e47d25
---
Fidelity:
- Situation: 24h return at an hourly close first reaches several times the 30-day mean absolute daily return, on the upside, while the 30-day return is positive -> adapted: the "several times" threshold becomes a graded surge in usual daily moves with a strong graded dead zone, "first reaches" becomes "while", and the positive 30-day return is kept as a regime condition.
- Comparison: more than the coin's usual 10-day return -> kept: the coin's 10-day return is measured against its normal 10-day drift.
- Outcome: price keeps rising over the next 10 days, more for larger surges -> kept: the book holds each bet for 240 bars.
- Verdict transfer: yes: the forecast is long only on upside surges inside a rising month and grows with the surge, so the 240-bar excess return after its bets confirms or rejects the idea.
Forecast: The forecast runs only on bars where the coin's 720-bar (30-day) return is above 0, the "trending" regime; on all other bars it is 0. On trending bars the raw value is the 24-bar return divided by the mean absolute 24-bar return over the last 720 bars (MeanAbsScaledReturnComponent, period 24, window 720). That value is standardised against its own past 500 values (min_periods 120) and clipped at 0, so only upside surges count. A signed_power with exponent 3 and pivot 10 then damps ordinary readings to near 0 and amplifies large surges. The forecast is never negative. It is near 0 away from a surge, and it grows steeply with the surge's size in usual daily moves.
Config: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b2_surge-in-rising-month_1h_config.json
Criterion:
- Horizon: 240 bars
- Main measure: Each case is a forecast rise of at least 2 points, read once per non-overlapping 240-bar grid cell of each window. For each case, take the coin's 240-bar return from the signal bar's close minus the coin's normal 240-bar drift over all windows; the measure is the t of the mean of these excess returns.
- Supporting check: Among the cases, the excess return grows with the forecast at the signal bar: the slope of a regression of excess return on forecast is positive.
- Confirm: The mean excess return is positive with t >= 2 over at least 30 cases, and the supporting slope is positive.
- Reject: The mean excess return is negative with t <= -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. A confirming t with a slope that is not positive is also inconclusive, and so is any result from fewer than 30 cases.
