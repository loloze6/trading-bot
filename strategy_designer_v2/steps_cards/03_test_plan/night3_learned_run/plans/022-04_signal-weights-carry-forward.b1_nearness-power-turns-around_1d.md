---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: the nearness-to-90-day-high signal had high predictive power for 5-day returns over the past 365 days -> kept: correlation of close/90-day-high−1 with the next 5-day return over the prior 365 days, w(t).
- Comparison: "the higher" that past power, judged against the coin's usual power -> kept: w(t) minus its mean over the prior 365 days, graded.
- Outcome: the same signal's power for 5-day returns over the following 90 days is lower, so leaning against it pays -> kept: the position is −(w−w̄) × z(nearness), held 5 bars, and it gains when realised power falls below its usual level.
- Verdict transfer: yes: the lean-against book earns on average b·(w−w̄)² when later power falls as past power rises, about zero when there is no such link, and loses when the link is positive.
Forecast: One component, ExcessPredictivePowerZComponent, with high_period 90, corr_lookback 365, horizon 5, z_window 365 and mean_window 365. It computes the nearness signal's past-365-day correlation with 5-day returns, minus that correlation's own 365-day mean, times today's z-score of the nearness to the 90-day high. It is standardised over 500 bars (min_periods 120), then negated. The forecast is positive (long) when the signal's power is unusually high and the close sits further from its high than usual, or when power is unusually low and the close sits nearer its high than usual. It is negative in the two opposite cases and zero when power equals its usual level or the nearness equals its mean. Its size grows with both the excess power and the nearness z-score. It is ungated and signed.
Config: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The mean of (forecast/10) × (the coin's 5-bar return minus the coin's mean 5-bar return over all its windows). It uses the forecast at the start of each non-overlapping 5-bar cell, pooled over coins and windows, and its t is the ordinary t of the mean. This is before costs and net of holding the coin.
- Supporting check: none
- Confirm: t ≥ 2 with at least 300 non-overlapping cases where the forecast is not zero.
- Reject: t ≤ −2 with at least 300 such cases: leaning against recently-working power loses, so the power tends to persist.
- Inconclusive: −2 < t < 2, or fewer than 300 non-zero cases; a mean near zero is inconclusive, never a reject.
