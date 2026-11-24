---
idea: 031-03_fading-volume-after-rise-reverses
brief: 031_medium-term-overreaction-reversal
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 31f1a8c6c7f6
---
Fidelity:
- Situation: after an unusually large 90-day rise -> adapted: "after" made "while"; the regime holds only while the 90-day return is at least 2 usual 90-day moves (1-year mean absolute 90-day return).
- Comparison: 14-day volume dropped below the run's average daily volume -> kept: the mean volume of the last 14 days over the mean of the 90-day run, graded by the size of the drop.
- Outcome: price falls over the next 30 days -> kept: a short position, larger the deeper the volume drop, held 30 bars.
- Verdict transfer: yes: the test measures this rise, this volume drop and the 30-day fall, so a clear result either way speaks for the idea.
Forecast: A regime holds only while the 90-day return is at least 2.0 times the coin's mean absolute 90-day return over the past 365 days. That rise is measured by MeanAbsScaledReturnComponent (period 90, window 365). Outside that regime the forecast is 0. Inside it, the forecast comes from VolumeRatioComponent, centred: the mean volume of the last 14 days divided by the mean volume of the last 90 days, minus 1. It is standardised over 90 bars and clipped at a maximum of 0. So the forecast is negative (short) only when recent volume is below the run's average. The short grows in proportion to how far volume has dropped. It is zero when recent volume is at or above the average. It is never positive.
Config: 031-03_fading-volume-after-rise-reverses_1d_config.json
Criterion:
- Horizon: 30 bars
- Main measure: On the non-overlapping 30-bar grid of each window, take the grid bars in the regime. On each, compute the coin's 30-day return minus its mean 30-day return over all windows (holding the coin). Regress that excess return on the forecast and read the slope's t, with the number of cases.
- Supporting check: On the cases with a short bet (forecast at or below -2), the mean excess 30-day return is below 0.
- Confirm: Slope above 0 with t ≥ 2.0, so a deeper volume drop is followed by a lower excess return. The supporting check must also pass.
- Reject: Slope below 0 with t ≤ -2.0, so a deeper volume drop is followed by a higher excess return.
- Inconclusive: Any slope with |t| < 2.0. Also a confirming slope whose check fails. Also fewer than 30 regime grid cases across all coins and windows.
