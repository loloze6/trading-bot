---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: the nearness-to-90-day-high signal's 365-day predictive power for 5-day returns is high -> kept: the correlation w over 365 days, 5-day horizon, 90-day high, graded by its excess over its own past mean.
- Comparison: that power against the power over the following 90 days, which turns lower -> adapted: the bet against the signal while power is above its usual level is the "while X" form, with no future data read.
- Outcome: the more strongly the reversal points up, the higher the 5-day return -> kept: long only, sized by the reversal's strength, over 5 bars.
- Verdict transfer: yes: the forecast is the idea's upward reversal bet, graded and long only, judged on the coin's next 5 days against its own drift.
Forecast: The forecast uses ExcessPredictivePowerZComponent (high_period 90, corr_lookback 365, horizon 5, z_window 365, mean_window 365). Its raw value is the signal's excess power (w minus its past-365-day mean) times the z-score of today's nearness to the 90-day high. It is standardised over its past 500 values and negated, which gives the reversal bet against the signal. It is then clipped at 0, so the forecast is long only. It is positive when the reversal points up: power is above its usual level and the close sits further from its high than usual, or power is below usual and the close sits nearer its high than usual. It is zero when the reversal points down, and its size grows in proportion to the reversal's strength.
Config: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: On the non-overlapping 5-bar grid of each window (bars 0, 5, 10, ...), take the grid bars with forecast > 0. On each, compute the coin's 5-day return minus that coin's mean 5-day return over all its windows. The measure is the one-sample t of the mean of these excess returns, pooled over coins and windows.
- Supporting check: On those grid bars, the mean excess return of the cases with the larger half of positive forecasts minus that of the smaller half must be above 0, so that gains grow with the position.
- Confirm: The mean excess 5-day return on positive-forecast grid bars has t >= 2, and the supporting check passes (larger-half minus smaller-half above 0).
- Reject: The mean excess 5-day return on positive-forecast grid bars has t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is t >= 2 with a check that fails. Fewer than 100 positive-forecast grid cases, across all coins and windows, is also inconclusive.
