---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week.g1_sunday-move-reverses-volatility-graded_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week.g1_sunday-move-reverses-volatility-graded
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean of (forecast/10) x excess 2-bar return on Sunday bars: 0.00602559; t of the mean: 5.3902 (threshold: confirm if t >= 2 with supporting check passing; reject if t <= -2)
- Supporting check: mean sign(forecast) x excess 2-bar return, top third by |forecast|: 0.00925795, passed: True
- Counts: Sunday cases: 5244, top-third cases: 1748
- Decided by: The main measure's t is >= 2 and the supporting check passes (confirm rule).
- Reading: Sunday bars are those whose UTC start timestamp is a Sunday (closing into Monday) with regime mean_reversion and forecast not 0, the expected side is opposite to the sign of Sunday's 1-bar return, the coin's mean 2-bar return is taken on the non-overlapping grid (positions 0, 2, 4, ...) pooled over its windows, and the 'top third' is the ceil(n/3) cases with the largest |forecast|.
- Size: unusual move +0.70 % per case over 2 bars, 0.096 of the coin's usual move (7.48 %); normal drift in its direction +0.01 %, total +0.71 %; 4447 cases
Plan: `steps_cards/03_test_plan/night_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week.g1_sunday-move-reverses-volatility-graded_1d.md`
Record: `steps_cards/04_backtest/night_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week.g1_sunday-move-reverses-volatility-graded_1d`
Measure: `measure.py`
