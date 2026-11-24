---
plan: 031-02.b1.g2.b1_volatile-falls-more-coins_1d
idea: 031-02.b1.g2.b1_volatile-falls-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope t of excess 2-day return on post_pipeline forecast, cases with positive forecast, day-clustered: 0.000316169; OLS slope t, standard error clustered by day: 1.33206 (threshold: t >= 2 confirms (with supporting check); t <= -2 rejects; otherwise inconclusive; fewer than 100 independent case-days not observable)
- Supporting check: mean excess 2-day return, high minus low 60-day volatility (median split): 0.000565832, passed: True
- Counts: independent case-days: 1230, cases: 8995, cases with 60-day volatility: 4444
- Decided by: The slope's t lies between -2 and 2.
- Reading: Cases are grid bars (positions 0, 2, 4, ... of each window) with forecast > 0; the coin's mean 2-day return is taken on that same grid over all its windows; 'the cases of one day pooled' is read as a standard error clustered by calendar day (UTC), with independent case-days the number of distinct days; the 60-day volatility is the ddof-1 standard deviation of the last 60 daily close returns inside the window (cases without 60 returns left out of the check), high meaning strictly above the median; the plan's fewer-than-100-case-days minimum is reported as not observable; the situation is a positive raw fall_vol value with a lower close, on the long side.
- Size: unusual move +0.03 % (t 0.14, the cases of one day together: 1958 days) per case over 2 bars, 0.004 of the coin's usual move (7.48 %); normal drift in its direction +0.30 %, total +0.32 %; 11129 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-02.b1.g2.b1_volatile-falls-more-coins_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-02.b1.g2.b1_volatile-falls-more-coins_1d`
Measure: `measure.py`
