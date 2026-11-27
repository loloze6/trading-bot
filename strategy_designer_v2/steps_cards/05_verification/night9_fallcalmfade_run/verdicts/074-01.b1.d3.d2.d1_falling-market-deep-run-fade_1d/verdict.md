---
plan: 074-01.b1.d3.d2.d1_falling-market-deep-run-fade_1d
idea: 074-01.b1.d3.d2.d1_falling-market-deep-run-fade
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual short gain over 1 day (next-day return minus coin mean daily return, sign flipped): 0.00825832; t of the mean, cases pooled by day: 3.02681 (threshold: confirm: mean > 0 with day-pooled t >= 2 and supporting check passes; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual short gain, top third by |forecast| minus bottom third: 0.0152059, passed: True
- Counts: cases: 867, distinct case days: 430
- Decided by: The mean unusual short gain is above 0 with t >= 2 and the top third beats the bottom third.
- Reading: Situation computed as raw run_depth > 0 on an up close after a down close, in a falling market read as a negative 60-bar price change inside the window (the recorded regime where 60 bars are not available), on a negative forecast; cases are bets of the short forecast rising in size by at least 2 from its lowest level since the last bet (reset at flat), every bar being a 1-bar grid cell; the t pools cases per UTC day (cluster standard error with D/(D-1) correction); thirds are floor(n/3) cases sorted by |forecast| then time; the plan's 'fewer than 30 distinct case days' is applied as a minimum count, giving 'not observable'.
- Size: unusual move +0.83 % (t 3.03, the cases of one day together: 430 days) per case over 1 bars, 0.176 of the coin's usual move (4.78 %); normal drift in its direction -0.12 %, total +0.71 %; 867 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.001867 on the check folds against +0.008258 on every fold
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/074-01.b1.d3.d2.d1_falling-market-deep-run-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/074-01.b1.d3.d2.d1_falling-market-deep-run-fade_1d`
Measure: `measure.py`
