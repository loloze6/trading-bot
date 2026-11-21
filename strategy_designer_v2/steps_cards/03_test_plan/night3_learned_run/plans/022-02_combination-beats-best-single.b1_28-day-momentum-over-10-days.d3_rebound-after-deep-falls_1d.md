---
idea: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d3_rebound-after-deep-falls
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: a deep 28-day fall and a close near its 60-day low -> kept: the 28-day fall depth and the position in the 60-day close range are both graded, and the forecast grows with each.
- Comparison: none -> kept
- Outcome: a higher return over the next 10 days -> kept: the coin's 10-bar forward return, judged against its normal drift.
- Verdict transfer: yes: the forecast grows with the depth of the fall and the nearness to the low, and the test reads the 10-day returns that follow.
Forecast: The forecast is the equal-weight mean of two long-only graded parts. The first is the 28-bar price change, standardised, negated and clipped at 0: it is positive only after a 28-day fall, and larger the deeper the fall. The second is the close's position in its 60-bar close range, standardised, negated and clipped at 0: it is positive only in the lower half of the range, and largest at the 60-day low. The forecast is zero when the coin has not fallen and sits in the upper half of its range. It is positive otherwise, growing as the fall deepens and the close nears the low. It is never negative.
Config: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d3_rebound-after-deep-falls_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: On a non-overlapping 10-bar grid in each window, regress the coin's 10-bar forward return, minus its normal drift (its mean 10-bar return over all windows), on the forecast. Pool all coins.
- Supporting check: The mean unusual move over the cases, measured in the long direction, is above 0. A case is a forecast rise of at least 2 points, read once per grid cell.
- Confirm: The slope is positive with t >= 2 and the supporting check passes.
- Reject: The slope is negative with t <= -2.
- Inconclusive: A slope t between -2 and 2 is inconclusive. A positive slope with t >= 2 whose check fails is also inconclusive. The test needs at least 300 grid cells with forecast > 0 and 100 cases; with fewer, the result is inconclusive.
