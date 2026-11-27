---
plan: 061-01.b1.b1.b1.d1.d1.d1.d2_upper-close-deep-fall-ten-day_1d
idea: 061-01.b1.b1.b1.d1.d1.d1.d2_upper-close-deep-fall-ten-day
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction unusual 10-bar move per case: 0.0213667; t of the mean, cases of one day together: 1.21922 (threshold: confirm: mean > 0 with t >= 2 on >= 30 cases and Spearman > 0; reject: mean < 0 with t <= -2 on >= 30 cases)
- Supporting check: Spearman(|forecast| at signal, short-direction unusual move) > 0: -0.142623, passed: False
- Counts: cases: 120, days: 97
- Decided by: The t lies between -2 and 2, so neither the confirm nor the reject rule is met.
- Reading: Situation computed from prices (close location (close-low)/(high-low) > 0.5, 5-bar return < 0, 20-bar return < -10 %, inside each window, the recorded fall20 raw value used where the window holds fewer than 20 prior bars) and active bars where it cannot be evaluated are left out; the profile is not part of the Fidelity situation; a case is the first short bet (rise of -forecast of >= 2 points from its low since the last bet, reset at flat) in each 10-bar grid cell of a window; the per-day t is the cluster-by-day t of the mean; forecast size is |forecast|; the plan's 'fewer than 30 cases' is reported as not observable.
- Size: unusual move +2.14 % (t 1.23, the cases of one day together: 97 days) per case over 10 bars, 0.114 of the coin's usual move (15.92 %); normal drift in its direction -1.26 %, total +0.87 %; 120 cases
Plan: `steps_cards/03_test_plan/night9_chopagishort_run/plans/061-01.b1.b1.b1.d1.d1.d1.d2_upper-close-deep-fall-ten-day_1d.md`
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1.b1.d1.d1.d1.d2_upper-close-deep-fall-ten-day_1d`
Measure: `measure.py`
