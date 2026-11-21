---
plan: 017-04_postsettle-decline-after-downtrend.g2_late-evening-rebound-after-falls_1h
idea: 017-04_postsettle-decline-after-downtrend.g2_late-evening-rebound-after-falls
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast x excess 2-bar return at 21:00 cases, pooled: 0.0100759; ordinary t: 4.77665 (threshold: t >= +2 to confirm (with top-minus-bottom > 0); t <= -2 to reject)
- Supporting check: top minus bottom forecast tercile, mean excess 2-bar return (Welch t): 0.001008, passed: True
- Counts: cases overall: 8553, cases in top tercile: 2851, cases in bottom tercile: 2851
- Decided by: Confirm rule met: main t = 4.78 >= +2 and top-minus-bottom difference 0.00101 > 0.
- Reading: Cases are bars whose timestamp + 1h is 21:00 UTC with forecast > 0, first per UTC date per window, return taken positionally close[t+2]/close[t]-1 inside the window; the coin mean uses the non-overlapping 0,2,4,... grid of all its windows; terciles are pooled forecast cut points with bottom <= lower cut and top >= upper cut.
Plan: `steps_cards/03_test_plan/intraday_1h_run/plans/017-04_postsettle-decline-after-downtrend.g2_late-evening-rebound-after-falls_1h.md`
Record: `steps_cards/04_backtest/intraday_1h_run/backtests/017-04_postsettle-decline-after-downtrend.g2_late-evening-rebound-after-falls_1h`
Measure: `measure.py`
