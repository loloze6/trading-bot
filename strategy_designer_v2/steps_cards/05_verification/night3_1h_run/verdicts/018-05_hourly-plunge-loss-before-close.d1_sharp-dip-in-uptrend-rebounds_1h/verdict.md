---
plan: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds_1h
idea: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 72-bar unusual move (return minus coin's normal 72-bar drift) of long bets: 0.00494388; t of the mean: 2.99186 (threshold: confirm: mean > 0 with t >= 2 over at least 30 cases; reject: mean < 0 with t <= -2 over at least 30 cases)
- Supporting check: Welch difference of mean unusual move, above minus at-or-below median entry forecast: None, passed: None
- Counts: independent cases: 2803, cases above median entry forecast: 0, cases at or below median entry forecast: 2803
- Decided by: A confirming mean (above 0, t >= 2, at least 30 cases) whose supporting check fails.
- Reading: Bets are long-side rises of the forecast of at least 2 points from its lowest level since the last bet (reset to 0 when flat), the first per 72-bar grid cell of each window counted from its first row, with cases whose 72-bar return leaves the window dropped; cases tied at the median entry forecast are put in the lower group, and the supporting check passes on the sign of the difference, as the confirm rule states.
- Size: unusual move +0.49 % per case over 72 bars, 0.057 of the coin's usual move (8.23 %); normal drift in its direction +0.41 %, total +0.90 %; 2803 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds_1h`
Measure: `measure.py`
