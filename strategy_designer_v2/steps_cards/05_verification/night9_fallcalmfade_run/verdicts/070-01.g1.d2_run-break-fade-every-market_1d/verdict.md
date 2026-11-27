---
plan: 070-01.g1.d2_run-break-fade-every-market_1d
idea: 070-01.g1.d2_run-break-fade-every-market
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction unusual 1-day move on bars with forecast <= -2: 0.0059314; t of the mean, cases of one day taken together: 3.57128 (threshold: confirm: mean > 0 with day-clustered t >= 2 (and supporting check passes); reject: mean < 0 with t <= -2; at least 100 case-days)
- Supporting check: mean unusual move, runs of 3+ (forecast <= -8) minus runs of 2 (-8 < forecast <= -2), above 0: 0.00241071, passed: True
- Counts: case-days: 922, cases: 2126, cases with forecast <= -8: 945, cases with forecast between -8 and -2: 1181
- Decided by: Mean short-direction unusual move above 0 with t >= 2 and longer runs show a larger move: the confirm rule.
- Reading: Situation from prices: close up on the bar and the previous close down (strict), using the regime column only on a window's first two bars; the next-day return stays inside the window and the coin's mean is over all its 1-bar returns in all windows; the day-clustered t sums deviations per UTC day with a G/(G-1) correction; case-days are distinct UTC days with a case; the shorter-run group is -8 < forecast <= -2.
- Size: unusual move +0.59 % (t 3.57, the cases of one day together: 922 days) per case over 1 bars, 0.125 of the coin's usual move (4.78 %); normal drift in its direction -0.12 %, total +0.47 %; 2126 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.001763 on the check folds against +0.005931 on every fold
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/070-01.g1.d2_run-break-fade-every-market_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/070-01.g1.d2_run-break-fade-every-market_1d`
Measure: `measure.py`
