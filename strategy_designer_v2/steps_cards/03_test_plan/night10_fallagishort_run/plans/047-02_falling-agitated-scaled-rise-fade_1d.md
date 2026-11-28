---
idea: 047-02_falling-agitated-scaled-rise-fade
brief: 047_agitated-downtrend-scaled-days-reverse
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: bd33e939b067
---
Fidelity:
- Situation: an up day, sized by its rise in units of the 30-day daily-return swing -> kept
- Comparison: the day's rise against its 30-day daily-return standard deviation -> kept
- Outcome: the price falls over the next 3 days, more after a larger scaled rise -> kept
- Verdict transfer: yes: the book is short only on up days, sized by the scaled rise, and held 3 days, so its gains measure exactly the claimed fall.
Forecast: The indicator is `VolatilityScaledReturnComponent` with period 1 and vol_period 30: the day's return divided by the standard deviation of the last 30 daily returns. It is standardised over its past 60 values, negated, and clipped at a maximum of 0. On a down or flat day the forecast is 0. On an up day it is negative (short), and its size grows linearly with the rise in usual daily moves. A rise of the usual absolute size gives about -10, and the forecast is capped at -20. Step 3's code keeps the book flat outside the falling agitated profile.
Config: 047-02_falling-agitated-scaled-rise-fade_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: The unusual move per case. A case is a short bet (a fall of the forecast of at least 2 points), read once per cell of a 3-bar grid in each window. The unusual move is the coin's 3-bar return from the signal's close minus the coin's mean 3-bar return over all windows, signed short. Its t clusters the cases of one day together.
- Supporting check: The cases with forecast at or below -10 (larger scaled rises) have a mean unusual move above that of the cases with forecast between 0 and -10. The difference is the larger group minus the smaller group, and it must be above 0.
- Confirm: The mean unusual move is positive (prices fall) with a day-clustered t of 2 or more, and the supporting check passes.
- Reject: The mean unusual move is negative (prices rise after up days) with a day-clustered t of -2 or less.
- Inconclusive: The result is inconclusive when the t lies between -2 and 2, or when the main measure confirms but the check fails. At least 30 days with cases are required, otherwise the result is inconclusive.
