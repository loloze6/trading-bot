---
plan: 071-01_falling-agitated-swing-rise-next-fade_1d
idea: 071-01_falling-agitated-swing-rise-next-fade
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on abs(forecast), forecast<0 bars: 0.000151919; OLS slope t, day-clustered: 0.490238 (threshold: confirm if slope t <= -2 (with mean excess < 0); reject if slope t >= +2)
- Supporting check: mean next-day excess return on forecast<0 bars below 0: -0.0055899, passed: True
- Counts: cases: 1326, distinct days: 633
- Decided by: The slope t lies between -2 and +2 (inconclusive rule).
- Reading: Profile read from regime 'unknown' and up day from raw scaled return > 0; the slope t uses an OLS of excess return on abs(forecast) with day-clustered (CR1) standard errors; the coin's mean daily return is the mean of all its within-window close-to-close returns; days are UTC calendar days of the bar's timestamp.
- Size: unusual move +0.61 % (t 2.38, the cases of one day together: 445 days) per case over 1 bars, 0.131 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.48 %; 857 cases
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/071-01_falling-agitated-swing-rise-next-fade_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/071-01_falling-agitated-swing-rise-next-fade_1d`
Measure: `measure.py`
