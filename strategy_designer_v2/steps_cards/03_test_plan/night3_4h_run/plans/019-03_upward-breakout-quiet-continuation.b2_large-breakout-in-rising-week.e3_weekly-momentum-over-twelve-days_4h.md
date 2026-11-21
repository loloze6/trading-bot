---
idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e3_weekly-momentum-over-twelve-days
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 3d6ac1c822df
---
Fidelity:
- Situation: a coin's 7-day return, measured in units of its own 4h volatility -> kept: VolatilityScaledReturnComponent, 42-bar return over 20-bar 4h-return volatility times sqrt(42).
- Comparison: larger scaled returns against smaller ones (the size of the return) -> kept: the forecast grows linearly with the scaled return.
- Outcome: the coin rises more over the next twelve days (72 bars), in the return's direction -> kept: 72-bar hold, judged against the coin's normal drift.
- Verdict transfer: yes: the forecast is the idea's own measure, held over the idea's own horizon, so its forward-return relation confirms or rejects the idea directly.
Forecast: One component, VolatilityScaledReturnComponent with period 42 (7 days of 4h bars), vol_period 20 (the default) and lag 0. It is the 42-bar return divided by the 20-bar standard deviation of 4h returns times sqrt(42). It is standardised over its past 60 values (min_periods 20), so its average size is about 10, capped at ±20. It is ungated and signed. It is positive (long) after a rise and negative (short) after a fall. Its size grows linearly with the volatility-scaled 7-day move. It is zero only when the 7-day return is zero.
Config: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e3_weekly-momentum-over-twelve-days_4h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: On each window's non-overlapping 72-bar grid, take the coin's 72-bar forward return minus its normal drift (its mean 72-bar return over all windows). Regress it, pooled across coins and windows, on the forecast at the grid bar. The measure is the slope's t-statistic.
- Supporting check: The same slope, computed per coin, is positive for at least 4 of the 6 coins.
- Confirm: The pooled slope has t >= 2 and the supporting check passes.
- Reject: The pooled slope has t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive, and so is t >= 2 when the per-coin check fails. At least 300 grid cases with a non-zero forecast are required (about 1,400 are expected); with fewer, the result is inconclusive.
