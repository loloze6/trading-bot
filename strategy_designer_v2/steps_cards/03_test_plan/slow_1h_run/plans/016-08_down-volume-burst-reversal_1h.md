---
idea: 016-08_down-volume-burst-reversal
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 1f000a7ba652
---
Fidelity:
- Situation: coin has fallen over the past 3 days -> adapted: "after a 3-day fall" made "while the 72-bar return is negative", a regime condition.
- Comparison: share of the period's volume in its few busiest hours -> kept: the share of the 72 bars' volume carried by the 3 largest-volume bars, graded.
- Outcome: the coin wins back more of the fall over the next 3 days (up) -> kept: the 72-bar forward rise, larger when the share is larger.
- Verdict transfer: yes: the test measures whether the rebound after 72-bar falls grows with the top-volume share, which is exactly the idea.
Forecast: A detector component, PriceEvolutionOnPeriodComponent with comparison_period 72, measures the 72-bar return. When that return is below 0, the bar is in mean_reversion; every other bar is unknown, which is null (flat). In mean_reversion the forecast is TopVolumesShareComponent (period 72, top_k 3), the share of the last 72 bars' volume carried by the 3 busiest bars. It is standardised against its own past 72 values (min_periods 20). The forecast is always long during a fall, near +10 at a usual share and up to +20 when the share is about twice its usual size. It shrinks toward 0 when volume is spread evenly. It is zero when the coin has not fallen over 72 bars.
Config: 016-08_down-volume-burst-reversal_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: Use the non-overlapping 72-bar grid of each window, keeping grid bars in the mean_reversion regime. Take each bar's 72-bar forward return minus the coin's mean 72-bar return over all windows. Compare bars with forecast above the median of those bars against bars at or below it: the top-half mean minus the bottom-half mean, with Welch t.
- Supporting check: none
- Confirm: The difference is positive with Welch t >= 2.
- Reject: The difference is negative with Welch t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. Fewer than 30 grid cases in either half is also inconclusive, whatever the t.
