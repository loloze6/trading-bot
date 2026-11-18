---
idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation.g1_calm-up-day-continuation
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: a large up day, gain relative to the 60-day mean absolute daily move, while 20-day volatility ranks low in its last 100 days -> adapted: the "large" and "low" thresholds become graded, as the product of the scaled gain and (1 - volatility rank).
- Comparison: larger gain and lower volatility rank, larger rise -> kept: the forecast grows with both factors.
- Outcome: further rise over the next 5 days, long only, no short after down days -> adapted: the 5-day hold is dropped, and the rise is measured 5 bars ahead.
- Verdict transfer: yes: the forecast is the idea's own graded situation, and the 5-bar forward return is the idea's own outcome.
Forecast: The forecast uses one indicator, RankWeightedScaledMoveComponent with abs_period 60, vol_period 20 and lookback 100. Its raw value is today's return divided by the 60-day mean absolute daily return, times (1 minus the rank of today's 20-day volatility among the last 100 days). - It is standardised against its own past 120 values. - It is clipped at 0, so a down day gives a forecast of zero and is never shorted. - It is then cubed around a pivot of 20, the strongest graded dead zone the guide allows. Ordinary up days stay near zero, and only sharp up days in calm stretches give a sizeable long. - The forecast is positive only on up days, and it grows with the size of the move and with how calm volatility is. It is zero otherwise.
Config: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation.g1_calm-up-day-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Use BTC and ETH, the idea's coins, on the non-overlapping 5-bar grid of each window. Take the mean 5-bar forward return of grid bars with forecast >= 2, minus the mean 5-bar forward return of all other grid bars, using Welch's t.
- Supporting check: Among grid bars with forecast > 0, the OLS slope of the 5-bar forward return on the forecast is positive.
- Confirm: The difference is positive with Welch t >= 2, from at least 30 cases with forecast >= 2, and the supporting slope is positive.
- Reject: The difference is negative with Welch t <= -2, from at least 30 cases with forecast >= 2.
- Inconclusive: Any of the following is inconclusive: - Welch t between -2 and 2. - Fewer than 30 cases with forecast >= 2. - t >= 2 while the supporting slope is not positive.
