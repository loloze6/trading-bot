---
idea: 026-04_thinner-weekend-larger-reversal
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 2a96c3272007
---
Fidelity:
- Situation: the coin's Saturday-Sunday move, at thinner weekend volume -> kept: the 48-bar return to Sunday's last close, in usual 48-bar moves, times the weekday-to-weekend volume ratio, read at Sunday's last bar.
- Comparison: weekend volume against its volume over the preceding five weekdays -> kept: mean volume of the 48 weekend bars against the mean of the 120 bars Monday 00:00 to Friday 23:00.
- Outcome: the move is partly reversed over Monday and Tuesday, more so when the weekend was thinner -> kept: bet against the move at Sunday's close and hold it 48 bars.
- Verdict transfer: yes: the forecast is the predicted reversal (move times thinness), and it is held exactly over Monday and Tuesday.
Forecast: The forecast is active only on the bar whose next bar starts Monday 00:00 UTC, which is the last hour of Sunday. On every other bar it is zero, and the holding period carries the bet through Monday and Tuesday. On that bar it reads ThinVolumeScaledReturnComponent with period 48, window 720, volume_period 48, base_near 48 and base_far 167. This is the weekend's 48-hour return in usual 48-hour moves, times the mean volume of the five weekdays divided by the weekend's mean volume. It is standardised over 500 bars with min_periods 120, then negated. The forecast is short after a weekend rise and long after a weekend fall. Its size grows with the size of the move and with how thin the weekend volume was against the weekdays. It is zero when the weekend was flat.
Config: 026-04_thinner-weekend-larger-reversal_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: On the signal bars (Sunday's last bar, one per week, so the cases never overlap), the least-squares slope of the coin's 48-bar return minus its normal 48-bar drift on the forecast, pooled over all coins and windows, with its t.
- Supporting check: The mean unusual move in the signal's direction over the cases (48-bar return minus drift, times the sign of the forecast) is above 0.
- Confirm: The slope has t ≥ 2 and the mean unusual move in the signal's direction is above 0, both before costs.
- Reject: The slope has t ≤ -2, meaning a thinner weekend's move is continued rather than reversed.
- Inconclusive: Any slope with t between -2 and 2 is inconclusive. A slope with t ≥ 2 whose supporting mean is not above 0 is also inconclusive. A result on fewer than 300 signal bars with a nonzero forecast is inconclusive.
