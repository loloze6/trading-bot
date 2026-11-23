---
idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d3_much-heavier-weekend-continuation
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: fc27df6a23f8
---
Fidelity:
- Situation: a Saturday-Sunday move made on weekend volume a multiple of the mean over the preceding five weekdays -> adapted: the "multiple" threshold is made graded as the 48-bar weekend return times the volume ratio, read at Sunday's last hourly bar.
- Comparison: weekend volume against its mean over the preceding five weekdays -> kept: the mean of the last 48 bars' volume over the mean of the 120 bars before them.
- Outcome: the move continues in the same direction over Monday's first 12 hours, more steeply the heavier the volume and the larger the move -> kept: held 12 bars from Sunday 23:00's close, sized by the product.
- Verdict transfer: yes: the forecast is the weekend move times its volume multiple, taken once per weekend and held for Monday's first 12 hours, so its result is the idea's result.
Forecast: A regime rule activates the forecast only on the bar whose next bar is Monday 00:00 UTC (weekday 0, hour 0), which is Sunday's 23:00 bar. On that bar the forecast is `RecentToPriorVolumeScaledReturnComponent` with period 48, base_period 120 and window 720. This is the Friday-close-to-Sunday-close return in usual 48-bar moves, times the weekend's mean hourly volume over the mean of the five weekdays before it. It is standardised over its last 500 values, then passed through `signed_power` with exponent 3 and pivot 20. That is the strongest graded dead zone, so ordinary weekends give almost no position and the heaviest-volume, largest-move weekends get the largest one. The forecast is positive after a weekend rise and negative after a weekend fall (continuation), and 0 on every other bar. The holding period keeps the bet for the 12 Monday bars.
Config: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d3_much-heavier-weekend-continuation_1h_config.json
Criterion:
- Horizon: 12 bars
- Main measure: The cases are the bars with regime "trending" and a nonzero forecast, one per coin and weekend. Take the top fifth of cases by |forecast|, pooled over coins. For each, compute sign(forecast) x (12-bar return from that bar's close minus the coin's mean 12-bar return over all its windows, on the non-overlapping grid). The measure is the mean of these values, with its t.
- Supporting check: The same mean over the top fifth minus the same mean over the bottom fifth of |forecast| cases is above 0.
- Confirm: The main mean is positive with t >= 2, and the supporting check passes.
- Reject: The main mean is negative with t <= -2.
- Inconclusive: Any |t| below 2, a confirming main measure with a failed check, or fewer than 100 cases in the top fifth.
