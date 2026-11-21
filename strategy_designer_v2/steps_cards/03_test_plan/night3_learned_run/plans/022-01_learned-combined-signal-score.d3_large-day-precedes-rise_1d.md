---
idea: 022-01_learned-combined-signal-score.d3_large-day-precedes-rise
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: a coin's absolute return over its last day -> kept: the 1-day percent return split into its up and down parts, both counted as positive, so the forecast equals half of |return| on its standardised scale.
- Comparison: the larger the absolute return, the higher what follows -> kept: the position grows continuously with the size of the absolute return.
- Outcome: the coin's return over the next 5 days is higher -> kept: each bet is held 5 daily bars and judged on the 5-day forward return.
- Verdict transfer: yes: the forecast is the idea's graded absolute 1-day return, so it tests the stated relation as written.
Forecast: The forecast uses one indicator, the coin's 1-day percent return (PriceEvolutionComponent, period 1). Each bar, that return is standardised against the mean absolute return of the previous 60 days (minimum 20 past values), giving x, about ±10 on a usual day and capped at ±20. One copy keeps the up part, max(x, 0). A second copy is negated and keeps the down part, max(-x, 0). The two copies have equal weights, so the forecast is |x| / 2. It is never negative (long only, as the idea leans long). It is near 0 on a still day, about +5 on a usual-sized move up or down, and up to +10 on a move twice the usual size or more. It grows smoothly with the size of the move, whatever its direction.
Config: 022-01_learned-combined-signal-score.d3_large-day-precedes-rise_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Use non-overlapping 5-bar grid points in each window, pooled across coins. At each point, take the coin's 5-day forward return close[t+5]/close[t] - 1 minus the coin's mean 5-day return over all windows. Compare the top third of forecast values with the bottom third: the mean excess return of the top third minus that of the bottom third, with Welch's t. Subtracting the drift and differencing the groups removes the gain from simply holding the coin.
- Supporting check: The mean excess 5-day return of the top-third group, before costs, is above 0 (it beats holding the coin).
- Confirm: The top-minus-bottom difference is positive with Welch t >= 2, and the supporting check passes.
- Reject: The top-minus-bottom difference is negative with Welch t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is a positive t >= 2 whose top third does not beat holding. The test needs at least 100 grid cases in each of the top and bottom thirds (about 580 cases expected in total); fewer is inconclusive.
