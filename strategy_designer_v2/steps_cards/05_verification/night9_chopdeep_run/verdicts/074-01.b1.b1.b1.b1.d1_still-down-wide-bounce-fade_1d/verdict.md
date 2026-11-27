---
plan: 074-01.b1.b1.b1.b1.d1_still-down-wide-bounce-fade_1d
idea: 074-01.b1.b1.b1.b1.d1_still-down-wide-bounce-fade
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day drift-adjusted short-side return per case (fraction): 0.0246476; t of the mean, cases of a day summed: 2.47702 (threshold: confirm: mean > 0 with t >= 2 and Spearman > 0; reject: mean < 0 with t <= -2)
- Supporting check: Spearman(|forecast|, drift-adjusted short-side next-day return) > 0: 0.215722, passed: True
- Counts: cases: 126, distinct case days: 52
- Decided by: The mean short-side unusual move is above 0 with a t of 2 or more and the Spearman correlation is above 0.
- Reading: Regime components recomputed from prices inside each window (60-day and 5-day returns in percent, range over the mean high-low of the last 20 bars including the bar, close location from the low); the agreement is taken over active bars where all five can be computed (falling back to the computable conditions only if none can be: basis 'full'); cases are short-side bets per the holding rule (rise of |forecast| of at least 2 from its lowest level since the last bet, reset on flat/long), drift is the coin's mean 1-bar return over all its windows, the t uses deviations summed per UTC day (day-clustered standard error), and fewer than 30 distinct case days is reported as not observable.
- Size: unusual move +2.46 % (t 2.50, the cases of one day together: 52 days) per case over 1 bars, 0.493 of the coin's usual move (5.31 %); normal drift in its direction -0.14 %, total +2.32 %; 126 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: too few cases on the check folds (35 cases, 35 days)
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/074-01.b1.b1.b1.b1.d1_still-down-wide-bounce-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/074-01.b1.b1.b1.b1.d1_still-down-wide-bounce-fade_1d`
Measure: `measure.py`
