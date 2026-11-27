---
idea: 086-01_first-down-day-streak-length
brief: 086_rising-agitated-first-dip-continues
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: bd33e939b067
---
Fidelity:
- Situation: in a rising, agitated market, a down close after a streak of consecutive up days -> kept: a regime on the up-run length broken by today's down close (2 or more up days), with the profile added by code.
- Comparison: the fall is larger the more up days the streak held -> kept: the forecast grows with the number of up days in the broken run.
- Outcome: the price keeps falling over the next 3 days -> kept: a short held for 3 daily bars.
- Verdict transfer: yes: the book is short only on first down days after up runs in the profile, sized by run length, and held for the idea's 3 days.
Forecast: On every bar, `PriorDownRunOnUpCloseComponent` (`side` "up", `form` "count", `max_bars` 30) gives the number of consecutive up days that today's down close breaks, and 0 otherwise. The regime detector selects `trending` only when that count is 2 or more; every other bar is in `unknown`, which is flat. Inside the regime, the same count is standardised over its 60 past values. Those past values are mostly 0, so the mean is about 0.5, and the target is set to 2 so the size stays graded instead of sitting at the cap. The value is then negated and clipped at 0, which makes it short only. The forecast is about -4 per up day in the broken run: -8 for 2 days, -12 for 3, -16 for 4, reaching the cap of -20 at 5 or more. It is zero outside the situation and outside the rising-agitated profile, which code adds.
Config: 086-01_first-down-day-streak-length_1d_config.json
Side: short only (the brief): each component's forecast capped at 0 by step 3's code
Profile: rising agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: The unusual move per case. A case is a short bet of the forecast, read once per 3-bar grid cell. Its unusual move is the coin's 3-bar return from the signal bar's close, minus the coin's normal 3-bar drift over all windows, taken in the short direction. The measure is the mean of these, with its t computed with same-day cases taken together.
- Supporting check: Across cases, the least-squares slope of the short-direction unusual move on the broken run's length (`last_history_value`) is positive with t ≥ 1.5.
- Confirm: The mean unusual move is above 0 with t ≥ 2, and the supporting check passes.
- Reject: The mean unusual move is below 0 with t ≤ -2, meaning the price rises more than its normal drift after these days.
- Inconclusive: Any t between -2 and 2, or a confirmed mean whose slope check fails. Fewer than 30 cases on at least 30 distinct days is also inconclusive.
