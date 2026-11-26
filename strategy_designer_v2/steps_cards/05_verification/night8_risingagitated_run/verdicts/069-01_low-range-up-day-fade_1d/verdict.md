---
plan: 069-01_low-range-up-day-fade_1d
idea: 069-01_low-range-up-day-fade
fit: exact
status: rejected
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day excess return x (-forecast/10) on short cases: -0.00390595; t of the mean, cases pooled per day: -2.71005 (threshold: confirm: mean > 0 with t >= 2 and supporting difference < 0; reject: mean < 0 with t <= -2)
- Supporting check: mean next-day excess return, forecast <= -10 minus up days with forecast 0: -0.00491, passed: True
- Counts: days with a case: 1350, cases: 3708, deep cases (forecast <= -10): 1269, up days with forecast 0: 5141
- Decided by: The main measure's mean is below 0 with t <= -2.
- Reading: The up day is the close-to-close return above 0 inside the window (on a window's first bar, where the previous close is not recorded, the recorded regime 'mean_reversion' stands for it); the per-day pooled t is the mean over its day-clustered standard error (deviations summed per day, G/(G-1) correction); 'up days with forecast 0' are up days by that same rule.
- Size: unusual move +0.54 % (t 2.93, the cases of one day together: 911 days) per case over 1 bars, 0.114 of the coin's usual move (4.78 %); normal drift in its direction -0.12 %, total +0.42 %; 2195 cases
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/069-01_low-range-up-day-fade_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/069-01_low-range-up-day-fade_1d`
Measure: `measure.py`
