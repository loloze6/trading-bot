---
plan: 074-01.g1.d1_wide-close-high-bounce-fade_1d
idea: 074-01.g1.d1_wide-close-high-bounce-fade
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side next-day excess return: 0.000723562; t of the mean, cases clustered by day: 0.0862633 (threshold: mean > 0 with t >= 2 (and correlation > 0) confirms; t <= -2 rejects)
- Supporting check: correlation forecast vs next-day excess return: -0.0233111, passed: False
- Counts: cases: 49, independent case days: 23
- Decided by: Only 23 independent case days, below the plan's minimum of 30.
- Reading: Agreement counts active bars whose situation can be computed inside the window (up day, close above mid-range, recorded or price-rebuilt compression below 0) and short; the 30 independent case days minimum is applied as 'not observable'; the t clusters deviations by UTC day with a D/(D-1) correction; the supporting correlation is Pearson between the forecast and the raw (unsigned) next-day excess return.
- Size: unusual move +0.02 % (t 0.02, the cases of one day together: 21 days) per case over 1 bars, 0.120 of the coin's usual move (3.33 %); normal drift in its direction -0.02 %, total +0.00 %; 42 cases
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/074-01.g1.d1_wide-close-high-bounce-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/unseen_2026/backtests/074-01.g1.d1_wide-close-high-bounce-fade_1d`
Measure: `measure.py`
