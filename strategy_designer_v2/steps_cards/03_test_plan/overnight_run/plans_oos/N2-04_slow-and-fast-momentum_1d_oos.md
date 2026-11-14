---
idea: N2-04_slow-and-fast-momentum
brief: 002_moving-average-cross-trend-persistence
data-instruments: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ
data-bar: 1d
data-period: folds A, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: the coin's 60-day return and its 20-day return are both positive -> kept: a regime rule on the two raw returns above 0, with the size graded by how far both returns are above 0.
- Comparison: the coin's average 20-day return -> kept: the coin's mean 20-bar return over all windows, used in the criterion.
- Outcome: the following 20 days rise more than that average, long side only, flat otherwise -> kept: the 20-bar forward return while long, measured against that average.
- Verdict transfer: yes: the same condition, comparison and horizon are measured, so a confirm or a reject carries over to the idea.
Forecast: The regime detector computes the 60-bar and 20-bar percent returns on daily bars. When both are above 0, the bar is "trending"; otherwise the forecast is 0 (flat, never short). In "trending", the forecast is the equal-weight mean of two components, each clipped at 0: - the 60-bar return, standardised against its own past values (window 61, min_periods 20); - the 20-bar return, standardised the same way (window 60, min_periods 20). The forecast is positive only while both returns are up. It grows as either return becomes larger than its usual size, and is capped at 20. It is near 0 when the trend has only just turned up.
Config: N2-04_slow-and-fast-momentum_1d_oos_config.json
Criterion:
- Horizon: 20 bars
- Main measure: On bars where the forecast is above 0, take the coin's 20-bar forward return minus the coin's mean 20-bar return over all windows pooled. Pool across coins and count each 20-bar block once (non-overlapping), then compute the t-statistic of the mean excess.
- Supporting check: Check that the forward excess return grows with forecast size: the slope of the 20-bar excess return on the forecast level, over active bars in non-overlapping blocks, should be positive.
- Confirm: The mean 20-bar excess return on active bars is above 0 with t ≥ 2, before costs.
- Reject: The mean 20-bar excess return on active bars is below 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2, or fewer than 30 non-overlapping 20-bar active blocks pooled across coins and windows.
