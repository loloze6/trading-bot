---
plan: 034-02_agitated-high-close-gives-back_1d
idea: 034-02_agitated-high-close-gives-back
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of position x (next-day return minus coin mean daily return): 0.000482827; t of the mean, cases of one day taken together: 1.0225 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; otherwise inconclusive)
- Supporting check: slope of next-day excess return on forecast > 0: 0.000557518, passed: True
- Counts: agitated bars in a position: 7510, coins: 6, measure bars: 7670, days: 2212
- Decided by: The main measure's t lies strictly between -2 and 2 (or its sign disagrees with the rule).
- Reading: Agitation is read from the recorded regime (not 'chop', the volatility-percentile veto, whose component is not recorded and cannot be rebuilt within windows shorter than its 365-bar lookback) and the expected side is short; the main measure uses every bar with a nonzero forecast and a next bar in the same window, drift is each coin's mean daily return pooled over all its windows, the day-clustered t sums deviations per UTC day with a K/(K-1) factor, and the minimum count is the agitated measure bars with a nonzero position, with coins counted among them.
- Size: unusual move +0.20 % (t 1.26, the cases of one day together: 1369 days) per case over 1 bars, 0.044 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.07 %; 3315 cases
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/034-02_agitated-high-close-gives-back_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/034-02_agitated-high-close-gives-back_1d`
Measure: `measure.py`
