---
idea: 018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the 24-hour return at an hourly close first reaches several times the 30-day average absolute daily return, on the upside -> adapted: the 24-bar return divided by its own mean absolute value over the past 720 bars, long side only, with a cubic graded dead zone ("first reaches" becomes "while above").
- Comparison: a rise larger than the coin's usual 5-day return -> kept: the coin's normal 120-bar drift is subtracted in the criterion.
- Outcome: the price rises over the next 5 days only while the 7-day return is positive, more so the larger it is -> kept: a regime on the sign of the 168-bar return, a 120-bar hold, and a check of the rise against the 7-day return's size.
- Verdict transfer: yes: the surge, the 30-day scale, the weekly gate, the 5-day horizon and the gradient are all measured as the idea states them.
Forecast: The 24-bar percent return is divided by the mean absolute 24-bar return of the previous 720 bars (30 days) and multiplied by 10, capped at ±20, so 10 means one average daily move. Falls are clipped to 0. A cubic dead zone (exponent 3, pivot 20) then damps it: an average up day gives about 2.5, 1.5 times gives about 8.4, and 2 times or more gives the full 20. The forecast is active only while the 168-bar (7-day) return is above 0. When that return is 0 or below, the regime is flat and the forecast is 0. It is never negative.
Config: 018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise_1h_config.json
Criterion:
- Horizon: 120 bars
- Main measure: The cases are bets (a rise of the forecast of at least 2), read once per 120-bar grid cell in each window. For each case, the measure is the 120-bar return from the signal's close minus the coin's normal 120-bar drift over all windows. Its mean is tested with the t of the mean.
- Supporting check: Split the cases at their median 168-bar return, recomputed from closes. The above-median half minus the below-median half, in unusual move, must be above 0 (Welch t).
- Confirm: The idea is confirmed when the mean unusual move is positive with t ≥ 2 over at least 30 cases, and the supporting difference is positive.
- Reject: The idea is rejected when the mean unusual move has t ≤ -2 over at least 30 cases, or the supporting difference has Welch t ≤ -2.
- Inconclusive: Any other result is inconclusive: a main t between -2 and 2, or a main t ≥ 2 with a supporting difference at or below 0 but Welch t above -2. Fewer than 30 cases overall, or fewer than 15 in either half, is also inconclusive.
