---
idea: 032-03_deep-fall-low-exhaustion-rebound
brief: 032_monthly-low-in-volatile-decline
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 051b3422f169
---
Fidelity:
- Situation: daily high-low ranges over the past 30 days wide against the past year, and a close at a new 30-day low -> kept: both conditions form one regime rule. The book is flat outside it. "Wide" takes the convention: the 30-day mean range is above the 365-day mean range.
- Comparison: the coin's own past year of daily ranges -> kept: 365-bar mean bar range over 30-bar mean bar range, below 1.
- Outcome: a rise over the next 5 days, larger the deeper the 30-day fall into the low -> kept: long, graded by the 30-day fall, held 5 bars.
- Verdict transfer: yes: the test buys only at the idea's lows, sized by the idea's fall, over the idea's horizon, so its result is the idea's result.
Forecast: The regime detector selects `mean_reversion` only when two conditions hold. First, the 365-day mean daily range divided by the 30-day mean daily range is below 1, so recent ranges are wider than the year's. Second, the close is below the lowest close of the prior 30 bars, a new 30-day low. On every other bar the forecast is 0. Inside the regime, the forecast is the 30-day percent return, standardised against its own past 60 values, negated, and clipped at 0. It is therefore positive, and it grows with the depth of the 30-day fall into the low: about 10 for a usual-sized 30-day move, up to the cap of 20. It is never negative.
Config: 032-03_deep-fall-low-exhaustion-rebound_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The unusual move of each case. A case is a long bet, a forecast rise of at least 2 points, read once per 5-bar grid cell. Its unusual move is the 5-bar return from the signal bar's close, minus the coin's normal 5-bar drift over all windows. The t uses cases grouped by day.
- Supporting check: Across cases, the Spearman correlation between the signal bar's forecast and the unusual move is above 0.
- Confirm: The idea is confirmed when both hold: the mean unusual move is above 0 with t ≥ 2, and the supporting check passes.
- Reject: The idea is rejected when the mean unusual move is below 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t ≥ 2 with the correlation at or below 0 is also inconclusive. The test needs at least 30 cases on distinct days; fewer is inconclusive.
