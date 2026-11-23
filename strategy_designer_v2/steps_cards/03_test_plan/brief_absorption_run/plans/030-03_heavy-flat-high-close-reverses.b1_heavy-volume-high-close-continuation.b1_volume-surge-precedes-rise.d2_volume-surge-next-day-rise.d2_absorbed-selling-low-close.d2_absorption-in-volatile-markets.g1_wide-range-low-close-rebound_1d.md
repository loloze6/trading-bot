---
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets.g1_wide-range-low-close-rebound
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 91c94c46188e
---
Fidelity:
- Situation: a day whose low close sits within a range that is wide against the prior 20-day average range -> kept: (high − close) / prior 20-day mean range, which equals the close's depth below the high times the range multiple
- Comparison: the day's range against its own prior 20-day average range -> kept: the base is bars t-20..t-1, so day t is excluded
- Outcome: the coin rises more over the next day -> kept: next-bar return, held 1 bar
- Verdict transfer: yes: the forecast is the idea's own graded product, and the test checks whether the next-day rise grows with it.
Forecast: One component: `BreakoutInMeanRangesComponent` with period 1, base_period 20, side "below", high_current 1 and base_exclude_current 1. It computes (high[t] − close[t]) / mean(high − low over the prior 20 days). That equals the day's range in prior-average ranges times how near the close sits to the low. It is standardised over its past 60 values (min_periods 20). The forecast is never negative and is 0 when the close is at the day's high. It grows smoothly as the day widens against its usual range and as the close sinks toward the low. It is about +10 on an average day and capped at +20. There is no regime and no dead zone, because the idea states a steady graded relation.
Config: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets.g1_wide-range-low-close-rebound_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: For every bar, take the coin's next-day return minus that coin's mean daily return over all its windows. Regress that excess return, pooled over coins and windows, on the bar's forecast (post_pipeline_value). Report the slope and its t.
- Supporting check: Compare the mean excess next-day return on bars in the top fifth of forecasts with the mean on the other bars. The check passes if the top-fifth mean is the larger one (Welch t).
- Confirm: The slope is positive with t ≥ 2, and the top-fifth bars have the larger mean excess return with Welch t ≥ 2.
- Reject: The slope is negative with t ≤ −2, and the top-fifth bars have the smaller mean excess return with Welch t ≤ −2.
- Inconclusive: Any other result is inconclusive, including a slope with |t| < 2, or a main measure and check that disagree. At least 1000 bars with a next-day return are required, and at least 200 of them in the top fifth; fewer is inconclusive.
