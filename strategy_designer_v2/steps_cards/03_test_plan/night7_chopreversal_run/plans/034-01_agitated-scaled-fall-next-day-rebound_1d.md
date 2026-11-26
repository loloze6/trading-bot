---
idea: 034-01_agitated-scaled-fall-next-day-rebound
brief: 034_agitated-market-fall-next-day-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: a coin's one-day fall, sized against its 30-day daily swing, in an agitated market -> kept: the agitated profile is added by code, and the fall in usual daily moves is graded, zero on bars that did not fall.
- Comparison: the fall measured against the 30-day standard deviation of daily returns -> kept
- Outcome: the larger the fall, the larger the rise over the next day -> kept: a graded long held for 1 bar.
- Verdict transfer: yes: the forecast is exactly the idea's fall in usual moves, inside the agitated profile, held over its one-day horizon.
Forecast: The forecast is built from the current day's return divided by the standard deviation of the last 30 daily returns (`VolatilityScaledReturnComponent`, period 1, vol_period 30). It is standardised (window 60, min_periods 20), negated, and clipped at 0. It is positive only after a down day, and it grows linearly with the depth of that fall in usual daily moves. It is 0 on up or flat days and never short. The agitated profile, added by code, keeps the book flat outside agitated markets.
Config: 034-01_agitated-scaled-fall-next-day-rebound_1d_config.json
Profile: agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: The slope of the coin's next-day return, minus that coin's mean daily return over all windows, on the forecast. It is taken over all bars with forecast > 0, pooled across coins and windows. Its t uses cases of one day taken together.
- Supporting check: The mean next-day excess return of the top third of forecast > 0 cases is above that of the bottom third (Welch t ≥ 1).
- Confirm: The slope is positive with t ≥ 2, and the supporting check passes.
- Reject: The slope is negative with t ≤ -2.
- Inconclusive: A slope with t between -2 and 2, or t ≥ 2 with the check failing, is inconclusive. A test with fewer than 150 cases with forecast > 0, or with cases on fewer than 100 distinct days, is inconclusive too.
