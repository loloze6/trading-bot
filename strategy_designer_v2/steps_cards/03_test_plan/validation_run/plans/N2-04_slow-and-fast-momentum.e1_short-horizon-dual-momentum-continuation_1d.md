---
idea: N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the coin's 60-day and 20-day returns are both positive -> adapted: the "both positive" condition gates a regime, and inside it the size is graded by how strong the two returns are.
- Comparison: higher than the coin's average daily return; short horizon rather than the following 20 days -> kept: measured against holding the coin, plus a 5-bar versus 20-bar check.
- Outcome: returns over the next few days are higher (upward continuation) -> kept: forward returns over 5 bars while long.
- Verdict transfer: yes: the gate is the idea's own condition, and grading the size inside it does not change which bars are long.
Forecast: Two 1d price-change measures, the 20-bar and the 60-bar percent return (PriceEvolutionComponent), feed the regime detector. When both are above 0, the bar is "trending"; on every other bar the regime is "unknown" and the forecast is 0 (flat). In "trending", the forecast is the equal-weight mean of the same two returns. Each is standardised against its own past 60 values (target 10) and clipped at 0. The forecast is therefore positive and grows with the strength of the fast and slow up-moves, about +10 at typical strength and up to +20. It is zero whenever either return is not positive. It never goes short, matching the long-or-flat consequence.
Config: N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: On the non-overlapping 5-bar grid of each window, take the bars where the forecast is above 0. For each, compute the coin's forward 5-bar return minus that coin's mean 5-bar return over all windows (holding the coin). The measure is the mean of this excess, before costs, with the t of the mean.
- Supporting check: On the same active bars, the mean excess per bar at 5 bars (5-bar excess / 5) minus the mean excess per bar at 20 bars (20-bar excess on its own non-overlapping 20-bar grid, / 20) is above 0.
- Confirm: The mean 5-bar excess is positive with t >= 2, and the supporting check is above 0.
- Reject: The mean 5-bar excess is negative with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t >= 2 with the supporting check at or below 0 is also inconclusive. At least 100 active non-overlapping 5-bar cases, pooled over coins and windows, are needed; with fewer the result is inconclusive.
