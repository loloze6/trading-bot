---
idea: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 2a96c3272007
---
Fidelity:
- Situation: the weekend (Sat 00:00 to Mon 00:00 UTC) had hourly moves more volatile than the previous week's, with a weekend return of a given sign -> adapted: the "more volatile than" threshold becomes graded, as the weekend return times the ratio of the weekend's 48-bar return standard deviation to that of the prior 168 bars, read at the bar closing Monday 00:00.
- Comparison: the weekend's volatility against the previous week's volatility -> kept
- Outcome: the price keeps moving in the weekend return's direction over the next 2 days, more so the higher the volatility ratio -> kept: the bet is held 48 bars from Monday 00:00.
- Verdict transfer: yes: the position follows the weekend return's direction from Monday 00:00 for 2 days, sized by the volatility ratio, so its result over those 48 bars speaks directly to the idea.
Forecast: A regime fires only on the hourly bar whose close is Monday 00:00 UTC; that is the bar stamped Sunday 23:00, where the coming bar is weekday 0 at hour 0. On that bar the forecast is RecentToPriorVolatilityWeightedReturnComponent with period 48, vol_period 48, base_period 168 and base_lag 48. Its value is the weekend's 48-hour percent return times (std of the weekend's 48 hourly returns / std of the 168 hourly returns of the week before). This is standardised over its past 217 values (min_periods 54). The forecast is positive after a rising weekend and negative after a falling one. Its size grows with the weekend return and with how much more volatile the weekend was than the prior week. On every other bar the regime is null and the forecast is 0. The 48-bar holding period carries Monday's bet through Monday and Tuesday.
Config: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: For each case (a bet on the Monday 00:00 bar, at most one per coin per week, so the cases do not overlap), take the coin's 48-bar return from that bar's close. Subtract the coin's normal 48-bar drift over all windows, and sign the result by the forecast. The measure is the mean of this unusual move over the cases, with its t.
- Supporting check: The mean unusual move of the cases whose |forecast| is above the median must exceed that of the cases below the median (difference above minus below > 0).
- Confirm: The mean unusual move is positive with t >= 2, and the supporting check passes.
- Reject: The mean unusual move is negative with t <= -2 (the weekend move reversed).
- Inconclusive: Any t between -2 and 2, or t >= 2 with the check failing, is inconclusive. So is a result on fewer than 100 cases across all coins and windows.
