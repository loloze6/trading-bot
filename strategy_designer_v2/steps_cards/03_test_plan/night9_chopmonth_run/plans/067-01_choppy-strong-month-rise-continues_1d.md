---
idea: 067-01_choppy-strong-month-rise-continues
brief: 067_choppy-market-monthly-move-continues
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: a coin's 30-day return above zero, in a choppy market -> adapted: the 30-day return is graded and clipped at 0, so the book is flat at or below zero; the choppy profile is added by code
- Comparison: larger 30-day returns against smaller ones -> kept
- Outcome: the coin rises more over the next 7 days -> kept
- Verdict transfer: yes: the forecast is the idea's 30-day rise, held 7 days only in choppy markets, so the test's verdict is the idea's verdict.
Forecast: The forecast is the coin's 30-bar percent return from PriceEvolutionComponent (period 30). It is standardised against its own last 60 values (min_periods 20), so a typical month's move is about 10, capped at 20. It is then clipped at 0. It is positive and grows with the size of the month's rise. It is exactly 0 when the 30-day return is zero or negative. It is never short. The choppy profile, added by code, keeps it at 0 outside choppy markets.
Config: 067-01_choppy-strong-month-rise-continues_1d_config.json
Profile: choppy (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 7 bars
- Main measure: Use the non-overlapping 7-bar grid of each window and keep the cells where the forecast is above 0. On those cells, take the slope of the coin's 7-bar forward return on the forecast, using the return minus the coin's mean 7-bar return over all windows. Give the slope's t and the number of cells.
- Supporting check: On the same cells, the mean of the 7-bar forward return minus the coin's mean 7-bar return is above 0.
- Confirm: The slope's t is 2 or more and the supporting check passes (mean excess return above 0), on at least 100 cells.
- Reject: The slope's t is -2 or less, on at least 100 cells.
- Inconclusive: A slope t between -2 and 2, or a t of 2 or more with a mean excess return at or below 0, or fewer than 100 cells with a forecast above 0.
