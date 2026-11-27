---
plan: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs_1d
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: top-minus-bottom half (by forecast) mean forward 10-bar excess return, trending grid cases: 0.0381217; Welch t: 4.04455 (threshold: confirm if Welch t >= 2 with supporting check passing; reject if Welch t <= -2)
- Supporting check: mean forward 10-bar excess return of cases with forecast > 0 is above 0: 0.0178812, passed: True
- Counts: top half grid cases: 998, bottom half grid cases: 998, trending grid cases: 1996, cases with forecast > 0: 1433
- Decided by: Welch t >= 2 for top minus bottom and cases with forecast > 0 have a positive mean excess return.
- Reading: The situation is checked on the regime column (the detector's MovingAverageAgeComponent(200) >= 1 rule, labelled 'trending'), with forecast > 0 as the expected long side; the coin's mean 10-bar return uses every non-overlapping grid case of all its windows; the halves split all trending grid cases pooled across coins and windows by forecast rank. Ties are ordered stably by coin, window and bar. The bottom half takes the extra case when the count is odd.
- Size: unusual move +1.36 % (t 1.91, the cases of one day together: 840 days) per case over 10 bars, 0.073 of the coin's usual move (16.37 %); normal drift in its direction +1.36 %, total +2.73 %; 1644 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/validation_run/plans/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs_1d.md`
Record: `steps_cards/04_backtest/paying_rerun_run/common/backtests/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs_1d`
Measure: `measure.py`
