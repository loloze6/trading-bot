---
plan: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1h
idea: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of next 240-bar excess return on forecast, trending grid bars: 0.00520582; OLS slope t: 7.18992 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; otherwise inconclusive)
- Supporting check: none
- Counts: grid cases in trending: 1562, cases at forecast 0: 772, cases with forecast > 0: 790
- Decided by: the slope is positive with t >= 2.
- Reading: the 4800-bar SMA cannot be rebuilt inside windows shorter than 4800 bars, so on those bars the situation is read from the recorded regime 'trending' (SMAs recomputed from prices on 0 bars), with long (forecast > 0) as the expected side; the coin's mean 240-bar return is the mean over all its windows' non-overlapping grid bars (all regimes), the regression has an intercept, and the plan's minimum counts are applied as 'not observable'.
- Size: unusual move +0.63 % per case over 240 bars, 0.027 of the coin's usual move (15.30 %); normal drift in its direction +1.58 %, total +2.21 %; 1188 cases
Plan: `steps_cards/03_test_plan/hold_paying_run/plans/002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1h.md`
Record: `steps_cards/04_backtest/paying_rerun_run/backtests/002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1h`
Measure: `measure.py`
