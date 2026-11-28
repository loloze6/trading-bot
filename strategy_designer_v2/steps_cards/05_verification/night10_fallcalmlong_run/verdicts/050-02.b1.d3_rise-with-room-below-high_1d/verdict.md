---
plan: 050-02.b1.d3_rise-with-room-below-high_1d
idea: 050-02.b1.d3_rise-with-room-below-high
fit: adapted
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 7-bar move after long bets: 0.00476393; t of the mean, cases grouped by day: 0.669436 (threshold: mean > 0 with t >= 2 (and the supporting check) to confirm; mean < 0 with t <= -2 to reject)
- Supporting check: mean unusual move above-median forecast minus below-median, grid bars with forecast > 0: 0.0288049, passed: True
- Counts: cases: 390, independent days: 278, grid bars with forecast above 0: 184
- Decided by: The t lies between -2 and 2 (or cannot be computed), which the plan calls inconclusive. No effect (common/verdicts.md): t in the idea's direction +0.669 (below 1), 390 cases (30 needed).
- Reading: One case per 7-bar grid cell (the cell's first long bet, a forecast rise of at least 2 from its lowest level since the last bet), its return taken from that bet's close over 7 bars inside the window minus the coin's mean grid 7-bar return over all windows; the day-grouped t is the clustered t of the mean; the supporting check uses the grid bars themselves with ties at the median left out; the 30-case minimum is counted in independent days and, per the workflow, gives 'not observable'.
- Size: unusual move +0.48 % (t 0.67, the cases of one day together: 278 days) per case over 7 bars, 0.035 of the coin's usual move (13.58 %); normal drift in its direction +0.83 %, total +1.30 %; 390 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction +0.669 (below 1), 390 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallcalmlong_run/plans/050-02.b1.d3_rise-with-room-below-high_1d.md`
Record: `steps_cards/04_backtest/night10_fallcalmlong_run/backtests/050-02.b1.d3_rise-with-room-below-high_1d`
Measure: `measure.py`
