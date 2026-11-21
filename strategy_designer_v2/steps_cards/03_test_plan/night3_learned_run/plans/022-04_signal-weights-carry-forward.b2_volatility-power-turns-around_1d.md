---
idea: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: af2e424c34f8
---
Fidelity:
- Situation: the 30-day volatility signal's predictive power for 5-day returns over the past 365 days -> kept: the correlation w_vol over 365 days, times the signal's current z-score.
- Comparison: the same signal's predictive power over the following 90 days -> kept: measured as what the signal earns on the 5-day returns that follow, pooled over the days after each reading.
- Outcome: the following power is lower, the opposite of the past relation -> kept: betting against the past relation should earn on the next 5-day returns.
- Verdict transfer: yes: a significant gain from betting against past power means past power reverses, and a significant loss means it persists, which refutes the idea.
Forecast: The forecast uses one component, PastPredictivePowerWeightedCompositeComponent with weighting "single" and signal "volatility". It uses 30-day volatility, a 365-day correlation lookback, 5-day forward returns and a 365-day z-score. Its raw value is w_vol x z_vol: the past-year correlation of minus the 30-day volatility with the next 5-day return, times the current z-score of that signal. The value is standardised over 455 bars (min_periods 114) and then negated. The forecast is therefore positive when the past relation says "short" and negative when it says "long". It is zero when the past correlation or the current z-score is zero. Its size grows with both the past correlation's strength and how far volatility sits from its yearly mean. The forecast is signed, ungated and has no dead zone, because the idea is a steady relation.
Config: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The timing gain per case, read on the non-overlapping 5-bar grid of each window. A case is a bar with a non-zero position. For each case, take the position after the bar's trade times (the coin's 5-bar forward return minus the coin's mean 5-bar return over all windows). Average this across cases and compute the ordinary t of that mean, before costs.
- Supporting check: The mean timing gain is positive in at least 4 of the 6 coins.
- Confirm: The idea is confirmed only if both hold: - the mean timing gain is above 0 with t >= 2; - the supporting check passes.
- Reject: The idea is rejected if the mean timing gain is below 0 with t <= -2. That would mean the past volatility relation persists rather than reverses.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is t >= 2 when the supporting check fails. The test needs at least 300 non-overlapping cases across all coins and windows; with fewer, it is inconclusive.
