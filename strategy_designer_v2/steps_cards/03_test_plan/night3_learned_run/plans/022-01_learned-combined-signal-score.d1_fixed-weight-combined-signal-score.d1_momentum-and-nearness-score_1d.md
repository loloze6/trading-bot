---
idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d1_momentum-and-nearness-score
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: the 28-day return and the closeness to the 90-day high, combined equally, each in its known direction -> kept
- Comparison: a higher score against a lower score -> kept
- Outcome: the return over the next 5 days is higher the higher the score -> kept
- Verdict transfer: yes: the forecast is the equal-weight score itself, so a slope of the 5-day return on it confirms or rejects the idea directly.
Forecast: The forecast averages two standardised signals with equal weight. - The first is the 28-day return (`PriceEvolutionComponent`, period 28), standardised over 60 bars. It is positive after a rise and grows with its size. - The second is the percent distance of the close below its 90-day closing high (`DistanceFromHighComponent`, period 90), standardised over 90 bars. It is always zero or negative. - A constant +10 (`BuyAndHoldStrategy`, standardised) centres the second signal. Distance plus constant is positive when the close sits nearer the high than usual and negative when further. - The forecast is (momentum + distance + 10) / 3. It is signed and continuous, with no dead zone. - It is long and larger when the coin has risen more and sits closer to its high than usual. It is short when both point the other way.
Config: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d1_momentum-and-nearness-score_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The slope of the coin's 5-bar forward return on the bar's forecast, with the return taken minus the coin's normal drift (its mean 5-bar return over all windows). It is measured on non-overlapping 5-bar grid bars of each window, pooled over coins and windows, and judged by its t-statistic.
- Supporting check: On the same grid, the mean drift-removed 5-bar return of the top fifth of forecasts minus that of the bottom fifth is above 0.
- Confirm: The slope's t is 2 or more and the top-minus-bottom-fifth difference is positive.
- Reject: The slope's t is -2 or less.
- Inconclusive: A slope t between -2 and 2 is inconclusive. So is t of 2 or more with a top-minus-bottom difference of 0 or less. A run with fewer than 300 non-overlapping grid cases with a non-zero forecast is also inconclusive.
