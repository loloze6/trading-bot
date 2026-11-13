---
plan: N4-02_new-high-not-shock_1d
idea: N4-02_new-high-not-shock
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: Top-minus-bottom half of positive forecast: mean excess 10-bar forward return (pp), pooled over coins: 1.67879; cluster-robust t (breakout clusters): 1.37665 (threshold: Reject if t >= 2 or t <= -2; confirm if |t| < 2 and both one-sided tests against +-1 pp reach t >= 2)
- Supporting check: TOST against +-1 pp: min of the two one-sided t: -0.556627, passed: False
- Counts: independent breakout clusters: 381, clusters in top half: 329, clusters in bottom half: 294
- Decided by: Inconclusive: |t| < 2 but the two one-sided tests against +-1 pp do not both reach t >= 2.
- Reading: Halves split at the pooled median of positive forecasts (top: forecast > median, bottom: forecast <= median). The coin's mean 10-bar return is taken over every bar of all its windows. Clusters are runs of positive-forecast bars less than or equal to 10 bars apart in the same window. The t is cluster-robust (CR1) on the top-indicator coefficient, and the per-half counts are the distinct clusters with a bar in that half.
Plan: `steps_cards/03_test_plan/overnight_run/plans/N4-02_new-high-not-shock_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N4-02_new-high-not-shock_1d`
Measure: `measure.py`
