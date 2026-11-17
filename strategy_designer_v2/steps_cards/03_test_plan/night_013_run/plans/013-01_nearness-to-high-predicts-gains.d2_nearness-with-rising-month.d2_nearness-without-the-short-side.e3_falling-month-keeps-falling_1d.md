---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: a coin's 30-day return is negative, the more negative the stronger -> kept
- Comparison: lower return than the coin would otherwise make -> kept
- Outcome: lower return over the next 3 days, more so the deeper the fall -> kept
- Verdict transfer: yes: a short position sized by the depth of the 30-day fall earns, over holding, exactly when deeper falls are followed by lower 3-day returns.
Forecast: The forecast is the 30-bar percent return of the close (PriceEvolutionComponent, period 30). It is standardised against its own past 60 values (target 10, cap 20). It is then clipped at a maximum of 0. When the coin's month is down, the forecast is negative and grows in size with the depth of the fall. When the month is flat or up, the forecast is zero, which means no position: the idea is about refusing longs, not about buying rises. The forecast never goes positive.
Config: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: The sample is the non-overlapping 3-bar grid of each window, on bars with forecast < 0. On each case, compute (forecast / 10) x (3-bar return minus the coin's mean 3-bar return over all windows). This is the short position's gain over holding, before costs. Take the t of its mean, pooled over coins.
- Supporting check: Among the forecast < 0 cases, the mean excess 3-bar return of the deeper half (forecast below the median) minus that of the shallower half is negative.
- Confirm: The main measure's t is 2 or more, and the supporting check is negative.
- Reject: The main measure's t is -2 or less. Deeper falls are then followed by higher-than-usual returns.
- Inconclusive: Any t between -2 and 2, or t of 2 or more with the supporting check not negative. The minimum is 100 independent forecast < 0 cases; with fewer, the result is inconclusive.
