---
plan: 061-01.b1.b1.b1.d3_high-close-fades-over-ten-days_1d
idea: 061-01.b1.b1.b1.d3_high-close-fades-over-ten-days
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 10-bar move per short case, in the short direction: 0.0258083; t of the mean, cases of one day pooled: 2.90374 (threshold: confirm: mean > 0 with day-pooled t >= 2 over >= 30 case-days (and check passes); reject: mean < 0 with t <= -2 over >= 30 case-days)
- Supporting check: mean unusual move of stronger |forecast| half minus weaker half: -0.0134822, passed: False
- Counts: case-days: 206, cases: 289
- Decided by: The main measure meets the confirm rule but the supporting check (stronger minus weaker half above 0) fails.
- Reading: The profile part of the situation is read from the recorded regime (mean_reversion is only reached when no chop veto of the profile fires) since the detector's components are not recorded, the close location from the raw value or else the prices; a case is the first short bet (rise of |forecast| on the short side of at least 2 from its lowest level since the last bet) in each 10-bar grid cell of a window, the t uses day-clustered deviations, the stronger half is |forecast| above the case median, and fewer than 30 case-days gives 'not observable' per the workflow's minimum-count rule.
- Size: unusual move +2.58 % (t 2.91, the cases of one day together: 206 days) per case over 10 bars, 0.153 of the coin's usual move (15.92 %); normal drift in its direction -1.26 %, total +1.32 %; 289 cases
Plan: `steps_cards/03_test_plan/night9_chopagishort_run/plans/061-01.b1.b1.b1.d3_high-close-fades-over-ten-days_1d.md`
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1.b1.d3_high-close-fades-over-ten-days_1d`
Measure: `measure.py`
