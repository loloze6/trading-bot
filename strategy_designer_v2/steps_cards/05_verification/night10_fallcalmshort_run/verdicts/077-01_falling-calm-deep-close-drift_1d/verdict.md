---
plan: 077-01_falling-calm-deep-close-drift_1d
idea: 077-01_falling-calm-deep-close-drift
fit: adapted
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 3-day return on post_pipeline_value: 0.000113633; OLS slope t, day-clustered: 0.22747 (threshold: confirm: slope > 0 with t >= 2 (and supporting check passes); reject: slope < 0 with t <= -2)
- Supporting check: book mean daily return minus position x coin mean daily return, before costs: 0.000151555, passed: True
- Counts: independent cases: 961, distinct days: 415
- Decided by: The slope's t lies between -2 and 2 (inconclusive rule). No effect (common/verdicts.md): t in the idea's direction +0.227 (below 1), 961 cases (30 needed).
- Reading: The falling calm profile is read from the recorded regime ('unknown' = no veto fired, since the detector's 365-bar components cannot be rebuilt inside 120-bar windows) and the situation as a close below its 20-day high (raw depth < 0) with a short forecast; the slope's t pools cases of one day by a day-clustered OLS standard error (with G/(G-1) correction); the supporting check uses the position's gain before costs per bar (each 1d bar is one day), averaged over the coins present each day; minimum counts not reached give 'not observable'.
- Size: unusual move +0.18 % (t 0.57, the cases of one day together: 463 days) per case over 3 bars, 0.018 of the coin's usual move (7.84 %); normal drift in its direction -0.29 %, total -0.11 %; 700 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction +0.227 (below 1), 961 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallcalmshort_run/plans/077-01_falling-calm-deep-close-drift_1d.md`
Record: `steps_cards/04_backtest/night10_fallcalmshort_run/backtests/077-01_falling-calm-deep-close-drift_1d`
Measure: `measure.py`
