---
plan: 074-01.g1.d1_wide-close-high-bounce-fade_1d
idea: 074-01.g1.d1_wide-close-high-bounce-fade
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side next-day excess return: 0.0101877; t of the mean, cases clustered by day: 2.50917 (threshold: mean > 0 with t >= 2 (and correlation > 0) confirms; t <= -2 rejects)
- Supporting check: correlation forecast vs next-day excess return: 0.0676608, passed: True
- Counts: cases: 900, independent case days: 358
- Decided by: Mean short-side excess return above 0 with t >= 2 and a positive forecast/excess-return correlation.
- Reading: Agreement counts active bars whose situation can be computed inside the window (up day, close above mid-range, recorded or price-rebuilt compression below 0) and short; the 30 independent case days minimum is applied as 'not observable'; the t clusters deviations by UTC day with a D/(D-1) correction; the supporting correlation is Pearson between the forecast and the raw (unsigned) next-day excess return.
- Size: unusual move +1.07 % (t 2.24, the cases of one day together: 292 days) per case over 1 bars, 0.217 of the coin's usual move (5.12 %); normal drift in its direction -0.11 %, total +0.96 %; 711 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/074-01.g1.d1_wide-close-high-bounce-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/common/backtests/074-01.g1.d1_wide-close-high-bounce-fade_1d`
Measure: `measure.py`
