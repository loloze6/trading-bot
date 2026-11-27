---
plan: 072-02.b1_choppy-deep-up-day-fade-more-coins_1d
idea: 072-02.b1_choppy-deep-up-day-fade-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: next-day excess return, deepest third minus shallowest third of forecast: -0.00142485; Welch t: -0.81626 (threshold: Welch t <= -2 (with deepest third mean < 0) to confirm, >= +2 to reject)
- Supporting check: deepest third mean next-day excess return below 0: -0.00280239, passed: True
- Counts: active bars: 3358, deepest third: 1120, middle third: 1119, shallowest third: 1119
- Decided by: Welch t lies between -2 and +2 (inconclusive rule).
- Reading: Thirds are cut on the pooled active bars sorted by forecast (stable sort, np.array_split, lowest third = deepest); the choppy profile is checked as a 60-bar close-to-close change within +/-10 % where the window holds 60 prior bars, else as a regime other than 'chop', the up day as close above the prior close in the window (first bar of a window left out), and the depth as a negative raw distance from the high.
- Size: unusual move +0.26 % (t 1.72, the cases of one day together: 954 days) per case over 1 bars, 0.048 of the coin's usual move (5.31 %); normal drift in its direction -0.15 %, total +0.11 %; 2072 cases
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/072-02.b1_choppy-deep-up-day-fade-more-coins_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/072-02.b1_choppy-deep-up-day-fade-more-coins_1d`
Measure: `measure.py`
