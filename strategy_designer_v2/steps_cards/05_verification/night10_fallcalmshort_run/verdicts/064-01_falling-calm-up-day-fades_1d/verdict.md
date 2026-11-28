---
plan: 064-01_falling-calm-up-day-fades_1d
idea: 064-01_falling-calm-up-day-fades
fit: adapted
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-bar move of short cases (return minus coin's normal 3-bar drift, short direction): -0.00230752; t of the mean, cases of one day summed together: -0.688372 (threshold: t >= 2 with positive mean confirms; t <= -2 rejects; t clustered by day)
- Supporting check: mean unusual move, larger-|forecast| half minus smaller half: -0.00259355, passed: False
- Counts: distinct case days: 443, cases: 746
- Decided by: The main-measure t lies between -2 and 2. No effect (common/verdicts.md): t in the idea's direction -0.688 (below 1), 443 cases (30 needed).
- Reading: Cases are short bets (forecast rise of >= 2 points on the short side) taken at the first bet bar of each 3-bar grid cell per window, measured from that bar's close over 3 bars, over all coins in the record; the larger half is the top floor(n/2) cases by |forecast|; the plan's fewer-than-30-case-days rule is applied as the minimum count giving 'not observable'.
- Size: unusual move -0.23 % (t -0.69, the cases of one day together: 443 days) per case over 3 bars, -0.027 of the coin's usual move (7.84 %); normal drift in its direction -0.28 %, total -0.51 %; 746 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction -0.688 (below 1), 443 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallcalmshort_run/plans/064-01_falling-calm-up-day-fades_1d.md`
Record: `steps_cards/04_backtest/night10_fallcalmshort_run/backtests/064-01_falling-calm-up-day-fades_1d`
Measure: `measure.py`
