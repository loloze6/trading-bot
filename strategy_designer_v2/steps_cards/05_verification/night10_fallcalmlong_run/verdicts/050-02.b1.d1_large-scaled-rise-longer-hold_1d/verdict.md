---
plan: 050-02.b1.d1_large-scaled-rise-longer-hold_1d
idea: 050-02.b1.d1_large-scaled-rise-longer-hold
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean excess 10-bar return: 0.0209158; t of the weighted mean, cases of one day pooled: 1.19957 (threshold: above 0 with t >= 2 confirms; below 0 with t <= -2 rejects)
- Supporting check: top-third minus bottom-third mean excess (by forecast): 0.0150695, passed: True
- Counts: independent cases (grid bars with forecast > 0): 132, days the cases fall on: 73
- Decided by: The t of the forecast-weighted mean excess lies between -2 and 2.
- Reading: The falling calm profile is read from the recorded regime ('unknown' = neither veto fired); grid bars without a 10-bar forward close in the window are dropped and drift is each coin's mean 10-bar grid return over all its windows; the weighted mean's t is a day-clustered standard error (per-day sums of f*(excess-mean), scaled by G/(G-1)); the thirds are floor(n/3) cases by forecast with unweighted mean excess.
- Size: unusual move +1.86 % (t 1.58, the cases of one day together: 202 days) per case over 10 bars, 0.107 of the coin's usual move (16.20 %); normal drift in its direction +1.09 %, total +2.96 %; 272 cases
- Effect check (common/verdicts.md): unclear: t in the idea's direction +1.200 (not below 1), 73 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallcalmlong_run/plans/050-02.b1.d1_large-scaled-rise-longer-hold_1d.md`
Record: `steps_cards/04_backtest/night10_fallcalmlong_run/backtests/050-02.b1.d1_large-scaled-rise-longer-hold_1d`
Measure: `measure.py`
