---
plan: 031-04_fading-volume-after-fall-rebounds_1d
idea: 031-04_fading-volume-after-fall-rebounds
fit: adapted
status: mismatch
---
Situation check: 0 % of the active bars are bars of the plan's situation on its side (90 % needed).
- Decided by: Fewer than 90% of the bars with a non-zero forecast are long bars in the mean_reversion fall regime with volume below its 90-day mean, as the Fidelity's situation requires.
- Reading: The situation is read from the recorded regime (the detector's 365-day volatility cannot be rebuilt inside ~120-bar windows), required long, with the vol_dry raw log ratio below 0 and, where 90 bars of the window exist, a negative 90-day return; the drift is the coin's mean 30-bar return on the non-overlapping grid of all its windows; the slope is pooled OLS with intercept over all coins with CR1 standard errors clustered by calendar day.
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-04_fading-volume-after-fall-rebounds_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-04_fading-volume-after-fall-rebounds_1d`
Measure: `measure.py`
