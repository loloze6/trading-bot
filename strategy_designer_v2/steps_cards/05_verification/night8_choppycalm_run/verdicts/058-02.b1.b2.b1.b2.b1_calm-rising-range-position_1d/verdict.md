---
plan: 058-02.b1.b2.b1.b2.b1_calm-rising-range-position_1d
idea: 058-02.b1.b2.b1.b2.b1_calm-rising-range-position
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (10-bar return - coin's mean 10-bar return), per-day sums, on the 10-bar grid: 0.0797568; t of the mean of per-day sums: 1.5867 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; otherwise inconclusive)
- Supporting check: none
- Counts: grid cases: 552, distinct days: 143
- Decided by: inconclusive rule met: t lies between -2 and 2
- Reading: The profile is the non-chop regime, and the side is the sign of the range position. Each coin's mean 10-bar return is over all its grid returns in all its windows. The cases of one UTC day are summed into one value, and the reported mean and t are those of these daily sums. The plain per-case mean is 0.020661629793881645. A count below the minimum gives 'not observable', as the workflow requires.
- Size: unusual move +1.18 % (t 1.67, the cases of one day together: 492 days) per case over 10 bars, 0.067 of the coin's usual move (15.92 %); normal drift in its direction +0.46 %, total +1.65 %; 879 cases
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/058-02.b1.b2.b1.b2.b1_calm-rising-range-position_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02.b1.b2.b1.b2.b1_calm-rising-range-position_1d`
Measure: `measure.py`
