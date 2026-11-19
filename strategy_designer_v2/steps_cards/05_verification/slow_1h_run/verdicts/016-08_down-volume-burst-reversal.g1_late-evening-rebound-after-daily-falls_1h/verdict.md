---
plan: 016-08_down-volume-burst-reversal.g1_late-evening-rebound-after-daily-falls_1h
idea: 016-08_down-volume-burst-reversal.g1_late-evening-rebound-after-daily-falls
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of OLS slope of excess 2-bar return on forecast (pooled): 7.14565e-05; OLS slope t: 2.6491 (threshold: slope t >= 2 confirms (with check), t <= -2 rejects, otherwise inconclusive; at least 500 cases)
- Supporting check: mean excess 2-bar return, top third minus bottom third of forecasts: 0.00107992, passed: True
- Counts: cases: 8626, top third: 2875, bottom third: 2875
- Decided by: Slope t = 2.65 >= 2 and top-minus-bottom third excess return 0.00108 > 0.
- Reading: Decision bars are those whose timestamp + 1h has hour 20 with a negative 24-bar raw change; one case per coin per UTC day (first such bar), cases without a full 2-bar return inside the window dropped; the coin mean uses non-overlapping 2-bar returns on each window's grid from its first row; thirds are the n//3 lowest and n//3 highest forecasts after a stable sort.
Plan: `steps_cards/03_test_plan/slow_1h_run/plans/016-08_down-volume-burst-reversal.g1_late-evening-rebound-after-daily-falls_1h.md`
Record: `steps_cards/04_backtest/slow_1h_run/backtests/016-08_down-volume-burst-reversal.g1_late-evening-rebound-after-daily-falls_1h`
Measure: `measure.py`
