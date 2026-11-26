---
plan: 036-01_fall-vs-swing-next-day-rebound_1d
idea: 036-01_fall-vs-swing-next-day-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day return minus coin's mean daily return, on bars with forecast > 0: 0.00622551; t of the mean, cases clustered by day: 2.74567 (threshold: confirm: mean > 0 with t >= 2 (and supporting check); reject: mean < 0 with t <= -2)
- Supporting check: top third minus bottom third by forecast, mean next-day excess return (Welch t -0.733): -0.00214416, passed: False
- Counts: cases: 2093, distinct days: 738
- Decided by: Inconclusive rule: the main measure confirms (mean > 0, t >= 2) but the supporting check fails.
- Reading: Next-day return is close[t+1]/close[t]-1 within a window on every case bar (horizon 1 bar, so the grid is every bar); the coin's mean is over all its next-day returns in all windows; the day-clustered t uses deviations from the mean summed per UTC day with SE = sqrt(D/(D-1) * sum S_d^2)/n; the thirds are the first and last floor(n/3) cases sorted by forecast (ties by timestamp, then coin) and the check passes when the top-minus-bottom difference of means is > 0.
- Size: unusual move +0.49 % (t 2.10, the cases of one day together: 699 days) per case over 1 bars, 0.095 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.60 %; 1878 cases
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/036-01_fall-vs-swing-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/036-01_fall-vs-swing-next-day-rebound_1d`
Measure: `measure.py`
