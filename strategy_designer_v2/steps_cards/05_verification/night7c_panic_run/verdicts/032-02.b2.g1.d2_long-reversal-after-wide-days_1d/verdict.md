---
plan: 032-02.b2.g1.d2_long-reversal-after-wide-days_1d
idea: 032-02.b2.g1.d2_long-reversal-after-wide-days
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: next-bar excess return, top forecast tercile minus bottom tercile: 0.0017578; Welch t: 1.18648 (threshold: difference > 0 with Welch t >= 2 confirms (with timing part > 0); difference < 0 with t <= -2 rejects)
- Supporting check: book mean daily return minus market-rise gain (timing part): 0.000271479, passed: True
- Counts: days in top tercile: 1814, days in bottom tercile: 1883
- Decided by: t lies between -2 and 2.
- Reading: Terciles are equal-count thirds of each coin's bars ranked by forecast with ties broken by time order, every bar is a 1-day case, cases of one UTC day are averaged per tercile before Welch's t, and the plan's 300-day minimum per tercile, when unmet, gives 'not observable'.
- Size: unusual move +0.09 % (t 0.81, the cases of one day together: 2071 days) per case over 1 bars, 0.020 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.21 %; 7074 cases
Plan: `steps_cards/03_test_plan/night7c_panic_run/plans/032-02.b2.g1.d2_long-reversal-after-wide-days_1d.md`
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-02.b2.g1.d2_long-reversal-after-wide-days_1d`
Measure: `measure.py`
