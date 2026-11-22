---
idea: 025-03_bounce-falling-versus-rising-regime.d1_bounce-fade-graded-by-depth
brief: 025_bounces-fade-in-falling-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 42de60c4e850
---
Fidelity:
- Situation: a one-day rise of several usual daily moves while the 90-day return is negative -> kept: a regime fires on bars whose 1-day return is at least 2 usual daily moves and whose 90-day return is below 0.
- Comparison: the same rises when the 90-day return is positive, and the size of the rise -> kept: measured on the record's prices, on rise bars with a positive 90-day return; the short is sized by 30-day depth, not by rise size.
- Outcome: lower 5-day return, with a shortfall that grows with the 30-day return's depth below zero in usual daily moves -> kept: a short held 5 bars, sized by the 30-day return in usual daily moves, clipped to its negative side.
- Verdict transfer: yes: the test trades exactly the bounces in 90-day-falling coins, sized by the 30-day depth, and compares them with bounces in rising coins.
Forecast: The regime is active only on a bar whose 1-day return is at least 2 usual daily moves (`VolatilityScaledReturnComponent`, period 1, vol_period 20) and whose 90-day return is negative. On every other bar the forecast is 0. On an active bar the forecast is the 30-day return in usual daily moves (`VolatilityScaledReturnComponent`, period 30, vol_period 20). It is standardised over 60 bars and clipped at 0 from above. It is negative (short) when the 30-day return is below zero, larger in size the deeper that return lies, and 0 when the 30-day return is not negative. It never reads the rise's size, and it never goes long.
Config: 025-03_bounce-falling-versus-rising-regime.d1_bounce-fade-graded-by-depth_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Welch t of the 5-day return from the rise bar's close, comparing two groups on the non-overlapping 5-bar grid of each window. Group A is the rise bars with a positive 90-day return, recomputed from prices (1-day return ≥ 2 × the 20-day std of daily returns). Group B is the bars where the forecast turns negative. The difference is A minus B.
- Supporting check: In group B, the slope of the short-signed 5-day return minus the coin's normal 5-day drift, regressed on |forecast|, is positive.
- Confirm: The main t is 2 or more and the supporting slope is above 0.
- Reject: The main t is -2 or less.
- Inconclusive: A main t between -2 and 2, or a confirming t with a slope at or below 0. A group with fewer than 30 cases is also inconclusive.
