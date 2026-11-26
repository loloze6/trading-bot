---
plan: 032-02.b1.e1.e1.e1.e2.e1_tight-ranges-break-out-further_1d
idea: 032-02.b1.e1.e1.e1.e2.e1_tight-ranges-break-out-further
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: Welch t of 20-bar excess return, narrower half minus wider half: 0.0168891; Welch t: 0.144623 (threshold: confirm: t >= 2 with positive narrow-half mean excess; reject: t <= -2)
- Supporting check: narrower-half mean excess 20-bar return > 0: -0.011354, passed: False
- Counts: cases: 21, narrower-half cases: 9, wider-half cases: 9
- Decided by: The plan's minimum of 60 cases with at least 20 in each half is not reached (21 cases, 9 narrower, 9 wider).
- Reading: The situation (close above the highest of the prior 60 closes, long side) is checked on active bars with 60 prior closes in their window, those without are left out of the agreement (regime used only if none is computable); a case is the first trending bar in each 20-bar grid cell (positions 0,20,40,... from the window's first row) with its 20-bar return from that bar inside the window; the coin's mean 20-bar return is over the non-overlapping grid returns of all its windows; the narrower half is narrow.last_history_value above the coin's median of its cases (a larger proximity to the low means a tighter range), the wider half below it, cases equal to the median are left out; a minimum count not reached gives 'not observable'.
- Size: unusual move -3.33 % (t -0.56, the cases of one day together: 13 days) per case over 20 bars, -0.236 of the coin's usual move (15.52 %); normal drift in its direction +1.89 %, total -1.44 %; 17 cases
Plan: `steps_cards/03_test_plan/night7c_rangefail_run/plans/032-02.b1.e1.e1.e1.e2.e1_tight-ranges-break-out-further_1d.md`
Record: `steps_cards/04_backtest/night7c_rangefail_run/unseen_2026/backtests/032-02.b1.e1.e1.e1.e2.e1_tight-ranges-break-out-further_1d`
Measure: `measure.py`
