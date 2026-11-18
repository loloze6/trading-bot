---
idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: a large one-day move while the 20-day volatility is low against the last 100 days -> adapted: "large" and "low" made graded as the day's move times one minus the volatility rank.
- Comparison: the move against the 60-day mean absolute daily move, and the 20-day volatility rank over 100 days -> kept.
- Outcome: the move continues in the same direction over the next 3 to 7 days, more for larger and calmer cases -> adapted: the 3-to-7-day holding period is dropped, and the outcome is measured 5 bars ahead.
- Verdict transfer: yes: the forecast is exactly the idea's graded product, and the outcome is read on the following 5-day returns.
Forecast: One component, RankWeightedScaledMoveComponent with abs_period 60, vol_period 20 and lookback 100. It is today's return divided by the 60-day mean absolute daily return, times one minus today's 20-day volatility rank over 100 days. It is standardised over 120 bars with min_periods 30. A signed_power with exponent 3 and pivot 20 follows, the strongest graded dead zone the guide allows. The forecast is positive after an up day and negative after a down day. It is near zero for small moves or high volatility ranks, and grows steeply as the move gets larger and the volatility rank gets lower. It is active on every bar, with no regime.
Config: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Use the non-overlapping 5-bar grid of each window. Rank the cases by |forecast| and take the top quintile of each coin. For each case, compute sign(forecast) x (5-bar forward return minus that coin's mean 5-bar return over all windows). Pool the coins and take the t of the mean.
- Supporting check: On the same grid, the mean of that signed excess return in the top quintile minus its mean in the other four quintiles is positive.
- Confirm: The main mean has t >= 2 with at least 30 top-quintile cases, and the supporting difference is positive.
- Reject: The main mean has t <= -2 with at least 30 top-quintile cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is t >= 2 when the supporting difference is not positive. So is any result from fewer than 30 top-quintile cases.
