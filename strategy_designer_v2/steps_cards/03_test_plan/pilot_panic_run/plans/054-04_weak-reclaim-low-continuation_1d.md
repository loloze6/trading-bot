---
idea: 054-04_weak-reclaim-low-continuation
brief: 054_reclaimed-monthly-low-in-falling-agitated
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 27e35f604dd2
---
Fidelity:
- Situation: in a falling, agitated market, the day trades below its lowest price of the past 30 days but closes back above it -> kept: the profile line holds the market, and a regime detector rule holds the pierce-and-reclaim of the prior 30-day low.
- Comparison: how close the close sits to that low, measured against the day's range -> kept: (close − low30) / (day's range) is graded within the pierce-and-reclaim days.
- Outcome: falls over the next 5 days, more the closer the close is to the low -> kept: a short held 5 daily bars, sized by nearness, judged against holding the coin.
- Verdict transfer: yes: the book is short only on reclaimed 30-day-low days in the named profile, sized by the idea's own nearness, so its 5-day result is the idea's claim.
Forecast: The forecast is flat on every bar except days whose low pierces the lowest low of the prior 30 days while the close ends back above it. A detector rule on `ReclaimedPriorLowPierceDepthComponent`(30) > 0 selects those days. On them, `PriorLowReclaimInRangeComponent` (period 30, form "nearness") gives 1 − (close − low30)/(high − low). This is near 1 when the close sits just above the pierced low and shrinks as the close climbs toward the day's high. The value is standardised over its past 500 stored values (min 120), because the history is mostly zeros between events and a 60-bar window would often give 0 on a real event. It is then negated, so the forecast is always short and larger the weaker the reclaim. Deep-nearness days can reach the −20 cap. The profile (falling agitated) is added by code.
Config: 054-04_weak-reclaim-low-continuation_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The unusual move of the cases, in the short direction. A case is a short bet (the forecast falls by at least 2 points), read once per 5-bar grid cell. The unusual move is the coin's 5-day return from the case bar's close minus the coin's normal 5-day drift over all windows. Its t uses the cases of one day taken together.
- Supporting check: Across cases, regress the short-direction unusual move on the raw nearness (`last_history_value` of `nearness`). The slope must be positive: closer to the low gives a larger fall.
- Confirm: The mean unusual move is above 0 with t ≥ 2 and the supporting slope is positive.
- Reject: The mean unusual move is below 0 with t ≤ −2, meaning the coin rises more than its drift after these days.
- Inconclusive: Anything else is inconclusive, including a t between −2 and 2, or a confirming mean whose slope is not positive. Fewer than 30 cases, counted on distinct days, is also inconclusive whatever the t.
