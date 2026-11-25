---
plan: 033-01_close-near-low-rebounds_1d
idea: 033-01_close-near-low-rebounds
fit: adapted
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean over days of the summed (forecast/10) x next-day excess return: 0.00309886; t of the mean over days: 2.64101 (threshold: confirm if t >= 2 (with check passing); reject if t <= -2; at least 500 distinct days of cases)
- Supporting check: mean next-day excess return, forecast >= +2.5 minus forecast <= -2.5: 0.00474812, passed: True
- Counts: distinct days of cases: 2898, days in main measure: 2898, bars with forecast >= +2.5: 4308, bars with forecast <= -2.5: 4490
- Decided by: The main-measure t is >= 2 and the supporting check's difference is above 0.
- Reading: The situation is rebuilt as the standardised close-from-high share (raw over the mean of its past 60 in-window raw values, recorded post-pipeline value where the window lacks history) above 10 for long and below 10 for short; the main measure's days are all calendar days with a bar that has a next-day return (zero-forecast bars add 0); 'days of cases' are distinct days holding a bar with non-zero forecast and a next-day return; excess return is the next-day return minus the coin's mean next-day return over all its windows; a minimum count not reached gives 'not observable'.
- Size: unusual move +0.22 % (t 2.46, the cases of one day together: 2539 days) per case over 1 bars, 0.049 of the coin's usual move (4.78 %); normal drift in its direction -0.00 %, total +0.22 %; 7862 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0005244 on the check folds against +0.003099 on every fold
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/033-01_close-near-low-rebounds_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/033-01_close-near-low-rebounds_1d`
Measure: `measure.py`
