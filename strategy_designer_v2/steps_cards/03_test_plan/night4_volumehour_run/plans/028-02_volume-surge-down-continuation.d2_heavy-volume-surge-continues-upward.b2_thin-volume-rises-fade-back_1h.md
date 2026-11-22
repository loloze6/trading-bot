---
idea: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b2_thin-volume-rises-fade-back
brief: 028_volume-confirmed-hourly-moves-continue
data-instruments: BTC, ETH
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 6e9b10174437
---
Fidelity:
- Situation: an hour rising far more than its typical 30-day hourly move, on volume at or below its 30-day average -> adapted: "far more" is made graded as the hour's rise in multiples of its 30-day mean absolute hourly return; the volume condition is kept as a regime.
- Comparison: the 30-day typical hourly move, and the 30-day average volume -> kept
- Outcome: price falls over the next four hours, more after a larger rise -> kept
- Verdict transfer: yes: the short is sized by the rise in typical moves and taken only on thin-volume hours, so a fall after such hours confirms the idea and a rise beyond drift rejects it.
Forecast: Volume test: the regime detector computes the hour's volume over its mean across the last 720 hours (30 days), current hour included. When that ratio is at or below 1.0 the bar is `mean_reversion`; otherwise it is `unknown`, which is flat. The signal, active only in `mean_reversion`: the hour's return divided by the mean absolute hourly return of the last 720 hours (`MeanAbsScaledReturnComponent`, period 1, window 720). It is then put through these steps: - standardise it (window 500, min_periods 120); - clip at 0, so only rises count; - negate it, so the position is short; - apply `signed_power` with exponent 3 and pivot 20, the strongest graded dead zone. The forecast is zero after a falling hour or on heavy volume. It is near zero after an ordinary rise: a standardised 10 gives -2.5. It reaches -20 when the hour rises about twice its usual size. It is never positive, and it grows in size with the rise.
Config: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b2_thin-volume-rises-fade-back_1h_config.json
Criterion:
- Horizon: 4 bars
- Main measure: The cases are short bets: a fall of the forecast of at least 2 points, read once per non-overlapping 4-bar grid cell of each window. For each case, take the coin's 4-bar return from the bet bar's close, minus the coin's mean 4-bar return over all windows, with the sign flipped to the short side. Measure the mean of that value across cases, pooled over both coins, with its t.
- Supporting check: The least-squares slope of that short-side unusual return on the case's |forecast| is above 0 (a larger rise gives a larger fall).
- Confirm: The mean short-side unusual 4-bar return is above 0 with t >= 2, and the supporting slope is above 0.
- Reject: The mean short-side unusual 4-bar return is below 0 with t <= -2, meaning price rises more than drift after thin-volume spikes.
- Inconclusive: Any t between -2 and 2; or the main measure confirms but the slope is <= 0; or fewer than 100 cases pooled over coins and windows.
