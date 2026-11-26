---
idea: 059-01_calm-decline-continues-return
brief: 059_calm-market-steady-declines-continue
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 4510fe2da56d
---
Fidelity:
- Situation: a coin's 14-day return fallen below zero, in units of its 30-day daily swing, in a calm market -> kept: the 14-day return over the 30-day std of daily returns, short side only; the calm condition is the brief's profile, added by code
- Comparison: the depth of the fall against the coin's own usual daily swing -> kept
- Outcome: a larger fall over the next 5 days, the deeper the decline -> kept: the short position is held 5 bars and grows with the depth
- Verdict transfer: yes: the forecast is the idea's swing-scaled decline, graded and short only, inside the calm profile, judged on the following 5-day returns.
Forecast: The config uses VolatilityScaledReturnComponent with period 14 and vol_period 30. Its raw value is the 14-day return divided by (the 30-day standard deviation of daily returns x sqrt(14)). The sqrt(14) is a constant, and standardise removes it. Standardise (window 60, min_periods 20) puts this value on the forecast scale and keeps its sign. A clip with max 0 then keeps only the falling side. The forecast is 0 when the 14-day return is zero or positive. It is negative (short) when the coin has fallen, and grows in size the deeper the fall is in units of the coin's usual swing, up to -20. It is never positive. The calm profile is added by code, so the book is flat outside calm markets.
Config: 059-01_calm-decline-continues-return_1d_config.json
Profile: calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: Use the non-overlapping 5-bar grid of each window, on bars with forecast < 0. On those bars, take the coin's 5-bar forward return minus its mean 5-bar return over all windows. Measure the slope of that excess return on the forecast (Welch-free OLS t). The expected slope is positive: a more negative forecast should come with a more negative excess return.
- Supporting check: Take the cases (short bets of at least 2 forecast points, one per grid cell). Their mean unusual move in the short direction must be above 0.
- Confirm: The slope's t is 2 or more, and the supporting check's mean unusual move is positive.
- Reject: The slope's t is -2 or less: deeper declines are followed by relatively higher returns, a rebound.
- Inconclusive: The result is inconclusive when the slope's t is between -2 and 2, or when the slope confirms but the check fails. It is also inconclusive with fewer than 100 grid bars with forecast < 0, or fewer than 30 cases.
