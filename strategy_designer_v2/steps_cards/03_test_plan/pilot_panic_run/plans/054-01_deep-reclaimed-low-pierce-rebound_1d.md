---
idea: 054-01_deep-reclaimed-low-pierce-rebound
brief: 054_reclaimed-monthly-low-in-falling-agitated
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 27e35f604dd2
---
Fidelity:
- Situation: in a falling, agitated market, a day trades below its lowest price of the past 30 days but closes back above that low -> kept: the profile is added by code, and the pierce-and-reclaim is a regime rule (`ReclaimedPriorLowPierceDepthComponent` above 0).
- Comparison: the rise is larger the deeper the day's low went below the 30-day low -> kept: the forecast is the pierce depth, so the position grows with depth.
- Outcome: the coin rises over the next 5 days -> kept: long, held for 5 daily bars.
- Verdict transfer: yes: the test bets long only on reclaimed 30-day-low pierces in the named profile, sizes each bet by pierce depth, and holds it for the idea's 5 days.
Forecast: The forecast uses `ReclaimedPriorLowPierceDepthComponent` with period 30. On days whose low went below the lowest low of the prior 30 days and whose close came back to or above it, the component gives the depth of the pierce, in percent of that prior low. On every other day it gives 0. The regime detector selects `mean_reversion` only when this depth is above 0. All other bars, and all bars outside the falling agitated profile, are flat. Inside the regime the depth is standardised against its own past 60 values (target 10, cap 20). The forecast is therefore positive (long) on reclaim days and grows with the depth of the pierce. It is never negative, and it is 0 when there is no reclaimed pierce.
Config: 054-01_deep-reclaimed-low-pierce-rebound_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The unusual move of the cases. A case is a bet: a forecast rise of at least 2 points, read once per 5-bar grid cell. For each case, take the coin's 5-bar return from the signal bar's close, minus the coin's normal 5-bar drift over all windows. Report the mean of these, with its t, cases on the same day taken together.
- Supporting check: Among the cases, the least-squares slope of the unusual 5-bar move on the forecast at the signal bar is above 0.
- Confirm: The mean unusual move is above 0 with t ≥ 2, and the depth slope is positive.
- Reject: The mean unusual move is below 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is t ≥ 2 with a slope of 0 or below. The minimum is 30 cases on at least 30 distinct days; fewer is inconclusive whatever the t.
