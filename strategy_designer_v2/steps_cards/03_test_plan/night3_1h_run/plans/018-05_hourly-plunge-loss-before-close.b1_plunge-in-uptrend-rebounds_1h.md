---
idea: 018-05_hourly-plunge-loss-before-close.b1_plunge-in-uptrend-rebounds
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a coin's 24-hour return, at an hourly close, first reaches the trigger on the downside while its 30-day return is positive -> adapted: "first reaches" becomes "while it is reached"; the 30-day return above zero is a regime rule.
- Comparison: the 24-hour fall against several times the 30-day average absolute daily return -> adapted: the threshold becomes a graded ratio with a cubic dead zone.
- Outcome: the price rises over the next 3 days, more after a larger 30-day rise -> kept: each bet is held 72 bars, and the size of the rebound is judged against the recorded 30-day rise.
- Verdict transfer: yes: the plunge ratio, the 30-day condition, the long side and the 3-day horizon are measured as the idea states them.
Forecast: The forecast is active only on bars whose 30-day (720-bar) return is above 0; on all other bars it is flat. It is built in four steps: - The 24-bar return is divided by the mean absolute value of the 24-bar return over the previous 720 bars, times 10 (cap 40). This gives the 24-hour move in units of the 30-day average absolute daily move: 10 means one average move, 30 means three. - The sign is flipped, so a fall reads positive. - Values below 0 are clipped, so the forecast is long only. - A cubic dead zone is applied (`signed_power`, exponent 3, pivot 20): a fall of one average move gives 2.5, two average moves give 20, and three or more reach the cap. The forecast is therefore near zero away from large plunges and grows smoothly with the depth of the plunge. The 30-day return is carried as a weight-0 component, so its value is recorded but does not change the forecast.
Config: 018-05_hourly-plunge-loss-before-close.b1_plunge-in-uptrend-rebounds_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: The unusual move per case: the coin's return over the 72 bars after each case, minus the coin's normal 72-bar drift over all windows. A case is a long bet (a rise of the forecast of at least 2 points), read once per 72-bar grid cell. The measure is the mean of these unusual moves, with its t over the independent cases.
- Supporting check: Among the cases, the mean unusual move when the recorded 30-day rise (`rise30_rec` `last_history_value`) is above its median, minus the mean when it is below. The check passes when this difference is above 0.
- Confirm: The mean unusual move has a t of at least 2, and the supporting check is above 0.
- Reject: The mean unusual move has a t of -2 or less.
- Inconclusive: A t between -2 and 2, or a t of 2 or more with a check at or below 0. Fewer than 30 independent cases across all coins and windows is also inconclusive.
