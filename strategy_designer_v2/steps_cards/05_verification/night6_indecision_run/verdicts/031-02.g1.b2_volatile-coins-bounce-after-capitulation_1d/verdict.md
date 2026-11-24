---
plan: 031-02.g1.b2_volatile-coins-bounce-after-capitulation_1d
idea: 031-02.g1.b2_volatile-coins-bounce-after-capitulation
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess next-day return on mean_reversion bars: 0.0128493; t of the mean, cases of one day taken together: 2.20865 (threshold: t >= 2 to confirm, t <= -2 to reject, over at least 30 case-days)
- Supporting check: mean excess of upper vol20 half minus lower half: 0.0207096, passed: True
- Counts: case-days: 150, cases: 330
- Decided by: The mean excess next-day return has t >= 2 over at least 30 case-days and the high-volatility half beats the low-volatility half.
- Reading: Situation recomputed from prices as 1-bar return over the std (ddof 1) of the last 20 one-bar returns including bar t, with close location (close-low)/(high-low), falling back to the recorded regime on bars without 20 returns of history; cases are bars with regime mean_reversion and a next bar in the same window; the coin's mean is over all its 1-bar returns in all windows; the t clusters cases by UTC day (deviations summed per day); the median split puts cases above the median in the upper half and the rest in the lower half; fewer than 30 case-days is reported as not observable.
- Size: unusual move +1.23 % (t 2.10, the cases of one day together: 146 days) per case over 1 bars, 0.260 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +1.35 %; 324 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-02.g1.b2_volatile-coins-bounce-after-capitulation_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-02.g1.b2_volatile-coins-bounce-after-capitulation_1d`
Measure: `measure.py`
