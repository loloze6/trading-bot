---
idea: 025-03_bounce-falling-versus-rising-regime.d2_sharp-rises-follow-monthly-trend
brief: 025_bounces-fade-in-falling-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 42de60c4e850
---
Fidelity:
- Situation: a one-day rise of several usual daily moves -> kept: a regime rule, a 1-day return of at least 2 usual (20-day std) daily moves.
- Comparison: the coin's 30-day return, in usual daily moves -> kept: the 30-day return over the 20-day daily std; the constant sqrt(30) cancels under standardise.
- Outcome: the 5-day return is higher the higher that 30-day return -> kept: the position is signed and sized by the 30-day reading and held 5 bars.
- Verdict transfer: yes: the test bets exactly the stated relation on the stated days, over the stated horizon.
Forecast: The forecast is active only on a bar whose 1-day return is at least 2 usual daily moves. VolatilityScaledReturnComponent (period 1, vol_period 20) measures that rise, and the regime detector checks it. On any other bar the forecast is 0. On an active bar, the forecast is the coin's 30-day return in usual daily moves (VolatilityScaledReturnComponent, period 30, vol_period 20). It is standardised against its own last 60 values, so a typical month's move gives about ±10, capped at ±20. It is positive after a rising month and negative after a falling one. Its size grows with the size of that month's move. Each bet is held for 5 bars.
Config: 025-03_bounce-falling-versus-rising-regime.d2_sharp-rises-follow-monthly-trend_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are bars in the trending regime with a non-zero forecast, read once per 5-bar grid cell of each window. For each case, take the coin's 5-day return minus its normal 5-day drift (its mean over all windows). Regress that on the case's forecast (`post_pipeline_value` of month_move), pooling all coins. The measure is the t of the slope.
- Supporting check: none
- Confirm: The slope is positive with t ≥ 2.0, on at least 30 cases.
- Reject: The slope is negative with t ≤ -2.0, on at least 30 cases.
- Inconclusive: Any t between -2.0 and 2.0, or fewer than 30 cases, is inconclusive.
