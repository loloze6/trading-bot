---
idea: 050-04_falling-calm-range-scaled-week-rise
brief: 050_calm-downtrend-scaled-weeks-continue
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: bd33e939b067
---
Fidelity:
- Situation: a coin that has risen over the last 7 days -> kept: the 7-day return clipped at 0, so the book is flat when the coin has not risen.
- Comparison: the 7-day rise in units of the 30-day average daily range -> adapted: graded, so the position grows with the rise measured in mean daily high-low ranges (relative to the close).
- Outcome: keeps rising over the next 3 days, more for larger scaled rises -> kept: a long position held 3 bars, sized by the scaled rise.
- Verdict transfer: yes: the forecast is the idea's own scaled 7-day rise, the outcome is its 3-day rise, and the profile is added by code.
Forecast: The forecast uses MeanAbsScaledReturnComponent with period 7, window 30, base "mean_relative_range" and form "ratio". Its raw value is the 7-day return divided by the 30-day mean of (high − low) / close. It is standardised against its last 60 values (min_periods 20), then clipped at 0. The forecast is positive and grows linearly with the scaled rise when the coin is up over 7 days. It is 0 when the coin is flat or down over 7 days. It is never negative. Outside the falling calm profile, step 3's code keeps it at 0.
Config: 050-04_falling-calm-range-scaled-week-rise_1d_config.json
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: The unusual move of the cases. A case is a rise of the forecast of at least the band, read on the non-overlapping 3-bar grid of each window. For each case, take the coin's 3-bar return from the signal's close minus the coin's mean 3-bar return over all windows. Report its mean and its t, with the cases of the same day pooled.
- Supporting check: Among the cases, compare the mean unusual move of the larger-forecast half with that of the smaller-forecast half. The difference (larger minus smaller) must be above 0.
- Confirm: The main measure's mean unusual move is positive with t ≥ 2, and the supporting difference is above 0.
- Reject: The main measure's mean unusual move is negative with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A main t ≥ 2 with a supporting difference at or below 0 is also inconclusive. So is a result from fewer than 30 distinct days with cases, which is the minimum count.
