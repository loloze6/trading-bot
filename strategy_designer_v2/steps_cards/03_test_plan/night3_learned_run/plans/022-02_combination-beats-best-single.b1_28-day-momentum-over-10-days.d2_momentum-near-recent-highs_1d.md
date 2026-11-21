---
idea: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: the coin's 28-day return, while it trades near its 60-day high -> adapted: the "only while near the high" condition is made graded by a proximity weight (1/(1+D))^2, where D is the percent distance below the 60-day closing high.
- Comparison: the closer to the 60-day high, the stronger the continuation -> kept: the weight grows smoothly toward 1 as the close nears the high.
- Outcome: the return over the next 10 days rises with the 28-day return -> kept: the position takes the sign of the 28-day return and is held 10 bars.
- Verdict transfer: yes: the forecast is the 28-day return scaled by nearness to the 60-day high, so its predictive slope on 10-day returns is the idea's claim.
Forecast: The forecast uses one indicator, HighProximityMomentumComponent (period 60, return_period 28, proximity "convex", power 2). Its raw value is the 28-day percent return times (1/(1+D))^2, where D is the percent distance of the close below its highest close of the last 60 days. That value is standardised against its own past 60 values (window 60, min_periods 20, target 10, cap 20). The forecast is positive after a 28-day rise and negative after a 28-day fall. Its size grows with the size of the return and with nearness to the 60-day high. It is near zero when the 28-day return is near zero or when the coin is far below its high. There is no regime: the forecast is active on every bar.
Config: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Take one case per window at positions 0, 10, 20, ... of each window. For each case, compute the coin's 10-bar forward return minus the coin's normal 10-bar drift (its mean over all windows). Regress that excess return on the forecast, pooled over coins, and measure the t of the slope.
- Supporting check: The book's timing gain must be above zero. This is the book's mean daily return before costs minus its gain from the market's own rise.
- Confirm: The slope's t is +2 or more, with at least 200 cases, and the timing gain is above zero.
- Reject: The slope's t is -2 or less, with at least 200 cases.
- Inconclusive: Any slope t between -2 and +2 is inconclusive. So is a positive slope t of 2 or more when the timing gain is zero or below. Fewer than 200 non-overlapping cases is also inconclusive.
