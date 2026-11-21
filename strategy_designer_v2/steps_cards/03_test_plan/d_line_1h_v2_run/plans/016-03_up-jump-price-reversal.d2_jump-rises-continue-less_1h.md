---
idea: 016-03_up-jump-price-reversal.d2_jump-rises-continue-less
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the coin has risen over the past 3 days (72 bars) -> kept: the residual form of TopGainsShareOfRiseComponent is 0 unless the 72-bar net return is above 0, and it is continuous at 0.
- Comparison: the share of that rise that came from its few (3) biggest hourly gains -> kept: TopGainsShareOfRiseComponent (period 72, k 3), read as 1 minus that share.
- Outcome: a smaller further rise over the next 3 days (72 bars) the larger that share, but still a rise -> kept: long exposure scaled down as the share grows, never short.
- Verdict transfer: yes: the forecast is long in proportion to how little of the 3-day rise came from its 3 biggest hours, so the 72-bar returns that follow measure exactly the idea's claim.
Forecast: TopGainsShareOfRiseComponent (period 72, k 3, form "residual") gives 1 minus the share of the 72-bar net rise carried by its 3 largest hourly gains. It gives 0 when the coin did not rise over the 72 bars. Standardise (window 72, min_periods 20) puts it on the forecast scale, and a clip at min 0 keeps it long-only. The forecast is 0 when the coin has not risen. It is positive when it has, and largest when the rise is a grind of many small hours. It shrinks towards 0 as the 3 biggest hours carry more of the rise, and it is never negative.
Config: 016-03_up-jump-price-reversal.d2_jump-rises-continue-less_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: The sample is the bars where the coin had risen over the past 72 bars (raw value of grind_residual above 0), taken on the non-overlapping 72-bar grid of each window. Split them at the per-coin median of grind_residual into a grind group (above the median) and a jump group (at or below it). The measure is the mean 72-bar forward return of the grind group minus that of the jump group, tested with Welch's t and pooled across coins and windows. The difference of two groups nets out the coin's own drift.
- Supporting check: none
- Confirm: The grind-minus-jump difference in mean 72-bar forward return is above 0 with Welch t >= 2.
- Reject: The grind-minus-jump difference is below 0 with Welch t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive, including a difference near zero. The test needs at least 200 independent grid cases in each group; with fewer, it is inconclusive.
