---
idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a coin's 24-hour return over Saturday -> kept: the Saturday 00:00–24:00 UTC return, read at Sunday's last bar (lag 24), in usual moves.
- Comparison: the larger Saturday's move, the larger the continuation -> kept: the position grows with the size of Saturday's return.
- Outcome: a move in the same direction over the next two days, Monday and Tuesday -> kept: the position follows Saturday's sign from Monday 00:00, held 48 bars.
- Verdict transfer: yes: the test measures whether Monday and Tuesday's move follows Saturday's sign and grows with its size, which is exactly the idea.
Forecast: The forecast is computed once a week, on the bar whose next bar starts Monday 00:00 UTC; it is 0 on every other bar. The regime detector selects that bar with two calendar measures, the weekday and the hour of the coming bar. The signal is Saturday's 24-hour return: `VolatilityScaledReturnComponent` with period 24 and lag 24, which is the close at the end of Saturday against the close at the end of Friday. It is divided by the 30-day (720-bar) standard deviation of hourly returns, so that it reads in usual moves. `standardise` (window 500, min_periods 120) then scales it against its own past values. The forecast is long after a rising Saturday and short after a falling one. Its size grows linearly with the size of Saturday's move, up to the cap of 20. The bet is held for 48 bars, which covers Monday and Tuesday.
Config: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: On each case (a bar where the regime is trending and |forecast| ≥ 2), take the coin's 48-bar return from that bar's close, minus the coin's mean 48-bar return over all its windows. Regress this excess return on the bar's forecast, pooled over coins and windows, and measure the slope against zero.
- Supporting check: The mean of sign(forecast) × (48-bar return − the coin's mean 48-bar return) over the cases must be above 0.
- Confirm: The slope is positive with t ≥ 2 and the supporting mean is above 0.
- Reject: The slope is negative with t ≤ −2, meaning Saturday's move is reversed early in the week.
- Inconclusive: Any slope with |t| < 2, or a positive slope with t ≥ 2 whose supporting mean is not above 0. A verdict needs at least 300 cases (about 400 weekends per coin are available).
