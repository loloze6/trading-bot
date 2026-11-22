---
idea: 028-02_volume-surge-down-continuation.d1_heavy-volume-plunge-rebounds
brief: 028_volume-confirmed-hourly-moves-continue
data-instruments: BTC, ETH
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: an hour in which the coin falls far more than its typical 30-day hourly move, on volume several times its 30-day average -> adapted: the two thresholds become graded, as the hour's fall in 720-bar return standard deviations times its volume over the 720-bar mean volume.
- Comparison: the fall against the typical 30-day hourly move, and the volume against the 30-day average volume -> kept
- Outcome: the price rebounds (rises) over the next two to four hours, more after deeper falls -> adapted: "after the hour" becomes "while the hour is the latest bar", and the book holds each bet 4 bars.
- Verdict transfer: yes: the forecast is long in proportion to the volume-weighted fall measured against the coin's own 30-day scales, and its bets are held over the idea's horizon.
Forecast: The forecast uses one component, VolumeWeightedScaledReturnComponent with vol_period 720 and volume_period 720. It computes the hour's return divided by the standard deviation of hourly returns over the last 30 days, times the hour's volume over its 30-day mean. The value is standardised over its past 500 values and negated, so falls read positive. It is clipped at 0, so up hours and the short side give a forecast of 0. It then goes through signed_power with exponent 3, the strongest graded dead zone. An ordinary fall gives a forecast near 0. A heavy-volume plunge gives a long position that grows steeply with the depth of the fall and with the volume surge. The forecast is never negative.
Config: 028-02_volume-surge-down-continuation.d1_heavy-volume-plunge-rebounds_1h_config.json
Criterion:
- Horizon: 4 bars
- Main measure: The unusual move of each case. A case is a rise of the forecast of at least the band, read once per 4-bar grid cell. Its unusual move is the coin's 4-bar return from the signal bar's close minus the coin's normal 4-bar drift over all windows. The measure is the mean over all cases of both coins, with its t.
- Supporting check: The least-squares slope of the cases' unusual moves on the forecast at the signal bar must be above 0, so that deeper plunges give larger rebounds.
- Confirm: The mean unusual move has t >= 2 over at least 30 cases, and the slope check is above 0.
- Reject: The mean unusual move has t <= -2 over at least 30 cases, meaning the price keeps falling after heavy-volume plunges.
- Inconclusive: Any t between -2 and 2 is inconclusive. A confirming t with a slope at or below 0 is also inconclusive. Fewer than 30 cases over both coins and all windows decides nothing.
