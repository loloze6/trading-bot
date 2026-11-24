---
plan: 034-01_agitated-low-close-rebounds_1d
idea: 034-01_agitated-low-close-rebounds
fit: adapted
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast x (next-day return minus coin mean), summed per day: 0.0311484; t of the mean (per-day cases): 2.94507 (threshold: confirm t >= 2 (with top-minus-bottom third difference > 0); reject t <= -2)
- Supporting check: next-day excess return, top third minus bottom third of forecasts (Welch t 4.433): 0.00684814, passed: True
- Counts: agitated days with a non-zero forecast: 2214
- Decided by: The main t is >= 2 and the top-minus-bottom third difference is above 0.
- Reading: The agitated situation is read as regime not 'chop' and the expected side as the sign of the rebuilt standardised close location minus 10; the 300-day minimum is counted as distinct UTC days with at least one non-zero forecast and a next-day return, and the supporting check's thirds are the forecast tertiles pooled over all coins' active bars, the difference judged by its sign with Welch t reported.
- Size: unusual move +0.39 % (t 2.77, the cases of one day together: 1597 days) per case over 1 bars, 0.092 of the coin's usual move (4.73 %); normal drift in its direction -0.00 %, total +0.39 %; 3587 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.01058 on the check folds against +0.03115 on every fold
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/034-01_agitated-low-close-rebounds_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/034-01_agitated-low-close-rebounds_1d`
Measure: `measure.py`
