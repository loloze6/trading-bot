---
idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the coin's weekend move (Sunday close-to-close), sized against its usual daily move -> kept: the Sunday bar's one-day return divided by the 20-day standard deviation of daily returns, read only at the Sunday close.
- Comparison: the weekend move's size relative to the coin's usual daily move -> kept: the volatility scaling, so a larger scaled move gives a larger opposite position.
- Outcome: over the next 2 days (Monday and Tuesday) the price moves against the weekend move, more after larger moves -> adapted: holding period dropped; the position lasts one bar (Monday), and the 2-bar return after Sunday's close is still measured.
- Verdict transfer: yes: the measure ties the Sunday-close forecast to the 2-bar return that follows, which is the idea's claim.
Forecast: The forecast is active only at the Sunday bar's close, when the coming bar is Monday. A weekday regime selects that bar; on every other bar the forecast is 0 (flat). On that bar the forecast is the Sunday one-day return divided by the standard deviation of the last 20 daily returns. It is standardised against its own past 60 daily values, and the sign is flipped: - It is short after a weekend rise and long after a weekend fall. - Its size grows with the weekend move measured in usual daily moves, capped at ±20.
Config: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways_1d_config.json
Criterion:
- Horizon: 2 bars
- Main measure: Take every Sunday-close bar where the forecast is not 0. These bars are 7 days apart, so the samples do not overlap. On each one, compute (forecast / 10) × (r2 − m2): - r2 is close[t+2] / close[t] − 1, inside the window. - m2 is the coin's mean non-overlapping 2-bar return over all windows (holding the coin). Pool these over coins and windows and test the mean with the ordinary t of the mean, before costs.
- Supporting check: Split the cases at the median of |forecast|. The mean of −sign(weekend move) × (r2 − m2) on the half with the larger |forecast| minus the same mean on the smaller half must be above 0.
- Confirm: The mean is above 0 with t ≥ 2.0, and the supporting check is above 0.
- Reject: The mean is below 0 with t ≤ −2.0.
- Inconclusive: Any t between −2.0 and 2.0 is inconclusive, and so is t ≥ 2.0 with the supporting check at or below 0. At least 300 Sunday cases are needed; fewer is inconclusive.
