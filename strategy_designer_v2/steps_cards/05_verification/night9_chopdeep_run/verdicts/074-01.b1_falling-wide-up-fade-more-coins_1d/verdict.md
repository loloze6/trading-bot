---
plan: 074-01.b1_falling-wide-up-fade-more-coins_1d
idea: 074-01.b1_falling-wide-up-fade-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day excess return in the short direction over short bets: 0.00555291; t of the mean, cases of one day taken together: 2.09986 (threshold: confirm: mean > 0 with t >= 2 over >= 100 cases; reject: mean < 0 with t <= -2 over >= 100 cases)
- Supporting check: Welch t, larger-half minus smaller-half |forecast| excess return (>= 1): -0.932985, passed: False
- Counts: cases: 1717, distinct days: 697
- Decided by: The main t is >= 2 but the supporting check fails.
- Reading: Profile trend recomputed as the 60-bar % price change (veto at >= -10) and up day as close > previous close, falling back to the recorded regime where a window's own bars cannot give them; cases are short-side forecast rises of >= 2 points from the lowest short level since the last bet; day-clustered t without small-sample correction; halves split at n//2 after sorting by |forecast|; both 100 cases and 60 distinct days taken as minimum counts.
- Size: unusual move +0.56 % (t 2.10, the cases of one day together: 697 days) per case over 1 bars, 0.109 of the coin's usual move (5.31 %); normal drift in its direction -0.15 %, total +0.40 %; 1717 cases
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/074-01.b1_falling-wide-up-fade-more-coins_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/074-01.b1_falling-wide-up-fade-more-coins_1d`
Measure: `measure.py`
