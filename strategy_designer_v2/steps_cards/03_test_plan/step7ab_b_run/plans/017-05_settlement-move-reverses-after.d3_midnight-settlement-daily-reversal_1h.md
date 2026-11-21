---
idea: 017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the 2-hour return into the 00 UTC funding settlement -> kept: the 2-bar return at the close of the 23:00 bar, with a regime rule that selects only that bar (coming bar starts at 00 UTC).
- Comparison: the move relative to the coin's usual 2-hour move -> kept: the return is divided by the 20-bar volatility of hourly returns times sqrt(2).
- Outcome: the next 24 hours run opposite, and the move back grows with the pre-settlement move -> kept: the negated graded forecast is held 24 bars.
- Verdict transfer: yes: the forecast is the idea's own measure, at its own clock time, held over its own horizon.
Forecast: Only on the bar whose close is 00:00 UTC (HourOfDayComponent reads 0), the forecast is the 2-bar return (22:00 to 00:00 close), divided by the coin's usual 2-hour move (20-bar standard deviation of hourly returns times sqrt 2). It is standardised against its own past 60 hourly values and negated. It is positive after a fall into settlement, negative after a rise, and grows with the size of the move in usual moves (cap ±20). On every other bar the regime is null and the forecast is 0. Each settlement bet is held 24 bars.
Config: 017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The cases are the settlement bars (one per day, so they do not overlap). On each case, take the coin's 24-bar return from that close minus the coin's mean 24-bar return over all windows. Regress this excess return on the bar's forecast, pooled over coins and windows. Report the t of the slope.
- Supporting check: The mean forecast-signed excess return of the top third of cases by |forecast| minus that of the bottom third must be above 0.
- Confirm: The slope is positive with t ≥ 2, and the supporting check passes.
- Reject: The slope is negative with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A positive slope with t ≥ 2 that fails the check is also inconclusive. At least 500 settlement cases with a non-zero forecast are needed; fewer is inconclusive.
