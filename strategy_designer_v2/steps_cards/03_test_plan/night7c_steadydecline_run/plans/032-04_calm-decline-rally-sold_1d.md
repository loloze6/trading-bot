---
idea: 032-04_calm-decline-rally-sold
brief: 032_calm-decline-keeps-falling
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 051b3422f169
---
Fidelity:
- Situation: a calm 28-day decline (ordinary daily ranges and volume) and the coin closes the day up -> kept: a regime holds the four conditions: 28-day return below 0, the day's return above 0, the 28-day mean bar range no wider than its 120-day mean, and the 28-day mean volume no heavier than the prior 120 days' (the levels follow the "ordinary = at most usual" convention).
- Comparison: the deeper the 28-day fall, the larger the drop -> kept: inside the regime, the short is graded by the size of the 28-day fall.
- Outcome: the price falls over the next 5 days -> kept: a short held for 5 daily bars.
- Verdict transfer: yes: the test bets short only on calm-decline up days, sized by the fall, over 5 days, so its result is the idea's result.
Forecast: The regime "trending" is active only on a bar where four things hold: - the 28-day return is negative; - the day's return is positive; - the 28-day mean daily range, set against the 120-day mean, is at most 1; - the 28-day mean volume, set against the 120 days before it, is at most 1. On every other bar the forecast is 0. Inside the regime, the forecast is the 28-day percent change of the close, standardised over its past 60 values (target 10, cap 20) and clipped at 0. It is therefore negative (short). Its size grows with the depth of the 28-day fall, about -10 for a usual-sized move and down to -20. It is never positive.
Config: 032-04_calm-decline-rally-sold_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: - Cases: each short bet, meaning a fall of the forecast of at least 2 points, read once per non-overlapping 5-bar grid cell of each window. - Measure: the mean unusual move, short side. Per case, this is minus (the coin's 5-day return from the signal bar's close, less its normal 5-day drift over all windows). - Test: its t, with the cases of one day taken together (before costs, against holding the coin).
- Supporting check: Across the cases, the least-squares slope of the unusual move (short side) on |forecast| at the signal bar is positive: deeper falls give larger drops.
- Confirm: The idea is confirmed only when both hold: - the mean unusual move is positive with t ≥ 2; - the supporting slope is above 0.
- Reject: The idea is rejected if either holds: - the mean unusual move is negative with t ≤ -2 (calm-decline up days are followed by rises beyond drift); - the slope is negative with t ≤ -2.
- Inconclusive: Any result with the main t between -2 and 2 is inconclusive. So is a main t ≥ 2 with a slope at or below 0 but its t above -2. At least 30 distinct case days are needed; fewer is inconclusive.
