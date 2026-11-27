---
plan: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1h
idea: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of next 240-bar excess return on forecast, trending grid bars: 0.00539922; OLS slope t: 7.35822 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; otherwise inconclusive)
- Supporting check: none
- Counts: grid cases in trending: 1605, cases at forecast 0: 758, cases with forecast > 0: 847
- Decided by: the slope is positive with t >= 2.
- Reading: the 4800-bar SMA cannot be rebuilt inside windows shorter than 4800 bars, so on those bars the situation is read from the recorded regime 'trending' (SMAs recomputed from prices on 0 bars), with long (forecast > 0) as the expected side; the coin's mean 240-bar return is the mean over all its windows' non-overlapping grid bars (all regimes), the regression has an intercept, and the plan's minimum counts are applied as 'not observable'.
- Size: unusual move +1.22 % (t 1.42, the cases of one day together: 643 days) per case over 240 bars, 0.065 of the coin's usual move (16.05 %); normal drift in its direction +1.86 %, total +3.08 %; 1229 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/hold2_rerun_run/plans/002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1h.md`
Record: `steps_cards/04_backtest/paying_rerun_run/common/backtests/002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1h`
Measure: `measure.py`
