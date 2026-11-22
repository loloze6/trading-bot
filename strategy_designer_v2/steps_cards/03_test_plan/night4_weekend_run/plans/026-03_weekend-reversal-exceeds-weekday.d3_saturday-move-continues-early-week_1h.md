---
idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 08ec5a873928
---
Fidelity:
- Situation: a coin's 24-hour return over Saturday -> kept: the 24-bar return from Saturday 00:00 to Sunday 00:00 (UTC), read at Monday 00:00 by a 24-bar lag and counted in the coin's usual hourly moves.
- Comparison: the larger Saturday's move, the larger the continuation -> kept: the position's size grows with the size of Saturday's move.
- Outcome: the price moves the same way as Saturday's move over the next two days, Monday and Tuesday -> kept: the bet is taken at Monday 00:00 and held 48 bars.
- Verdict transfer: yes: the test bets with Saturday's sign, sized by its size, over Monday and Tuesday only, so a positive or negative result speaks to the idea itself.
Forecast: The forecast is active on one bar a week, the bar that closes at Monday 00:00 UTC. A regime rule selects it: the coming bar is weekday 0 at hour 0. On that bar the forecast is Saturday's 24-hour return, from close[t-48] to close[t-24], divided by the standard deviation of the 168 hourly returns that end at Saturday's close. That value is standardised over its past 192 hourly values. It is positive after a Saturday rise and negative after a Saturday fall, and it grows with the size of the move. On every other bar the regime is null and the forecast is 0. The holding period keeps each Monday bet for 48 bars, through Tuesday.
Config: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: The slope, across cases, of the coin's 48-bar return from the Monday 00:00 entry bar, minus the coin's normal 48-bar drift (its mean over all windows), regressed on that bar's forecast. One case per coin-week; the cases do not overlap.
- Supporting check: The mean unusual move in the forecast's direction is above 0 over all cases (the forecast's sign times the return minus the drift).
- Confirm: The slope is positive with t ≥ 2 over at least 500 cases, and the supporting check's mean is above 0.
- Reject: The slope is negative with t ≤ -2 over at least 500 cases, which means Saturday's move is reversed on Monday and Tuesday.
- Inconclusive: Any slope with |t| < 2 is inconclusive. A positive slope with t ≥ 2 whose supporting mean is not above 0 is also inconclusive. Fewer than 500 cases is inconclusive whatever the result.
