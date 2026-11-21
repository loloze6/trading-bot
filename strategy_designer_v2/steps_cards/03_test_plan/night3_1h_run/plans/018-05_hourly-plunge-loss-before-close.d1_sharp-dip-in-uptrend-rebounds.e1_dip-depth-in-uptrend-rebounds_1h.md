---
idea: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e1_dip-depth-in-uptrend-rebounds
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 1efb53e47d25
---
Fidelity:
- Situation: the 24-hour fall, in multiples of the 30-day average absolute daily return -> kept
- Comparison: only when the coin's 30-day return is positive; rise judged against the coin's normal drift -> kept: the 30-day condition is a regime, and the drift is in the criterion
- Outcome: the coin rises above its normal drift over the next 3 days, more after deeper falls -> kept
- Verdict transfer: yes: the 30-day condition, the scaled fall depth and the 3-day rise against drift are all measured as stated.
Forecast: A regime rule makes the strategy active only while the 720-bar (30-day) return is positive; on all other bars the forecast is 0. While active, the forecast is the 24-bar return divided by the mean absolute 24-bar return over the last 720 bars. It is standardised against its own past 500 values, then negated and clipped at 0. The forecast is 0 when the last 24 hours rose. It is positive after a 24-hour fall, and it grows with the depth of that fall in usual daily moves, up to the cap of 20. It is never short.
Config: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e1_dip-depth-in-uptrend-rebounds_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: Use each window's 72-bar grid, and take the grid bars with forecast > 0 as cases. For each case, the unusual move is the 72-bar forward return minus the coin's mean 72-bar return over all its windows. The measure is the forecast-weighted mean of the unusual move, with the t of the per-case product forecast × unusual move.
- Supporting check: Split the cases into thirds by forecast. The top third's mean unusual move minus the bottom third's must be > 0.
- Confirm: The weighted mean unusual move is > 0 with t ≥ 2, and the top-minus-bottom-third difference is > 0.
- Reject: The weighted mean unusual move is < 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t ≥ 2 with a failed supporting check is also inconclusive. So is any result with fewer than 200 cases over all coins and windows.
