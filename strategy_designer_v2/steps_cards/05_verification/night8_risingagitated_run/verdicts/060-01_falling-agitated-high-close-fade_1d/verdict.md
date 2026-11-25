---
plan: 060-01_falling-agitated-high-close-fade_1d
idea: 060-01_falling-agitated-high-close-fade
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: top-minus-middle close-location group mean next-day return net of coin mean: -0.00587368; Welch t: -2.46416 (threshold: confirm at Welch t <= -2 (with timing gain > 0), reject at Welch t >= +2)
- Supporting check: mean timing gain per bar in a position (position x (next return - coin mean)): 0.000845665, passed: True
- Counts: bars in top group: 942, bars in middle group: 886, bars in a position: 2689
- Decided by: The top-minus-middle Welch t is -2 or less and the timing gain is above 0 (confirm rule).
- Reading: The profile is read from the recorded regime ('unknown', the regime left when neither chop veto fires, since the detector's components are not recorded) with the situation being any close above the day's low on the short side; the groups are top = raw close location >= 2/3 and middle = 1/3 <= location < 2/3 on profile bars where close_loc is recorded, every bar used (1-bar horizon, no overlap), the timing gain pooled over all coins' bars in a position, and the plan's 'fewer than 30 per group' minimum is reported as not observable as the workflow requires.
- Size: unusual move +0.29 % (t 1.22, the cases of one day together: 661 days) per case over 1 bars, 0.066 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.16 %; 1287 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure -0.002826 on the check folds against -0.005874 on every fold
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/060-01_falling-agitated-high-close-fade_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/060-01_falling-agitated-high-close-fade_1d`
Measure: `measure.py`
