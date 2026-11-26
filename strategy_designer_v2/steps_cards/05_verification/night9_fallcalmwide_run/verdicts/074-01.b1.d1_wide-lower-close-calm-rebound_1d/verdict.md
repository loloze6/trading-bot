---
plan: 074-01.b1.d1_wide-lower-close-calm-rebound_1d
idea: 074-01.b1.d1_wide-lower-close-calm-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day excess return over coin drift on bars with forecast > 0: 0.00473888; t of the mean, same-day cases taken together: 1.70785 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of next-day excess return on forecast > 0: 0.00105832, passed: True
- Counts: distinct days with cases: 330, cases: 641
- Decided by: t between -2 and 2 (inconclusive rule).
- Reading: The rising-calm profile cannot be recomputed from the recorded bars (365-bar lookback), so the situation is width >= 2 and (high-close)/(high-low) > 0.5 on bars whose regime is mean_reversion (profile vetoes not hit); the same-day t uses deviations summed per UTC day with a G/(G-1) correction, the drift is each coin's mean 1-day return over all its windows, and the plan's 30-day minimum is treated as 'not observable'.
- Size: unusual move +0.39 % (t 1.37, the cases of one day together: 307 days) per case over 1 bars, 0.084 of the coin's usual move (5.33 %); normal drift in its direction +0.14 %, total +0.53 %; 580 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmwide_run/plans/074-01.b1.d1_wide-lower-close-calm-rebound_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/074-01.b1.d1_wide-lower-close-calm-rebound_1d`
Measure: `measure.py`
