---
idea: 017-05_settlement-move-reverses-after.d1_extreme-two-hour-move-reverses
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a coin's 2-hour move, the larger the stronger -> kept: the 2-bar return, graded by its size.
- Comparison: relative to its usual 2-hour move -> kept: divided by the 20-bar volatility of 1h returns times sqrt(2).
- Outcome: the coin gives back the move over the next 24 hours, more so for extreme moves -> kept: a faded position held 24 bars, convex in the move's size.
- Verdict transfer: yes: the forecast fades the volatility-scaled 2-hour move convexly over 24 hours, so either result is the idea's own.
Forecast: The forecast starts from the coin's 2-hour return measured in usual 2-hour moves (VolatilityScaledReturnComponent, period 2, vol_period 20, the conventional volatility window). This value is standardised over its past 60 values, so an average move reads about 10, capped at ±20. It is then negated, so the forecast fades the move: short after a rise, long after a fall. Last, it is passed through signed_power with exponent 3 and pivot 20, the strongest graded dead zone the guide allows. An ordinary move (about 10) gives about 2.5. A small one gives nearly 0. The most violent moves (about 20) give the full ±20. The forecast is 0 only when the 2-hour move is 0. It is ungated and runs on every bar.
Config: 017-05_settlement-move-reverses-after.d1_extreme-two-hour-move-reverses_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The mean unusual move per case, pooled over all coins and windows, with its ordinary t. A case is a bet: a rise of the forecast on its side of at least 2 points, read once per non-overlapping 24-bar grid cell. The unusual move is the coin's 24-bar return from the signal bar's close, minus the coin's normal 24-bar drift over all its windows, taken in the signal's direction. Measured before costs.
- Supporting check: The mean unusual move of the cases in the top quartile of |forecast| at the signal bar minus that of the other cases is above 0, so the give-back grows fastest for the most extreme moves.
- Confirm: Confirmed only if the main measure has t ≥ 2 over at least 30 cases and the supporting check's difference is above 0.
- Reject: Rejected if the main measure has t ≤ -2 over at least 30 cases, meaning the extreme moves continue rather than reverse.
- Inconclusive: Inconclusive if t is between -2 and 2, or if t ≥ 2 but the top-quartile difference is not above 0, or if there are fewer than 30 cases.
