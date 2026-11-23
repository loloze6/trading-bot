---
idea: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: edf20a924da4
---
Fidelity:
- Situation: the 30-day volatility signal's predictive power for 5-day returns over the past 365 days is high -> kept: the correlation of minus the 30-day volatility with the next 5-day return, over the past 365 days.
- Comparison: higher past power against lower past power -> kept: the past power above or below its own 365-day mean, graded.
- Outcome: that signal's predictive power for 5-day returns over the following 90 days is lower -> kept: each bar bets against the excess power on the next 5-day return, and the bars of the following 90 days add up the power.
- Verdict transfer: yes: counter-bet gains on the following 5-day returns are positive exactly when the power after a reading falls as its past level rises.
Forecast: The forecast uses one indicator, ExcessPredictivePowerZComponent with the volatility signal (30-day volatility, 365-day correlation, 5-day horizon, 365-day z-score and 365-day mean of past power). Its value is (past power minus its usual level) times the volatility signal's z-score. It is standardised over 365 bars and then negated. The forecast is short the signal's usual reading when its past power is above its usual level, and with it when the power is below. Its size grows with the distance of the power from its usual level and with the signal's z-score. It is zero when the power sits at its usual level or the signal sits at its mean.
Config: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Use non-overlapping 5-bar grid cells of each window. In each cell, take forecast/10 at the cell's first bar times (the coin's 5-day return minus that coin's mean 5-day return over all its windows). Measure the t of the mean over all coins and windows pooled.
- Supporting check: none
- Confirm: The mean forecast-weighted excess 5-day return is positive with t >= 2, over at least 300 non-zero cells.
- Reject: The mean is negative with t <= -2, over at least 300 non-zero cells. This would mean high past power is followed by higher, not lower, power.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is any result from fewer than 300 non-zero cells.
