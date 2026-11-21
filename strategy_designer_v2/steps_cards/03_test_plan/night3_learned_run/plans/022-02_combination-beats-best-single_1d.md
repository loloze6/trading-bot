---
idea: 022-02_combination-beats-best-single
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: af2e424c34f8
---
Fidelity:
- Situation: each coin's relearned combined score of its 28-day return, 1-day return, closeness to its 90-day high and 30-day volatility -> kept
- Comparison: the score of whichever single signal has predicted best -> kept
- Outcome: the next 5-day return lines up more closely with the combined score than with the best single score -> kept
- Verdict transfer: yes: both scores come from one catalogue component relearned only on past bars, and they are compared directly against the next 5-day return.
Forecast: The forecast is the coin's past-predictive-power composite (`weighting` "correlation"). It uses the defaults: 28-day return, 1-day reversal, closeness to the 90-day high and 30-day volatility. Each signal is a 365-bar z-score, weighted by its correlation with the following 5-day return over the past 365 bars. The composite is standardised over 455 bars and is signed: long when the learned combination points up, short when it points down. Its size grows with the strength of the combined score. A second copy with `weighting` "best" (the sign-adjusted z-score of the single signal that has predicted best) is standardised the same way. It carries weight 0, so it is recorded but does not move the position. The forecast is 0 only when the composite is 0.
Config: 022-02_combination-beats-best-single_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are the non-overlapping 5-bar grid of each window. For each case, y is the coin's 5-bar return minus its normal drift (its mean 5-bar return over all windows). The measure is the per-case value y x (post_pipeline_value of combined - post_pipeline_value of best) / 10, pooled over coins and windows, with the ordinary t of its mean. Both scores share the same standardised scale, so a positive mean means the combined score correlates more with the return than the best single score does.
- Supporting check: The Pearson correlation of y with the combined post_pipeline_value over the same cases is above 0.
- Confirm: The main mean's t is 2 or more and the supporting check passes, on at least 300 cases.
- Reject: The main mean's t is -2 or less: the best single signal lines up with the coming 5-day return more closely than the combination.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t of 2 or more with a combined correlation at or below 0 is also inconclusive. Fewer than 300 non-overlapping cases is inconclusive.
