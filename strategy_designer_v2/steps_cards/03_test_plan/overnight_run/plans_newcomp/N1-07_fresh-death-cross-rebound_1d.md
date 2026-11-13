---
idea: N1-07_fresh-death-cross-rebound
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: 50-day SMA crossed below 200-day SMA within the last 20 bars -> adapted: a regime rule keeps the exact condition, and inside it the long position is graded by how far the 50-day SMA sits below the 200-day SMA.
- Comparison: rise larger than the coin's average 10-day move -> kept
- Outcome: the coin rises over the next 10 days -> adapted: holding period dropped; the position is held while the cross is fresh, and the 10-day return is measured in the criterion.
- Verdict transfer: yes: the regime selects exactly the fresh-death-cross bars, so the excess 10-bar return on those bars confirms or rejects the idea directly.
Forecast: The regime detector reads the age of the 50/200 SMA cross. The age is -n while SMA50 has been below SMA200 for n bars. When the age is between -20 and -1, the bar is a fresh death cross and the mean_reversion regime is active. On every other bar the forecast is 0 (flat). Inside the regime, the forecast is long: - It uses the SMA50-SMA200 spread in percent, standardised over its own past 200 values and then negated. - It is clipped at 0, so it is never short. - It is 0 at the cross and grows as SMA50 falls further below SMA200. - min_allocation_change is lowered to 0.02, so the small early positions are not rejected.
Config: N1-07_fresh-death-cross-rebound_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The mean 10-bar forward return of the coin on bars in the fresh-death-cross regime, minus that coin's mean 10-bar return over all test windows together (holding). Returns are taken on non-overlapping 10-bar blocks and the t-statistic is clustered by cross event, so overlapping returns count once.
- Supporting check: Position-weighted excess return: the strategy's return on regime bars per unit of allocation, minus holding, should have the same sign as the main measure.
- Confirm: Mean excess 10-bar return is above 0 with t ≥ +2, and the supporting check is positive.
- Reject: Mean excess 10-bar return is below 0 with t ≤ -2 (fresh death crosses are followed by further falls versus holding).
- Inconclusive: Any t between -2 and +2, or fewer than 15 distinct death-cross events (fewer than 30 non-overlapping 10-bar blocks) across all coins and windows.
