---
plan: 061-01.b1.b1.b1.d2.d2_upper-close-quiet-day-fade_1d
idea: 061-01.b1.b1.b1.d2.d2_upper-close-quiet-day-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 10-bar move of short cases: 0.0139877; day-clustered t: 1.67972 (threshold: confirm: mean > 0 with t >= 2 and supporting check passing; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, larger |forecast| half minus smaller half: 0.0222937, passed: True
- Counts: cases: 325, distinct days: 254
- Decided by: t lies between -2 and 2.
- Reading: Situation = close location >= 0.5 of the day's range and 0 < day return / 20-day std (ddof 1, current day included) <= 1, short side, profile not re-checked, bars without 20 returns left out; a case is the first short-side bet (rise of -forecast >= 2 from its low since the last bet) in each 10-bar grid cell of a window; the day-clustered t uses sqrt(G/(G-1) * sum of squared per-day deviation sums)/n; the larger half is |forecast| above the median, the smaller at or below it; the plan's 'fewer than 30 cases or days' is treated as the minimum counts (not observable).
- Size: unusual move +1.40 % (t 1.68, the cases of one day together: 254 days) per case over 10 bars, 0.085 of the coin's usual move (15.92 %); normal drift in its direction -1.27 %, total +0.13 %; 325 cases
Plan: `steps_cards/03_test_plan/night9_chopagishort_run/plans/061-01.b1.b1.b1.d2.d2_upper-close-quiet-day-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1.b1.d2.d2_upper-close-quiet-day-fade_1d`
Measure: `measure.py`
