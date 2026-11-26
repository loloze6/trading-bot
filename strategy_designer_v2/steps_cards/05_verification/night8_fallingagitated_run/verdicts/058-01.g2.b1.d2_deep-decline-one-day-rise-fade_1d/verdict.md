---
plan: 058-01.g2.b1.d2_deep-decline-one-day-rise-fade_1d
idea: 058-01.g2.b1.d2_deep-decline-one-day-rise-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-day move after short bets, short direction: 0.0056467; t of the mean, same-day cases together: 1.33798 (threshold: confirm: mean > 0 with t >= 2 and correlation > 0; reject: mean < 0 with t <= -2)
- Supporting check: correlation of |forecast| with unusual move: 0.0197154, passed: True
- Counts: cases: 1465, distinct case days: 510
- Decided by: The t of the mean unusual move lies between -2 and 2.
- Reading: The rise and the 60-day fall are read from the recorded raw values (rise > 0, fall < -10 as the config's veto), the agitation (365-day volatility percentile, not recomputable inside ~122-bar windows) from the detector's regime being 'trending', a case is the first short bet in each 3-bar grid cell of a window, and the t clusters deviations by signal day with a G/(G-1) correction.
- Size: unusual move +0.56 % (t 1.34, the cases of one day together: 510 days) per case over 3 bars, 0.068 of the coin's usual move (8.85 %); normal drift in its direction -0.43 %, total +0.13 %; 1465 cases
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.g2.b1.d2_deep-decline-one-day-rise-fade_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.b1.d2_deep-decline-one-day-rise-fade_1d`
Measure: `measure.py`
