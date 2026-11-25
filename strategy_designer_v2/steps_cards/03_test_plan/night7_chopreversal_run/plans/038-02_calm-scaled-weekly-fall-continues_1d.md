---
idea: 038-02_calm-scaled-weekly-fall-continues
brief: 038_calm-market-scaled-move-continues
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: a coin's 7-day fall, in a calm market -> kept: the 7-bar return, short side only, graded by its size; the calm profile is added by code.
- Comparison: the fall measured against the coin's 30-day daily swing -> kept: the 7-bar return divided by the 30-bar standard deviation of daily returns.
- Outcome: a further fall over the next 5 days, larger for larger scaled falls -> kept: a short position sized by the scaled fall, held 5 bars.
- Verdict transfer: yes: the forecast is the idea's scaled fall inside its profile, held for its horizon, so a confirm or a reject carries over to the idea.
Forecast: The forecast uses VolatilityScaledReturnComponent with period 7 and vol_period 30. Its raw value is the 7-day return divided by (the 30-day standard deviation of daily returns x sqrt 7), so it is negative after a fall. The value is standardised (window 60, min_periods 20), which gives about -10 for a typical fall, capped at -20. It is then clipped at a maximum of 0. The forecast is therefore 0 after a 7-day rise, negative after a 7-day fall, and its size grows linearly with the fall in usual moves. It is never positive. The code's calm profile keeps the book flat outside calm markets.
Config: 038-02_calm-scaled-weekly-fall-continues_1d_config.json
Profile: calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The unusual move over 5 bars, before costs, in the short direction. Per case (a short bet of at least the band, one per 5-bar grid cell), it is minus (the 5-bar return minus the coin's normal 5-bar drift over all windows). Its t takes the cases of one day together.
- Supporting check: Use the bars of the 5-bar grid where the forecast is below 0. The slope of the short-direction unusual 5-bar return on abs(forecast) must be above 0, so that a larger scaled fall comes with a larger further fall.
- Confirm: The mean unusual move in the short direction is above 0 with t >= 2, and the supporting slope is above 0.
- Reject: The mean unusual move in the short direction is below 0 with t <= -2, which means the falls partly reverse.
- Inconclusive: Any t between -2 and 2 is inconclusive. A confirming t with a slope at or below 0 is also inconclusive. So is any result from fewer than 30 cases or fewer than 30 distinct days.
