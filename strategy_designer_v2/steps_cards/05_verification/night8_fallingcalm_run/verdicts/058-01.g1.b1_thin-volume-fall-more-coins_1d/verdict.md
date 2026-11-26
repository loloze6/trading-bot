---
plan: 058-01.g1.b1_thin-volume-fall-more-coins_1d
idea: 058-01.g1.b1_thin-volume-fall-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean short-direction 5-bar excess return: 0.00552967; t of the weighted mean, cases of one day pooled: 0.904174 (threshold: confirm: mean > 0 with t >= 2 and supporting check > 0; reject: mean < 0 with t <= -2)
- Supporting check: mean excess of larger-|forecast| half minus smaller half: 0.0113197, passed: True
- Counts: distinct days with cases: 263, cases: 907
- Decided by: t lies between -2 and 2 (or cannot be computed), which the plan calls inconclusive.
- Reading: Situation bars are bars with regime 'unknown' (the falling calm profile, the only regime with a strategy) and a negative thin_fall raw value (30-day return from prices where it is not recorded), on the short side; cases are grid bars 0,5,10,... of each window with forecast < 0 and a 5-bar return inside the window, the coin's mean is over all its grid cells in all windows, t is the |forecast|-weighted mean over a day-clustered standard error (weighted deviations summed per UTC day, G/(G-1) correction), and the supporting check splits at the median |forecast| into |forecast| > median versus <= median with unweighted half means.
- Size: unusual move +0.80 % (t 1.71, the cases of one day together: 489 days) per case over 5 bars, 0.073 of the coin's usual move (11.38 %); normal drift in its direction -0.64 %, total +0.16 %; 897 cases
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/058-01.g1.b1_thin-volume-fall-more-coins_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/058-01.g1.b1_thin-volume-fall-more-coins_1d`
Measure: `measure.py`
