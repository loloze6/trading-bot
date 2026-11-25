---
idea: 054-03_deep-pierce-reclaim-continuation
brief: 054_reclaimed-monthly-low-in-falling-agitated
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 27e35f604dd2
---
Fidelity:
- Situation: the day trades below its lowest price of the past 30 days but closes back above that low -> kept: a regime is active when low[t] is under the prior 30-day low (bars t-30..t-1) and close[t] is at or above it.
- Comparison: the fall is larger the deeper the day's low went below the 30-day low -> kept: inside the regime, the short is sized by the pierce depth in percent of that low.
- Outcome: the coin falls over the next 5 days -> kept: a short held for 5 daily bars.
- Verdict transfer: yes: the test measures this exact day pattern and sizes the short by the idea's own depth, inside the named profile.
Forecast: One component, `ReclaimedPriorLowPierceDepthComponent` with `period` 30. It reads max(0, L − low[t]) / L × 100 when close[t] ≥ L, else 0, where L is the lowest low of the 30 prior days. The regime detector selects the active regime only on bars where this reading is above 0, so the book is flat on every other bar. Inside that regime the forecast is the reading put through `standardise` (window 500, min_periods 120, target 0.15), then `negate`. It is therefore always short, and the short grows linearly with how deep the day's low pierced the 30-day low, capped at −20. Why target 0.15: the component's history is 0 on almost every day. With the default target 10, every case would sit at the −20 cap, which is on/off. Under a random walk, a new 30-day low comes about 1 day in 31, and about half of those close back above it. So the target is 10 × 1/31 × 1/2 ≈ 0.15, which puts a typical case near −10. This comes from the idea's own 30-day setting, not from the data. The profile (falling agitated) is added by code.
Config: 054-03_deep-pierce-reclaim-continuation_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The unusual move per case, in the short direction. A case is a short bet on a pierce-and-reclaim day, read once per 5-bar grid cell. For each case, take the coin's 5-day return from the signal bar's close, subtract the coin's mean 5-day return over all windows, and sign it so a fall counts as positive. Report its mean and its t, with cases on the same day summed into one.
- Supporting check: The position-weighted mean of that unusual move, weighted by abs(post_pipeline_value), must be at least its equal-weighted mean. This checks that deeper pierces fall more.
- Confirm: The mean unusual move is a fall with t ≥ 2, and the supporting check passes.
- Reject: The mean unusual move is a rise (a rebound) with t ≤ −2.
- Inconclusive: Any t between −2 and 2. Also a fall with t ≥ 2 where the check fails. Also any result from fewer than 30 cases.
