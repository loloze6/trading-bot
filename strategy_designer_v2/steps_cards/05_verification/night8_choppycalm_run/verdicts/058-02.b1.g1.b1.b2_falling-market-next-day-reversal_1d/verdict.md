---
plan: 058-02.b1.g1.b1.b2_falling-market-next-day-reversal_1d
idea: 058-02.b1.g1.b1.b2_falling-market-next-day-reversal
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the mean over days of the cross-coin daily sum of forecast (post_pipeline_value) x (next-day return - coin mean daily return): 0.142423; t of the mean of daily sums: 1.71736 (threshold: confirm if t >= 2 and timing part > 0; reject if t <= -2; otherwise inconclusive; at least 200 distinct days with a nonzero forecast)
- Supporting check: book mean daily return before costs minus market-rise gain (timing part) > 0: 0.000340942, passed: True
- Counts: distinct days carrying a nonzero forecast: 2085, days in the main measure: 2069, bars with a nonzero forecast: 14200
- Decided by: The main measure's t is 1.72, between -2 and 2.
- Reading: The falling profile is read from the recorded regime (not 'chop', the config's veto of a 60-bar change >= -10) with the component recorded; a bar's evidence and book gain are dated by its own bar's day; the 200-day minimum counts all distinct days with a nonzero forecast and, per the workflow, a shortfall gives 'not observable'; the book's daily return before costs is the mean over the coins present that day of position held x next-day return, and its market part the same with the coin's mean daily return.
- Size: unusual move +0.17 % (t 1.42, the cases of one day together: 1911 days) per case over 1 bars, 0.035 of the coin's usual move (5.31 %); normal drift in its direction +0.01 %, total +0.18 %; 9335 cases
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/058-02.b1.g1.b1.b2_falling-market-next-day-reversal_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02.b1.g1.b1.b2_falling-market-next-day-reversal_1d`
Measure: `measure.py`
