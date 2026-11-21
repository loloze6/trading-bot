---
idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d2_strong-rises-keep-rising
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: a coin's 28-day rise, larger is stronger -> kept
- Comparison: the extra 5-day return grows faster than the rise -> adapted: graded convex (squared) sizing of the rise, flat after falls
- Outcome: higher 5-day return, largest after the largest rises -> kept
- Verdict transfer: yes: the test sizes longs convexly in the 28-day rise and measures the 5-day returns that follow, as the idea states.
Forecast: The forecast is the 28-day percent price change (PriceEvolutionComponent, period 28), standardised against its own last 60 values. It is clipped at 0, so falls give no position. It is then squared with signed_power (exponent 2, pivot 10). The forecast is 0 after a 28-day fall and positive after a rise. It grows with the square of the rise's standardised size, so a rise at its usual size gives about 10, half that size gives 2.5, and 1.5 times that size gives 22.5 before the clip at 20. It is never negative.
Config: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d2_strong-rises-keep-rising_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The sample is the non-overlapping 5-bar grid of each window. For each grid bar, take the coin's 5-day return minus that coin's mean 5-day return over all its windows. The grid bars are pooled over coins. Compare the bars in the top fifth of positive forecasts against all other grid bars, with Welch's t.
- Supporting check: The top-fifth group's mean excess return is above that of the remaining positive-forecast grid bars. This shows the gain grows faster than the rise.
- Confirm: Welch t >= 2 (top fifth minus the rest) and the supporting check passes.
- Reject: Welch t <= -2 (top fifth minus the rest).
- Inconclusive: Any t between -2 and 2 is inconclusive, and so is t >= 2 when the supporting check fails. The test needs at least 30 independent grid cases in the top-fifth group, else it is inconclusive.
