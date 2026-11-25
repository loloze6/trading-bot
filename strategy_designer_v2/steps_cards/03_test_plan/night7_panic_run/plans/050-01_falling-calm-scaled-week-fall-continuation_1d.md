---
idea: 050-01_falling-calm-scaled-week-fall-continuation
brief: 050_calm-downtrend-scaled-weeks-continue
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 18d3cc56dd45
---
Fidelity:
- Situation: a coin that has fallen over the last 7 days, in a falling calm market -> kept: the 7-day return clipped at zero, so there is no position after a 7-day rise; the profile is added by code.
- Comparison: the size of the 7-day fall in units of the 30-day daily-return swing -> kept: the 7-day return divided by the 30-day standard deviation of daily returns (the constant sqrt(7) cancels in standardise).
- Outcome: keeps falling over the next 3 days, further for larger scaled falls -> kept: short, graded by the scaled fall, held 3 bars.
- Verdict transfer: yes: the short forecast exists only after 7-day falls, its size is the scaled fall, and it is judged on the next 3 days.
Forecast: One component, VolatilityScaledReturnComponent with period 7 and vol_period 30. It reads the 7-day return over the 30-day daily-return swing, times 1/sqrt(7). It is standardised over 60 bars (min_periods 20), then clipped at max 0. The forecast is zero whenever the coin rose over the 7 days. After a fall it is negative (short), and its size grows linearly with the fall in usual moves, capped at -20. It is never positive. The code adds the falling-calm profile, so the book is flat outside it.
Config: 050-01_falling-calm-scaled-week-fall-continuation_1d_config.json
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: The cases are the bars at positions 0, 3, 6, ... of each window where forecast < 0. For each case, take the coin's 3-bar return minus the coin's mean 3-bar return over all windows (its normal drift), and negate it so that a fall is a gain. Average this over the cases. Its t is computed with the cases of one day summed together.
- Supporting check: On the same cases, the least-squares slope of that short-direction excess return on |forecast| is positive, with t ≥ 2 (larger scaled falls carry further).
- Confirm: The main measure is above 0 with t ≥ 2, and the supporting slope is above 0 with t ≥ 2.
- Reject: The main measure is below 0 with t ≤ -2 (a reversal), or the slope is below 0 with t ≤ -2 (the carry shrinks with the fall's size).
- Inconclusive: Any other result, including a main t between -2 and 2, or a main t ≥ 2 with a slope t between -2 and 2. It is also inconclusive if the cases fall on fewer than 30 distinct days.
