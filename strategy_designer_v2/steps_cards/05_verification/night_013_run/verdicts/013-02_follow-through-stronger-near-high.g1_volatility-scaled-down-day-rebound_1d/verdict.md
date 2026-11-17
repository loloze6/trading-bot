---
plan: 013-02_follow-through-stronger-near-high.g1_volatility-scaled-down-day-rebound_1d
idea: 013-02_follow-through-stronger-near-high.g1_volatility-scaled-down-day-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of OLS slope of next-bar excess return on forecast, forecast > 0 bars, pooled: 3.90392; OLS slope t: 3.90392 (threshold: slope t >= +2 (with forecast-weighted mean excess > 0) confirms; t <= -2 rejects; otherwise inconclusive; at least 500 bars with forecast > 0)
- Supporting check: forecast-weighted mean next-bar excess return over forecast > 0 bars, above 0: 0.00315566, passed: True
- Counts: bars with forecast > 0: 8514
- Decided by: The slope's t is +2 or more and the forecast-weighted mean next-bar excess return is above 0.
- Reading: Bars with forecast > 0 counted where the next bar's close exists in the same window; the coin's mean daily return is the mean of all its in-window next-bar returns over all windows; the slope t is the ordinary OLS t (slope / its standard error); the plan's 500-bar minimum, when unmet, is reported as not observable.
Plan: `steps_cards/03_test_plan/night_013_run/plans/013-02_follow-through-stronger-near-high.g1_volatility-scaled-down-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night_013_run/backtests/013-02_follow-through-stronger-near-high.g1_volatility-scaled-down-day-rebound_1d`
Measure: `measure.py`
