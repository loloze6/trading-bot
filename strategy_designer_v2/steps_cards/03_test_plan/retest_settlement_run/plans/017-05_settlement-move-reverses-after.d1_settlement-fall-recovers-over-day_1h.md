---
idea: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a fall over the 2 hours before a 00:00 or 16:00 UTC settlement -> kept
- Comparison: the fall sized against the coin's usual 2-hour move -> kept
- Outcome: the coin rises over the next 24 hours, more after a larger fall; long only -> kept
- Verdict transfer: yes: the config sizes a long bet on each 00:00 and 16:00 settlement by the scaled 2-hour fall into it, and holds that bet for 24 hours.
Forecast: The regime detector reads the clock with HourOfDayComponent. It selects `mean_reversion` only on the bar whose close is a 00:00 or 16:00 UTC settlement. Those are the bars stamped 23:00 and 15:00, where the coming bar starts at hour 0 or 16. Every other bar is `unknown`, which is flat. On a settlement bar the forecast is built from MeanAbsScaledReturnComponent (period 2, window 720). Its raw value is the 2-hour return into settlement divided by the mean absolute 2-hour return of the last 30 days. The transforms are, in order: - standardise (window 500, min_periods 120), which puts the value on the forecast scale against its own past; - negate, so a fall reads positive; - clip at min 0, so the forecast is long-only. The forecast is 0 after a rise into settlement, and on every non-settlement bar. It grows continuously with the size of the fall measured in usual 2-hour moves, capped at 20. Each bet is held for 24 bars through the holding period.
Config: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The measure is taken over cases. A case is a settlement bar with forecast above 0, read once per 24-bar grid cell. For each case, take the coin's 24-bar return from the signal bar's close, minus the coin's normal 24-bar drift over all windows. The main measure is the forecast-weighted mean of these excess returns, before costs.
- Supporting check: The mean excess return of cases in the top half of forecast, minus that of the bottom half, is above 0.
- Confirm: Both of these hold: - the forecast-weighted mean excess return is above 0 with t >= 2; - the supporting check passes.
- Reject: The forecast-weighted mean excess return is below 0 with t <= -2.
- Inconclusive: Any t strictly between -2 and 2 is inconclusive. A confirming main measure whose supporting check fails is also inconclusive. Fewer than 100 independent cases over all coins and windows is inconclusive whatever the result.
