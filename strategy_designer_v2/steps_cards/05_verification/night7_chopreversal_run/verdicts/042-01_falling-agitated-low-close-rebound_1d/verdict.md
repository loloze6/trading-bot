---
plan: 042-01_falling-agitated-low-close-rebound_1d
idea: 042-01_falling-agitated-low-close-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on low_close raw value (in-profile): 0.0180891; slope t (day-clustered): 2.97646 (threshold: slope t >= +2 with bottom-fifth mean > 0 confirms; slope t <= -2 rejects)
- Supporting check: mean next-day excess return, in-profile bars with raw >= 0.8: 0.0106022, passed: True
- Counts: in-profile bars: 2797, bottom-fifth bars: 540, days (in-profile): 1135, active bars: 2786
- Decided by: The slope's t is +2 or more and the bottom-fifth mean next-day excess return is above 0.
- Reading: The falling agitated profile is read as the bars whose recorded regime is 'unknown' (the only regime with a strategy, the vetoes sending every other bar to 'chop'), the situation as an in-profile bar whose close sits below the day's high (raw value > 0) on the long side, the coin's mean daily return over all its windows' bars, every bar as a 1-bar case, and the slope's t as an OLS slope with day-clustered (per-day summed) standard error.
- Size: unusual move +0.77 % (t 3.08, the cases of one day together: 656 days) per case over 1 bars, 0.166 of the coin's usual move (4.73 %); normal drift in its direction +0.13 %, total +0.90 %; 1274 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.006978 on the check folds against +0.01809 on every fold
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/042-01_falling-agitated-low-close-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/042-01_falling-agitated-low-close-rebound_1d`
Measure: `measure.py`
