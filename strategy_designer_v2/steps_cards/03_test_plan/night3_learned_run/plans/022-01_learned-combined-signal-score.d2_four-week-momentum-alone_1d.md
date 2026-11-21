---
idea: 022-01_learned-combined-signal-score.d2_four-week-momentum-alone
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: a coin's 28-day return, the higher the stronger -> kept
- Comparison: higher against lower 28-day returns, as a graded relation -> kept
- Outcome: a higher return over the next 5 days -> kept
- Verdict transfer: yes: the forecast is the 28-day return itself, sized in proportion and held 5 days, so its result over 5 days is the idea's result.
Forecast: The forecast is the coin's 28-bar percent return (PriceEvolutionComponent, period 28), divided by the mean absolute size of its previous 60 values and multiplied by 10, capped at ±20. It is positive and grows with the size of a 4-week rise. It is negative and grows with the size of a 4-week fall. It is near zero when the 4-week return is near zero. No short is ever taken against a 4-week rise, because the sign always follows the 28-day return.
Config: 022-01_learned-combined-signal-score.d2_four-week-momentum-alone_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Use the non-overlapping 5-bar grid of each window, pooled over coins and windows. For each cell, take forecast/10 at the cell's bar times (the coin's 5-day return minus its normal drift over all windows). Measure the ordinary t of the mean of these values, before costs.
- Supporting check: none
- Confirm: The mean is positive with t ≥ 2, from at least 300 independent cases.
- Reject: The mean is negative with t ≤ -2, from at least 300 independent cases.
- Inconclusive: The result is inconclusive if -2 < t < 2, or if there are fewer than 300 grid cases with a non-zero forecast.
