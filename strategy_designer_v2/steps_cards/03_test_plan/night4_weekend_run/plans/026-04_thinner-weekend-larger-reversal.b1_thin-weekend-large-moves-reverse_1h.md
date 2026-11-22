---
idea: 026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 2a96c3272007
---
Fidelity:
- Situation: a large Saturday-Sunday move, only while weekend volume is below the weekdays' -> kept: the 48-bar weekend return times the weekday-to-weekend volume ratio, read once at Sunday's last bar, with a regime for "only while".
- Comparison: weekend mean volume against the mean volume of the preceding five weekdays -> kept: 48 weekend bars against the 120 bars from Monday to Friday, in a rule and in the size.
- Outcome: the weekend move is partly reversed over the next 48 hours, Monday and Tuesday -> kept: the position leans against the move and is held 48 bars.
- Verdict transfer: yes: the test bets against thin-volume weekend moves over Monday and Tuesday, sized by the move and the volume thinness, so a confirm or a reject transfers to the idea.
Forecast: The forecast is active on one bar a week: the bar stamped Sunday 23:00 UTC, whose next bar opens Monday. It is active only when the log ratio of the weekend's mean hourly volume to the mean hourly volume of Monday to Friday is below 0. On that bar the forecast is minus the standardised value of ThinVolumeScaledReturnComponent. That value is the 48-bar return from Friday 23:00 to Sunday 23:00, counted in usual 48-bar moves, times the weekday base volume (bars t-167 to t-48) over the weekend volume (bars t-47 to t). The forecast is short after a weekend rise and long after a weekend fall. It grows with the size of the move and with how thin the weekend was against the week. It is zero on every other bar and on heavy-volume weekends, and the 48-bar holding period carries the bet through Monday and Tuesday.
Config: 026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: At each case, a Sunday 23:00 bar in the mean_reversion regime with a nonzero forecast, take the coin's 48-bar forward return minus its normal 48-bar drift. Regress it on the forecast, pooled over coins and windows, and take the t of the slope.
- Supporting check: The mean unusual move in the forecast's direction over the cases is above 0.
- Confirm: The slope's t is 2 or more, and the mean unusual move in the forecast's direction is positive.
- Reject: The slope's t is -2 or less: forecasts against the weekend move are followed by continuation.
- Inconclusive: A slope t between -2 and 2, or a confirming slope whose mean unusual move is not positive. Fewer than 200 cases over all coins is inconclusive whatever the t.
