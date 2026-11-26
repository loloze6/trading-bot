---
plan: 031-01.g1.g1.g2_volatile-weekends-follow-trend_1d
idea: 031-01.g1.g1.g2_volatile-weekends-follow-trend
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the mean per-Friday summed gain (forecast/10 x excess 2-bar return): 0.0429135; t of the mean over days: 3.35189 (threshold: confirm if t >= 2 over >= 100 distinct Fridays; reject if t <= -2)
- Supporting check: high-vol minus other-Fridays slope of excess weekend return on standardised 14-day return (Welch t 1.300): 0.000296478, passed: True
- Counts: distinct Fridays with cases: 317, cases: 1103, high-volatility Fridays in slope: 979, other Fridays in slope: 1193
- Decided by: Confirm: main t at least 2 over at least 100 distinct Fridays and slope difference above 0.
- Reading: Friday bars are those whose next bar starts on Saturday (UTC); high-volatility Fridays are read from the recorded regime 'trending'; the situation check recomputes the 20/60 volatility ratio from window closes and falls back to the recorded regime where the window is too short; the coin's mean 2-bar return uses a non-overlapping grid over all its windows; slopes are pooled OLS over coins and their Welch t is (b_high - b_other)/sqrt(se_high^2 + se_other^2).
- Size: unusual move +1.12 % (t 3.89, the cases of one day together: 309 days) per case over 2 bars, 0.163 of the coin's usual move (6.58 %); normal drift in its direction +0.02 %, total +1.14 %; 962 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-01.g1.g1.g2_volatile-weekends-follow-trend_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1.g1.g2_volatile-weekends-follow-trend_1d`
Measure: `measure.py`
