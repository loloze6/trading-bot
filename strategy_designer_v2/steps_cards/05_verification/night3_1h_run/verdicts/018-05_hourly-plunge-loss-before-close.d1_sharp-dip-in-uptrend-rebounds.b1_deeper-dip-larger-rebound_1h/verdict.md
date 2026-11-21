---
plan: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.b1_deeper-dip-larger-rebound_1h
idea: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.b1_deeper-dip-larger-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 72-bar return of the bets (return minus coin's normal drift), pooled: 0.00553742; t of the mean: 2.98349 (threshold: confirm if mean > 0 with t >= 2 (and supporting check passes); reject if mean < 0 with t <= -2; at least 30 independent cases)
- Supporting check: mean unusual return of larger-forecast half minus smaller-forecast half > 0: -0.0023223, passed: False
- Counts: independent cases: 2440, larger-forecast half: 1220, smaller-forecast half: 1220
- Decided by: Mean unusual 72-bar return above 0 with t >= 2, but the larger-forecast half does not beat the smaller half.
- Reading: Bets are long forecast rises of at least 2 points from the lowest level since the last bet (reset to 0 when flat), the first per 72-bar grid cell counted from each window's first row, with cases lacking 72 bars ahead in the window dropped; the median split puts forecasts above the median in the larger half and those at or below it in the smaller half; a missed 30-case minimum is reported as not observable.
- Size: unusual move +0.55 % per case over 72 bars, 0.064 of the coin's usual move (8.23 %); normal drift in its direction +0.41 %, total +0.96 %; 2440 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.b1_deeper-dip-larger-rebound_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.b1_deeper-dip-larger-rebound_1h`
Measure: `measure.py`
