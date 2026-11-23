---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a coin's nearness to its 90-day high had high predictive power for its 5-day returns over the past 365 days -> kept: 365-day correlation of nearness with 5-day returns, measured against its own mean over the prior 365 days and multiplied by today's nearness z-score.
- Comparison: the higher the past power, the lower the future power -> kept: a graded slope, betting against the excess past power on the current nearness reading.
- Outcome: the same signal's power over the following 90 days, for 5-day returns, is lower -> kept: the forecast's gain on each next 5-day return inside the following days.
- Verdict transfer: yes: the counter-bet earns before costs exactly when 5-day returns move against nearness where the past power was unusually high, and it loses when the power persists.
Forecast: The forecast is the negated ExcessPredictivePowerZComponent, with nearness to the 90-day closing high, a 365-day correlation window, 5-day returns, a 365-day z-window and a 365-day mean of past power. Its raw value is the 365-day correlation of nearness with the next 5-day returns, minus that correlation's mean over the prior 365 days, times today's nearness z-score. The raw value is standardised over 500 past values and then negated. It is positive (long) when past power is above usual and the close sits further from its high than usual. It is also positive when past power is below usual and the close sits nearer its high than usual. It is negative in the two mirror cases. It is zero when past power is at its usual level or nearness is at its mean. Its size grows with both the excess power and the nearness deviation.
Config: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are the non-overlapping 5-bar grid of each window, pooled over coins. For each case, take forecast/10 times the coin's 5-bar forward return minus the coin's mean 5-bar return over all its windows. The measure is the mean of this product and its t-statistic, before costs.
- Supporting check: none
- Confirm: The mean is above 0 with t >= 2, on at least 300 cases with a non-zero forecast.
- Reject: The mean is below 0 with t <= -2, on at least 300 cases with a non-zero forecast. That would show past power persisting rather than turning around.
- Inconclusive: Any t strictly between -2 and 2 is inconclusive, as is fewer than 300 non-zero-forecast cases.
