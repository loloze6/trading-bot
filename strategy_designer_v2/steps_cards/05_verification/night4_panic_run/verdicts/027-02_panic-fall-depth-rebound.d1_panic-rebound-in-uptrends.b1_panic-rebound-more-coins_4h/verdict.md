---
plan: 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends.b1_panic-rebound-more-coins_4h
idea: 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends.b1_panic-rebound-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 84-bar move per long case: 0.0446563; ordinary t of the mean: 2.56192 (threshold: confirm: mean > 0 with t >= 2 and upper-minus-lower half > 0; reject: mean < 0 with t <= -2)
- Supporting check: upper-half minus lower-half mean unusual move (split at median forecast): None, passed: None
- Counts: cases: 256, upper half cases: 0, lower half cases: 256
- Decided by: The mean unusual move is positive with t >= 2 but the upper-half-minus-lower-half difference is not above 0.
- Reading: The panic stretch is the 6-bar high-low width over the mean high-low of the last 180 bars (current bar included) >= 7.5, taken from the regime column where 180 bars are not available, the fall with a positive 90-day return is a positive raw panic value, and the side is long; a case is the first long bet in each 84-bar grid cell of its window (positions counted from the window's first row) whose 84-bar return lies inside the window, the normal drift is the mean of the coin's non-overlapping 84-bar returns over all its windows, the halves are forecast > median versus <= median, and fewer than 30 cases is reported as not observable.
- Size: unusual move +4.47 % per case over 84 bars, 0.198 of the coin's usual move (20.73 %); normal drift in its direction +2.81 %, total +7.27 %; 256 cases
Plan: `steps_cards/03_test_plan/night4_panic_run/plans/027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends.b1_panic-rebound-more-coins_4h.md`
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends.b1_panic-rebound-more-coins_4h`
Measure: `measure.py`
