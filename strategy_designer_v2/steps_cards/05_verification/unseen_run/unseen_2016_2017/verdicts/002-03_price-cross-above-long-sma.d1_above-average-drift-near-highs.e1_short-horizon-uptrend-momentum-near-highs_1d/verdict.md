---
plan: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs_1d
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: top-minus-bottom half (by forecast) mean forward 10-bar excess return, trending grid cases: 0.0606218; Welch t: 1.77333 (threshold: confirm if Welch t >= 2 with supporting check passing; reject if Welch t <= -2)
- Supporting check: mean forward 10-bar excess return of cases with forecast > 0 is above 0: 0.013899, passed: True
- Counts: top half grid cases: 79, bottom half grid cases: 79, trending grid cases: 158, cases with forecast > 0: 125
- Decided by: A half has fewer than the plan's minimum of 100 grid cases across all coins and windows.
- Reading: The situation is checked on the regime column (the detector's MovingAverageAgeComponent(200) >= 1 rule, labelled 'trending'), with forecast > 0 as the expected long side; the coin's mean 10-bar return uses every non-overlapping grid case of all its windows; the halves split all trending grid cases pooled across coins and windows by forecast rank. Ties are ordered stably by coin, window and bar. The bottom half takes the extra case when the count is odd.
Plan: `steps_cards/03_test_plan/validation_run/plans/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs_1d.md`
Record: `steps_cards/04_backtest/unseen_run/unseen_2016_2017/backtests/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs_1d`
Measure: `measure.py`
