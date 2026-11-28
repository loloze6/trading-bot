---
idea: 086-02_first-up-after-deep-down-run
brief: 086_rising-agitated-run-break-continues
data-instruments: LTC, ETH, XMR, INJ, GRT, DOGE, XRP, TRX
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: bd33e939b067
---
Fidelity:
- Situation: first up day after a run of consecutive down days, in a rising agitated market -> adapted: the profile is added by code; the run is a regime of at least 2 down closes broken by an up close.
- Comparison: the run's total fall against the standard deviation of the past 30 days' daily returns -> kept: run loss in 30-day return standard deviations.
- Outcome: the coin rises over the next 5 days, more after deeper runs -> kept: 5-bar hold sized by depth, judged on 5-day excess return.
- Verdict transfer: yes: the regime picks exactly the break days and the size follows the run's depth in usual swings, so both outcomes carry over to the idea.
Forecast: The regime detector fires on a bar whose close is above the prior close and ends a run of at least 2 lower closes. It reads `PriorDownRunOnUpCloseComponent` (count of 2 or more). On every other bar the book is flat. On a firing bar the forecast is the run's total loss divided by the standard deviation of the 30 daily returns ending the day before. That value is `PriorDownRunLossOnUpCloseComponent` with base "std", window 30, exclude_current 1, and it is standardised against its own past 60 values. The forecast is never negative (long only), it is 0 outside the situation, and it grows with the run's depth in usual swings, up to the cap of 20. The 5-day holding period keeps the bet after the break day. Note: the component is 0 on most days, so its past mean is small and deep runs will often reach the cap.
Config: 086-02_first-up-after-deep-down-run_1d_config.json
Side: long only (the brief): each component's forecast capped at 0 by step 3's code
Profile: rising agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: A case is a regime "trending" bar with forecast above 0, read once per 5-bar grid cell. For each case, the 5-day return from its close minus the coin's mean 5-day return over all windows (non-overlapping). Take the mean over the cases and its t, with cases on the same day taken together.
- Supporting check: Across cases, the least-squares slope of that excess return on the run depth (`depth` last_history_value) is positive with t ≥ 2.
- Confirm: The mean excess 5-day return is above 0 with t ≥ 2, and the supporting slope is positive with t ≥ 2.
- Reject: The mean excess 5-day return has t ≤ -2, or the depth slope has t ≤ -2.
- Inconclusive: Any other result, including t between -2 and 2 on either measure. Fewer than 30 independent case-days is inconclusive whatever the t.
