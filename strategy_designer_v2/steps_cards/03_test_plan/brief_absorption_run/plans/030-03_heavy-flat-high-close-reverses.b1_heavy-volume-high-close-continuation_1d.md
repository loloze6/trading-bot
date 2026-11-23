---
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 2035953e3f95
---
Fidelity:
- Situation: a day with volume far above its 20-day average and its close near the day's high -> adapted: the volume threshold is made graded, as the bar's signed close location times its volume over the prior 20-day mean, damped by a cubic dead zone.
- Comparison: that day's volume against its 20-day average, with a larger effect the heavier the volume -> kept: the volume ratio to the prior 20 days multiplies the reading.
- Outcome: the coin rises more over the next 10 days, the closer the close sits to the high -> kept: each bet is held 10 daily bars, long only, since the idea refuses shorts.
- Verdict transfer: yes: the forecast is large only on heavy-volume days that close high, so the cases that follow it test exactly the idea's claim.
Forecast: The component is `VolumeWeightedCloseLocationComponent` with `volume_period` 20, `exclude_current` 1 and `reference` "signed". It is the bar's close location (-1 at the low, +1 at the high) times its volume over the mean of the prior 20 days' volume. It is standardised over 60 bars with min_periods 20. A cubic `signed_power` (exponent 3, pivot 10) then keeps ordinary days near 0 and amplifies heavy-volume days. A `clip` at min 0 makes it long-only. The forecast is positive and grows with both the nearness of the close to the high and the size of the volume surge. It is zero when the close is in the lower half of the bar. It is near zero on ordinary-volume days.
Config: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The mean unusual move over 10 bars after each case, in the long direction. A case is a long-side forecast rise of at least 2 points, read once per non-overlapping 10-bar grid cell per window. The unusual move is the coin's 10-bar return from the case bar's close minus the coin's normal 10-bar drift over all windows. The t is the t of the mean, pooled over coins and windows.
- Supporting check: Split the cases at their median forecast. The mean unusual move of the larger-forecast half, minus that of the smaller half, must be above 0.
- Confirm: The main measure's mean is positive with t >= 2, and the supporting check passes (top half minus bottom half > 0).
- Reject: The main measure's mean is negative with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t >= 2 whose supporting check fails is inconclusive. Fewer than 30 cases pooled over all coins and windows is inconclusive whatever the t.
