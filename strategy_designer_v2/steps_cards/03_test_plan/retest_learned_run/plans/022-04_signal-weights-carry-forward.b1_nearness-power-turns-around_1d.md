---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: the nearness-to-90-day-high signal's predictive power for 5-day returns over the past 365 days -> kept: the rolling 365-day correlation w of the nearness signal with the 5-day return that followed.
- Comparison: the higher that past power, against the coin's usual power -> kept: w minus its own mean over the prior 365 days, graded.
- Outcome: the same signal's power for 5-day returns over the following 90 days is lower, so leaning against it pays -> kept: a counter-bet of -(w - wbar) x nearness z-score, scored on the following 5-day returns over the next months.
- Verdict transfer: yes: the counter-bet's expected gain equals minus the covariance of excess past power with later realised power, which is exactly the idea's claim.
Forecast: One component, ExcessPredictivePowerZComponent (high_period 90, corr_lookback 365, horizon 5, z_window 365, mean_window 365). It first computes the nearness of the close to its 90-day closing high, as a z-score against the past 365 days. It multiplies that by how far the signal's past-365-day correlation with 5-day returns sits above its own mean of the prior 365 days. The product is standardised over 365 past values, then negated. The forecast is short when the close sits nearer its high than usual while the relation has worked more than usual. It is long when the close sits further from its high than usual in that same case. The signs reverse when the past power is below its usual level. The forecast is near zero when the power is at its usual level or the nearness is at its mean, and its size grows with the product of the two.
Config: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The measure uses non-overlapping 5-bar cases on each window's grid of rows 0, 5, 10, and so on. In each case it multiplies forecast / 10 by (the coin's 5-bar return minus the coin's mean 5-bar return over all windows). It then takes the mean of that product, with its t, pooled over all coins and windows.
- Supporting check: The book's mean daily return before costs, minus its gain from the market's own rise, is above 0.
- Confirm: The main mean is positive with t >= 2 over at least 300 cases, and the supporting check passes.
- Reject: The main mean is negative with t <= -2 over at least 300 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. A positive t of 2 or more is also inconclusive when the timing gain is not above 0. Fewer than 300 non-overlapping cases is inconclusive whatever the t.
