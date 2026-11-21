---
idea: 020-01_resistance-retest-turns-down.d3_nearness-to-90-day-high
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: e48527ec0eac
---
Fidelity:
- Situation: the daily close sits below its highest close of the past 90 days, and the gap can be small or large -> kept: the proximity of the close to its 90-day closing high, graded and including the high itself.
- Comparison: closer to the high against farther from it -> kept: the position grows with nearness, so nearer bars are compared with farther ones.
- Outcome: the coin rises more over the next 5 days -> kept: 5-bar forward return, held 5 bars.
- Verdict transfer: yes: the forecast grows exactly with nearness to the 90-day high, so a 5-day return that rises with it confirms the idea, and a return that falls with it rejects it.
Forecast: One indicator, the proximity of the close to its 90-day highest close. It is `DistanceFromHighComponent` with period 90, source close and bar t included. Its form is proximity, power 1: (1 / (1 + D)), where D is the percent the close sits below that high. It is 1 at the high and falls toward 0 the deeper the close sits below it. It is standardised against its own last 90 values (min_periods 22), so it averages about +10. The forecast is always long, never short, and never zero once the strategy is ready. Its size grows continuously as the close nears the 90-day high, up to the cap of 20 when nearness is twice its usual level.
Config: 020-01_resistance-retest-turns-down.d3_nearness-to-90-day-high_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The slope of the coin's 5-bar forward return, minus its normal drift, on the forecast (`post_pipeline_value`) at the bar it is read. Bars are read on the non-overlapping 5-bar grid of each window, pooled over all coins and windows. The t is the slope's t-statistic, given with the number of cases.
- Supporting check: The book's timing gain must be above 0. That gain is its mean daily return before costs minus the part it gets from the market's own rise (position x the coin's mean daily return).
- Confirm: Two results together confirm the idea. The slope's t must be 2 or more over at least 300 cases. The timing gain before costs must also be above 0.
- Reject: The slope's t is -2 or less over at least 300 cases, so nearer the high is followed by smaller 5-day returns.
- Inconclusive: These results are inconclusive: - a t between -2 and 2; - a t of 2 or more while the timing gain is 0 or below; - fewer than 300 grid cases.
