---
plan: 058-02.b1.b2.b1.b2_calm-market-range-position_1d
idea: 058-02.b1.b2.b1.b2_calm-market-range-position
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: clustered-by-day t of the slope of 5-bar excess return on forecast, in-profile grid bars: 0.000513035; slope t, clustered by day: 1.69957 (threshold: t >= +2 confirms (with timing part > 0); t <= -2 rejects; between is inconclusive)
- Supporting check: book mean daily return before costs minus market-rise gain (timing part): 0.000836523, passed: True
- Counts: non-overlapping in-profile cases: 3436, distinct days: 506
- Decided by: The slope's t lies between -2 and +2.
- Reading: In-profile means regime 'unknown' on the grid bar (positions 0,5,10,... of each window, forward return inside the window), all such bars are regressed with an intercept on the recorded forecast including forecast 0, the slope's t uses day-clustered standard errors with the usual G/(G-1)*(N-1)/(N-K) correction, the drift is the coin's mean non-overlapping 5-bar return over all its windows, and the timing part uses each bar as a day with the coins present that day averaged.
- Size: unusual move +0.87 % (t 3.00, the cases of one day together: 1306 days) per case over 5 bars, 0.075 of the coin's usual move (11.68 %); normal drift in its direction -0.02 %, total +0.85 %; 3374 cases
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/058-02.b1.b2.b1.b2_calm-market-range-position_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02.b1.b2.b1.b2_calm-market-range-position_1d`
Measure: `measure.py`
