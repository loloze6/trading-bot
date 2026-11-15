---
idea: 002-05_sma-up-regime-positive-drift.a1_sma-up-regime-positive-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C and D
outcome: plan
fit: exact
---
Fidelity:
- Situation: the 50-day SMA is above the 200-day SMA, more so as the gap widens -> kept: the SMA50/SMA200 percent spread is clipped at 0, so it is zero below and grows with the gap.
- Comparison: the next-day return on the coin's other days -> kept: next-day returns are compared between bars with a positive forecast and bars with a zero forecast.
- Outcome: the close-to-close return over the next 1 day is higher, and grows with the gap -> kept: horizon of 1 bar, long side.
- Verdict transfer: yes: the forecast is exactly the idea's graded condition, and the measure is the idea's own comparison at its 1-day horizon.
Forecast: The forecast starts from the percent spread (SMA50 − SMA200) / SMA200, using simple averages of 50 and 200 daily closes. This spread is standardised against its own past 200 values (window 200, min_periods 50), so a typical spread size is about 10. It is then clipped at 0. The forecast is zero while SMA50 ≤ SMA200. It is positive while SMA50 > SMA200 and grows in proportion to the gap, capped at 20. It is never short.
Config: 002-05_sma-up-regime-positive-drift.a1_sma-up-regime-positive-drift_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The 1-bar next return (close[t+1]/close[t] − 1) on bars with forecast > 0, minus the same return on bars with forecast = 0. Every bar counts, inside each window, pooled over coins and windows. The test is Welch's t.
- Supporting check: Among bars with forecast > 0, the slope of the next-day return regressed on the forecast must be positive.
- Confirm: The main measure is positive with Welch t ≥ 2, and the supporting slope is above 0.
- Reject: The main measure is negative with Welch t ≤ −2.
- Inconclusive: A Welch t between −2 and 2 is inconclusive. A t ≥ 2 with a slope ≤ 0 is also inconclusive. The test needs at least 100 bars in each group, pooled across coins and windows; with fewer it is inconclusive.
