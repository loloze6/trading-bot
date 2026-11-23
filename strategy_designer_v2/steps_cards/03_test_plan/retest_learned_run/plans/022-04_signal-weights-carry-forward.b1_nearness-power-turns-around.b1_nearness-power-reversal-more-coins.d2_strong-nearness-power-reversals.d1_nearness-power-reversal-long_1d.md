---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: the excess of nearness-to-90-day-high power (365-day correlation with 5-day returns) over its usual level, times today's nearness deviation from usual -> kept: ExcessPredictivePowerZComponent (high_period 90, corr_lookback 365, horizon 5) computes (w − wbar) x z.
- Comparison: the reading points against the past relation (a fall implied), with high past power expected to fade -> kept: `negate` takes the counter-bet, and `clip` min 0 keeps only its long side.
- Outcome: the coin rises over the next 5 days, more as the joint reading grows -> kept: the next 5-bar return, compared with the size of the forecast.
- Verdict transfer: yes: the forecast is the idea's own joint reading, taken long only, and it is judged on the idea's 5-day rise.
Forecast: One component, ExcessPredictivePowerZComponent, with high_period 90, corr_lookback 365, horizon 5, z_window 365 and mean_window 365. It is the 365-day correlation of nearness-to-high with the next 5-day return, minus that correlation's mean over the past 365 days, times the z-score of today's nearness over 365 days. It is standardised over its past 500 values (min_periods 120) and negated, so it bets against the excess past relation. It is then clipped at 0, so it is long only. The forecast is positive and grows with the product when that counter-reading points up. It is 0 when the reading points down, or when either factor is 0. It is never short.
Config: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The pooled least-squares slope of the coin's next 5-bar return, minus its normal drift (its mean 5-bar return over all windows), on the bar's forecast. It uses the non-overlapping 5-bar grid of each window, pooled over all coins and windows, with its t-statistic.
- Supporting check: On grid bars with forecast > 0, the mean next 5-bar return minus the coin's normal drift is above 0.
- Confirm: The slope is positive with t ≥ 2, and the supporting check passes.
- Reject: The slope is negative with t ≤ -2.
- Inconclusive: Any slope with -2 < t < 2, or a confirming slope whose supporting check fails. The test needs at least 100 grid bars with forecast > 0, else it is inconclusive.
