---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d3_nearness-reversal-after-quiet-week
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: edf20a924da4
---
Fidelity:
- Situation: the excess of the 90-day-high nearness's past 365-day power for 5-day returns, times nearness's deviation from its usual level -> kept: ExcessPredictivePowerZComponent (signal "high", 90, 365, horizon 5), graded product.
- Comparison: the reading points against a past relation that implies a fall, and the rise is larger the lower the prior 5-day return -> kept: the forecast is the negated product, long side only; the prior-return modulation is measured in the criterion from recorded closes.
- Outcome: the coin rises over the next 5 days -> kept: a long held 5 bars, judged on the 5-day return against the coin's drift.
- Verdict transfer: yes: the forecast is the idea's exact reading, and the criterion tests both the rise and its dependence on the prior 5-day return.
Forecast: The forecast uses one indicator, ExcessPredictivePowerZComponent, with signal "high", high_period 90, corr_lookback 365, horizon 5, z_window 365 and mean_window 365. Its value is (w − wbar) × z, where: - w is the past 365-day correlation of nearness to the 90-day high with the next 5-day return; - wbar is the usual level of w; - z is today's deviation of nearness from its usual level. The value is standardised over its past 365 values and then negated, so it is positive when the reading implies a fall. It is then clipped at 0, so the book is long only. It is zero when the reading implies a rise or is absent. It grows with the size of the product.
Config: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d3_nearness-reversal-after-quiet-week_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Use the bars where the forecast is above 0, read on the non-overlapping 5-bar grid of each window. Regress the 5-day return close[t+5]/close[t]−1, minus the coin's mean 5-day return over all its windows, on the forecast. Report the t of the slope.
- Supporting check: Among the same cases, take the mean excess 5-day return of cases whose prior 5-day return (close[t]/close[t−5]−1) is ≤ 0, minus that of cases whose prior return is > 0. Report the Welch t.
- Confirm: The slope's t is ≥ 2 and the supporting check's Welch t is ≥ 2.
- Reject: The slope's t is ≤ −2, or the supporting check's Welch t is ≤ −2 (the edge is larger after run-ups).
- Inconclusive: Any other result is inconclusive, as is a run with fewer than 100 grid cases with a positive forecast or fewer than 30 cases in either prior-return group.
