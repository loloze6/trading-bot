---
plan: 002-05_sma-up-regime-positive-drift_1d
idea: 002-05_sma-up-regime-positive-drift
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: in-stretch minus all-bar mean next-bar return (before costs): 0.000865053 (threshold: above 0 with one-sided t-statistic >= 2.0 confirms; at or below 0 or t <= -2.0 rejects)
- Supporting check: in-stretch up-day share minus all-bar up-day share: -0.000657268, passed: False
- Cases: 290
- Decided by: Inconclusive rule: the t-statistic lies between -2.0 and 2.0.
- Reading: In-stretch bars are rows with forecast > 0 and next-bar returns are taken inside each window. The t-statistic on the difference is a Welch two-sample t-test of in-stretch returns against all-bar returns, and an up day is a next-bar return > 0. Distinct up-cross stretches are runs of consecutive forecast > 0 bars inside each window (5 found). t = 0.49516162785129425, mean_in = 0.0011363914899525335, mean_all = 0.0002713384034471068, n_all = 724.
Plan: `steps_cards/03_test_plan/plans/002-05_sma-up-regime-positive-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-05_sma-up-regime-positive-drift_1d`
Measure: `measure.py`
