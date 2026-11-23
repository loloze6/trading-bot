---
idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a coin's 24-hour return over Sunday, measured at Monday 00:00 UTC -> kept: a regime fires only on the bar whose close is Monday 00:00, and the component reads that bar's 24-bar return.
- Comparison: the move measured in the coin's usual 30-day move -> kept: the return is divided by the mean absolute 24-bar return over 720 bars.
- Outcome: an opposite move over Monday and Tuesday, larger after larger Sunday moves -> kept: the bet is against the sign of the move, grows with its size, and is held 48 bars.
- Verdict transfer: yes: the test bets against Sunday's move in usual moves at Monday 00:00 and holds it for two days, which is the idea as stated.
Forecast: The forecast is non-zero only on the hourly bar that closes at Monday 00:00 UTC. The regime detector finds that bar with two rules: the coming bar's weekday is Monday (0) and its hour is 0. On that bar the component reads Sunday's 24-bar return (MeanAbsScaledReturnComponent, period 24, window 720), measured in multiples of the coin's mean absolute 24-hour return over the last 30 days. The value is standardised against the coin's own past values (window 500, min_periods 120) and then negated. So the forecast is short after a Sunday rise and long after a Sunday fall, and its size grows linearly with Sunday's move in usual moves, capped at ±20. On every other bar the regime is null and the forecast is 0. The holding period keeps each Monday bet for 48 bars.
Config: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: The cases are the Monday 00:00 bars with a non-zero forecast, one per coin per week, so the cases do not overlap. For each case, take the coin's 48-bar return from that bar's close minus the coin's mean 48-bar return over all windows. Regress that drift-adjusted return on the forecast (`post_pipeline_value` of `sunday_move`) across all coins and cases. Report the slope and its t.
- Supporting check: Over cases with |forecast| ≥ 2, the mean of the drift-adjusted 48-bar return times the forecast's sign must be above 0.
- Confirm: The slope is positive with t ≥ 2, and the supporting check passes.
- Reject: The slope is negative with t ≤ -2, which means Sunday's move continues rather than reverses.
- Inconclusive: The result is inconclusive when t lies between -2 and 2, or when t ≥ 2 but the check fails. The test needs at least 200 cases across all coins and windows; with fewer, the result is inconclusive.
