---
plan: 032-02_flat-range-downside-break-recovers_1d
idea: 032-02_flat-range-downside-break-recovers
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 10-bar return of long bets over the coin's mean 10-bar return: -0.015555; day-clustered t: -0.551916 (threshold: confirm: mean > 0 with day-clustered t >= 2 over >= 30 cases; reject: t <= -2)
- Supporting check: OLS slope of recovered share (excess / depth) on depth (t): 0.730717, passed: False
- Counts: cases: 61, days: 39, cases with depth: 61
- Decided by: Inconclusive rule: the main t is between -2 and 2 and no reject rule is met.
- Reading: A case is the first long bet (forecast rise >= 2 points from its lowest long level since the last bet, reset to 0 when flat) in each non-overlapping 10-bar grid cell from each window's first row, kept only when 10 bars remain in the window; the coin's mean 10-bar return is taken on the same grid over all its windows; the day-clustered t sums deviations per UTC day with a G/(G-1) correction; the slope t is OLS; situation bars use the 60-bar ER recomputed from closes (SMA-5 smoothing), falling back on the recorded regime where the window is too short, and the recorded depth (else recomputed from prior 60-bar lows); fewer than 30 cases is reported 'not observable' per the workflow's minimum-count rule.
- Size: unusual move -1.56 % (t -0.56, the cases of one day together: 39 days) per case over 10 bars, -0.120 of the coin's usual move (14.49 %); normal drift in its direction +1.15 %, total -0.40 %; 61 cases
Plan: `steps_cards/03_test_plan/night7c_rangefail_run/plans/032-02_flat-range-downside-break-recovers_1d.md`
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-02_flat-range-downside-break-recovers_1d`
Measure: `measure.py`
