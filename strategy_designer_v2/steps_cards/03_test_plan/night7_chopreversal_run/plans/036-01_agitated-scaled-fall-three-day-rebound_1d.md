---
idea: 036-01_agitated-scaled-fall-three-day-rebound
brief: 036_agitated-fall-three-day-recovery
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: a coin's one-day fall against its 30-day daily swing, in an agitated market -> kept: the one-day return divided by the 30-day std of daily returns, falls only; the agitated profile is added by code
- Comparison: larger scaled fall against smaller scaled fall -> kept: the forecast grows with the scaled fall
- Outcome: the price rises over the next three days, more after larger falls -> kept: held 3 daily bars, gain graded by the fall's size
- Verdict transfer: yes: the forecast is the idea's scaled fall itself, held over its three-day horizon inside its agitated profile.
Forecast: One indicator: the day's return divided by the standard deviation of the last 30 daily returns (VolatilityScaledReturnComponent, period 1, vol_period 30). It is standardised against its own past 60 values, sign-flipped, and clipped at 0. The forecast is positive only on days that closed down, and it grows linearly with the fall measured in usual daily moves. It is 0 on up or flat days, so the book is long only. Code keeps the book flat outside the agitated profile.
Config: 036-01_agitated-scaled-fall-three-day-rebound_1d_config.json
Profile: agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: The cases are the bars with forecast > 0 on the non-overlapping 3-bar grid of each window. For each case, take the coin's return over the next 3 bars minus the coin's mean 3-bar return over all its windows. Regress that excess return on the forecast; the measure is the slope's t, with cases of the same day taken together.
- Supporting check: The forecast-weighted mean of the excess return from close[t+1] to close[t+3] over the same cases is above 0. This tests that the rise is not confined to the next day and given back.
- Confirm: The slope t is 2 or more, with at least 100 cases, and the supporting check passes.
- Reject: The slope t is -2 or less, with at least 100 cases.
- Inconclusive: A slope t between -2 and 2, or a confirming slope whose supporting check fails, is inconclusive. Fewer than 100 cases across all coins and windows is also inconclusive.
