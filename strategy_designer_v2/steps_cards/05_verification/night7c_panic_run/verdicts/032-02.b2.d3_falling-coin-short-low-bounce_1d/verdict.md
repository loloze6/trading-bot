---
plan: 032-02.b2.d3_falling-coin-short-low-bounce_1d
idea: 032-02.b2.d3_falling-coin-short-low-bounce
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: position-weighted mean next-day excess return over the coin's mean: 0.00694613; t of weighted mean, cases clustered by day: 1.17865 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of next-day excess on break_depth post_pipeline_value > 0: 0.00294098, passed: True
- Counts: cases (distinct days): 750, cases (bars): 1278
- Decided by: The t of the weighted mean excess lies between -2 and 2.
- Reading: Situation recomputed from prices inside each window (30-bar close-to-close return < 0, close below the minimum low of the 10 prior bars, falling back to the recorded break_depth raw value), active bars whose 30-bar return cannot be computed inside the window are left out of the agreement; cases are bars with a held position > 0, the coin's mean is the mean next-bar return over all its windows, the weighted mean's t clusters cases by UTC day (weighted deviations summed per day), and the slope is an unweighted least-squares fit over cases with a recorded post_pipeline_value.
- Size: unusual move +0.45 % (t 0.75, the cases of one day together: 167 days) per case over 1 bars, 0.090 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.57 %; 373 cases
Plan: `steps_cards/03_test_plan/night7c_panic_run/plans/032-02.b2.d3_falling-coin-short-low-bounce_1d.md`
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-02.b2.d3_falling-coin-short-low-bounce_1d`
Measure: `measure.py`
