---
idea: N1-04_rebound-after-large-drop
brief: 002_moving-average-cross-trend-persistence
data-instruments: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ
data-bar: 1d
data-period: folds A, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a daily close falling more than 1.5 times the trailing 20-day standard deviation of daily returns -> adapted: the threshold is made graded. The one-day return is divided by the mean absolute return of the prior 20 days (`standardise` over 20 bars), which is about 0.8 of their standard deviation. Only drops count, and a strong dead zone keeps ordinary days near 0.
- Comparison: next-day results after ordinary days -> kept: the hit rate after the largest positions is compared with the coin's hit rate over all days of all windows.
- Outcome: the next day's close is above the drop day's close more often -> kept: the one-bar close-to-close return after the forecast bar, long side.
- Verdict transfer: yes: the forecast takes its largest long positions exactly after drops of about 1.5 trailing deviations or more and is held for one day. Whether the next close is higher more often can be read directly from the record.
Forecast: The forecast uses one indicator, the one-day percent return (`PriceEvolutionComponent`, period 1). It is standardised against the mean absolute value of the previous 20 daily returns (window 20, from the brief), so an average day is about 10 and a 1.5-standard-deviation drop is about 18.8. The sign is flipped so that drops are positive, then clipped at 0, so up days give 0. Then `signed_power` with exponent 3 and pivot 20 is applied, the strongest dead zone the guide allows: - a typical drop of 10 gives 2.5; - a 1.5-standard-deviation drop gives about 16.5; - the largest drops reach the cap of 20. The forecast is never negative (long only). It is zero on up days and near zero on ordinary down days, and grows steeply with the size of the drop relative to recent volatility.
Config: N1-04_rebound-after-large-drop_1d_oos_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The share of positive next-bar close-to-close returns on bars where the forecast is 16 or more (a drop of about 1.5 trailing standard deviations or more). This is compared with the coin's share of positive daily returns over all bars of all 24 windows together, pooled over the 6 coins. The test is a two-proportion z-test; the horizon is one bar, so no returns overlap.
- Supporting check: On the same bars, the mean next-bar return minus the coin's mean daily return over all windows together, with its t-statistic. This is before costs.
- Confirm: The hit-rate excess is positive with z ≥ 2, over at least 100 qualifying bars.
- Reject: The hit-rate excess is negative with z ≤ -2, over at least 100 qualifying bars.
- Inconclusive: Any z strictly between -2 and 2, including results near zero, or fewer than 100 qualifying bars in total.
