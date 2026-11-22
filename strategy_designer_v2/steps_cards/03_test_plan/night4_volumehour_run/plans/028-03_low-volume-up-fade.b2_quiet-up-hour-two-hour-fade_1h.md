---
idea: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade
brief: 028_volume-confirmed-hourly-moves-continue
data-instruments: BTC, ETH
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: an hour that rises far more than its 30-day typical hourly move, with volume near its 30-day hourly average -> adapted: the 1h rise in mean absolute 1h moves over 720 bars, made graded with a strong dead zone; "after that hour" becomes "while that hour is the latest bar"; volume near average is kept as a regime condition on the 720-bar volume ratio.
- Comparison: the typical hourly move and the average hourly volume over the past 30 days -> kept
- Outcome: price gives back part of the rise over the next two hours, more for a larger rise -> kept
- Verdict transfer: yes: a graded short on quiet-volume rises, held 2 bars, gains only if those rises give back more than usual, and more for larger rises.
Forecast: The forecast is computed only on bars where the latest bar's volume is between 0.67 and 1.5 times its 720-bar mean volume (the mean_reversion regime); on every other bar it is 0. On those bars, MeanAbsScaledReturnComponent (period 1, window 720) gives the last hour's return in multiples of the 30-day mean absolute hourly return. It is standardised (window 500, min_periods 120) and clipped at 0, so only rises count. It then goes through signed_power with exponent 3 and pivot 10, so ordinary rises give almost 0 and far-larger-than-usual rises give a large value. Finally it is negated. The forecast is therefore 0 or negative (short), and its size grows steeply with the size of the quiet-volume rise. It is 0 after down hours, on high-volume or very-low-volume hours, and close to 0 after small rises.
Config: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade_1h_config.json
Criterion:
- Horizon: 2 bars
- Main measure: The cases are bets: a fall of the forecast of at least 2 points on the short side, read once per cell of a non-overlapping 2-bar grid in each window, pooled over BTC and ETH. For each case, take the unusual move in the short direction: -(close[t+2]/close[t]-1) minus the coin's mean 2-bar return over all windows. Measure the mean of that unusual move and its t.
- Supporting check: Across the cases, regress the unusual move on |forecast|; the slope must be above 0 (a larger rise gives a larger giveback).
- Confirm: The mean unusual move is positive with t >= 2 over at least 30 cases, and the supporting slope is above 0.
- Reject: The mean unusual move is negative with t <= -2 over at least 30 cases (quiet-volume rises keep extending beyond drift).
- Inconclusive: Any t between -2 and 2, or t >= 2 with a slope not above 0, or fewer than 30 cases in total.
