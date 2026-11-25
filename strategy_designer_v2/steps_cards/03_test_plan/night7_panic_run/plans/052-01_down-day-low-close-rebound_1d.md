---
idea: 052-01_down-day-low-close-rebound
brief: 052_down-day-low-close-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: f9d41455da54
---
Fidelity:
- Situation: a down day, its close's nearness to the day's low as a share of the high-low range -> adapted: "after a down day" made "while the day closed below the prior close" (a regime); the nearness to the low is kept as the graded size
- Comparison: down days closing near the low against those closing near the high -> kept: the position grows with (high - close) / (high - low)
- Outcome: the coin rises over the next day, more the nearer the close sat to the low -> kept: long for 1 bar on daily bars
- Verdict transfer: yes: the book is long only on down days, sized by the close's nearness to the low, and held for the next day, so its next-day gains test the idea directly.
Forecast: The regime detector reads the day's close-to-close return (`PriceEvolutionComponent`, period 1). On a down day (return below 0) the bar is in `mean_reversion`; every other bar is flat. On down days the forecast is `CloseLocationInRangeComponent` (reference "high"), which is (high - close) / (high - low): 0 with the close at the day's high and 1 at its low. It is standardised over its past 60 values, so a usual reading gives about +10 and the cap is +20. The forecast is long only. It is near 0 when the down day closed at its high and largest when it closed at its low. It is 0 on up days and flat days.
Config: 052-01_down-day-low-close-rebound_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Among down-day bars (regime `mean_reversion`), split the bars into terciles of `near_low` post_pipeline_value within each coin. The measure is the Welch t of the next-day return close[t+1]/close[t]-1 in the top tercile (closes nearest the low) minus that in the bottom tercile (closes nearest the high), pooled over coins and windows, before costs.
- Supporting check: The top tercile's mean next-day return minus the coin's mean daily return over all its windows (holding the coin) is above 0.
- Confirm: Both conditions hold. The top-minus-bottom difference is positive with a Welch t of 2 or more, and the supporting check passes.
- Reject: The top-minus-bottom difference has a Welch t of -2 or less. Alternatively, the top tercile's next-day return minus holding has a t of -2 or less, meaning closes at the low are followed by further falls.
- Inconclusive: Any result with a t between -2 and 2 is inconclusive. A difference that confirms while the supporting check fails is also inconclusive. The test needs at least 300 down-day cases in each tercile, pooled over coins and windows; with fewer, the result is inconclusive.
