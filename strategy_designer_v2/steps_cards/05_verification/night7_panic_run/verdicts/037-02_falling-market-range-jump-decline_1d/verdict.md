---
plan: 037-02_falling-market-range-jump-decline_1d
idea: 037-02_falling-market-range-jump-decline
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-bar move per case, short direction: -0.0021901; t of the mean, cases of one day taken together: -0.403739 (threshold: confirm: mean > 0 with day-clustered t >= 2 over >= 30 cases and slope < 0; reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of 3-bar excess return on raw range multiple (must be < 0): 0.00301023, passed: False
- Counts: cases (non-overlapping 3-bar cells): 500, days with cases: 293, cases in slope regression: 500
- Decided by: The t of the mean unusual move lies between -2 and 2 (or could not be computed).
- Reading: Situation = range ratio >= 1.5 (recorded range_mult, else recomputed from prices) in a falling market (60-bar close return < 0, or regime 'trending' where 60 bars are not available in the window), short side; a case is the first short bet (forecast falling >= 2 points below its lowest short level since the last bet) in each 3-bar grid cell of a window, its return taken from that bet bar's close over 3 bars inside the window, drift = per-coin mean of non-overlapping grid 3-bar returns over all windows, t clustered by UTC day, slope = OLS of raw (unsigned) excess return on range_mult at the case bar.
- Size: unusual move -0.22 % (t -0.40, the cases of one day together: 293 days) per case over 3 bars, -0.025 of the coin's usual move (7.96 %); normal drift in its direction -0.37 %, total -0.59 %; 500 cases
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/037-02_falling-market-range-jump-decline_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/backtests/037-02_falling-market-range-jump-decline_1d`
Measure: `measure.py`
