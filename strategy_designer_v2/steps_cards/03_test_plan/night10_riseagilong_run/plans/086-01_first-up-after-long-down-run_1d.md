---
idea: 086-01_first-up-after-long-down-run
brief: 086_rising-agitated-run-break-continues
data-instruments: LTC, ETH, XMR, INJ, GRT, DOGE, XRP, TRX
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: bd33e939b067
---
Fidelity:
- Situation: the first up day after a run of consecutive down days, in a rising agitated market -> adapted: a regime holds only on that up close after 2 or more down closes; the profile is added by code.
- Comparison: the more down days the run had, the larger the rise -> adapted: the forecast is graded by the run's down-day count.
- Outcome: the coin rises over the next 5 days -> kept: each bet is held 5 daily bars, long only.
- Verdict transfer: yes: the test bets only on the idea's event, sized by run length and held over its horizon, so its result is the idea's result.
Forecast: A detector component, `PriorDownRunOnUpCloseComponent` (side "down", form "count", max_bars 30), reads n. On the first up close after n consecutive down closes, n is that count; on every other bar it is 0. When n is 2 or more, the bar goes to regime `mean_reversion`. Every other bar is `unknown`, which is flat. Inside the regime the forecast is the same count, put through `standardise` (window 60, min_periods 20, target 2.5). The count is 0 on about three bars in four, so its past mean absolute value is about 0.5 (the random-walk expectation: a quarter of bars are events, with a mean run of 2). Target 10 would therefore pin every event at the cap of 20. Target 2.5 grades it instead: about 10 at n = 2, about 15 at n = 3, and 20 (the cap) at 4 or more. The forecast is never negative (long only) and is zero outside the event. The 5-bar holding period, set by code, keeps each bet through the idea's horizon.
Config: 086-01_first-up-after-long-down-run_1d_config.json
Side: long only (the brief): each component's forecast capped at 0 by step 3's code
Profile: rising agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The mean unusual 5-bar move over the cases. A case is a forecast rise of at least 2, read once per 5-bar grid cell. Its unusual move is the coin's return from the case's close over 5 bars minus the coin's normal 5-bar drift (holding the coin over all windows). Its t is computed with cases on the same day taken together.
- Supporting check: The least-squares slope of the cases' unusual 5-bar moves on their run length (`last_history_value` of `run_len`) is positive.
- Confirm: The idea is confirmed when the main measure is above 0 with t ≥ 2 and the slope of the supporting check is above 0.
- Reject: The idea is rejected when the main measure is below 0 with t ≤ -2.
- Inconclusive: Any result with t between -2 and 2 is inconclusive. So is a main measure with t ≥ 2 whose run-length slope is 0 or negative. At least 30 cases on at least 30 distinct days are needed; with fewer the result is inconclusive.
