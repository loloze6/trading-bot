---
idea: 022-04_signal-weights-carry-forward
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: af2e424c34f8
---
Fidelity:
- Situation: each signal's past 365-day predictive power for the coin's 5-day returns -> kept: the Pearson correlation w_k of each signal with 5-day returns over the past 365 days.
- Comparison: the higher that past power, the higher the same signal's future power -> kept: each signal is weighted by its own past w_k, so its stake grows with that past power.
- Outcome: the same signal's power for 5-day returns over the following 90 days, same sign -> kept: forecast-weighted 5-day excess returns on later, unlearned bars.
- Verdict transfer: yes: positive gains that grow with w_k x signal mean the past power carried forward; a strong negative result means it reversed.
Forecast: Four components of PastPredictivePowerWeightedCompositeComponent use `weighting` "single", one each for momentum (28-day return), reversal (1-day move), nearness to the 90-day high, and low volatility (30-day). Each one outputs w_k x z_k(t). Here w_k is the correlation of that signal with the coin's next 5-day returns over the past 365 days, using only completed returns. z_k(t) is the signal's 365-day z-score today. Each component is standardised over 455 bars, and the four get equal weights. The forecast is positive when the signals that predicted well are bullish now (or the ones that worked in reverse are bearish), and negative in the opposite case. It is near zero when past power is near zero or the signals sit at their means. Its size grows with both the past power and the signal's strength.
Config: 022-04_signal-weights-carry-forward_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The mean over cases of (forecast / 10) x (the coin's 5-day return minus its normal 5-day drift), on the non-overlapping 5-bar grid of each window. All coins and windows are pooled, and the t of that mean is reported.
- Supporting check: none
- Confirm: The mean forecast-weighted excess 5-day return is positive with t >= 2, on at least 300 independent cases.
- Reject: The mean forecast-weighted excess 5-day return is negative with t <= -2, on at least 300 independent cases.
- Inconclusive: Any t between -2 and 2, or fewer than 300 non-overlapping cases with a non-zero forecast.
