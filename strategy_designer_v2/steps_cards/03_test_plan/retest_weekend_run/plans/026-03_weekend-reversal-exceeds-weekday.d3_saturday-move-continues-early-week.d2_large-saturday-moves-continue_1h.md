---
idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a coin's 24-hour return over Saturday -> kept: the 24-bar return on the bar whose close is Sunday 00:00 UTC, selected by a calendar regime.
- Comparison: measured against the coin's usual 30-day move -> kept: divided by the mean absolute 24-bar return over the last 720 bars.
- Outcome: same-direction move over the next two days, growing faster than in proportion -> kept: the bet is held 48 bars, with a convex (squared) size.
- Verdict transfer: yes: the forecast is Saturday's move in usual moves, convexly sized and held exactly two days, so its directional gain is the idea's claim.
Forecast: The forecast is non-zero only on the hourly bar stamped Saturday 23:00 UTC, whose close is Sunday 00:00. On that bar it reads MeanAbsScaledReturnComponent (period 24, window 720). That is Saturday's 24-hour return divided by the coin's mean absolute 24-hour return over the last 30 days. The value is standardised against its own past 500 values, all hours included. A signed square (signed_power, exponent 2, pivot 10) is then applied. The forecast is positive after an up Saturday and negative after a down one. It is about 0 for an ordinary Saturday. It grows with the square of the move's size, so a two-usual-move Saturday gets about four times the position of a one-usual-move Saturday. On every other bar the regime is flat (forecast 0). The bet is held for the 48-bar horizon (Sunday and Monday).
Config: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: The cases are Saturday-end bars with a non-zero forecast; each is a separate week, so the cases do not overlap. For each case, x = (forecast / 10) × (the coin's 48-bar return from that bar's close − the coin's normal 48-bar drift over all windows). The measure is the ordinary t of the mean of x over all coins and windows.
- Supporting check: Rank the cases by |forecast| and take the top quartile. Their mean of sign(forecast) × (48-bar return − drift) must be above that of the other cases (difference > 0).
- Confirm: Main t >= 2 and the supporting check passes (top-quartile directional excess return above the rest's).
- Reject: Main t <= -2: the convexly sized position loses against the coin's drift over the two days after Saturday.
- Inconclusive: The idea is neither confirmed nor rejected in three cases: - -2 < t < 2; - t >= 2 but the top quartile does not beat the rest; - fewer than 100 cases, or fewer than 25 in the top quartile.
