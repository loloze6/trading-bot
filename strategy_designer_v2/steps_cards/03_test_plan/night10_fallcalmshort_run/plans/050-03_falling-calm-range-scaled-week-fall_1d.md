---
idea: 050-03_falling-calm-range-scaled-week-fall
brief: 050_calm-downtrend-scaled-weeks-continue
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: bd33e939b067
---
Fidelity:
- Situation: a coin that has fallen over the last 7 days, in a falling calm market -> kept: the 7-day return is clipped so only falls are read, and the code adds the falling calm profile.
- Comparison: the 7-day fall in units of the 30-day average daily range -> kept: the 7-day return is divided by the 30-day mean of (high − low) / close.
- Outcome: the coin keeps falling over the next 3 days, further for larger scaled falls -> adapted: the short position is graded by the scaled fall and held 3 bars.
- Verdict transfer: yes: the forecast is short only after a 7-day fall, sized by that fall in mean daily ranges, and held over the idea's 3 days.
Forecast: The forecast uses one component, `MeanAbsScaledReturnComponent` with `period` 7, `window` 30, `base` "mean_relative_range" and `form` "ratio". It is the 7-day return divided by the 30-day mean of the daily (high − low) / close. It is standardised over its past 60 values (target 10, cap 20) and then clipped at a maximum of 0. When the coin has fallen over 7 days, the forecast is negative (short). Its size grows linearly with the fall in mean daily ranges. When the 7-day return is zero or positive, the forecast is exactly 0, and it is continuous at that edge. The code limits it to the falling calm profile.
Config: 050-03_falling-calm-range-scaled-week-fall_1d_config.json
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: Use the bars where the forecast is below 0, on the non-overlapping 3-bar grid of each window. For each case, take the coin's 3-bar forward return minus its normal 3-bar drift (its mean over all windows), signed in the short direction. Measure the mean of this unusual move and its t, with cases of one day taken together.
- Supporting check: On the same cases, regress the short-direction unusual move on |forecast|. The slope must be above 0 (the carry grows with the scaled fall).
- Confirm: The main measure's mean is above 0 with t ≥ 2, and the supporting slope is above 0.
- Reject: The main measure's mean is below 0 with t ≤ −2 (a reversal after scaled falls).
- Inconclusive: Anything else is inconclusive. That covers t between −2 and 2, and a main t ≥ 2 with a slope at or below 0. A verdict needs at least 100 grid cases on at least 60 distinct days.
