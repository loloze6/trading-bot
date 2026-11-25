---
idea: 046-02_calm-scaled-rise-two-day-continues
brief: 046_calm-large-rise-delayed-follow-through
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 0e977cd77240
---
Fidelity:
- Situation: a one-day rise, large against the coin's 30-day daily swing -> kept: the day's return over the 30-day std of daily returns, counted only when the day rose (calm profile added by code).
- Comparison: the rise's size against the coin's 30-day daily swing -> kept: the return is divided by that std.
- Outcome: the coin rises over the next two days, more the larger the rise -> kept: a long position graded by the scaled rise, held 2 bars.
- Verdict transfer: yes: the forecast is the idea's own scaled rise inside its calm profile, and the position earns exactly the next two days' move.
Forecast: The forecast is the day's return divided by the standard deviation of the last 30 daily returns (`VolatilityScaledReturnComponent`, period 1, vol_period 30). It is standardised against its own past 60 values and clipped at 0. It is 0 on down or flat days. On up days it is positive and grows linearly with the rise in usual daily moves. It is never negative. The code keeps the book flat outside calm bars.
Config: 046-02_calm-scaled-rise-two-day-continues_1d_config.json
Profile: calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 2 bars
- Main measure: On each window's non-overlapping 2-bar grid, take the bars with forecast > 0. Regress the coin's 2-bar forward return close[t+2]/close[t]-1, minus that coin's mean 2-bar return over all its windows, on the forecast. The result is the slope and its t.
- Supporting check: The forecast-weighted mean of the same excess 2-bar return on those bars is above 0.
- Confirm: The slope's t is 2 or more, and the forecast-weighted mean excess return is above 0.
- Reject: The slope's t is -2 or less: larger calm rises are followed by smaller or more negative two-day returns than the drift.
- Inconclusive: A slope t between -2 and 2 is inconclusive. A t of 2 or more with a non-positive weighted mean is also inconclusive. Any result on fewer than 100 grid bars with forecast > 0, across all coins and windows, is inconclusive.
