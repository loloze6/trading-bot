---
plan: 050-02.b1.d2_scaled-rise-strong-case_1d
idea: 050-02.b1.d2_scaled-rise-strong-case
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-day move after scaled weekly rises: 0.00955483; t of the mean, cases pooled by day: 2.38766 (threshold: mean > 0 with t >= 2 (and Spearman > 0) to confirm; mean < 0 with t <= -2 to reject)
- Supporting check: Spearman(forecast at signal, unusual move) > 0: -0.0217967, passed: False
- Counts: distinct case days: 297, cases: 410
- Decided by: t >= 2 but the Spearman correlation is not above 0.
- Reading: A case is the first long bet (forecast rise >= 2 points from its lowest level since the last bet, from 0 after flat) in each non-overlapping 3-bar cell counted from each window's first row, the falling calm profile is the recorded regime 'unknown', the day-pooled t uses cluster-robust standard errors with per-day summed deviations (G/(G-1) correction), and fewer than 30 case days is reported as not observable.
- Size: unusual move +0.96 % (t 2.39, the cases of one day together: 297 days) per case over 3 bars, 0.112 of the coin's usual move (8.43 %); normal drift in its direction +0.36 %, total +1.31 %; 410 cases
- Effect check (common/verdicts.md): unclear: t in the idea's direction +2.388 (not below 1), 297 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallcalmlong_run/plans/050-02.b1.d2_scaled-rise-strong-case_1d.md`
Record: `steps_cards/04_backtest/night10_fallcalmlong_run/backtests/050-02.b1.d2_scaled-rise-strong-case_1d`
Measure: `measure.py`
