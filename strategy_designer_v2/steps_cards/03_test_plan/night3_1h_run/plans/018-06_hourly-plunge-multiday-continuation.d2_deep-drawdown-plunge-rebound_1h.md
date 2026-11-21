---
idea: 018-06_hourly-plunge-multiday-continuation.d2_deep-drawdown-plunge-rebound
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 1efb53e47d25
---
Fidelity:
- Situation: a coin's 24-hour drop, in multiples of its 30-day average absolute daily return, while it stands far below its 30-day high -> kept: a regime selects bars 20 % or more below the 720-bar closing high, and there the drop is graded in usual daily moves.
- Comparison: the deeper the coin stands below that high, the larger the rise -> kept: the depth is recomputed from closes on each case and its rebounds are compared by depth.
- Outcome: the price rises over the next 3 days -> kept: a long position held 72 bars.
- Verdict transfer: yes: both the drop's graded effect and the depth effect are measured as stated, over the idea's 3-day horizon.
Forecast: The regime is active only on bars whose close is at least 20 % below the highest close of the last 720 bars (the convention for "far below", read from `DistanceFromHighComponent`, period 720). On every other bar the forecast is 0. On active bars, the 24-bar return is measured in multiples of its 720-bar mean absolute 24-bar return (`MeanAbsScaledReturnComponent`, period 24, window 720). That value is standardised over 500 past values and negated, so a drop reads positive. It is clipped at 0, so the forecast is long only. It then goes through `signed_power` with exponent 3, the strongest graded dead zone. The forecast stays near 0 for ordinary drops and grows steeply with drops of several usual daily moves, up to the +20 cap. It is never negative.
Config: 018-06_hourly-plunge-multiday-continuation.d2_deep-drawdown-plunge-rebound_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: The cases are the bets: rises of the forecast of at least 2 points, read once per 72-bar grid cell of each window and pooled over all coins and windows. For each case, take the 72-bar return from the signal's close minus the coin's normal 72-bar drift. Measure the mean of this unusual move and its t, against holding the coin and before costs.
- Supporting check: For each case, recompute the depth from closes: (close − highest of the last 720 closes) / that high × 100. The deeper half of the cases (depth below the cases' median) must show a larger mean unusual move than the shallower half (Welch difference, deeper minus shallower, above 0).
- Confirm: The idea is confirmed when the mean unusual move is above 0 with t ≥ 2 over at least 30 cases, and the deeper half's mean unusual move exceeds the shallower half's.
- Reject: The idea is rejected when the mean unusual move is below 0 with t ≤ −2 over at least 30 cases.
- Inconclusive: A main t between −2 and 2 is inconclusive. So is a main t of 2 or more with a failed depth check, or fewer than 30 cases.
