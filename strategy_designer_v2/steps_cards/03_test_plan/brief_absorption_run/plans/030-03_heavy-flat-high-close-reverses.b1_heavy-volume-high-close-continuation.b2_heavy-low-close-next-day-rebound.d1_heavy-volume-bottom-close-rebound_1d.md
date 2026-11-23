---
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 2035953e3f95
---
Fidelity:
- Situation: a day whose volume is far above its 20-day average -> adapted: "far above" is read as at least twice the prior 20-day mean volume, held as a regime condition.
- Comparison: close near the day's low, especially in the lowest quarter, against closes in the middle or upper range -> adapted: the lowest-quarter threshold becomes a graded close location with the strongest dead zone, near zero in the middle and upper range.
- Outcome: the coin rises over the next 1 day, more the nearer the close is to the low -> kept: the book holds 1 daily bar, long only.
- Verdict transfer: yes: on heavy-volume days the test measures whether the next day's rise grows with the close's nearness to the low, which is the idea's claim.
Forecast: The forecast is zero unless the day's volume is at least 2 times its mean over the prior 20 days (`VolumeRatioComponent`, period 20, base excluding today); those days are the `mean_reversion` regime, and every other day is flat. On heavy days the forecast is long only. It starts from the close's distance from the day's high as a share of the range (`CloseLocationInRangeComponent`, reference "high"): 0 at the high, 1 at the low. This is standardised over 60 bars, which puts a typical close near 10 and a close at the low near 20. Then a cubic `signed_power` (exponent 3, pivot 20) is applied. As a result: - a close at the very low gives about +20; - a close at the top of the lowest quarter gives about +8; - a close at mid-range gives about +2.5; - a close in the upper quarter gives near 0.
Config: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The slope of the next-day return (close[t+1]/close[t]-1, minus the coin's mean daily return over all windows) on the forecast. It uses all heavy-volume days (regime `mean_reversion`), pooled across coins and windows, one case per day.
- Supporting check: Lowest-quarter days (`post_pipeline_value` of loc_low ≥ 8.4) must have a mean next-day excess return above that of the other heavy-volume days (Welch t ≥ 2).
- Confirm: Both conditions must hold. The slope is positive with t ≥ 2. The supporting check passes.
- Reject: Either condition below is enough. - The slope is negative with t ≤ -2. - Lowest-quarter days show a mean next-day excess return below the other heavy-volume days with Welch t ≤ -2.
- Inconclusive: Every result between these is inconclusive, including a slope or difference near zero. A test with fewer than 300 heavy-volume days or fewer than 60 lowest-quarter days is inconclusive whatever the t.
