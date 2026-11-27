---
idea: 072-03_choppy-deep-down-day-continuation
brief: 072_choppy-deep-below-high-falls
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: a choppy-market day that closed down, with its close far below the 20-day high in 20-day return-std units -> kept: the down close is a regime rule, and the depth is graded by VolatilityScaledDistanceFromHighComponent (20, 20); code adds the choppy profile.
- Comparison: deeper closes against shallower ones (the fall grows with depth) -> kept: the short position grows with the depth.
- Outcome: a larger fall over the next day -> kept: a short held 1 bar, judged on the next day's return.
- Verdict transfer: yes: the test measures this depth, only on down days, at this horizon, so a confirm or a reject carries over to the idea.
Forecast: The forecast is computed only on bars whose daily return is below 0 (regime `trending`). All other bars are flat; code also keeps the book flat outside the choppy profile. Inside the regime the forecast is the close's distance below the highest of the last 20 closes, divided by that high and by the standard deviation of the last 20 daily returns. This distance is standardised over its past 60 values (min 20). It is never positive. It is near 0 when the close sits at the high, and it grows more negative (more short, capped at -20) the deeper the close sits below the high in usual moves. It is about -10 at a typical depth. The book is short only.
Config: 072-03_choppy-deep-down-day-continuation_1d_config.json
Side: short only (the brief): each component's forecast capped at 0 by step 3's code
Profile: choppy (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bars
- Main measure: The timing gain per case. A case is a bar with a nonzero position after its trade. Its gain is the position held x (the next bar's return minus the coin's mean daily return over all its windows), so the market's own drift is not credited to the idea. The measure is the mean of this gain over all cases, with its t. The cases of one day are summed into one piece of evidence across coins.
- Supporting check: Split the cases by the median of |forecast|. The mean next-day excess return (as above) of the deeper half, minus that of the shallower half, must be below 0.
- Confirm: The mean timing gain is above 0 with t ≥ 2, over at least 100 cases on at least 100 distinct days, and the supporting check is below 0.
- Reject: The mean timing gain is below 0 with t ≤ -2, over at least 100 cases on at least 100 distinct days.
- Inconclusive: The result is inconclusive when the t of the mean timing gain lies between -2 and 2. It is also inconclusive when the main measure confirms but the supporting check is 0 or above, or when there are fewer than 100 cases or fewer than 100 distinct days.
