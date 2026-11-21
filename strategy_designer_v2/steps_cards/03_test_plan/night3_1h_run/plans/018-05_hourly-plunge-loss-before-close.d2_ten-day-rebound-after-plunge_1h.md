---
idea: 018-05_hourly-plunge-loss-before-close.d2_ten-day-rebound-after-plunge
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 1efb53e47d25
---
Fidelity:
- Situation: the 24-hour return, read at an hourly close, falls by several times the 30-day average absolute daily return -> adapted: "several times" becomes graded, the 24-bar fall measured in usual daily moves with a cubic dead zone.
- Comparison: the 30-day average absolute daily return, and the 30-day return before the drop -> kept: the mean absolute 24-bar return over 720 bars, multiplied by the positive 720-bar return, which ends at the signal bar.
- Outcome: the coin rises over the next 10 days more than its normal drift, more so the larger the prior 30-day return -> kept: long, held for 240 bars, judged against the coin's drift and against the forecast's size.
- Verdict transfer: yes: the forecast is the idea's fall-times-prior-rise reading, held for the idea's 10 days and judged against holding the coin.
Forecast: One component, MeanAbsScaledFallTimesRiseComponent (fall_period 24, window 720, rise_period 720). It multiplies two factors. The first is the 24-hour fall measured in usual daily moves, taken as the mean absolute 24-bar return over the last 30 days. The second is the positive 30-day percent return. It is 0 when the last 24 hours did not fall or the 30-day return is not positive. It is standardised against its own past 500 values, with min_periods 120. Then signed_power, exponent 3, pivot 10, keeps ordinary drops near zero and amplifies the sharp ones. The forecast is never negative: long only. It is zero when there is no drop. It grows with the depth of the drop and the size of the prior rise.
Config: 018-05_hourly-plunge-loss-before-close.d2_ten-day-rebound-after-plunge_1h_config.json
Criterion:
- Horizon: 240 bars
- Main measure: A case is a long bet: a rise of the forecast of at least 2 points, read once per non-overlapping 240-bar grid cell of each window. For each case, take the coin's return over the next 240 bars from the signal bar's close, inside the same window. Subtract the coin's normal 240-bar drift, its mean over all windows. The measure is the t of the mean of these unusual moves, pooled over coins.
- Supporting check: Across the cases, the slope of the unusual move on the signal bar's forecast is positive, with a t of 1 or more. This checks "larger prior rise, larger rebound".
- Confirm: The mean unusual move is positive with t >= 2 over at least 30 cases, and the supporting check passes.
- Reject: The mean unusual move is negative with t <= -2 over at least 30 cases.
- Inconclusive: The idea is neither confirmed nor rejected when: - t lies between -2 and 2; - t >= 2 but the slope check fails; - there are fewer than 30 cases over all coins and windows.
