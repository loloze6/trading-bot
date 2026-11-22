---
idea: 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth
brief: 029_failed-breakout-traps-late-buyers
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 5f0a6e1d2346
---
Fidelity:
- Situation: a close back below the old 20-day high within 3 days of a close above it -> kept: `FailedBreakoutDepthInUsualMovesComponent` (period 20, fail_window 3, exclude_current 1) is non-zero only on such a re-entry close.
- Comparison: depth of the re-entry close below the old high, in units of 20-day daily volatility, deep against shallow -> kept: that depth is the component's value (vol_period 20), so deeper re-entries get larger shorts.
- Outcome: the fall from day 2 to day 10 after the failure is larger the deeper the re-entry -> adapted: "after X" made "while X", using lag 2 and a hold of 8 bars from day 2's close.
- Verdict transfer: yes: the forecast shorts exactly the failed re-entries, sized by their volatility-scaled depth, over the idea's own day-2-to-day-10 span.
Forecast: The forecast is the failed-breakout depth, read with a lag of 2 days. The failure bar e is 2 bars back. The breakout is a close above the prior 20 closes' high on one of the 3 bars before e. The depth is how far close[e] sits below that old high, divided by the standard deviation of the 20 daily returns ending at e. The depth is scaled by its mean absolute size over the past 500 bars, so most bars, which have no failure, read 0. Target 1 is used because the value is zero on most bars; at the default target of 10, every case would hit the cap. The scaled depth is negated so the forecast is short only. It is then passed through signed_power with exponent 3 and pivot 20, so shallow re-entries are damped close to 0 and deep ones approach -20. The forecast is 0 whenever no failed breakout sits 2 bars back. It is never positive. It grows more negative with the depth of the re-entry.
Config: 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth_1d_config.json
Criterion:
- Horizon: 8 bars
- Main measure: Cases are the short bets: falls of the forecast of at least 2 points, read once per non-overlapping 8-bar grid cell of each window. For each case, take the coin's 8-bar return from the signal bar's close, minus the coin's normal 8-bar drift, signed for a short. The measure is the mean of this value weighted by the case's |forecast|, with its t.
- Supporting check: Split the cases at the median |forecast|. The mean short-side excess fall of the deeper half minus that of the shallower half must be above 0.
- Confirm: The weighted mean short-side excess fall is positive with t >= 2 over at least 30 cases, and the deeper half's excess fall exceeds the shallower half's.
- Reject: The weighted mean short-side excess fall has t <= -2 over at least 30 cases, meaning the coin rises more than its drift after deep failures.
- Inconclusive: The result is inconclusive if t is between -2 and 2, if the main measure confirms but the deep-minus-shallow difference is not above 0, or if there are fewer than 30 cases.
