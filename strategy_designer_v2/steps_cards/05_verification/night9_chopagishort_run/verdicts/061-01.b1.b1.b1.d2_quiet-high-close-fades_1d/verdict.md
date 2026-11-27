---
plan: 061-01.b1.b1.b1.d2_quiet-high-close-fades_1d
idea: 061-01.b1.b1.b1.d2_quiet-high-close-fades
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-day move in the short's direction: 0.0190216; t of the mean, cases of one day taken together: 2.45323 (threshold: mean > 0 with t >= 2 and correlation > 0 (confirm); mean < 0 with t <= -2 (reject))
- Supporting check: correlation of forecast size with unusual move: 0.0617987, passed: True
- Counts: distinct days with cases: 105, cases: 120
- Decided by: The mean unusual move is above 0 with t >= 2 and the size-move correlation is above 0.
- Reading: The profile is read from the recorded regime (not 'chop', since its 365-bar volatility percentile cannot be rebuilt from the recorded bars), the gain from the recorded small_gain raw value + 1 (else rebuilt from prices with the 20-bar window including the bar), a case is the first short bet (rise of the short forecast of at least 2 points) in each 5-bar grid cell, forecast size is |forecast|, the correlation is Pearson, and the day-clustered t uses summed daily deviations with a D/(D-1) correction.
- Size: unusual move +1.90 % (t 2.46, the cases of one day together: 105 days) per case over 5 bars, 0.168 of the coin's usual move (11.68 %); normal drift in its direction -0.67 %, total +1.23 %; 120 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: too few cases on the check folds (79 cases, 79 days)
Plan: `steps_cards/03_test_plan/night9_chopagishort_run/plans/061-01.b1.b1.b1.d2_quiet-high-close-fades_1d.md`
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1.b1.d2_quiet-high-close-fades_1d`
Measure: `measure.py`
