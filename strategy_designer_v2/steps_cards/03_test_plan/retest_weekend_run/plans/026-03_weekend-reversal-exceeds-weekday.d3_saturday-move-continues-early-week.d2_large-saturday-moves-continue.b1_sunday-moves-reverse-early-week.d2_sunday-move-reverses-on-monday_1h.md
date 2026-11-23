---
idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: the coin's 24-hour return over Sunday, read at Monday 00:00 UTC -> kept: a calendar regime (the coming bar is Monday 00:00) reads the 24-bar return ending then.
- Comparison: against the coin's usual 30-day move -> kept: the return is divided by the mean absolute 24-bar return over 720 bars.
- Outcome: an opposite move over Monday, larger the higher the 30-day hourly volatility -> kept: the 24-bar hold against the move, with the volatility dependence checked on the record.
- Verdict transfer: yes: the test measures Sunday's scaled move and Monday's reversal, and the reversal's growth with volatility, as the idea states them.
Forecast: The forecast is non-zero only on the bar whose close is Monday 00:00 UTC. That bar's regime has coming weekday 0 and coming hour 0; every other bar's regime is flat. On that bar, `MeanAbsScaledReturnComponent` (period 24, window 720) gives Sunday's 24-hour return in usual 30-day daily moves. It is standardised over its last 500 hourly values and negated. So the forecast is negative after an up Sunday and positive after a down Sunday, and its size grows linearly with the size of Sunday's move in usual moves. It is 0 for a flat Sunday. The 24-bar holding period keeps that bet from Monday 00:00 to Tuesday 00:00, and the position is then flat. Volatility does not enter the size, because `standardise` would cancel it. It is tested by the supporting check instead.
Config: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: Each case is a Monday 00:00 bar with a non-zero position. For each case, take the coin's return over the next 24 bars, minus the coin's mean non-overlapping 24-bar return over all windows, signed by the forecast's sign. The measure is the mean of these values over cases, with its t, before costs.
- Supporting check: Recompute the 720-bar standard deviation of hourly returns from closes at each case. The mean signed excess return of cases above each coin's median of that volatility, minus that of cases below it, must be positive.
- Confirm: The main measure is positive with t >= 2, and the supporting check is positive.
- Reject: The main measure is negative with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A positive main measure with t >= 2 and a non-positive check is also inconclusive. Fewer than 100 cases with a position is inconclusive. Cases whose 24 bars run past a window's end are dropped.
