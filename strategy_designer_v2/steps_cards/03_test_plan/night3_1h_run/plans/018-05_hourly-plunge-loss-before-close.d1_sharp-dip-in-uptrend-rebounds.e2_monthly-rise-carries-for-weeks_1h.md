---
idea: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e2_monthly-rise-carries-for-weeks
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 1efb53e47d25
---
Fidelity:
- Situation: the coin's 30-day return is positive, measured in multiples of its usual 30-day move -> kept
- Comparison: the coin's normal drift over the same 2 weeks -> kept
- Outcome: a larger scaled 30-day return is followed by a larger rise above drift over the next 2 weeks -> kept
- Verdict transfer: yes: the forecast is the idea's own scaled 30-day return, zero when that return is not positive, held for the idea's 2 weeks.
Forecast: The forecast uses one indicator, MeanAbsScaledReturnComponent with period 720 (30 days of 1h bars) and window 8760 (one year). It is the 720-bar return divided by the mean absolute 720-bar return over the past year, so it reads in multiples of the coin's usual 30-day move. The value is standardised against its own last 500 values (min_periods 120), then clipped at 0. The forecast is zero whenever the 30-day return is not positive. Above zero it grows in proportion to the scaled return, capped at +20, and it is never short.
Config: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e2_monthly-rise-carries-for-weeks_1h_config.json
Criterion:
- Horizon: 336 bars
- Main measure: On each window's non-overlapping 336-bar grid, use the bars with forecast > 0. Regress each bar's 336-bar forward return minus the coin's normal 336-bar drift (its mean over all windows) on the forecast. Report the slope's t, before costs.
- Supporting check: Split the grid bars with forecast > 0 into terciles by forecast. The top tercile's mean excess return over drift must be above 0.
- Confirm: The slope t is 2 or more, the top-tercile mean excess return is above 0, and there are at least 100 cases.
- Reject: The slope t is -2 or less, with at least 100 cases.
- Inconclusive: Any slope t between -2 and 2 is inconclusive. A t of 2 or more with the top-tercile mean at or below 0 is also inconclusive. So is any result with fewer than 100 grid cases where forecast > 0.
