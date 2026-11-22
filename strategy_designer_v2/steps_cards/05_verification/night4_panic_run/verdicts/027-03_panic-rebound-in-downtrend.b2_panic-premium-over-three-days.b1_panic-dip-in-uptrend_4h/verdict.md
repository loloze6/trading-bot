---
plan: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend_4h
idea: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend
fit: adapted
status: mismatch
---
Situation check: 66 % of the active bars are bars of the plan's situation on its side (90 % needed).
- Decided by: Fewer than 90% of the bars with a non-zero forecast are long bars of the plan's panic situation (24h range >= 3x its 30-day mean, 24h fall, prior 30-day rise).
- Reading: Situation computed from prices with bar range = (high-low)/close and the ratio = 180-bar mean / 6-bar mean (<= 0.3333), using the recorded raw fall/rise values for the return signs where present, bars where it cannot be computed (window start) left out of the agreement; cases are long bets (rise >= 2 from the lowest long level since the last bet), the first per 18-bar cell of each window, and fewer than 30 cases is 'not observable'.
Plan: `steps_cards/03_test_plan/night4_panic_run/plans/027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend_4h.md`
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend_4h`
Measure: `measure.py`
